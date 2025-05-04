# Hatboy Tool

Hatboy is a lightweight and ethical tool designed for testing and debugging purposes. It allows you to collect browser cookies upon user consent through a locally hosted web interface. Additionally, Hatboy offers a live deployment option via Cloudflare Tunnel for remote accessibility.

## Features
- **Interactive Local Website**: A user-friendly interface to request and collect browser cookies after user consent.
- **Secure Cookie Storage**: Saves browser cookies in a pre-defined JSON file for debugging and analysis purposes.
- **Live Deployment Option**: Automatically generates a live URL using Cloudflare Tunnel without requiring login or complex configuration.
- **Cross-Platform Compatibility**: Automatically detects and configures `cloudflared` for various operating systems and architectures.

## Installation Guide

### Prerequisites
1. **Python 3.x**
   - Install Python from [python.org](https://www.python.org/).
2. **Cloudflared (No Manual Installation Required)**
   - The script automatically downloads and configures Cloudflare Tunnel.

### Steps to Install and Run
1. **Clone the Repository**
   ```bash
   git clone https://github.com/mister-god/hatboy.git
   cd hatboy
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Tool**
   ```bash
   bash start_hatboy.sh
   ```

## Usage
1. Upon running the `start_hatboy.sh` script, the tool will:
   - Start the local Flask web server on port `8080`.
   - Automatically start the Cloudflare Tunnel.
   - Generate a live URL to access the site.

2. Open the live URL displayed on the terminal to interact with the tool.

### Menu Options
- **Option 1: Start Local Server**
  - Launches the web tool locally.
- **Option 2: Use Cloudflare Tunnel**
  - Exposes the local web tool to the internet with a secure URL using Cloudflare.

## File Structure
```
hatboy/
├── hatboy_server.py       # Flask server
├── start_hatboy.sh        # Main script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # HTML template
├── cookies/               # Captured cookies
└── README.md              # Documentation
```

## Disclaimer
This tool is intended only for ethical purposes, such as testing and debugging, and must be used in compliance with all applicable laws and regulations. Always ensure explicit user consent before collecting or storing any data through this tool.

---
