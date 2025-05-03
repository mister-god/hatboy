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

# Start the Flask web server
echo "Starting the local web server..."
python3 hatboy_server.py &

# Start Cloudflare Tunnel
echo "Starting Cloudflare Tunnel..."
cloudflared tunnel run hatboy
