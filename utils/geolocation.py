# utils/geolocation.py

import requests

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data.get("loc", "0,0").split(",")
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")
        return f"Latitude: {loc[0]}, Longitude: {loc[1]} (Approx. via IP) - {city}, {region}, {country}"
    except Exception as e:
        return f"Location unavailable (error: {e})"
