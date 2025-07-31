import os
from pathlib import Path
from huggingface_hub import hf_hub_download

# ✅ إعداد مجلد النماذج
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# ✅ قائمة النماذج المراد تحميلها
MODELS = [
    {
        "name": "mistral-7b-instruct",
        "repo": "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
        "filename": "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    },

    {
    "name": "leolm-german",
    "repo": "TheBloke/leo-hessianai-7B-GGUF",
    "filename": "leo-hessianai-7b.Q4_K_M.gguf"
    }




]

# ✅ تحميل النماذج
for model in MODELS:
    print(f"\n🔽 Checking: {model['name']}")
    local_path = os.path.join(MODEL_DIR, model["filename"])

    if Path(local_path).exists():
        print(f"🔁 Already exists: {local_path}")
    else:
        try:
            model_path = hf_hub_download(
                repo_id=model["repo"],
                filename=model["filename"],
                local_dir=MODEL_DIR,
                cache_dir=MODEL_DIR,
                force_download=False,
                resume_download=True,
            )
            print(f"✅ Downloaded: {model_path}")

            # ✅ التحقق من رأس GGUF
            with open(model_path, "rb") as f:
                if f.read(4) != b"GGUF":
                    raise ValueError("❌ Invalid format: not a GGUF model.")
            print("🧠 GGUF header is valid.")

        except Exception as e:
            print(f"❌ Failed to download {model['name']}: {e}")
