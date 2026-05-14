import time

from playwright.sync_api import sync_playwright

from browser_manager import abrir_navegadores, fechar_navegadores
from config_manager import ajustar_niveis, carregar_config
from logger import log
from rewards_runner import executar_automacao


def main():
    config = carregar_config()

    total_navegadores = int(config["navegadores"])
    tempo_login = int(config["tempo_login"])
    browser_path = config["browser_path"]
    niveis = ajustar_niveis(config.get("niveis", []), total_navegadores)

    with sync_playwright() as playwright:
        navegadores = abrir_navegadores(
            playwright,
            total_navegadores,
            browser_path,
            niveis,
            log
        )

        try:
            log(f"\n[SISTEMA] {total_navegadores} navegadores abertos.")
            log("[SISTEMA] Aguardando comando para iniciar...")

            input()

            log(f"[SISTEMA] Aguardando {tempo_login}s...")
            time.sleep(tempo_login)

            executar_automacao(navegadores, log)

            log("\n[SISTEMA] Pesquisas finalizadas.")

        finally:
            fechar_navegadores(navegadores)


if __name__ == "__main__":
    main()
