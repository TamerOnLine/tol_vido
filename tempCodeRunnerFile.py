# === [1] Activate virtual environment (for current process) ===
venv_site_packages = os.path.join(os.path.dirname(__file__), "venv", "Lib", "site-packages")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)
    print(f"✅ Virtual environment activated: {venv_site_packages}")