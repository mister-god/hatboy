#!/bin/bash

# Display Hatboy ASCII Art
printf "\e[1;92m        _____  \e[0m\n"
printf "\e[1;92m       /     \ \e[0m\n"
printf "\e[1;92m      | () () |\e[0m\n"
printf "\e[1;92m       \  ^  / \e[0m\n"
printf "\e[1;92m        |||||  \e[0m\n"
printf "\e[1;92m        |||||  \e[0m\n"
printf "\e[1;77m     __/_____\__ \e[0m\n"
printf "\e[1;77m    |___________| \e[0m\n"
printf "\e[1;77m     MISTER  X \e[0m\n"

install_cloudflared() {
    if [[ ! -e cloudflared ]]; then
        echo "Cloudflared binary not found. Downloading..."
        arch=$(uname -m)
        os=$(uname -s)
        case "$os" in
            "Linux")
                case "$arch" in
                    "x86_64") url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64" ;;
                    "aarch64") url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64" ;;
                    "armv7l") url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm" ;;
                    *) echo "Unsupported Linux architecture: $arch"; exit 1 ;;
                esac
                ;;
            "Darwin")
                case "$arch" in
                    "arm64") url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64" ;;
                    "x86_64") url="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64" ;;
                    *) echo "Unsupported macOS architecture: $arch"; exit 1 ;;
                esac
                ;;
            *) echo "Unsupported OS: $os"; exit 1 ;;
        esac
        wget --no-check-certificate "$url" -O cloudflared
        chmod +x cloudflared
        echo "Cloudflared installed successfully."
    fi
}

start_local_server() {
    echo "Starting local Flask server on port 8080..."
    python3 hatboy_server.py &
    SERVER_PID=$!
    sleep 3
    if ps -p $SERVER_PID > /dev/null; then
        echo "Local server started successfully."
    else
        echo "Failed to start local server. Ensure Flask is installed."
        exit 1
    fi
}

start_cloudflare_tunnel() {
    echo "Starting Cloudflare Tunnel..."
    ./cloudflared tunnel --url http://localhost:8080 --logfile .cloudflared.log > /dev/null 2>&1 &
    sleep 10
    TUNNEL_URL=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' .cloudflared.log)
    if [[ -z "$TUNNEL_URL" ]]; then
        echo "Failed to generate Cloudflare URL. Check your connection or run manually."
        exit 1
    fi
    echo -e "Your site is live at: \e[1;92m$TUNNEL_URL\e[0m"
}

echo "Welcome to Hatboy!"
echo "Please select an option:"
echo "1. Start Local Server"
echo "2. Use Cloudflare Tunnel"
read -p "Select an option (1 or 2): " option

case $option in
    1) start_local_server ;;
    2) install_cloudflared; start_local_server; start_cloudflare_tunnel ;;
    *) echo "Invalid option! Exiting..."; exit 1 ;;
esac
