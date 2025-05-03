# Hatboy Tool

Hatboy is a lightweight and ethical tool designed for testing and debugging purposes. It allows you to collect browser cookies upon user consent through a locally hosted web interface. The collected cookies are securely stored in a JSON file for further analysis.

## Features
- **Interactive Local Website**: A user-friendly interface to request and collect browser cookies after user consent.
- **Secure Cookie Storage**: Saves browser cookies in a pre-defined JSON file for debugging and analysis purposes.
- **Live Deployment Option**: Automatically generates a live URL using Cloudflare Tunnel.

## Installation Guide

### Prerequisites
1. **Python 3.x**
   - Install Python from [python.org](https://www.python.org/).
2. **Cloudflared**
   - Install Cloudflare Tunnel by following the instructions [here](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/).

### Steps to Install and Run
1. **Clone the Repository**
   ```bash
   git clone https://github.com/mister-god/hatboy.git
   cd hatboy
   ```

2. **Install Dependencies**
   ```bash
   pip install flask
   ```

3. **Authenticate Cloudflare Tunnel**
   ```bash
   cloudflared tunnel login
   ```

4. **Create a Cloudflare Tunnel**
   ```bash
   cloudflared tunnel create hatboy
   ```

5. **Configure the Tunnel**
   - Save the `config.yml` file in the `.cloudflared` directory:
     ```bash
     mv config.yml ~/.cloudflared/config.yml
     ```

6. **Run the Tool**
   ```bash
   bash start_hatboy.sh
   ```

## Usage
1. Upon running the `start_hatboy.sh` script, the tool will:
   - Start the local Flask web server.
   - Automatically start the Cloudflare Tunnel on port `4444`.
   - Generate a live URL to access the site.

2. Open the live URL displayed on the terminal to access the tool.

## File Structure
```
hatboy/
├── hatboy_server.py       # Flask server
├── start_hatboy.sh        # Main script
├── config.yml             # Cloudflare Tunnel config
├── templates/
│   └── index.html         # HTML template
├── cookies/               # Captured cookies
└── README.md              # Documentation
```

## Disclaimer
This tool is intended only for ethical purposes, such as testing and debugging, and must be used in compliance with all applicable laws and regulations. Always ensure explicit user consent before collecting any data.

---
