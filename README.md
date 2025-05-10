# HatBoy Ethical Testing Tool

## Description
HatBoy is a tool designed for ethical penetration testing to capture user data (camera, microphone, location, etc.) in a simulated phishing environment.

## Features
- Generate victim URLs via:
  - Localhost
  - Cloudflared
  - LocalXpose
- Capture and save victim data in separate folders by IP address.
- Customizable templates for phishing pages.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mister-god/hatboy.git
   cd hatboy
   ```
2. Run the setup script:
   ```bash
   python setup.py
   ```

## Usage
1. Start the tool:
   ```bash
   python hatboy.py
   ```
2. Select the hosting option and share the victim URL.

## Disclaimer
This tool is for educational and ethical testing purposes only.
