# Created by: Cole Hagen& Joshua Pianto
# Project : NeuroSock

import wifi
import socketpool
import board
import neopixel
import time

# Neopixel setup
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Connect to WiFi
SSID = "UD Devices"
PASSWORD = ""

print("Connecting to WiFi...")
try:
    wifi.radio.connect(SSID, PASSWORD)
    print(f"Connected to WiFi! IP: {wifi.radio.ipv4_address}")
    pixel.fill((0, 255, 0))  # Green LED for successful connection
except Exception as e:
    print("Failed to connect to WiFi:", e)
    pixel.fill((255, 0, 0))  # Red LED for failure
    while True:
        time.sleep(1)  # Halt if WiFi fails

# HTTP server setup
HOST = str(wifi.radio.ipv4_address)  # Use the board's IP address
PORT = 80  # Port for the server

# Create a socket for the webserver
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket()
server.bind((HOST, PORT))
server.listen(1)  # Listen for one connection at a time
server.settimeout(None)  # No timeout
print(f"Webserver running at http://{HOST}:{PORT}")

# Function to generate an HTTP response
def generate_response(content):
    return f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head>
        <title>ESP32-S3 Webserver</title>
    </head>
    <body>
        <h1>{content}</h1>
    </body>
</html>
"""

# Main loop to serve requests
# Main loop to serve requests
while True:
    try:
        print("Waiting for connection...")
        conn, addr = server.accept()  # Accept an incoming connection
        print(f"Connection from {addr}")

        # Receive and parse the HTTP request
        buffer = bytearray(1024)  # Create a buffer for the incoming data
        bytes_received = conn.recv_into(buffer)  # Use recv_into to receive data
        request = buffer[:bytes_received].decode("utf-8")  # Decode the received data
        print("Request received:", request)

        # Generate and send a response
        response = generate_response("Hello from ESP32-S3!")
        conn.send(response.encode("utf-8"))
        print("Response sent.")

        # Close the connection
        conn.close()
        print("Connection closed.")

    except Exception as e:
        print("Error during request handling:", e)
        pixel.fill((255, 255, 0))  # Yellow LED for errors
        time.sleep(1)
