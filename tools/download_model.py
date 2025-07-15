import os
import sys

# ✅ Activate virtual environment
venv_path = os.path.join(os.path.dirname(__file__), "..", "venv", "Lib", "site-packages")
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)
print("🧠 Virtual environment activated.")

# ✅ Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# ✅ Import required packages
from huggingface_hub import hf_hub_download

# ✅ Read model name from .env
MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    raise ValueError("❌ MODEL_NAME is not defined in the .env file.")

REPO_ID = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# ✅ Download model if not already present
try:
    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=MODEL_NAME,
        local_dir=MODEL_DIR,
        cache_dir=MODEL_DIR,
        force_download=False,
        resume_download=True,
    )
    print(f"✅ Model downloaded to: {model_path}")
except Exception as e:
    print("❌ Download failed:", e)
    sys.exit(1)

# ✅ Verify GGUF file header
with open(model_path, "rb") as f:
    if f.read(4) != b"GGUF":
        raise ValueError("❌ Invalid file format: not a GGUF model.")
print("✅ GGUF header is valid.")
