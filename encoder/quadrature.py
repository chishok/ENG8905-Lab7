"""Decode and scale incremental quadrature encoder."""
from Encoder.encoder import Encoder
from encoder.configuration import EncoderReadConfiguration
import RPi.GPIO as GPIO
from threading import Lock


class Quadrature:
    """Custom quadrature encoder decoding."""

    # state A and B can be either high H or low L
    AL_BL: int = 0b00
    AL_BH: int = 0b01
    AH_BH: int = 0b11
    AH_BL: int = 0b10

    # movement is increment or decrement
    INCR: int = 1
    DECR: int = -1

    def __init__(self, pin_a: int, pin_b: int) -> None:

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_a, GPIO.IN)
        GPIO.setup(pin_b, GPIO.IN)

        # pins
        self.pin_a = pin_a
        self.pin_b = pin_b

        # initialize state
        self.mutex = Lock()
        self.position: int = 0
        self.state: int = self._get_input()
        self.movement: int = self.INCR

        # set callbacks
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self._update)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self._update)

    def read(self) -> int:
        return self.position

    def _get_input(self) -> int:
        state = 0b00
        if GPIO.input(self.pin_a):
            state |= 0b10
        if GPIO.input(self.pin_b):
            state |= 0b01
        return state

    def _update(self, _) -> None:
        # mutual exclusion
        self.mutex.acquire()

        # get new state
        new_state = self._get_input()

        # STUDENT WORK SECTION BEGIN
        # ==========================

        # gray code logic
        if new_state is not self.state:

            if self.state is self.AL_BL:
                # gray code: either AL_BH or AH_BL is valid

                # >>> Add logic here to update state and position
                pass

            elif self.state is self.AL_BH:
                # gray code: either AH_BH or AL_BL is valid

                # >>> Add logic here to update state and position
                pass

            elif self.state is self.AH_BH:
                # gray code: either AH_BL or AL_BH is valid

                # >>> Add logic here to update state and position
                pass

            else:
                # state is self.AH_BL
                # gray code: either AL_BL or AH_BH is valid

                # >>> Add logic here to update state and position
                pass

        # ========================
        # STUDENT WORK SECTION END

        # release mutex
        self.mutex.release()


class RotaryEncoder():
    """Encoder Sensor readings."""

    def __init__(self, config: EncoderReadConfiguration):
        """Initialize encoder with configuration parameters.

        Args:
            config (EncoderReadConfiguration): Configuration parameters
        """
        # Create encoder
        if config.ENC_CUSTOM_DECODER:
            # self.enc: QuadratureLut = QuadratureLut(config.ENC_PIN_A, config.ENC_PIN_B)
            self.enc: Quadrature = Quadrature(config.ENC_PIN_A, config.ENC_PIN_B)
        else:
            self.enc: Encoder = Encoder(config.ENC_PIN_A, config.ENC_PIN_B)

        self.counts_per_rev: float = float(config.ENC_CPR)
        self.units_per_rev: float = 360.0
        self.offset: float = 0.0

    def read(self) -> float:
        """Read encoder sensor data.

        Returns:
            float: Scaled encoder reading.
        """
        return float(self.enc.read()) * self.units_per_rev / self.counts_per_rev + self.offset
