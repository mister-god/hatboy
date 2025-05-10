import os
import platform
import subprocess

def install_dependencies():
    print("[*] Installing Python dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    print("[*] Python dependencies installed successfully.")

def check_and_install_tool(tool_name):
    if not shutil.which(tool_name):
        print(f"[!] {tool_name} is not installed. Please install it manually.")

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
