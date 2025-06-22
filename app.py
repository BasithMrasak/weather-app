from flask import Flask, render_template,request,redirect, url_for
import requests
import os
API_KEY = os.environ.get("API_KEY")

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["POST", "GET"])
def weather():
    url = None  # define url early to avoid reference error

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    
    elif request.method == "GET":
        lat = request.args.get("lat")
        lon = request.args.get("lon")
        if lat and lon:
            url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}"

    # If URL was not set due to missing input
    if not url:
        return redirect(url_for("index"))

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "error" in data:
            error_message = data["error"]["message"]
            return render_template("weather.html", weather=None, error=error_message)

        weather_data = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temp": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "wind": data["current"]["wind_kph"],
            "humidity": data["current"]["humidity"],
            "localtime": data["location"]["localtime"]
        }
        return render_template("weather.html", weather=weather_data)

    except requests.exceptions.RequestException:
        return render_template("weather.html", weather=None, error="Network error. Please try again later.")
