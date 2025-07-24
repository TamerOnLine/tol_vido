# 🎬 tol_vido – YouTube to Clean Text (LLM Powered)

[![Build](https://github.com/TamerOnLine/pro_venv/actions/workflows/test-pro_venv.yml/badge.svg)](https://github.com/TamerOnLine/pro_venv/actions)
[![License](https://img.shields.io/github/license/TamerOnLine/pro_venv?style=flat-square)](LICENSE)

`tol_vido` is a powerful, local-first Python tool that transcribes YouTube videos into well-formatted German paragraphs using Large Language Models (LLMs) like **Mistral** via `.gguf`. It's fast, customizable, and runs entirely on your machine.

---

## 🚀 Features

- ✅ Download and convert YouTube audio with `yt-dlp`
- ✅ Segment and transcribe speech with `SpeechRecognition` (Google)
- ✅ Format the raw text using a local LLM (e.g. Mistral via `llama-cpp-python`)
- ✅ Full local processing — **no cloud required**
- ✅ Modular and extensible codebase
- ✅ Auto-setup: project config, `venv`, VS Code files, and more

---

## 🧱 Project Structure

```bash
tol_vido/
├── 01_pro_venv.py          # Setup: venv, config, VS Code
├── 02_start_llm_server.py  # Run local LLM server
├── 03_main.py              # Entry point runner
├── app.py                  # Main processing logic
├── extract_text_from_video.py  # Transcribe audio from video
├── format_text.py          # Format using local LLM
├── output.txt              # Raw transcription result
├── formatted_output.txt    # Final cleaned-up version
├── setup-config.json       # Project metadata
├── requirements.txt        # Dependencies
├── env-info.txt            # Python & installed packages
├── tools/
│   └── download_model.py   # GGUF model downloader
└── .github/workflows/      # GitHub Actions
```

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YourUsername/tol_vido.git
cd tol_vido
```

### 2. Run the setup script

```bash
python 01_pro_venv.py
```

This will:
- Create a virtual environment
- Install dependencies
- Generate `main.py`, `app.py`, `.vscode/` settings

### 3. Start the LLM server

```bash
python 02_start_llm_server.py
```

> Make sure the `.gguf` model exists in the `models/` folder. You can use `tools/download_model.py` to fetch it from Hugging Face.

### 4. Run the full pipeline

```bash
python 03_main.py
```

You’ll be prompted for a YouTube URL. After processing, the result will be saved in:

- `output.txt`: raw transcription  
- `formatted_output.txt`: structured, punctuated paragraphs

---

## 📦 Requirements

Python 3.12+ and:

```text
yt-dlp
speechrecognition
pydub
transformers
torch
llama-cpp-python[server]
fastapi
uvicorn
tiktoken
starlette
...
```

Install manually:
```bash
pip install -r requirements.txt
```

---

## 🌐 Model Setup (GGUF)

### 1. Create `.env` file

```env
# Required for downloading and running the model
MODEL_NAME=mistral-7b-instruct-v0.1.Q4_K_M.gguf

# Local path to the GGUF model file
MODEL=r:/tol_vido/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf

# LLM Server runtime parameters
N_CTX=4096
N_THREADS=8
N_GPU_LAYERS=35
VERBOSE=true
```

> These are used in both `tools/download_model.py` and `02_start_llm_server.py`.

### 2. Download the model

```bash
python tools/download_model.py
```

Model will be downloaded from:
> [TheBloke/Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

---

## 💡 Notes

- All audio processing and formatting are local.
- Transcription uses `Google Speech Recognition` — no API key required.
- Formatting uses a **local** LLM server (default: `localhost:11434`).
- Works offline once the model is downloaded.

---

## 🛠 VS Code Support

The setup script automatically generates:

- `.vscode/settings.json` → sets interpreter path
- `.vscode/launch.json` → debugger config
- `project.code-workspace` → pre-configured workspace

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Mistral 7B](https://mistral.ai/)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [tiktoken](https://github.com/openai/tiktoken)

---

> Made with ❤️ by [Tamer Faour](https://github.com/TamerOnLine)