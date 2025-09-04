#Created by Joshua Pianto
#Takes a single Input from analog pin A1 which is connected to a pressure sensitive resistors.
#Taking these inputs and displaying thier value on the TFT

import board
import terminalio
import displayio
from adafruit_display_text import label
import analogio  # Import analogio module

# Setup for FSR
fsr_pin = board.A1  # Change pin as per your wiring
fsr = analogio.AnalogIn(fsr_pin)

# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 2
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

# Function to read FSR value
def read_fsr_value():
    return fsr.value

# Display FSR value on the display
fsr_value_label = label.Label(terminalio.FONT, text='FSR Value: 0000', color=TEXT_COLOR)
fsr_value_label_group = displayio.Group(
    scale=FONTSCALE,
    x=30,  # Adjust position based on your layout
    y=display.height - 70  # Adjust position based on your layout
)
fsr_value_label_group.append(fsr_value_label)
splash.append(fsr_value_label_group)

while True:
    # Update the FSR reading
    fsr_value = read_fsr_value()
    if fsr_value >= 56000:
        color_palette[0] = ALERT_COLOR  # Change background to red
        fsr_value_label.text = 'Pressure High'  # Change text
        fsr_value_label.color = 0xFFFFFF  # Change text color to white for visibility
    else:
        color_palette[0] = BACKGROUND_COLOR  # Revert to original background
        fsr_value_label.text = f'FSR Value:\n {fsr_value}'  # Show normal FSR value
        fsr_value_label.color = TEXT_COLOR  # Revert text color to yellow

    display.refresh()  # Refresh the display to update the value
