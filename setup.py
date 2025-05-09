import os
import subprocess

def start_tool():
    print("HatBoy Setup")
    print("[01] Localhost")
    print("[02] Cloudflared")
    print("[03] LocalXpose")
    choice = input("Select an option to host the tool: ")

    if choice == "1":
        print("Starting on localhost...")
        os.system("python3 -m http.server 8080")
    elif choice == "2":
        print("Starting with Cloudflared...")
        os.system("cloudflared tunnel --url http://localhost:8080")
    elif choice == "3":
        print("Starting with LocalXpose...")
        os.system("lx start http 8080")
    else:
        print("Invalid option. Please try again.")
        start_tool()

if __name__ == "__main__":
    print("Welcome to HatBoy Ethical Testing Tool")
    start_tool()
