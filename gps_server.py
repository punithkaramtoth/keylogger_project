from flask import Flask, request, render_template_string
import threading

# Shared variable to store GPS info
gps_data = {"latitude": None, "longitude": None, "accuracy": None}

# Create Flask app
app = Flask(__name__)

# HTML page to request location from browser
html_page = """
<!DOCTYPE html>
<html>
  <head>
    <title>GPS Tracker</title>
  </head>
  <body>
    <h2>📍 Allow location access</h2>
    <p id="status">Waiting for permission...</p>
    <script>
      navigator.geolocation.getCurrentPosition(function(position) {
          fetch('/location', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                  latitude: position.coords.latitude,
                  longitude: position.coords.longitude,
                  accuracy: position.coords.accuracy
              })
          }).then(response => {
              document.getElementById("status").innerText = "✅ Location sent!";
          }).catch(error => {
              document.getElementById("status").innerText = "❌ Failed to send location.";
          });
      }, function(error) {
          document.getElementById("status").innerText = "❌ " + error.message;
      });
    </script>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_page)

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.json
    gps_data["latitude"] = data.get("latitude")
    gps_data["longitude"] = data.get("longitude")
    gps_data["accuracy"] = data.get("accuracy")
    print(f"[📍] GPS: {gps_data}")
    return {'status': 'ok'}

def run_gps_server():
    app.run(port=5050)

def start_gps_tracking():
    thread = threading.Thread(target=run_gps_server, daemon=True)
    thread.start()

def get_gps_data():
    lat = gps_data["latitude"]
    lon = gps_data["longitude"]
    acc = gps_data["accuracy"]
    if lat is not None and lon is not None:
        return f"Latitude: {lat}, Longitude: {lon}, Accuracy: ±{acc} meters"
    else:
        return "📡 GPS data not received yet."
