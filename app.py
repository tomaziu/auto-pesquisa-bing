import customtkinter as ctk
from tkinter import END
import subprocess
import threading
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Auto Pesquisa - Bing")
        self.geometry("510x720")
        self.minsize(490, 660)

        # ===================== CORES =====================

        self.cor_principal = "#00d4ff"
        self.cor_secundaria = "#6366f1"
        self.cor_bg = "#0a0a0f"
        self.cor_card = "#12121a"

        self.configure(fg_color=self.cor_bg)

        # ===================== TOPMOST =====================

        self.attributes("-topmost", True)

        self.bind(
            "<Unmap>",
            lambda e: self.attributes("-topmost", False)
        )

        self.bind(
            "<Map>",
            lambda e: self.attributes("-topmost", True)
        )

        self.processo = None

        # ===================== TOPO =====================

        self.topo = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=90
        )

        self.topo.pack(fill="x", pady=(5, 0))

        self.titulo = ctk.CTkLabel(
            self.topo,
            text="AUTO PESQUISA",
            font=("Segoe UI", 24, "bold"),
            text_color=self.cor_principal
        )

        self.titulo.pack(pady=(12, 0))

        self.subtitulo = ctk.CTkLabel(
            self.topo,
            text="Automação de Pesquisas • Bing",
            font=("Segoe UI", 11),
            text_color="#94a3b8"
        )

        self.subtitulo.pack()

        ctk.CTkFrame(
            self.topo,
            fg_color=self.cor_principal,
            height=2
        ).pack(fill="x", padx=60, pady=(10, 0))

        # ===================== CONTAINER =====================

        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.cor_card,
            corner_radius=20,
            border_width=0
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=16
        )

        # ===================== STATUS =====================

        self.status = ctk.CTkLabel(
            self.container,
            text="● PARADO",
            font=("Segoe UI", 13, "bold"),
            text_color="#f87171"
        )

        self.status.pack(pady=(12, 8))

        # ===================== CONFIG =====================

        self.criar_secao(
            "Configurações",
            self.container
        )

        self.frame_inputs = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        self.frame_inputs.pack(
            fill="x",
            padx=16,
            pady=(0, 6)
        )

        self.frame_inputs.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.criar_input(
            self.frame_inputs,
            "Navegadores",
            "navegadores",
            "4",
            0
        )

        self.criar_input(
            self.frame_inputs,
            "Tempo (s)",
            "login",
            "5",
            1
        )

        self.entry_navegadores.bind(
            "<KeyRelease>",
            lambda e: self.atualizar_niveis()
        )

        # ===================== PATH =====================

        self.criar_input_full(
            "Caminho do Navegador"
        )

        # ===================== NÍVEIS =====================

        self.criar_secao(
            "Nível de Cada Navegador",
            self.container
        )

        self.frame_niveis = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        self.frame_niveis.pack(
            fill="x",
            padx=16,
            pady=(0, 8)
        )

        self.niveis_vars = []

        # ===================== CHECKBOX =====================

        self.auto_inicio = ctk.BooleanVar(value=False)

        self.checkbox_auto = ctk.CTkCheckBox(
            self.container,
            text="Iniciar automaticamente",
            variable=self.auto_inicio,
            font=("Segoe UI", 12),
            text_color="#e2e8f0",
            checkbox_width=16,
            checkbox_height=16,
            command=self.checkbox_evento
        )

        self.checkbox_auto.pack(
            anchor="w",
            padx=20,
            pady=(4, 10)
        )

        # ===================== BOTÕES =====================

        self.frame_botoes = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )

        self.frame_botoes.pack(
            fill="x",
            padx=16,
            pady=(2, 10)
        )

        self.frame_botoes.grid_columnconfigure(
            (0, 1),
            weight=1
        )

        self.btn_abrir = ctk.CTkButton(
            self.frame_botoes,
            text="🌐 Abrir Navegadores",
            height=38,
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            fg_color=self.cor_secundaria,
            hover_color="#4f52cc",
            command=self.iniciar
        )

        self.btn_abrir.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=4,
            pady=(0, 8),
            sticky="ew"
        )

        self.btn_iniciar = ctk.CTkButton(
            self.frame_botoes,
            text="▶ INICIAR",
            height=38,
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            fg_color="#22c55e",
            hover_color="#16a34a",
            command=self.enviar_enter
        )

        self.btn_parar = ctk.CTkButton(
            self.frame_botoes,
            text="■ PARAR",
            height=38,
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.parar
        )

        self.btn_iniciar.grid(
            row=1,
            column=0,
            padx=4,
            pady=4,
            sticky="ew"
        )

        self.btn_parar.grid(
            row=1,
            column=1,
            padx=4,
            pady=4,
            sticky="ew"
        )

        # ===================== CONSOLE =====================

        self.criar_secao(
            "Console",
            self.container
        )

        self.terminal = ctk.CTkTextbox(
            self.container,
            height=220,
            corner_radius=14,
            fg_color="#0a0a12",
            font=("Consolas", 11),
            text_color="#67e8f9",
            border_width=0
        )

        self.terminal.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(4, 14)
        )

        # ===================== INIT =====================

        self.carregar_config()

        self.atualizar_niveis()

        self.atualizar_botoes()

        self.log("🚀 Interface carregada com sucesso.")

    # =========================================================

    def criar_secao(self, titulo, parent):

        label = ctk.CTkLabel(
            parent,
            text=titulo.upper(),
            font=("Segoe UI", 11, "bold"),
            text_color="#818cf8"
        )

        label.pack(
            anchor="w",
            padx=20,
            pady=(10, 4)
        )

    # =========================================================

    def criar_input(
        self,
        parent,
        texto,
        nome,
        valor_padrao,
        coluna
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=coluna,
            padx=4,
            sticky="ew"
        )

        ctk.CTkLabel(
            frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="w", pady=(0, 3))

        entry = ctk.CTkEntry(
            frame,
            height=34,
            corner_radius=10,
            border_width=1,
            border_color="#334155",
            fg_color="#1e2233",
            font=("Segoe UI", 11)
        )

        entry.pack(fill="x")

        entry.insert(0, valor_padrao)

        entry.bind(
            "<KeyRelease>",
            lambda e: self.salvar_config()
        )

        setattr(
            self,
            f"entry_{nome}",
            entry
        )

    # =========================================================

    def criar_input_full(self, texto):

        ctk.CTkLabel(
            self.container,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="w", padx=20, pady=(8, 3))

        self.entry_path = ctk.CTkEntry(
            self.container,
            height=34,
            corner_radius=10,
            border_width=1,
            border_color="#334155",
            fg_color="#1e2233",
            font=("Segoe UI", 11)
        )

        self.entry_path.pack(
            fill="x",
            padx=20
        )

        self.entry_path.insert(
            0,
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        )

        self.entry_path.bind(
            "<KeyRelease>",
            lambda e: self.salvar_config()
        )

    # =========================================================

    def atualizar_niveis(self):

        niveis_anteriores = [
            var.get()
            for var in self.niveis_vars
        ]

        for widget in self.frame_niveis.winfo_children():
            widget.destroy()

        self.niveis_vars.clear()

        try:
            total = int(self.entry_navegadores.get())
        except:
            total = 1

        for i in range(total):

            frame = ctk.CTkFrame(
                self.frame_niveis,
                fg_color="#1a1a25",
                corner_radius=10,
                height=40
            )

            frame.pack(
                fill="x",
                pady=3
            )

            label = ctk.CTkLabel(
                frame,
                text=f"Navegador {i+1}",
                font=("Segoe UI", 11, "bold")
            )

            label.pack(
                side="left",
                padx=12,
                pady=8
            )

            valor = "1"

            if i < len(niveis_anteriores):
                valor = niveis_anteriores[i]

            var = ctk.StringVar(value=valor)

            combo = ctk.CTkComboBox(
                frame,
                values=["1", "2"],
                variable=var,
                width=85,
                height=30,
                corner_radius=8,
                font=("Segoe UI", 11),
                command=lambda valor: self.salvar_config()
            )

            combo.pack(
                side="right",
                padx=8,
                pady=5
            )

            self.niveis_vars.append(var)

        self.salvar_config()

    # =========================================================

    def checkbox_evento(self):

        self.atualizar_botoes()

        self.salvar_config()

    # =========================================================

    def log(self, texto):

        if "LIMITE DE PONTOS ATINGIDO" in texto:

            self.terminal.insert(
                END,
                f"{texto}\n",
                "verde"
            )

        else:

            self.terminal.insert(
                END,
                f"{texto}\n"
            )

        self.terminal.tag_config(
            "verde",
            foreground="#22c55e"
        )

        self.terminal.see("end")

    # =========================================================

    def atualizar_botoes(self):

        if self.auto_inicio.get():

            self.btn_iniciar.grid_remove()

            self.btn_parar.grid(
                row=1,
                column=0,
                columnspan=2,
                padx=4,
                pady=4,
                sticky="ew"
            )

        else:

            self.btn_parar.grid(
                row=1,
                column=1,
                padx=4,
                pady=4,
                sticky="ew"
            )

            self.btn_iniciar.grid(
                row=1,
                column=0,
                padx=4,
                pady=4,
                sticky="ew"
            )

    # =========================================================

    def carregar_config(self):

        if os.path.exists("config_app.json"):

            try:

                with open(
                    "config_app.json",
                    "r",
                    encoding="cp1252"
                ) as f:

                    config = json.load(f)

                self.entry_navegadores.delete(0, "end")

                self.entry_navegadores.insert(
                    0,
                    config.get("navegadores", 4)
                )

                self.entry_login.delete(0, "end")

                self.entry_login.insert(
                    0,
                    config.get("tempo_login", 5)
                )

                self.entry_path.delete(0, "end")

                self.entry_path.insert(
                    0,
                    config.get(
                        "browser_path",
                        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                    )
                )

                self.auto_inicio.set(
                    config.get("auto_inicio", False)
                )

                self.atualizar_niveis()

                niveis = config.get("niveis", [])

                for i, nivel in enumerate(niveis):

                    if i < len(self.niveis_vars):

                        self.niveis_vars[i].set(
                            str(nivel)
                        )

                self.log(
                    "[CONFIG] Configurações carregadas."
                )

            except Exception as e:

                self.log(
                    f"[ERRO] {e}"
                )

    # =========================================================

    def salvar_config(self):

        try:

            config = {

                "navegadores": int(
                    self.entry_navegadores.get()
                ),

                "tempo_login": int(
                    self.entry_login.get()
                ),

                "browser_path": self.entry_path.get(),

                "auto_inicio": self.auto_inicio.get(),

                "niveis": [
                    var.get()
                    for var in self.niveis_vars
                ]
            }

            with open(
                "config_app.json",
                "w",
                encoding="cp1252"
            ) as f:

                json.dump(
                    config,
                    f,
                    indent=4
                )

        except:
            pass

    # =========================================================

    def iniciar(self):

        self.status.configure(
            text="● EXECUTANDO",
            text_color="#4ade80"
        )

        self.btn_abrir.configure(
            state="disabled"
        )

        self.log(
            "[SISTEMA] Abrindo navegadores..."
        )

        def rodar():

            try:

                niveis = ",".join(
                    [
                        var.get()
                        for var in self.niveis_vars
                    ]
                )

                self.processo = subprocess.Popen(

                    [
                        "py",
                        "main.py",
                        niveis
                    ],

                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="cp1252",
                    universal_newlines=True
                )

                if self.auto_inicio.get():

                    self.processo.stdin.write("\n")

                    self.processo.stdin.flush()

                while True:

                    linha = self.processo.stdout.readline()

                    if not linha:
                        break

                    linha = linha.strip()

                    if linha:

                        self.after(
                            0,
                            lambda l=linha: self.log(l)
                        )

            except Exception as e:

                self.log(
                    f"[ERRO] {e}"
                )

            finally:

                self.status.configure(
                    text="● FINALIZADO",
                    text_color="#60a5fa"
                )

                self.btn_abrir.configure(
                    state="normal"
                )

        threading.Thread(
            target=rodar,
            daemon=True
        ).start()

    # =========================================================

    def enviar_enter(self):

        if self.processo:

            try:

                self.processo.stdin.write("\n")

                self.processo.stdin.flush()

                self.log(
                    "[SISTEMA] Sinal de início enviado."
                )

            except:

                self.log(
                    "[ERRO] Não foi possível enviar comando."
                )

    # =========================================================

    def parar(self):

        if self.processo:

            try:

                self.processo.terminate()

                self.log(
                    "[SISTEMA] Processo parado pelo usuário."
                )

            except:
                pass

            self.status.configure(
                text="● PARADO",
                text_color="#f87171"
            )

            self.btn_abrir.configure(
                state="normal"
            )


if __name__ == "__main__":

    app = App()

    app.mainloop()