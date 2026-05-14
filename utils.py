def carregar_pesquisas():

    with open(
        "pesquisas.txt",
        "r",
        encoding="utf-8"
    ) as arquivo:

        return [
            linha.strip()
            for linha in arquivo.readlines()
            if linha.strip()
        ]