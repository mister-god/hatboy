import os
import platform
import subprocess
import time
from typing import Optional

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
    print("         Ethical Testing Tool v3.2")
    print("\033[1;93m")
    print("       Developed by Mister-God")
    print("\033[0m")

# Function to download and install Cloudflared
def install_cloudflared():
    print("[*] Installing Cloudflared...")
    if not os.path.exists(".server"):
        os.makedirs(".server")
    arch = platform.machine()
    os_type = platform.system().lower()
    cloudflared_path = ".server/cloudflared"

    # Determine the correct Cloudflared binary based on OS and architecture
    if os_type == "windows":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
        cloudflared_path += ".exe"
    elif os_type == "darwin":
        if arch == "arm64":
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64"
        else:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64"
    elif os_type == "linux":
        if arch == "x86_64":
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        elif arch in ["i686", "i386"]:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386"
        elif arch in ["aarch64", "arm64"]:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
        elif arch in ["armv7l", "armv6l", "arm"]:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm"
        else:
            print("[!] Unsupported architecture. Defaulting to amd64.")
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    else:
        print("[!] Unsupported operating system.")
        return

    # Download the binary
    try:
        subprocess.run(["curl", "-s", "-L", "-o", cloudflared_path, url], check=True)
        os.chmod(cloudflared_path, 0o755)
        print("[*] Cloudflared installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to download Cloudflared: {e}")
        exit(1)

# Function to start a Cloudflared tunnel
def start_cloudflared(port: int) -> Optional[str]:
    cloudflared_path = ".server/cloudflared"
    if platform.system().lower() == "windows":
        cloudflared_path += ".exe"

    # Verify if the Cloudflared binary exists
    if not os.path.exists(cloudflared_path):
        print("[!] Cloudflared binary is missing. Attempting to install...")
        install_cloudflared()

    try:
        print("[*] Starting Cloudflared tunnel...")
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", f"http://127.0.0.1:{port}", "--loglevel", "debug"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        log_file = ".cloudflared.log"
        with open(log_file, "w") as log:
            start_time = time.time()
            timeout = 30  # Timeout in seconds

            # Continuously check for the generated URL
            while True:
                line = process.stdout.readline()
                log.write(line)
                if "trycloudflare.com" in line:
                    url = line.split(" ")[-1].strip()
                    print(f"[+] Cloudflared Tunnel URL: {url}")
                    return url

                # Handle timeout
                if time.time() - start_time > timeout:
                    print("[!] Cloudflared failed to generate a URL within the timeout period.")
                    process.terminate()
                    with open(log_file, "r") as log_read:
                        print("[Cloudflared Logs]")
                        print(log_read.read())
                    return None
    except Exception as e:
        print(f"[!] Error starting Cloudflared: {e}")
        return None

# Function to stop Cloudflared
def stop_cloudflared():
    try:
        print("[*] Stopping Cloudflared...")
        if platform.system().lower() == "windows":
            subprocess.run(["taskkill", "/F", "/IM", "cloudflared.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-f", "cloudflared"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[!] Error stopping Cloudflared: {e}")

# Usage within the script
if __name__ == "__main__":
    display_banner()
    install_cloudflared()  # Install Cloudflared if not already installed
    start_cloudflared(8080)  # Start Cloudflared tunnel on port 8080
