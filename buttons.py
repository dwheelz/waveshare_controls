"""Main app for button presses"""

from time import sleep

from PIL import Image
from PIL import ImageDraw

import RPi.GPIO as GPIO

from common import KEYS, OUTLINE, FILL_ZERO, FILL_ONE
from common.waveshare.SH1106 import SH1106


# on screen icons
gpio_pins = {
    KEYS.KEY_UP_PIN: ["polygon", [(60, 30), (42, 21), (42, 41)]],
    KEYS.KEY_LEFT_PIN: ["polygon", [(20, 20), (30, 2), (40, 20)]],
    KEYS.KEY_RIGHT_PIN : ["polygon",  [(30, 60), (40, 42), (20, 42)]],
    KEYS.KEY_DOWN_PIN: ["polygon",  [(0, 30), (18, 21), (18, 41)]],
    KEYS.KEY_PRESS_PIN: ["rectangle", (20, 22, 40, 40)],
    KEYS.KEY1_PIN: ["ellipse", (70, 0, 90, 20)],
    KEYS.KEY2_PIN: ["ellipse", (100, 20, 120, 40)],
    KEYS.KEY2_PIN: ["ellipse", (70, 40, 90, 60)]
}

key_state = {
    KEYS.KEY1_PIN: False,
    KEYS.KEY2_PIN: False,
    KEYS.KEY2_PIN: False
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
            print("Key pressed, set two waits (1: debounce, 2: re-draw for niceness)")
            sleep(0.2) # debounce
            render_wait = True

        return render_wait

    # listen for button inputs/draw the icons
    while True:
        for key, vals in gpio_pins.items():
            draw_shape = getattr(draw, vals[0])
            if key in [KEYS.KEY1_PIN, KEYS.KEY2_PIN, KEYS.KEY3_PIN]:
                pass
            #     if GPIO.input(key) and persistent_key != key_state[key]:
            #         key_state[key] = False
            #         _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ZERO)
            #     else:
            #         wait_after_render = True
            #         persistent_key = key_state[key]
            #         key_state[key] = True
            #         _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ONE)
            #         print(str(key))

            elif GPIO.input(key):
                _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ZERO)
            else:
                wait_after_render = True
                _draw(draw_shape, vals[1], outline=OUTLINE, fill=FILL_ONE)
                print(str(key))

        # if GPIO.input(KEYS.KEY_UP_PIN): # button is released
        #     _draw(draw.polygon, up, outline=255, fill=0)
        # else: # button is pressed:
        #     wait_after_render = _draw(draw.polygon, up, outline=255, fill=1)
        #     print("Up")

        # if GPIO.input(KEYS.KEY_LEFT_PIN):
        #     _draw(draw.polygon, left, outline=255, fill=0)
        # else:
        #     wait_after_render = _draw(draw.polygon, left, outline=255, fill=1)
        #     print("left")

        # if GPIO.input(KEYS.KEY_RIGHT_PIN):
        #     _draw(draw.polygon, right, outline=255, fill=0)
        # else:
        #     wait_after_render = _draw(draw.polygon, right, outline=255, fill=1)
        #     print("right")

        # if GPIO.input(KEYS.KEY_DOWN_PIN):
        #     _draw(draw.polygon, down, outline=255, fill=0)
        # else:
        #     wait_after_render = _draw(draw.polygon, down, outline=255, fill=1)
        #     print("down")

        # if GPIO.input(KEYS.KEY_PRESS_PIN):
        #     _draw(draw.rectangle, middle, outline=255, fill=0)
        # else:
        #     wait_after_render = _draw(draw.rectangle, middle, outline=255, fill=1)
        #     print("centre")

        # if GPIO.input(KEYS.KEY1_PIN) and persistent_key != KEYSTATE["ONE"][0]:
        #     _draw(draw.ellipse, pin_1, outline=255, fill=0)
        #     KEYSTATE["ONE"][1] = False
        # else:
        #     persistent_key = KEYSTATE["ONE"][0]
        #     if not KEYSTATE["ONE"][1]:
        #         wait_after_render = _draw(draw.ellipse, pin_1, outline=255, fill=1)
        #         print("KEY1")
        #         KEYSTATE["ONE"][1] = True

        # if GPIO.input(KEYS.KEY2_PIN) and persistent_key != KEYSTATE["TWO"][0]:
        #     _draw(draw.ellipse, pin_2, outline=255, fill=0)
        #     KEYSTATE["TWO"][1] = False
        # else:
        #     persistent_key = KEYSTATE["TWO"][0]
        #     if not KEYSTATE["TWO"][1]:
        #         wait_after_render = _draw(draw.ellipse, pin_2, outline=255, fill=1)
        #         print("KEY2")
        #         KEYSTATE["TWO"][1] = True

        # if GPIO.input(KEYS.KEY3_PIN) and persistent_key != KEYSTATE["THREE"][0]:
        #     _draw(draw.ellipse, pin_3, outline=255, fill=0)
        #     KEYSTATE["THREE"][1] = False
        # else:
        #     persistent_key = KEYSTATE["THREE"][0]
        #     if not KEYSTATE["THREE"][1]:
        #         wait_after_render = _draw(draw.ellipse, pin_3, outline=255, fill=1)
        #         print("KEY3")
        #         KEYSTATE["THREE"][1] = True

        disp.show_image(disp.getbuffer(image))
        if wait_after_render:
            sleep(0.4)
            wait_after_render = False

if __name__ == "__main__":
    main()