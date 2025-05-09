import os
import json
import subprocess
import platform

CONFIG_FILE = "config.json"

# Load or initialize the configuration file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return {"localxpose_token": "", "port": "8080"}

# Save configuration to file
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

# Check and install dependencies
def check_dependencies():
    print("[*] Checking dependencies...")
    required_tools = ["php", "curl"]
    for tool in required_tools:
        if not shutil.which(tool):
            print(f"[!] Missing dependency: {tool}. Please install it and try again.")
            exit(1)
    print("[*] All dependencies are installed.")

# Install Cloudflared
def install_cloudflared():
    print("[*] Installing Cloudflared...")
    arch = platform.machine()
    if arch == "x86_64":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    elif "arm" in arch:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
    else:
        print("[!] Unsupported architecture.")
        return
    subprocess.run(["curl", "-s", "-L", "-o", ".server/cloudflared", url], check=True)
    os.chmod(".server/cloudflared", 0o755)
    print("[*] Cloudflared installed successfully.")

# Install LocalXpose
def install_localxpose():
    print("[*] Installing LocalXpose...")
    arch = platform.machine()
    if arch == "x86_64":
        url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-amd64.zip"
    elif "arm" in arch:
        url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-arm.zip"
    else:
        print("[!] Unsupported architecture.")
        return
    subprocess.run(["curl", "-s", "-L", "-o", "loclx.zip", url], check=True)
    subprocess.run(["unzip", "-qq", "loclx.zip", "-d", ".server"], check=True)
    os.chmod(".server/loclx", 0o755)
    os.remove("loclx.zip")
    print("[*] LocalXpose installed successfully.")

# Start a PHP server
def start_php_server(port):
    print(f"[*] Starting PHP server on port {port}...")
    os.chdir(".server/www")
    subprocess.Popen(["php", "-S", f"127.0.0.1:{port}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir("../..")

# Start Cloudflared
def start_cloudflared(port):
    print("[*] Starting Cloudflared...")
    subprocess.Popen([".server/cloudflared", "tunnel", "--url", f"http://127.0.0.1:{port}"], stdout=subprocess.PIPE)

# Start LocalXpose
def start_localxpose(port):
    config = load_config()
    token = config.get("localxpose_token")
    if not token:
        token = input("[*] Enter your LocalXpose token: ").strip()
        config["localxpose_token"] = token
        save_config(config)
    print("[*] Starting LocalXpose...")
    subprocess.Popen([".server/loclx", "tunnel", "--raw-mode", "http", "--port", port, "--token", token], stdout=subprocess.PIPE)

# Main menu
def main_menu():
    config = load_config()
    port = config.get("port", "8080")
    print("[*] Select an option:")
    print("[1] Localhost")
    print("[2] Cloudflared")
    print("[3] LocalXpose")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        start_php_server(port)
        print(f"[*] Server running at http://127.0.0.1:{port}")
    elif choice == "2":
        start_php_server(port)
        start_cloudflared(port)
    elif choice == "3":
        start_php_server(port)
        start_localxpose(port)
    else:
        print("[!] Invalid choice. Exiting.")

if __name__ == "__main__":
    if not os.path.exists(".server/www"):
        os.makedirs(".server/www")
    check_dependencies()
    main_menu()
