import os
import platform
import shutil  # Importing shutil to fix the NameError
import subprocess
import sys
import time

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

def install_python_dependencies():
    print("[*] Installing Python dependencies from requirements.txt...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("[*] Python dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to install Python dependencies: {e}")
        exit(1)

def check_and_install_tool(tool_name):
    print(f"[*] Checking for {tool_name}...")
    if not shutil.which(tool_name):
        print(f"[!] {tool_name} is not installed. Please install it manually and try again.")
        exit(1)
    else:
        print(f"[*] {tool_name} is already installed.")

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

    # Download the binary with retry mechanism
    retries = 3
    for attempt in range(1, retries + 1):
        try:
            print(f"[*] Attempt {attempt}/{retries}: Downloading Cloudflared...")
            subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-o", cloudflared_path, url], check=True)
            os.chmod(cloudflared_path, 0o755)
            print("[*] Cloudflared installed successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"[!] Attempt {attempt} failed: {e}")
            if attempt < retries:
                print("[*] Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("[!] Cloudflared installation failed after multiple attempts. Check your network connection or try manually.")
                exit(1)

def setup_tool():
    # Display the banner
    display_banner()

    # Step 1: Install Python dependencies
    install_python_dependencies()

    # Step 2: Check and install PHP
    check_and_install_tool("php")

    # Step 3: Check and install curl
    check_and_install_tool("curl")

    # Step 4: Install Cloudflared
    install_cloudflared()

    print("[*] All dependencies installed and managed successfully. You can now run 'python hatboy.py' to start the tool.")

if __name__ == "__main__":
    setup_tool()
