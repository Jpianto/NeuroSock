# Created by: Joshua Pianto & Cole Hagen 
# Project : NeuroSock

import board
import digitalio
import analogio
import time
from adafruit_display_text import label
import displayio
import terminalio
import busio
import adafruit_mpu6050
import neopixel

# Setup GPIO pins
mosfet_gate = digitalio.DigitalInOut(board.D6)
mosfet_gate.direction = digitalio.Direction.OUTPUT

switch = digitalio.DigitalInOut(board.D5)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

green_led = digitalio.DigitalInOut(board.D10)
green_led.direction = digitalio.Direction.OUTPUT

red_led = digitalio.DigitalInOut(board.D11)
red_led.direction = digitalio.Direction.OUTPUT

yellow_led = digitalio.DigitalInOut(board.D12)
yellow_led.direction = digitalio.Direction.OUTPUT

# Setup Neopixel for status
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Setup sensors
heel_sensor = analogio.AnalogIn(board.A0)
ball_sensor = analogio.AnalogIn(board.A1)

# Initialize accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Thresholds
HEEL_THRESHOLD = 60500
BALL_THRESHOLD = 60500
DYNAMIC_ACCEL_THRESHOLD = 0.5
ACCELERATION_THRESHOLD = 0.3

# Display setup
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash

# Create a background
BACKGROUND_COLOR = 0x000000
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Add a status label
status_label = label.Label(
    terminalio.FONT, text="Initializing...", color=0xFFFFFF, scale=2
)
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = (display.width // 2, display.height // 2)
splash.append(status_label)

# Function to control TENS
def activate_tens():
    mosfet_gate.value = True
    green_led.value = True
    red_led.value = False
    status_label.text = "TENS Active"
def deactivate_tens():
    mosfet_gate.value = False
    green_led.value = False
    red_led.value = True
    status_label.text = "TENS Standby"
# Function to read accelerometer data
def get_acceleration():
    accel_x, accel_y, accel_z = mpu.acceleration
    dynamic_accel = ((accel_x ** 2) + (accel_y ** 2) + (accel_z ** 2)) ** 0.5 - 9.8
    return max(dynamic_accel, 0) if dynamic_accel > DYNAMIC_ACCEL_THRESHOLD else 0
# Main loop
while True:
    state = "Standby" if switch.value else "Idle"
    heel_value = ball_value = acceleration = 0  # Defaults for standby mode
    if switch.value:
        # Standby mode
        yellow_led.value = True
        green_led.value = False
        red_led.value = False
        deactivate_tens()
        pixel.fill((255, 255, 0))  # Yellow for standby
    else:
        # Active logic mode
        yellow_led.value = False
        pixel.fill((0, 0, 255))  # Blue for active logic
        heel_value = heel_sensor.value
        ball_value = ball_sensor.value
        acceleration = get_acceleration()

        # Determine state and control TENS
        if heel_value > HEEL_THRESHOLD and ball_value > BALL_THRESHOLD and acceleration < ACCELERATION_THRESHOLD:
            state = "Sitting"
            activate_tens()
           
            #deactivate_tens()
        elif heel_value < HEEL_THRESHOLD and ball_value < BALL_THRESHOLD and acceleration < ACCELERATION_THRESHOLD:
            state = "Standing"
            deactivate_tens
        elif acceleration > ACCELERATION_THRESHOLD:
            state = "Walking"
            activate_tens() if heel_value > HEEL_THRESHOLD and ball_value > BALL_THRESHOLD else deactivate_tens()
        else:
            state = "Idle"
            deactivate_tens()
    # Refresh display
    display.refresh()
    time.sleep(0.1)
