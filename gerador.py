import random

temas = [
    "tecnologia",
    "inteligência artificial",
    "espaço",
    "programação",
    "energia solar",
    "robótica",
    "ciência",
    "computadores",
    "internet",
    "carros elétricos",
    "astronomia",
    "saúde",
    "história",
    "educação",
    "física"
]

acoes = [
    "como funciona",
    "história de",
    "benefícios de",
    "curiosidades sobre",
    "impacto de",
    "evolução da",
    "avanços em",
    "o futuro de"
]

extras = [
    "na sociedade",
    "na medicina",
    "moderna",
    "em 2026",
    "no mundo",
    "na educação",
    "digital",
    "atual"
]

def gerar_pesquisa():

    return (
        f"{random.choice(acoes)} "
        f"{random.choice(temas)} "
        f"{random.choice(extras)}"
    )