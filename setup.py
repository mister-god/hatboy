import os
import json
import shutil

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from the config file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_config(config):
    """Save configuration to the config file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def check_dependencies():
    """Check if required dependencies are installed."""
    # Check if Cloudflared is installed
    if not shutil.which("cloudflared"):
        print("Cloudflared is not installed. Please install it using 'pip install cloudflared'.")
        exit(1)

    # Check if LocalXpose is installed
    if not shutil.which("lx"):
        print("LocalXpose is not installed. Please install it manually from https://localxpose.io/")
        exit(1)

def setup_localxpose():
    """Setup LocalXpose by asking for a token if not already configured."""
    config = load_config()
    if "localxpose_token" not in config:
        print("It looks like this is your first time using LocalXpose.")
        token = input("Please enter your LocalXpose token: ").strip()
        config["localxpose_token"] = token
        save_config(config)
    return config["localxpose_token"]

def start_localxpose():
    """Start LocalXpose with the configured token."""
    token = setup_localxpose()
    os.system(f"lx start http 8080 --token {token}")

def start_tool():
    print("HatBoy Setup")
    print("[01] Localhost")
    print("[02] Cloudflared")
    print("[03] LocalXpose")
    choice = input("Select an option to host the tool: ")

    if choice == "1":
        print("Starting on localhost...")
        os.system("python3 -m http.server 8080")
    elif choice == "2":
        print("Starting with Cloudflared...")
        os.system("cloudflared tunnel --url http://localhost:8080")
    elif choice == "3":
        print("Starting with LocalXpose...")
        check_dependencies()
        start_localxpose()
    else:
        print("Invalid option. Please try again.")
        start_tool()

if __name__ == "__main__":
    print("Welcome to HatBoy Ethical Testing Tool")
    check_dependencies()
    start_tool()
