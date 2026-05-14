import json


def iniciar_navegadores(playwright):

    navegadores = []

    qtd = 3

    # lê config
    try:

        with open(
            "config_app.json",
            "r",
            encoding="utf-8"
        ) as f:

            dados = json.load(f)

            qtd = dados.get(
                "navegadores",
                3
            )

    except:
        pass

    for i in range(qtd):

        perfil = f"perfis/edge_{i+1}"

        navegador = playwright.chromium.launch_persistent_context(

            user_data_dir=perfil,

            channel="msedge",

            headless=False,

            no_viewport=True,

            args=[
                "--start-maximized"
            ]
        )

        navegadores.append(
            navegador
        )

    return navegadores