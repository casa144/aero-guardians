import pandas as pd
import os
from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return "Server is running"


def fetch_live_data():
    """Fetch live air quality data for Mumbai from Open-Meteo API."""
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": 19.0760,          # Mumbai coordinates
        "longitude": 72.8777,
        "hourly": "pm2_5,pm10",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Take the latest available hour (last element in list)
    i = -1

    entry = {
        "timestamp": data["hourly"]["time"][i],
        "pm2_5": data["hourly"]["pm2_5"][i],
        "pm10": data["hourly"]["pm10"][i],
    }
    return entry


def classify_risk(entry):
    def log_to_csv(entry):
     df = pd.DataFrame([entry])
     file_path = os.path.join("data", "realtime_log.csv")
     header = not os.path.exists(file_path)  # write header only first time
     df.to_csv(file_path, mode="a", header=header, index=False)

    pm2_5 = entry["pm2_5"]

    if pm2_5 <= 30:
        risk = "Low"
        alert = "✅ Air quality is good."
    elif pm2_5 <= 60:
        risk = "Moderate"
        alert = "🟡 Mild pollution. Sensitive groups should be cautious."
    elif pm2_5 <= 90:
        risk = "High"
        alert = "🟠 Unhealthy for sensitive groups."
    else:
        risk = "Very High"
        alert = "⚠️ Unhealthy. Avoid prolonged exposure."

    return risk, alert

def log_to_csv(entry):
    """Save each reading into a CSV file."""
    df = pd.DataFrame([entry])
    file_path = os.path.join("data", "realtime_log.csv")

    # Write header only the first time
    header = not os.path.exists(file_path)

    df.to_csv(file_path, mode="a", header=header, index=False)



@app.route("/data")
def get_data():
    # 1) Get live readings
    entry = fetch_live_data()

    # 2) Add risk + alert
    risk, alert = classify_risk(entry)
    entry["risk"] = risk
    entry["alert"] = alert

    # 3) Log this entry to CSV
    log_to_csv(entry)

    # 4) Return JSON
    return jsonify(entry)



if __name__ == "__main__":
    app.run(debug=True)
