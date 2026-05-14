import random


PALAVRAS_INICIO = [
    "impacto",
    "beneficios",
    "avancos",
    "historia",
    "curiosidades",
    "o futuro"
]

PALAVRAS_TEMA = [
    "internet",
    "tecnologia",
    "astronomia",
    "robotica",
    "inteligencia artificial",
    "programacao"
]

PALAVRAS_CONTEXTO = [
    "moderna",
    "atual",
    "digital",
    "na educacao",
    "na sociedade",
    "em 2026"
]


def gerar_pesquisa():
    return (
        f"{random.choice(PALAVRAS_INICIO)} "
        f"de {random.choice(PALAVRAS_TEMA)} "
        f"{random.choice(PALAVRAS_CONTEXTO)}"
    )
