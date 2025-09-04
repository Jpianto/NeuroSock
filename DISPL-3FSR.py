#Created by Cole Hagen & Joshua Pianto
#Takes 3 Inputs from analog pin A1-A3 which are connected to 3 pressure sensitive resistors.
#Taking these inputs and displaying thier value on the TFT

import board
import terminalio
import displayio
from adafruit_display_text import label
import analogio  # Import analogio module

# Setup for FSRs on A1, A2, and A3
fsr_A1 = analogio.AnalogIn(board.A1)
fsr_A2 = analogio.AnalogIn(board.A2)
fsr_A3 = analogio.AnalogIn(board.A3)

# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 1  # Adjusted for space to display more text
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00
ALERT_COLOR = 0xFF0000  # Red for high pressure alert

display = board.DISPLAY

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR  # Initial background color

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Setup label groups for FSR values on the display
labels = []
positions = [(30, display.height - 90), (30, display.height - 60), (30, display.height - 30)]
fsr_sensors = [fsr_A1, fsr_A2, fsr_A3]
for i, pos in enumerate(positions):
    fsr_label = label.Label(terminalio.FONT, text=f'FSR{i+1} Value: 0000', color=TEXT_COLOR, scale=FONTSCALE)
    fsr_label_group = displayio.Group(x=pos[0], y=pos[1])
    fsr_label_group.append(fsr_label)
    splash.append(fsr_label_group)
    labels.append(fsr_label)

def read_fsr_value(sensor):
    return sensor.value

while True:
    pressure_high = False
    for fsr, label in zip(fsr_sensors, labels):
        value = read_fsr_value(fsr)
        label.text = f'FSR Value: {value}'
        if value >= 56000:
            pressure_high = True

    if pressure_high:
        color_palette[0] = ALERT_COLOR  # Change background to red
        for label in labels:
            label.text = 'Pressure High'  # Change text
            label.color = 0xFFFFFF  # Change text color to white for visibility
    else:
        color_palette[0] = BACKGROUND_COLOR  # Revert to original background
        for i, label in enumerate(labels):
            label.text = f'FSR{i+1} Value: {fsr_sensors[i].value}'  # Show normal FSR value
            label.color = TEXT_COLOR  # Revert text color to yellow

    display.refresh()  # Refresh the display to update the value
