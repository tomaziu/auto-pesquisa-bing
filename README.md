# 🚀 Auto Pesquisa Bing

Automação de pesquisas no Bing utilizando Python + Playwright com interface moderna em CustomTkinter.

---

## ✨ Funcionalidades

- 🌐 Abertura automática de múltiplos navegadores
- 🎯 Sistema de níveis por navegador
- ⚡ Pesquisas automáticas no Bing
- 💾 Salvamento automático das configurações
- 🖥️ Interface moderna e compacta
- 📊 Console integrado em tempo real
- 🔄 Suporte a auto início
- 👤 Perfis separados para cada navegador
- 🎲 Pesquisas aleatórias humanizadas
- 🛑 Controle de iniciar/parar processos

---

# 🖼️ Interface

## Tela Principal

- Configuração rápida
- Seleção de níveis
- Controle de navegadores
- Console em tempo real

---

# 📦 Tecnologias Utilizadas

- Python 3
- Playwright
- CustomTkinter
- Microsoft Edge

---

# ⚙️ Instalação

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/tomaziu/auto-pesquisa-bing.git
```

---

## 2️⃣ Entre na pasta

```bash
cd auto-pesquisa-bing
```

---

## 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Instale os navegadores do Playwright

```bash
playwright install
```

---

# ▶️ Como usar

Execute:

```bash
py app.py
```

ou

```bash
python app.py
```

---

# 🧠 Sistema de Níveis

| Nível | Limite Diário |
|------|----------------|
| 1 | 30 pontos |
| 2 | 90 pontos |

Cada navegador pode possuir um nível diferente.

---

# 📁 Estrutura do Projeto

```bash
📦 auto-pesquisa-bing
 ┣ 📂 perfis
 ┣ 📜 app.py
 ┣ 📜 main.py
 ┣ 📜 config.py
 ┣ 📜 utils.py
 ┣ 📜 gerador.py
 ┣ 📜 navegadores.py
 ┣ 📜 pesquisas.txt
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```

---

# ⚠️ Importante

As pastas de perfis NÃO devem ser enviadas para o GitHub.

Certifique-se de possuir no `.gitignore`:

```gitignore
perfil_*/
perfis/
config_app.json
__pycache__/
*.pyc
```

---

# 🔒 Observações

- O projeto utiliza perfis persistentes do navegador.
- Pode armazenar sessões e cookies localmente.
- Utilize com responsabilidade.

---

# 📌 Requisitos

- Windows 10/11
- Python 3.10+
- Microsoft Edge instalado

---

# 👨‍💻 Autor

Projeto desenvolvido por Thomaz de Morais Nunes.

---

# ⭐ Contribuição

Sinta-se livre para abrir:

- Issues
- Pull Requests
- Sugestões
- Melhorias

---

# 📄 Licença

Este projeto é apenas para fins educacionais.