from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import os
import httpx
import random

load_dotenv()

BASE = os.environ["BASE"].rstrip("/")
USER = os.environ["FRESHRSS_USER"]
API_PASSWORD = os.environ["API_PASSWORD"]


def login(client):
    r = client.post(
        f"{BASE}/accounts/ClientLogin",
        data={"Email": USER, "Passwd": API_PASSWORD},
    )
    r.raise_for_status()
    dados = dict(l.split("=", 1) for l in r.text.splitlines() if "=" in l)
    return {"Authorization": f"GoogleLogin auth={dados['Auth']}"}


def listar_feeds(client, headers):
    r = client.get(
        f"{BASE}/reader/api/0/subscription/list",
        params={"output": "json"},
        headers=headers,
    )
    r.raise_for_status()
    return r.json()["subscriptions"]


def noticias_do_feed(client, headers, feed_id, n=10, so_nao_lidas=False):
    params = {"output": "json", "n": n}
    if so_nao_lidas:
        params["xt"] = "user/-/state/com.google/read"

    r = client.get(
        f"{BASE}/reader/api/0/stream/contents/{feed_id}",
        params=params,
        headers=headers,
    )
    r.raise_for_status()
    return r.json()["items"]

def primeira_imagem(html, base_url=""):
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img")

    if not img:
        return None
    
    src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
    if not src:
        return None
    
    return urljoin(base_url, src)

def html_para_texto(html):
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)

def feeds_da_categoria(feeds, nome_categoria):
    return [
        f for f in feeds
        if any(c["label"] == nome_categoria for c in f.get("categories", []))
    ]

def pegar_feed(feeds):
    tempo = datetime.now().hour

    if 0 <= tempo <= 17:
        label = "Manhã"
    else:
        label = "Tarde"

    noticias = feeds_da_categoria(feeds, label)
    if not noticias:
        raise SystemExit(f"Nenhum feed na categoria '{label}'")

    return random.choice(noticias), label.upper()

def feedrss():
    with httpx.Client(timeout=15, follow_redirects=True) as client:
        headers = login(client)
        feeds = listar_feeds(client, headers)

        feed, periodo = pegar_feed(feeds)

        a = 0
        for i in feeds:
            print(f"ID: {a} JSON: {i}")
            a += 1

        itens = noticias_do_feed(client, headers, feed["id"], n=6)

        noticias = [
            {
                "title": item["title"],
                "data": datetime.fromtimestamp(item["published"]),
                "link": (item.get("canonical") or item.get("alternate") or [{}])[0].get("href", ""),
                "texto": html_para_texto(item.get("summary", {}).get("content", "")),
                "imagem": primeira_imagem(
                    item.get("summary", {}).get("content", ""),
                    base_url=(item.get("canonical") or item.get("alternate") or [{}])[0].get("href", ""),
                ),
            }
            
            for item in itens
        ]

        return noticias, periodo