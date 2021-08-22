"""Main app for button presses"""

from time import sleep

from PIL import Image
from PIL import ImageDraw

import RPi.GPIO as GPIO

from common import KEYS, KEYSTATE
from common.waveshare.SH1106 import SH1106


# icons
up = [(60, 30), (42, 21), (42, 41)]
down = [(0, 30), (18, 21), (18, 41)]
right = [(30, 60), (40, 42), (20, 42)]
left = [(20, 20), (30, 2), (40, 20)]
middle = (20, 22,40, 40)
pin_1 = (70, 0, 90, 20)
pin_2 = (100, 20, 120, 40)
pin_3 = (70, 40, 90, 60)


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

    # Create initial image and set it
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    def _draw(obj, *args, **kwargs):
        """draws the provided object"""
        obj(*args, **kwargs)
        if kwargs["fill"] == 1:
            sleep(0.5)

    persistent_key = None

    # listen for button inputs/draw the icons
    while True:
        if GPIO.input(KEYS.KEY_UP_PIN): # button is released
            _draw(draw.polygon, up, outline=255, fill=0)
        else: # button is pressed:
            _draw(draw.polygon, up, outline=255, fill=1)
            print("Up")

        if GPIO.input(KEYS.KEY_LEFT_PIN):
            _draw(draw.polygon, left, outline=255, fill=0)
        else:
            _draw(draw.polygon, left, outline=255, fill=1)
            print("left")

        if GPIO.input(KEYS.KEY_RIGHT_PIN):
            _draw(draw.polygon, right, outline=255, fill=0)
        else:
            _draw(draw.polygon, right, outline=255, fill=1)
            print("right")

        if GPIO.input(KEYS.KEY_DOWN_PIN):
            _draw(draw.polygon, down, outline=255, fill=0)
        else:
            _draw(draw.polygon, down, outline=255, fill=1)
            print("down")

        if GPIO.input(KEYS.KEY_PRESS_PIN):
            _draw(draw.rectangle, middle, outline=255, fill=0)
        else:
            _draw(draw.rectangle, middle, outline=255, fill=1)
            print("centre")

        if GPIO.input(KEYS.KEY1_PIN) and persistent_key != KEYSTATE["ONE"][0]:
            _draw(draw.ellipse, pin_1, outline=255, fill=0)
            KEYSTATE["ONE"][1] = False
        else:
            persistent_key = KEYSTATE["ONE"][0]
            if not KEYSTATE["ONE"][1]:
                _draw(draw.ellipse, pin_1, outline=255, fill=1)
                print("KEY1")
                KEYSTATE["ONE"][1] = True

        if GPIO.input(KEYS.KEY2_PIN) and persistent_key != KEYSTATE["TWO"][0]:
            _draw(draw.ellipse, pin_2, outline=255, fill=0)
            KEYSTATE["TWO"][1] = False
        else:
            persistent_key = KEYSTATE["TWO"][0]
            if not KEYSTATE["TWO"][1]:
                _draw(draw.ellipse, pin_2, outline=255, fill=1)
                print("KEY2")
                KEYSTATE["TWO"][1] = True

        if GPIO.input(KEYS.KEY3_PIN) and persistent_key != KEYSTATE["THREE"][0]:
            _draw(draw.ellipse, pin_3, outline=255, fill=0)
            KEYSTATE["THREE"][1] = False
        else:
            persistent_key = KEYSTATE["THREE"][0]
            if not KEYSTATE["THREE"][1]:
                _draw(draw.ellipse, pin_3, outline=255, fill=1)
                print("KEY3")
                KEYSTATE["THREE"][1] = True

        disp.show_image(disp.getbuffer(image))

if __name__ == "__main__":
    main()