from dotenv import load_dotenv
import os
import httpx

load_dotenv()

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def montar_payload(feed, resumo: str):
    return {
        "flags": 32768,
        "components": [
            {
            "type": 17,
            "components": [
                {
                "type": 10,
                "content": f"## :black_cat:  JORNAL DIÁRIO\n\n[{feed[0]["title"]}]({feed[0]["link"]})\n>  -# {resumo}\n\n### `📰` **MAIS NOTÍCIAS:**\n> * [{feed[1]["title"]}]({feed[1]["link"]})\n> * [{feed[2]["title"]}]({feed[2]["link"]})\n> * [{feed[3]["title"]}]({feed[3]["link"]})\n> * [{feed[4]["title"]}]({feed[4]["link"]})\n> * [{feed[5]["title"]}]({feed[5]["title"]})"
                }
            ],
            "accent_color": 8135871
            }
        ]
    }

def enviar_content_discord(client: httpx.Client, feed, resumo: str):
    payload = montar_payload(feed, resumo)
    resp = client.post(WEBHOOK_URL, json=payload)

    if resp.status_code >= 400:
            print(resp.status_code, resp.text)

    resp.raise_for_status()


def rodar_tudo(feed: dict, resumo: str):
    resumo_ia = resumo
    feedrss = feed

    timeout = httpx.Timeout(30.0, connect=10.0)
    with httpx.Client(http2=True, timeout=timeout) as client:
        enviar_content_discord(client=httpx.Client, resumo=feedrss, feed=resumo_ia)
