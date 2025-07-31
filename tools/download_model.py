import os
from pathlib import Path
from huggingface_hub import hf_hub_download

# Define the base and model directories
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# List of models to download
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

def download_model(model):
    """
    Download a model from Hugging Face if it doesn't exist locally.

    Args:
        model (dict): A dictionary with model details ('name', 'repo', 'filename').
    """
    print(f"\nChecking: {model['name']}")
    local_path = os.path.join(MODEL_DIR, model["filename"])

    if Path(local_path).exists():
        print(f"Already exists: {local_path}")
        return

    try:
        model_path = hf_hub_download(
            repo_id=model["repo"],
            filename=model["filename"],
            local_dir=MODEL_DIR,
            cache_dir=MODEL_DIR,
            force_download=False,
            resume_download=True,
        )
        print(f"Downloaded: {model_path}")

        # Verify GGUF header
        with open(model_path, "rb") as file:
            if file.read(4) != b"GGUF":
                raise ValueError("Invalid format: not a GGUF model.")
        print("GGUF header is valid.")

    except Exception as error:
        print(f"Failed to download {model['name']}: {error}")

if __name__ == "__main__":
    for model in MODELS:
        download_model(model)
