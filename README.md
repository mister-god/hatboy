# Hatboy Tool

Hatboy is a lightweight and ethical tool designed for testing and debugging purposes. It allows you to collect browser cookies upon user consent through a locally hosted web interface. The collected cookies are securely stored in a JSON file for further analysis.

## Features
- **Interactive Local Website**: A user-friendly interface to request and collect browser cookies after user consent.
- **Secure Cookie Storage**: Saves browser cookies in a pre-defined JSON file for debugging and analysis purposes.
- **Live Deployment Option**: Easily make the local website live using Cloudflare Tunnel.

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
   - Create a `config.yml` file:
     ```yaml
     tunnel: hatboy
     credentials-file: /path/to/.cloudflared/hatboy.json

     ingress:
       - hostname: hatboy.example.com
         service: http://localhost:8080
       - service: http_status:404
     ```

6. **Start the Tool**
   ```bash
   bash start_hatboy.sh
   ```

## Usage
1. Open your browser and navigate to `http://localhost:8080`.
2. Allow cookies by clicking the "Allow Cookies" button on the page.
3. The cookies will be saved to a file named `cookies.json` in the root directory.
4. If you configured Cloudflare Tunnel, access the live site using the hostname you configured in the `config.yml`.

## File Structure
```
hatboy/
├── hatboy_server.py       # Flask server script
├── start_hatboy.sh        # Bash script to start the tool
├── templates/
│   └── index.html         # HTML template for the local site
├── cookies.json           # File where cookies are saved
└── README.md              # Documentation
```

## Disclaimer
This tool is intended only for ethical purposes, such as testing and debugging, and must be used in compliance with all applicable laws and regulations. Always ensure explicit user consent before collecting any data.

---
