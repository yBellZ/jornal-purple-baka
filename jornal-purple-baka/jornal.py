from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

BASE = os.environ["BASE"].rstrip("/")
USER = os.environ["USER"]
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

def html_para_texto(html):
    return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)

def main():
    with httpx.Client(timeout=15, follow_redirects=True) as client:
        headers = login(client)
        feeds = listar_feeds(client, headers)

        # Exemplo: notícias do primeiro feed da lista
        feed = feeds[0]
        print(f"== {feed['title']} ==\n")

        itens = noticias_do_feed(client, headers, feed["id"], n=6)

        noticias = [
        {
            "titulo": item["title"],
            "data": datetime.fromtimestamp(item["published"]),
            "link": (item.get("canonical") or item.get("alternate") or [{}])[0].get("href", ""),
            "texto": html_para_texto(item.get("summary", {}).get("content", "")),
        }
        for item in itens
]
        return noticias


if __name__ == "__main__":
    main()