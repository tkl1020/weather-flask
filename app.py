from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "3693c91ad91148a707581e0b2a3481dd"  # your Weatherstack key

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            error = "Please enter a city name."
        else:
            url = "https://api.weatherstack.com/current"  # Weatherstack current endpoint :contentReference[oaicite:0]{index=0}
            params = {
                "access_key": API_KEY,
                "query": city,
                "units": "m"             # metric units by default, but explicit is fine :contentReference[oaicite:1]{index=1}
            }

            # ——— DEBUG INFO ———
            response = requests.get(url, params=params)
            print("→ Request URL:", response.url)
            print("→ Status code:", response.status_code)
            print("→ Body:", response.text)
            # ————————————

            if response.status_code == 200:
                data = response.json()

                # Weatherstack signals errors via a “success”:false flag
                if data.get("success", True) is False:
                    error = data["error"].get("info", "Unknown API error")
                else:
                    loc = data["location"]
                    cur = data["current"]
                    weather = {
                        "city": loc.get("name"),
                        "country": loc.get("country"),
                        "temperature": cur.get("temperature"),
                        "description": cur.get("weather_descriptions", [""])[0],
                        "humidity": cur.get("humidity"),
                        "wind": cur.get("wind_speed")
                    }
            else:
                error = f"API error: HTTP {response.status_code}"

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
