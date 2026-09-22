from dotenv import load_dotenv
import os
import httpx

load_dotenv()

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def montar_payload(feed, resumo, periodo):
    return {
        "flags": 32768,
        "components": [
            {
            "type": 17,
            "components": [
                {
                "type": 10,
                "content": f"## <:B_Baka:1539255932977025084> JORNAL DA {periodo}\n\n[**{feed[0]['title']}**]({feed[0]['link']})\n> {resumo}"
                },
                {
                "type": 14,
                "divider": False
                },
                {
                "type": 12,
                "items": [
                    {
                    "media": {
                        "url": feed[0]['imagem']
                    }
                    }
                ]
                },
                {
                "type": 14,
                "spacing": 2,
                },
                {
                "type": 10,
                "content": f"### `📰` **MAIS NOTÍCIAS:**\n> * [**{feed[1]['title']}**]({feed[1]['link']})\n> * [**{feed[2]['title']}**]({feed[2]['link']})\n> * [**{feed[3]['title']}**]({feed[3]['link']})\n> * [**{feed[4]['title']}**]({feed[4]['link']})\n> * [**{feed[5]['title']}**]({feed[5]['link']})\n\n-# [Github do bot](https://github.com/yBellZ/jornal-purple-baka)"
                }
            ],
            "accent_color": 8135871
            }
        ],
    }

def enviar_content_discord(client: httpx.Client, feed, resumo, periodo):
    payload = montar_payload(feed, resumo, periodo)
    resp = client.post(WEBHOOK_URL, json=payload)

    if resp.status_code >= 400:
            print(resp.status_code, resp.text)

    resp.raise_for_status()


def rodar_tudo(feed, resumo, periodo):
    timeout = httpx.Timeout(30.0, connect=10.0)
    with httpx.Client(http2=True, timeout=timeout) as client:
        enviar_content_discord(client=client, feed=feed, resumo=resumo, periodo=periodo)
