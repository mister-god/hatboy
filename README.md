# HatBoy Ethical Testing Tool

## Prerequisites
- Install Cloudflared using `pip install cloudflared`.
- Download and install LocalXpose from [https://localxpose.io/](https://localxpose.io/).

## Description
HatBoy is a tool designed for ethical penetration testing and browser vulnerability assessment. It should only be used in authorized environments to demonstrate how attackers might exploit vulnerabilities and how developers can protect against them.

## Setup
1. Clone the repository: `git clone https://github.com/your-repo/hatboy.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Install LocalXpose manually from [https://localxpose.io/](https://localxpose.io/).
4. Run the setup file: `python setup.py`
5. Choose a hosting option:
    - Localhost
    - Cloudflared
    - LocalXpose (requires a token).

### LocalXpose Token
- The first time you select the LocalXpose option, you will be prompted to enter your LocalXpose token.
- The token will be saved in the `config.json` file for future use.
- If you need to update the token, simply delete the `config.json` file and restart the tool.

## Usage
### Generated Links
- **Victim URL**: Simulates the client-side behavior.
- **Attacker URL**: Provides a dashboard for viewing collected data (authorized use only).

### Ethical Guidelines
- Obtain proper authorization before using this tool.
- Use it strictly for educational and ethical purposes.
- Do not use it for malicious or illegal activities.

## Disclaimer
The creators of this tool are not responsible for any misuse. Use it responsibly and ethically.
