"""Main app for button presses"""

from time import sleep

from PIL import Image
from PIL import ImageDraw

import RPi.GPIO as GPIO

from common import KEYS, OUTLINE, FILL_ZERO, FILL_ONE, EXPECTED_BULB_NAMES
from common.waveshare.SH1106 import SH1106
from common.kasa_bulbs import get_bulbs, async_run


# on screen icons
gpio_pins = {
    KEYS.KEY_UP_PIN: ["polygon", [(60, 30), (42, 21), (42, 41)]],
    KEYS.KEY_LEFT_PIN: ["polygon", [(20, 20), (30, 2), (40, 20)]],
    KEYS.KEY_RIGHT_PIN : ["polygon",  [(30, 60), (40, 42), (20, 42)]],
    KEYS.KEY_DOWN_PIN: ["polygon",  [(0, 30), (18, 21), (18, 41)]],
    KEYS.KEY_PRESS_PIN: ["rectangle", (20, 22, 40, 40)],
    KEYS.KEY1_PIN: ["ellipse", (70, 0, 90, 20)],
    KEYS.KEY2_PIN: ["ellipse", (100, 20, 120, 40)],
    KEYS.KEY3_PIN: ["ellipse", (70, 40, 90, 60)]
}

def main():
    """The main funct"""
    # Setup
    disp = SH1106()
    disp.init()
    disp.clear()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(KEYS.KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
    GPIO.setup(KEYS.KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up

    # GET BULBS
    _bulbs = get_bulbs()
    bulb_keys = {KEYS.KEY1_PIN: _bulbs[EXPECTED_BULB_NAMES[0]], KEYS.KEY2_PIN: _bulbs[EXPECTED_BULB_NAMES[0]]}

    # Create initial image and set it
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    persistent_key = None
    wait_after_render = False

    def _draw(obj, *args, **kwargs):
        """draws the provided object"""
        render_wait = False
        obj(*args, **kwargs)
        if kwargs["fill"] == 1:
            sleep(0.2) # debounce
            render_wait = True

        return render_wait

    # listen for button inputs/draw the icons
    while True:
        for key, vals in gpio_pins.items():
            draw_shape = getattr(draw, vals[0])
            if key in [KEYS.KEY1_PIN, KEYS.KEY2_PIN, KEYS.KEY3_PIN]:
                if not GPIO.input(key) and (persistent_key != key):
                    # BUTTON PRESSED
                    wait_after_render = True
                    persistent_key = key
                    _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ONE)
                elif GPIO.input(key) and (persistent_key != key):
                    _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ZERO)
            elif GPIO.input(key):
                _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ZERO)
            else:
                # BUTTON PRESSED
                wait_after_render = True
                _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ONE)

        disp.show_image(disp.getbuffer(image))
        if wait_after_render:
            sleep(0.4)
            wait_after_render = False

if __name__ == "__main__":
    main()