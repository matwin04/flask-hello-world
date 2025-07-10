from flask import Flask, render_template
import requests
import json
app = Flask(__name__)

API_KEY = "WOo9vL8ECMWN76EcKjsNGfo8YgNZ7c2u"
HEADERS = {
    "apikey": API_KEY,
}

FEEDS = {
    "LA Metro Rail RT": "f-metro~losangeles~rail~rt",
    "Amtrak California": "f-9-amtrak~amtrakcalifornia~amtrakcharteredvehicle",
    "North County Transit District": "f-9mu-northcountytransitdistrict",
    "Metrolink Trains": "f-9qh-metrolinktrains",
}

@app.route("/")
def index():
    feeds_data = []

    for name, feed_id in FEEDS.items():
        try:
            res = requests.get(f"https://transit.land/api/v2/rest/feeds/{feed_id}", headers=HEADERS)
            feeds_data.append({
                "name": name,
                "status": res.status_code,
                "feed": res.json().get("feed", {})
            })
        except Exception as e:
            feeds_data.append({"name": name, "status": "error", "feed": {"error": str(e)}})

    return render_template("index.html", feeds=feeds_data)

@app.route("/departures/<station_id>")
def departures(station_id):
    stop_name = "Unknown Stop"
    departures = []

    try:
        res = requests.get(
            f"https://transit.land/api/v2/rest/stops/{station_id}/departures",
            headers=HEADERS
        )
        data = res.json()
        stops = data.get("stops", [])
        if stops:
            stop = stops[0]
            stop_name = stop.get("stop_name", stop.get("stop_id", station_id))
            departures = stop.get("departures", [])
    except Exception as e:
        departures = [{"trip": {}, "scheduled_departure_time": None, "error": str(e)}]

    return render_template("departures.html", departures=departures, station_id=station_id, stop_name=stop_name)

if __name__ == "__main__":
    app.run(debug=True)
