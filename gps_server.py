import streamlit as st

# Initialize GPS storage in session state
if "gps_data" not in st.session_state:
    st.session_state.gps_data = {"latitude": None, "longitude": None, "accuracy": None}

def start_gps_tracking():
    """
    Requests GPS coordinates from the user's browser and stores them in session state.
    Works entirely inside Streamlit (no Flask).
    """
    st.markdown("""
    <h2>📍 Allow location access</h2>
    <p id="status">Waiting for permission...</p>
    <script>
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const data = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                accuracy: position.coords.accuracy
            };
            // Send data to Streamlit via custom event
            const event = new CustomEvent("streamlitGPS", {detail: data});
            window.dispatchEvent(event);
            document.getElementById("status").innerText = "✅ Location captured!";
        },
        function(error) {
            document.getElementById("status").innerText = "❌ " + error.message;
        }
    );
    </script>
    """, unsafe_allow_html=True)

def get_gps_data():
    """
    Returns the latest GPS coordinates stored in session state.
    """
    data = st.session_state.get("gps_data", {"latitude": None, "longitude": None, "accuracy": None})
    lat = data["latitude"]
    lon = data["longitude"]
    acc = data["accuracy"]
    if lat is not None and lon is not None:
        return f"Latitude: {lat}, Longitude: {lon}, Accuracy: ±{acc} meters"
    else:
        return "📡 GPS data not received yet."

# Event listener to update GPS coordinates
# Streamlit runs this in every rerun
st.experimental_rerun_trigger = st.session_state.get("gps_listener_added", False)
if not st.experimental_rerun_trigger:
    st.session_state.gps_listener_added = True
    st.components.v1.html("""
        <script>
        window.addEventListener("streamlitGPS", (event) => {
            const data = event.detail;
            window.parent.postMessage(
                {isStreamlitMessage: true, type: "streamlit:setComponentValue", value: data},
                "*"
            );
        });
        </script>
    """, height=0)
