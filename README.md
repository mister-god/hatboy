# HatBoy Ethical Testing Tool

## Description
HatBoy is a tool designed for ethical penetration testing and browser vulnerability assessment. It allows you to create phishing templates and capture victim data, including camera, microphone, and location information.

## Features
- Launch phishing templates via Localhost or Cloudflared.
- Automatically save victim data in separate folders named after their IP addresses.
- Capture and log data securely for ethical testing purposes.
- Editable templates for customization.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mister-god/hatboy.git
   cd hatboy
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the tool:
   ```bash
   python hatboy.py
   ```
2. Select a hosting option and launch the phishing template.

## Templates
- Templates are stored in the `templates` folder.
- Edit them to customize the phishing pages.

## Troubleshooting
- Ensure PHP and curl are installed on your system.
- Update your Cloudflared binaries if errors occur.

## Disclaimer
This tool is for educational and ethical use only. Unauthorized use is strictly prohibited.
