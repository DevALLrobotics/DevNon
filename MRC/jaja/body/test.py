from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MISTY_IP = "192.168.3.34"  # Replace with the actual IP address of Misty II

@app.route("/api/led", methods=["POST"])
def change_led():
    try:
        data = request.json
        red = data.get("red")
        green = data.get("green")
        blue = data.get("blue")

        # Validate color values
        if not all(isinstance(i, int) and 0 <= i <= 255 for i in [red, green, blue]):
            return jsonify({"error": "Invalid color values. Must be integers between 0 and 255."}), 400

        # Send request to Misty II
        url = f"http://{MISTY_IP}/api/led"
        headers = {"Content-Type": "application/json"}
        payload = {"red": red, "green": green, "blue": blue}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return jsonify({"status": "LED updated successfully", "response": response.json()}), 200
        else:
            return jsonify({"error": "Failed to update LED", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
