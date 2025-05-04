from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# Path to save cookies
COOKIES_FOLDER = "cookies"
os.makedirs(COOKIES_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save_cookies", methods=["POST"])
def save_cookies():
    data = request.json
    if not data or "cookies" not in data:
        return jsonify({"error": "Invalid input: 'cookies' field is required"}), 400

    cookies = data["cookies"]
    file_path = os.path.join(COOKIES_FOLDER, "all_cookies.json")
    with open(file_path, "w") as file:
        json.dump({"cookies": cookies}, file, indent=4)

    print(f"Cookies saved to {file_path}")
    return jsonify({"message": "Cookies saved successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
