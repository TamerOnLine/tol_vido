import os
import subprocess
from dotenv import load_dotenv

MODELS = {
    "1": ".env.mistral",
    "2": ".env.leolm-german"

}

def run_llm_server(env_file):
    print(f"\n📦 Loading config from: {env_file}")
    load_dotenv(env_file)

    model = os.getenv("MODEL")
    n_ctx = os.getenv("N_CTX", "4096")
    host = "127.0.0.1"
    port = "11434"

    if not model or not os.path.exists(model):
        print(f"❌ MODEL not found or missing in {env_file}")
        return

    venv_python = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe")

    print(f"🚀 Launching LLM server for: {model}")
    subprocess.run([
        venv_python, "-m", "llama_cpp.server",
        "--model", model,
        "--n_ctx", n_ctx,
        "--host", host,
        "--port", port
    ])

if __name__ == "__main__":
    print("💬 اختر النموذج:")
    print("[1] Mistral")
    print("[2] LeoLM-German")
    choice = input("👉 اختيارك: ").strip()

    if choice in MODELS:
        run_llm_server(MODELS[choice])
    else:
        print("❌ خيار غير صالح.")
