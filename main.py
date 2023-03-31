import pulseio
import board

"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel

PULSE_THRESHOLD = 5

pulses = pulseio.PulseIn(board.A0)

pixel_pin = board.D11
num_pixels = 36

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

COLUMN_1 = (0,5)
COLUMN_2 = (11,6)
COLUMN_3 = (12,17)
COLUMN_4 = (23,18)
COLUMN_5 = (24,29)
COLUMN_6 = (35,30)

OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


class LEDCOL:
    def __init__(self, ends, color):
        self.bottom = ends[0]
        self.top = ends[1]
        self.color = color
        self.current_count = 0

    def increment(self):
        self.current_count += 1
        if self.current_count > 6:
            self.current_count = 6
            return True
        self.update_pixels()
        return False

    def decrement(self):
        self.current_count -= 1
        if self.current_count < 0:
            self.current_count = 0
            return True
        self.update_pixels()
        return False

    def update_pixels(self):
        if self.top > self.bottom:
            for i in range(0,6):
                pixels[self.bottom + i] = OFF
            for j in range(0, self.current_count):
                pixels[self.bottom + j] = self.color
        else:
            for i in range(0,6):
                pixels[self.bottom - i] = OFF
            for j in range(0, self.current_count):
                pixels[self.bottom - j] = self.color
        pixels.show()



def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


pixels.fill(OFF)
pixels.show()
col_1 = LEDCOL(COLUMN_1, RED)
col_2 = LEDCOL(COLUMN_2, BLUE)
col_3 = LEDCOL(COLUMN_3, GREEN)
col_4 = LEDCOL(COLUMN_4, CYAN)
col_5 = LEDCOL(COLUMN_5, YELLOW)
col_6 = LEDCOL(COLUMN_6, PURPLE)

pulse_count = 0

while True:
    # pixels.fill(RED)
    # pixels.show()
    # # Increase or decrease to change the speed of the solid color change.
    # time.sleep(1)
    # pixels.fill(GREEN)
    # pixels.show()
    # time.sleep(1)
    # pixels.fill(BLUE)
    # pixels.show()
    # time.sleep(1)

    # color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    # color_chase(YELLOW, 0.1)
    # color_chase(GREEN, 0.1)
    # color_chase(CYAN, 0.1)
    # color_chase(BLUE, 0.1)
    # color_chase(PURPLE, 0.1)

    # rainbow_cycle(0)  # Increase the number to slow down the rainbow

    if len(pulses) > 0:
        pulses.pause()
        print(f"Pulses len: {len(pulses)}")

        pulse_count += len(pulses)
        if pulse_count > PULSE_THRESHOLD:
            if col_1.increment():
                if col_2.increment():
                    if col_3.increment():
                        if col_4.increment():
                            if col_5.increment():
                                if col_6.increment():
                                    print("Matrix Full")
            pulse_count = 0

        pulses.clear()
        pulses.resume()

