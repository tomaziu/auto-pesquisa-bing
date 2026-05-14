from playwright.sync_api import sync_playwright
import time
import random
import json
import os
import sys

def log(texto):
    print(texto, flush=True)

TOTAL_PESQUISAS = 1000

# =========================
# CONFIG
# =========================

def carregar_config():

    if os.path.exists("config_app.json"):

        with open(
            "config_app.json",
            "r",
            encoding="cp1252"
        ) as f:

            return json.load(f)

    return {
        "navegadores": 3,
        "tempo_login": 5,
        "browser_path": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "auto_inicio": False,
        "niveis": ["1", "1", "1"]
    }


# =========================
# GERAR PESQUISA
# =========================

def gerar_pesquisa():

    palavras1 = [
        "impacto",
        "benefícios",
        "avanços",
        "história",
        "curiosidades",
        "o futuro"
    ]

    palavras2 = [
        "internet",
        "tecnologia",
        "astronomia",
        "robótica",
        "inteligência artificial",
        "programação"
    ]

    palavras3 = [
        "moderna",
        "atual",
        "digital",
        "na educação",
        "na sociedade",
        "em 2026"
    ]

    return (
        f"{random.choice(palavras1)} "
        f"de {random.choice(palavras2)} "
        f"{random.choice(palavras3)}"
    )


# =========================
# CONFIGURAÇÕES
# =========================

config = carregar_config()

NUM_NAVEGADORES = config["navegadores"]

TEMPO_LOGIN = config["tempo_login"]

BROWSER_PATH = config["browser_path"]

NIVEIS = config.get("niveis", [])

DELAY_MIN = 2
DELAY_MAX = 4

# Garante quantidade correta
while len(NIVEIS) < NUM_NAVEGADORES:
    NIVEIS.append("1")

# =========================
# PLAYWRIGHT
# =========================

with sync_playwright() as p:

    navegadores = []

    # =========================
    # ABRIR NAVEGADORES
    # =========================

    for i in range(NUM_NAVEGADORES):

        contexto = p.chromium.launch_persistent_context(

            user_data_dir=f"perfil_{i+1}",

            executable_path=BROWSER_PATH,

            headless=False,

            channel="msedge",

            args=[
                "--start-maximized",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-session-crashed-bubble",
                "--disable-features=msRestoreTabsOnStartup",
                "--homepage=about:blank"
            ],

            no_viewport=True
        )

        time.sleep(2)

        # PEGA PRIMEIRA ABA
        if len(contexto.pages) > 0:

            pagina = contexto.pages[0]

        else:

            pagina = contexto.new_page()

        # FECHA EXTRAS
        paginas = contexto.pages.copy()

        if len(paginas) > 1:

            for extra in paginas[1:]:

                try:
                    extra.close()
                except:
                    pass

        pagina.goto(
            "about:blank",
            wait_until="domcontentloaded"
        )

        # =========================
        # NIVEL / LIMITE
        # =========================

        nivel = int(NIVEIS[i])

        limite = 30

        if nivel == 2:
            limite = 90

        navegadores.append({

            "contexto": contexto,
            "pagina": pagina,
            "nivel": nivel,
            "limite": limite,
            "pontos": 0,
            "limite_avisado": False

        })

        log(
            f"[NAVEGADOR {i+1}] "
            f"Inicializado com sucesso "
            f"(Nível {nivel} - Máx {limite} pontos)"
        )

    log(
        f"\n[SISTEMA] {NUM_NAVEGADORES} navegadores abertos."
    )

    # =========================
    # ESPERA INICIAR
    # =========================

    log(
        "[SISTEMA] Aguardando comando para iniciar..."
    )

    input()

    log(
        f"[SISTEMA] Aguardando {TEMPO_LOGIN}s..."
    )

    time.sleep(TEMPO_LOGIN)

    contador = 0

    ultima_pesquisa = {}

    for i in range(NUM_NAVEGADORES):

        ultima_pesquisa[i] = 0

    # =========================
    # LOOP
    # =========================

    while contador < TOTAL_PESQUISAS:

        for indice, navegador_data in enumerate(navegadores):

            if contador >= TOTAL_PESQUISAS:
                break

            contexto = navegador_data["contexto"]

            limite = navegador_data["limite"]

            pontos = navegador_data["pontos"]

            pesquisa = gerar_pesquisa()

            agora = time.time()

            tempo_desde = agora - ultima_pesquisa[indice]

            # =========================
            # VERIFICA LIMITE
            # =========================

            if pontos >= limite:

                if not navegador_data["limite_avisado"]:

                    log(
                        f"\n[NAVEGADOR {indice+1}] "
                        f"LIMITE DE PONTOS ATINGIDO "
                        f"({pontos}/{limite})"
                    )

                    navegador_data["limite_avisado"] = True

                continue

            log(
                f"\n=============================="
            )

            log(
                f"[NAVEGADOR {indice+1}] "
                f"INICIANDO PESQUISA"
            )

            log(
                f"[NAVEGADOR {indice+1}] "
                f"Nível Rewards: {navegador_data['nivel']}"
            )

            log(
                f"[NAVEGADOR {indice+1}] "
                f"Pesquisa número: {contador+1}"
            )

            if ultima_pesquisa[indice] != 0:

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Última pesquisa há "
                    f"{tempo_desde:.2f}s"
                )

            log(
                f"[NAVEGADOR {indice+1}] "
                f"Pesquisa: {pesquisa}"
            )

            try:

                paginas = contexto.pages.copy()

                # GARANTE SOMENTE 1 ABA
                if len(paginas) > 1:

                    for extra in paginas[1:]:

                        try:
                            extra.close()
                        except:
                            pass

                # PEGA ABA PRINCIPAL
                if len(contexto.pages) == 0:

                    pagina = contexto.new_page()

                else:

                    pagina = contexto.pages[0]

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Abrindo Bing..."
                )

                pagina.goto(
                    "https://www.bing.com/?toWww=1",
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                time.sleep(
                    random.uniform(0.15, 0.35)
                )

                # PESQUISA
                try:

                    barra = pagina.locator(
                        'textarea[name="q"]'
                    )

                    if barra.count() == 0:

                        barra = pagina.locator(
                            'input[name="q"]'
                        )

                    barra.first.click()

                except:

                    pagina.keyboard.press("Ctrl+L")

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Digitando pesquisa..."
                )

                pagina.keyboard.type(
                    pesquisa,
                    delay=random.randint(5, 12)
                )

                time.sleep(
                    random.uniform(0.08, 0.20)
                )

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Enviando pesquisa..."
                )

                pagina.keyboard.press(
                    "Enter"
                )

                pagina.wait_for_load_state(
                    "domcontentloaded"
                )

                log(
                    f"[NAVEGADOR {indice+1}] Página carregada."
                )

                # SCROLL
                pagina.mouse.wheel(
                    0,
                    random.randint(400, 1200)
                )

                tempo = random.uniform(
                    0.7,
                    1.8
                )

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Lendo por {tempo:.2f}s"
                )

                time.sleep(tempo)

                ultima_pesquisa[indice] = time.time()

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Pesquisa concluída."
                )

                # =========================
                # PONTOS
                # =========================

                navegador_data["pontos"] += 3

                pontos_atuais = navegador_data["pontos"]

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Pontos: "
                    f"{pontos_atuais}/{limite}"
                )

                if pontos_atuais >= limite:

                    log(
                        f"[NAVEGADOR {indice+1}] "
                        f"LIMITE DE PONTOS ATINGIDO "
                        f"({pontos_atuais}/{limite})"
                    )

                    navegador_data["limite_avisado"] = True

            except Exception as e:

                log(
                    f"[NAVEGADOR {indice+1}] "
                    f"Erro: {e}"
                )

            contador += 1

            delay = random.uniform(
                DELAY_MIN,
                DELAY_MAX
            )

            log(
                f"[NAVEGADOR {indice+1}] "
                f"Próxima pesquisa em "
                f"{delay:.2f} segundos"
            )

            log(
                f"=============================="
            )

            time.sleep(delay)

        if all(
            navegador_data["pontos"] >= navegador_data["limite"]
            for navegador_data in navegadores
        ):

            log(
                "\n[SISTEMA] Todos os navegadores atingiram o limite de pontos."
            )

            break

    log(
        "\n[SISTEMA] Pesquisas finalizadas."
    )

    # =========================
    # FECHAR TUDO
    # =========================

    for navegador_data in navegadores:

        try:

            navegador_data["contexto"].close()

        except:
            pass
