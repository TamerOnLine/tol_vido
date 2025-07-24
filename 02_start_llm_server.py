import subprocess
import os
import sys

# === [1] Activate virtual environment (for current process) ===
venv_site_packages = os.path.join(os.path.dirname(__file__), "venv", "Lib", "site-packages")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)
    print(f"✅ Virtual environment activated: {venv_site_packages}")

# === [2] Check for model file ===
model_path = os.path.join("models", "mistral-7b-instruct-v0.1.Q4_K_M.gguf")
if not os.path.exists(model_path):
    print("❌ Model not found.")
    sys.exit(1)

# === [3] Launch LLM server using venv's Python ===
print("🚀 Launching llama_cpp.server...")

venv_python = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "python.exe")

subprocess.run([
    venv_python, "-m", "llama_cpp.server",
    "--model", model_path,
    "--n_ctx", "4096",
    "--host", "127.0.0.1",
    "--port", "11434"
])
