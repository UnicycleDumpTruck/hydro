import pulseio
import board

"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel

from random import choice

PULSE_THRESHOLD = 1
DECREMENT_TIME = 0.1 # Seconds between column decrements

last_decrement = time.monotonic()

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
        if self.current_count == 0:
            non_empty_cols.add(self)
            empty_cols.remove(self)
        self.current_count += 1
        if self.current_count > 6:
            self.current_count = 6
        self.update_pixels()
        return (self.current_count > 1)

    def decrement(self):
        self.current_count -= 1
        if self.current_count < 0:
            self.current_count = 0
        if self.current_count == 0:
            empty_cols.add(self)
            non_empty_cols.remove(self)

        self.update_pixels()
        return (self.current_count == 0)

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


pixels.fill(OFF)
pixels.show()
col_1 = LEDCOL(COLUMN_1, RED)
col_2 = LEDCOL(COLUMN_2, BLUE)
col_3 = LEDCOL(COLUMN_3, GREEN)
col_4 = LEDCOL(COLUMN_4, PURPLE)
col_5 = LEDCOL(COLUMN_5, YELLOW)
col_6 = LEDCOL(COLUMN_6, CYAN)

cols = [col_1, col_2, col_3, col_4, col_5, col_6]
non_empty_cols = set()
empty_cols = set(cols)

pulse_count = 0

while True:
    # print((time.monotonic() - last_decrement))
    if (time.monotonic() - last_decrement) > DECREMENT_TIME:
        # for c in cols:
        #     c.decrement()

        # if col_1.decrement():
        #     if col_2.decrement():
        #         if col_3.decrement():
        #             if col_4.decrement():
        #                 if col_5.decrement():
        #                     if col_6.decrement():
        #                         print("Matrix Empty")
        if len(non_empty_cols):
            choice(tuple(non_empty_cols)).decrement()

        last_decrement = time.monotonic()

    if len(pulses) > 0:
        pulses.pause()
        print(f"Pulses len: {len(pulses)}")

        pulse_count += len(pulses)
        if pulse_count > PULSE_THRESHOLD:
            choice(cols).increment()
            # if col_1.increment():
            #     if col_2.increment():
            #         if col_3.increment():
            #             if col_4.increment():
            #                 if col_5.increment():
            #                     if col_6.increment():
            #                         print("Matrix Full")
            pulse_count = 0

        pulses.clear()
        pulses.resume()

