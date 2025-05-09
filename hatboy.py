import os
import json
import subprocess
import platform
import shutil

CONFIG_FILE = "config.json"

# ASCII Art Banner
def display_banner():
    print("\033[1;93m      _______        \033[0m")
    print("\033[1;93m     /       \\\\      \033[0m")
    print("\033[1;93m    /  _____  \\\\     \033[0m")
    print("\033[1;92m   |  |     |  |     \033[0m")
    print("\033[1;92m   |  | o o |  |     \033[0m")
    print("\033[1;92m   |  |  ^  |  |     \033[0m")
    print("\033[1;92m   |  | '-' |  |     \033[0m")
    print("\033[1;97m    \\  \\___/  /      \033[0m")
    print("\033[1;97m     \\_______/       \033[0m")
    print("\033[1;96m     / ||||| \\       \033[0m")
    print("\033[1;96m    /  |||||  \\      \033[0m")
    print("\033[1;96m   |___|||||___|     \033[0m")
    print("\033[1;94m    [ MISTER X ]      \033[0m\n")

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
    subprocess.run(["curl", "-s", "-L", "-o", cloudflared_path, url], check=True)
    os.chmod(cloudflared_path, 0o755)

    if not os.path.exists(cloudflared_path):
        print("[!] Cloudflared installation failed. Please check your connection or try again.")
        exit(1)

    print("[*] Cloudflared installed successfully.")

# Install LocalXpose
def install_localxpose():
    print("[*] Installing LocalXpose...")
    if not os.path.exists(".server"):
        os.makedirs(".server")

    arch = platform.machine()
    if arch == "x86_64":
        url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-amd64.zip"
    elif "arm" in arch:
        url = "https://api.localxpose.io/api/v2/downloads/loclx-linux-arm.zip"
    else:
        print("[!] Unsupported architecture.")
        return

    loclx_zip_path = "loclx.zip"
    subprocess.run(["curl", "-s", "-L", "-o", loclx_zip_path, url], check=True)
    subprocess.run(["unzip", "-qq", loclx_zip_path, "-d", ".server"], check=True)
    os.chmod(".server/loclx", 0o755)
    os.remove(loclx_zip_path)

    if not os.path.exists(".server/loclx"):
        print("[!] LocalXpose installation failed. Please check your connection or try again.")
        exit(1)

    print("[*] LocalXpose installed successfully.")

# Start a PHP server
def start_php_server(port):
    print(f"[*] Starting PHP server on port {port}...")
    os.chdir(".server/www")
    subprocess.Popen(["php", "-S", f"127.0.0.1:{port}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir("../..")

# Start Cloudflared and parse the tunnel URL
def start_cloudflared(port):
    cloudflared_path = ".server/cloudflared"
    if not os.path.exists(cloudflared_path):
        print("[!] Cloudflared binary is missing. Attempting to reinstall...")
        install_cloudflared()

    print("[*] Starting Cloudflared...")
    try:
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        tunnel_url = None
        for line in process.stdout:
            if "trycloudflare.com" in line:
                tunnel_url = line.split(" ")[-1].strip()
                break

        if tunnel_url:
            print(f"[+] Tunnel created successfully: {tunnel_url}")
        else:
            print("[!] Failed to create a tunnel. Check Cloudflared logs for more details.")

    except Exception as e:
        print(f"[!] An error occurred while starting Cloudflared: {e}")

# Start LocalXpose
def start_localxpose(port):
    loclx_path = ".server/loclx"
    if not os.path.exists(loclx_path):
        print("[!] LocalXpose binary is missing. Attempting to reinstall...")
        install_localxpose()

    config = load_config()
    token = config.get("localxpose_token")
    if not token:
        token = input("[*] Enter your LocalXpose token: ").strip()
        config["localxpose_token"] = token
        save_config(config)

    print("[*] Starting LocalXpose...")
    subprocess.Popen([loclx_path, "tunnel", "--raw-mode", "http", "--port", port, "--token", token], stdout=subprocess.PIPE)

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
    display_banner()  # Call the banner function
    if not os.path.exists(".server/www"):
        os.makedirs(".server/www")
    check_dependencies()
    main_menu()
