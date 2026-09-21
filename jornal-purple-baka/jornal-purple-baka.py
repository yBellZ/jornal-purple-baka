from feedrss import feedrss
from ia_resumo import ia_resumo

def main():
    feed = feedrss()
    resumo = ia_resumo(feed[0]["texto"])

    print(feed[0]["texto"])
    print(f"\n{"-" * 60}\n")
    print(f"Resumo muehehehe:\n{resumo}")
    

if __name__ == "__main__":
    main()