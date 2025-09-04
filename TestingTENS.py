# Created by: Cole Hagen & Joshua Pianto
# Project : NeuroSock

import board
import digitalio
import time
import displayio
import terminalio
from adafruit_display_text import label

# Setup GPIO pin for MOSFET Gate control
mosfet_gate = digitalio.DigitalInOut(board.D6) 
mosfet_gate.direction = digitalio.Direction.OUTPUT


# Setup GPIO pin for toggle switch
toggle_switch = digitalio.DigitalInOut(board.D5)  
toggle_switch.direction = digitalio.Direction.INPUT
toggle_switch.pull = digitalio.Pull.UP  # Enable pull-up resistor

# Setup TFT display
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash

# Background color
BACKGROUND_COLOR = 0x000000  # Black
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Status label for TFT screen
status_label = label.Label(
    terminalio.FONT, text="Initializing...", color=0xFFFFFF, scale=2
)
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = (display.width // 2, display.height // 2)
splash.append(status_label)

# Functions to control TENS unit
def turn_on_tens():
    mosfet_gate.value = True
    status_label.text = "Flow ON"
    print("Flow ON: Gate Voltage HIGH")

def turn_off_tens():
    mosfet_gate.value = False
    status_label.text = "Flow OFF"
    print("Flow OFF: Gate Voltage LOW")

# Main loop
while True:
    if not toggle_switch.value:  # Toggle switch is pressed
        turn_on_tens()
    else:  # Toggle switch is released
        turn_off_tens()

    # Refresh the display
    display.refresh()
    time.sleep(0.1)  # Small delay to debounce the toggle switch
