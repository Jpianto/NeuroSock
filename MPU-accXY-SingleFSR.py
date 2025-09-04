# Code Created by Cole Hagen & Joshua Pianto



 
import board
import terminalio
import displayio
from adafruit_display_text import label
import busio
import adafruit_mpu6050  # Import MPU6050 library

# Setup for MPU-6050 Accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

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

# Function to read accelerometer values
def read_accel_values():
    accel = mpu.acceleration  # Get (x, y, z) tuple of acceleration
    return accel

# Display Accelerometer X value on the display
accel_x_label = label.Label(terminalio.FONT, text='Accel X: 0', color=TEXT_COLOR)
accel_x_label_group = displayio.Group(
    scale=FONTSCALE,
    x=30,  # Adjust position based on your layout
    y=display.height - 100  # Adjust position based on your layout
)
accel_x_label_group.append(accel_x_label)
splash.append(accel_x_label_group)

# Display Accelerometer Y value on the display
accel_y_label = label.Label(terminalio.FONT, text='Accel Y: 0', color=TEXT_COLOR)
accel_y_label_group = displayio.Group(
    scale=FONTSCALE,
    x=30,  # Adjust position based on your layout
    y=display.height - 50  # Adjust position based on your layout
)
accel_y_label_group.append(accel_y_label)
splash.append(accel_y_label_group)

while True:
    # Read and display accelerometer X and Y values
    accel_x, accel_y, _ = read_accel_values()
    accel_x_label.text = f"Accel X: {accel_x:.2f}"
    accel_y_label.text = f"Accel Y: {accel_y:.2f}"

    display.refresh()  # Refresh the display to update the values
