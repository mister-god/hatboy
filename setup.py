import os
import platform
import shutil  # Importing shutil to fix the NameError
import subprocess
import sys

def install_dependencies():
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

def setup_cloudflared():
    print("[*] Setting up Cloudflared...")
    # Logic for downloading and setting up Cloudflared

def setup_localxpose():
    print("[*] Setting up LocalXpose...")
    # Logic for downloading and setting up LocalXpose

if __name__ == "__main__":
    install_dependencies()
    check_and_install_tool("php")
    check_and_install_tool("curl")
    setup_cloudflared()
    setup_localxpose()
    print("[*] Setup complete.")
