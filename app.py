import os
from dotenv import load_dotenv
import requests
from flask import Flask, render_template, request

# ── Load local .env (only in development) ──────────────────────────
load_dotenv()  # reads .env and populates os.environ
# ────────────────────────────────────────────────────────────────────

app = Flask(__name__)

# Grab the Weatherstack key from the environment
API_KEY = os.getenv("WEATHERSTACK_ACCESS_KEY")
if not API_KEY:
    raise RuntimeError("Missing WEATHERSTACK_ACCESS_KEY in environment")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            error = "Please enter a city name."
        else:
            url = "https://api.weatherstack.com/current"
            params = {
                "access_key": API_KEY,
                "query": city,
                "units": "m"
            }

            # (Optional) debug
            response = requests.get(url, params=params)
            print("→ URL:", response.url)
            print("→ Status:", response.status_code)
            print("→ Body:", response.text)

            if response.status_code == 200:
                data = response.json()
                if data.get("success", True) is False:
                    error = data["error"].get("info", "Unknown API error")
                else:
                    loc = data["location"]
                    cur = data["current"]
                    weather = {
                        "city":        loc.get("name"),
                        "country":     loc.get("country"),
                        "temperature": cur.get("temperature"),
                        "description": cur.get("weather_descriptions", [""])[0],
                        "humidity":    cur.get("humidity"),
                        "wind":        cur.get("wind_speed")
                    }
            else:
                error = f"API error: HTTP {response.status_code}"

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
