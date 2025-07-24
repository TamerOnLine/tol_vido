import os
import sys
import subprocess
import json
from typing import Optional, Dict, Any

IS_WINDOWS: bool = os.name == "nt"

def get_python_path(venv_dir: str) -> str:
    return os.path.join(venv_dir, "Scripts", "python.exe") if IS_WINDOWS else os.path.join(venv_dir, "bin", "python")

def get_pip_path(venv_dir: str) -> str:
    return os.path.join(venv_dir, "Scripts", "pip.exe") if IS_WINDOWS else os.path.join(venv_dir, "bin", "pip")

def get_site_packages_path(venv_dir: str) -> str:
    if IS_WINDOWS:
        return os.path.join(venv_dir, "Lib", "site-packages")
    versions = os.listdir(os.path.join(venv_dir, "lib"))
    return os.path.join(venv_dir, "lib", versions[0], "site-packages")

def load_or_create_config() -> Dict[str, Any]:
    print("\n[1] Setting up setup-config.json")
    config_path: str = os.path.join(os.getcwd(), "setup-config.json")

    if not os.path.exists(config_path):
        print("Creating config file...")
        default_config: Dict[str, Any] = {
            "project_name": os.path.basename(os.getcwd()),
            "main_file": "app.py",
            "entry_point": "main.py",
            "requirements_file": "requirements.txt",
            "venv_dir": "venv",
            "python_version": "3.12"
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)
        print("setup-config.json created.")
    else:
        print("Config file already exists.")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_virtualenv(venv_dir: str, python_version: Optional[str] = None) -> None:
    print("\n[2] Checking virtual environment")
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment at: {venv_dir}")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")

def create_requirements_file(path: str) -> None:
    print("\n[3] Checking requirements.txt")
    if not os.path.exists(path):
        print("Creating empty requirements.txt...")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Add your dependencies here\n")
        print("requirements.txt created.")
    else:
        print("requirements.txt already exists.")

def install_requirements(venv_dir: str, requirements_path: str) -> None:
    print("\n[4] Installing requirements")
    pip_path: str = get_pip_path(venv_dir)
    subprocess.run([pip_path, "install", "-r", requirements_path], check=True)
    print("Packages installed.")

def upgrade_pip(venv_dir: str) -> None:
    print("\n[5] Upgrading pip")
    python_path: str = get_python_path(venv_dir)
    subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    print("pip upgraded.")

def create_env_info(venv_dir: str) -> None:
    print("\n[6] Creating env-info.txt")
    info_path: str = "env-info.txt"
    python_path: str = get_python_path(venv_dir)
    with open(info_path, "w", encoding="utf-8") as f:
        subprocess.run([python_path, "--version"], stdout=f)
        f.write("\nInstalled packages:\n")
        subprocess.run([python_path, "-m", "pip", "freeze"], stdout=f)
    print(f"Environment info saved to {info_path}")

def create_main_file(main_file_path: str, venv_dir: str) -> None:
    print("\n[7] Checking main.py")
    if not os.path.exists(main_file_path):
        print(f"Creating {main_file_path}...")
        venv_site: str = get_site_packages_path(venv_dir)
        main_code: str = f'''
import os
import sys
import json

# Activate the virtual environment (embedded)
venv_site_packages = os.path.join(os.path.dirname(__file__), r"{venv_site}")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

print("Virtual environment activated within script.")
print("sys.path includes:", venv_site_packages)

# Load configuration from config file for flexibility
CONFIG_FILE = "setup-config.json"

def load_entry_point():
    if not os.path.exists(CONFIG_FILE):
        print(f"{{CONFIG_FILE}} not found.")
        sys.exit(1)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    main_file = config.get("main_file", "app.py")
    if not os.path.exists(main_file):
        print(f"{{main_file}} does not exist.")
        sys.exit(1)

    print(f"Running: {{main_file}}")
    with open(main_file, encoding="utf-8") as f:
        exec(f.read(), globals())

if __name__ == "__main__":
    load_entry_point()
'''
        with open(main_file_path, "w", encoding="utf-8") as f:
            f.write(main_code.strip())
        print(f"{main_file_path} created.")
    else:
        print("main.py already exists.")

def create_app_file(app_file_path: str) -> None:
    print("\n[7.1] Checking app.py")
    if not os.path.exists(app_file_path):
        print(f"Creating {app_file_path} with welcome message...")
        welcome_code: str = '''\
print("Welcome! This is your app.py file.")
print("You can now start writing your application code here.")
'''
        with open(app_file_path, "w", encoding="utf-8") as f:
            f.write(welcome_code)
        print(f"{app_file_path} created.")
    else:
        print(f"{app_file_path} already exists.")

def create_vscode_files(venv_dir: str) -> None:
    print("\n[8] Creating VS Code files: settings, launch, workspace")
    vscode_dir: str = os.path.join(os.getcwd(), ".vscode")
    settings_path: str = os.path.join(vscode_dir, "settings.json")
    launch_path: str = os.path.join(vscode_dir, "launch.json")
    workspace_path: str = os.path.join(os.getcwd(), "project.code-workspace")

    os.makedirs(vscode_dir, exist_ok=True)
    interpreter_path: str = get_python_path(venv_dir)

    settings: dict[str, str | bool] = {
        "python.defaultInterpreterPath": interpreter_path,
        "python.terminal.activateEnvironment": True,
        "editor.formatOnSave": True,
        "python.formatting.provider": "black"
    }
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

    launch: dict[str, object] = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run main.py",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/main.py",
                "console": "integratedTerminal",
                "justMyCode": True
            }
        ]
    }
    with open(launch_path, "w", encoding="utf-8") as f:
        json.dump(launch, f, indent=2)

    workspace: dict[str, object] = {
        "folders": [{"path": "."}],
        "settings": {
            "python.defaultInterpreterPath": interpreter_path
        }
    }
    with open(workspace_path, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2)

    print("VS Code files created successfully: settings.json, launch.json, project.code-workspace")

if __name__ == "__main__":
    print("\nStarting project setup...\n" + "-" * 40)
    config: Dict[str, Any] = load_or_create_config()

    venv_dir: str = str(config["venv_dir"])
    requirements_path: str = str(config["requirements_file"])
    main_file: str = str(config["main_file"])
    python_version: str = str(config["python_version"])

    create_virtualenv(venv_dir, python_version)
    create_requirements_file(requirements_path)
    install_requirements(venv_dir, requirements_path)
    upgrade_pip(venv_dir)
    create_env_info(venv_dir)

    entry_point: str = str(config.get("entry_point", "main.py"))
    create_main_file(entry_point, venv_dir)

    create_app_file(main_file)
    create_vscode_files(venv_dir)

    print("\nProject setup complete.")
