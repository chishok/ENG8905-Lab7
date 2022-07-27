"""Display data on small LED."""

from encoder.configuration import EncoderReadConfiguration
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class TextWithBorderDisplay():
    """Small LED text display inside rectangular border."""

    def __init__(self, config: EncoderReadConfiguration):
        """Initialize i2c display with ssd1306 protocol and set border.

        Args:
            config (EncoderReadConfiguration): Configuration parameters
        """
        # Create display
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.oled = adafruit_ssd1306.SSD1306_I2C(config.WIDTH, config.HEIGHT, self.i2c, addr=config.ADDRESS)
        # Clear display
        self.oled.fill(0)
        self.oled.show()
        # Create blank image for drawing
        self.image = Image.new('1', (self.oled.width, self.oled.height))
        # Get drawing object to draw on image
        self.draw = ImageDraw.Draw(self.image)
        # Draw a white background
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height),
                            outline=255, fill=255)
        # Draw inner black rectangle
        top_left_corner = (config.BORDER, config.BORDER)
        bottom_right_corner = (self.oled.width - config.BORDER - 1, self.oled.height - config.BORDER - 1)
        self.draw.rectangle(
            (top_left_corner[0], top_left_corner[1], bottom_right_corner[0], bottom_right_corner[1]),
            outline=0,
            fill=0,
        )
        # Load default font
        self.font = ImageFont.load_default()
        # save border config
        self.border = config.BORDER

    def update(self, text: str):
        """Update the display to show text.

        Args:
            text (str): text to display
        """
        # Draw inner black rectangle
        top_left_corner = (self.border, self.border)
        bottom_right_corner = (self.oled.width - self.border - 1, self.oled.height - self.border - 1)
        self.draw.rectangle(
            (top_left_corner[0], top_left_corner[1], bottom_right_corner[0], bottom_right_corner[1]),
            outline=0,
            fill=0,
        )
        # Write text
        (font_width, font_height) = self.font.getsize(text)
        # Put text at center of display
        top_left_x = self.oled.width // 2 - font_width // 2
        top_left_y = self.oled.height // 2 - font_height // 2
        self.draw.text(
            (top_left_x, top_left_y),
            text,
            font=self.font,
            fill=255,
        )
        # Display image
        self.oled.image(self.image)
        self.oled.show()
