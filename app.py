from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# In-memory storage for demo
DASHBOARD_DATA = {
    "history": [],  # list of dicts with timestamp, waste, battery
    "latest": {"lastWasteType": "None", "battery": "N/A", "timestamp": None}
}

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    data_entry = {
        "lastWasteType": data.get("lastWasteType", "Unknown"),
        "battery": data.get("battery", "N/A"),
        "timestamp": data.get("timestamp", time.time())
    }

    DASHBOARD_DATA["latest"] = data_entry
    DASHBOARD_DATA["history"].append(data_entry)
    if len(DASHBOARD_DATA["history"]) > 100:  # keep last 100 entries
        DASHBOARD_DATA["history"].pop(0)

    return jsonify({"status": "data received"})

@app.route("/status")
def status():
    return jsonify(DASHBOARD_DATA)

if __name__ == "__main__":
    app.run(debug=True)
