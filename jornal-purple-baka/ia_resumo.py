from dotenv import load_dotenv
import os
import openai

load_dotenv()

LLAMA_URL = os.environ["LLAMA_URL"]
print(f"OLLAMA URL: {LLAMA_URL}")

client = openai.OpenAI(base_url=LLAMA_URL, api_key="no-key-required")

SYSTEM_PROMPT = """Você resume notícias em português do Brasil, com um texto vivo e envolvente.

Você receberá o texto de uma notícia. Escreva um resumo dela com cerca de 200 caracteres (3 a 4 linhas curtas), em texto corrido, num único parágrafo.

Regras:
1. Responda somente com o resumo. Sem título, sem marcadores, sem introdução, sem conclusão, sem comentários.
2. Use apenas informações presentes no texto. Nunca invente fatos, números, nomes ou datas.
3. Diga o que aconteceu, com quem e onde. Ignore propaganda, "leia mais", "assine" e chamadas para redes sociais.
4. Se a notícia for engraçada, curiosa ou leve, escreva com humor e personalidade, como quem conta a novidade para um amigo.
5. Se a notícia for séria (crime, morte, tragédia, guerra, saúde, política, economia), mantenha um tom claro e respeitoso, sem piadas.
6. Seja curto: no máximo 250 caracteres.
7. Se o texto estiver vazio ou for insuficiente, responda apenas: Sem conteúdo suficiente para resumir.

Exemplo 1

Texto:
A prefeitura anunciou nesta segunda que a avenida central ficará interditada por 30 dias para obras de drenagem. O desvio será feito pela rua das Flores. Segundo o secretário, o investimento é de R$ 2 milhões. Leia também: veja outras notícias da cidade.

Resumo:
Prepare a paciência: a avenida central ficará interditada por 30 dias para obras de drenagem, com desvio pela rua das Flores. A prefeitura vai investir R$ 2 milhões na obra.

Exemplo 2

Texto:
Um gato invadiu a sessão da Câmara de Vereadores de uma cidade do interior, subiu na mesa e dormiu em cima da pauta. A sessão foi suspensa por dez minutos até o animal ser retirado por um assessor.

Resumo:
Um gato invadiu a sessão da Câmara, subiu na mesa e tirou uma soneca em cima da pauta. Resultado: sessão suspensa por dez minutos até um assessor convencer o vereador de quatro patas a sair."""

def ia_resumo(title, feedrss: str) -> str:
    completion = client.chat.completions.create(
        model="unsloth/Qwen3.5-0.8B-GGUF:Q4_K_XL",
        max_tokens=8192,
        temperature=0.7,
        top_p=0.8,
        presence_penalty=1.5,
        extra_body={
            "top_k": 20,
            "min_p": 0.0,
            "chat_template_kwargs": {"enable_thinking": False},
        },
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Título: {title}\nTexto: {feedrss}"},
        ],
    )

    choice = completion.choices[0]
    if choice.finish_reason == "length":
        print("aviso: resposta cortada por max_tokens")

    return (choice.message.content or "").strip()