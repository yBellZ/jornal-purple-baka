from feedrss import feedrss
from ia_resumo import ia_resumo
from mandar_discord import rodar_tudo

def main():
    feed, periodo = feedrss()
    resumo = ia_resumo(feed[0]["title"], feed[0]["texto"])

    rodar_tudo(feed, resumo, periodo)

    print(feed[0]["texto"])
    print(f"\n{"-" * 60}\n")
    print(f"Resumo muehehehe:\n{resumo}")
    

if __name__ == "__main__":
    main()