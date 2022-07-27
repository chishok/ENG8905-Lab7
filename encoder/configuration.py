"""Encoder test configuration."""


class EncoderReadConfiguration():
    """Parameters for encoder test."""

    # Step size (seconds) to capture sensor readings
    STEP_SIZE: float = 0.05
    # Step size (seconds) to print feedback
    DISPLAY_STEP_SIZE: float = 0.1
    # Duration of timed loop (seconds)
    DURATION: float = 15.0
    # Encoder pins
    ENC_PIN_A: int = 6
    ENC_PIN_B: int = 13
    # Encoder counts per revolution (CPR)
    ENC_CPR: int = 64
    # Use custom quadrature decoder
    ENC_CUSTOM_DECODER: bool = False
    # Display properties
    WIDTH: int = 128
    HEIGHT: int = 32
    BORDER: int = 3
    # Display i2C address
    ADDRESS: int = 0x3c
    # Data file prefix
    DATA_LOG_PREFIX: str = 'dataLog'
    # username
    USER: str = 'user'
