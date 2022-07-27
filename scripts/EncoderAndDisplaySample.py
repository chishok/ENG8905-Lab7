import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from Encoder.encoder import Encoder
import time

# Step size (seconds) to print feedback in timed loop
STEP_SIZE = 0.1
# Duration of timed loop (seconds)
DURATION = 60.0

# Encoder pins
ENC_PIN_A = 6
ENC_PIN_B = 13

# Display size
WIDTH = 128
HEIGHT = 32
BORDER = 3

# Display i2C address
ADDRESS = 0x3c

# Create encoder
enc = Encoder(ENC_PIN_A, ENC_PIN_B)

# Create display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=ADDRESS)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
# Load default font.
font = ImageFont.load_default()


def update_display(text: str):
    """Updates the display to show text

    Args:
        text (str): text to display
    """
    # Draw inner black rectangle
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,
        fill=0,
    )
    # Write text
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    # Display image
    oled.image(image)
    oled.show()


# Initialize loop
stop_loop = False
time_start = time.monotonic()
time_target = 0
time_elapsed = 0
while not stop_loop:
    # Update elapsed time
    time_elapsed = time.monotonic() - time_start
    if time_elapsed >= time_target:
        # Print out reading
        update_display('Count: {:}'.format(enc.read()))
        time_target += STEP_SIZE
    if time_elapsed >= DURATION:
        # End loop
        stop_loop = True
update_display('Done')
