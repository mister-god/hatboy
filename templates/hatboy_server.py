from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Default path to save cookies
COOKIE_STORAGE_PATH = "cookies.json"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/save_cookies", methods=["POST"])
def save_cookies():
    try:
        # Get cookies from the request
        cookies = request.json.get("cookies")

        # Save cookies to the default path
        with open(COOKIE_STORAGE_PATH, "w") as file:
            json.dump(cookies, file, indent=4)

        return jsonify({"message": "Cookies saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Running the local Flask server
    app.run(host="0.0.0.0", port=8080, debug=True)
