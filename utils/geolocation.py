import requests

def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()

        latitude = data.get("lat", "N/A")
        longitude = data.get("lon", "N/A")
        city = data.get("city", "Unknown City")
        region = data.get("regionName", "Unknown Region")
        country = data.get("country", "Unknown Country")
        ip = data.get("query", "Unknown IP")

        return f"""
        IP Address: {ip}
        Latitude: {latitude}
        Longitude: {longitude}
        City: {city}
        Region: {region}
        Country: {country}
        """
    except Exception as e:
        return f"Error getting location: {e}"
