import wifi
import json
import board

# Load WiFi details from secrets.json
try:
    with open("/secrets.json") as f:
        secrets = json.load(f)
except OSError:
    print("Couldn't find secrets.json file")
    raise

# Connect to WiFi
wifi.radio.connect(secrets["ssid"], secrets["password"])

print("Connected to WiFi:", secrets["ssid"])
print("IP Address:", wifi.radio.ipv4_address)
