import array
import math
import time

import audiobusio
import board
from adafruit_circuitplayground import cp


def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(sum_of_samples / len(values))


def activate():
    global isActive
    isActive = True
    cp.pixels.fill(green)


def deactivate():
    global isActive
    isActive = False
    cp.pixels.fill(red)


mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)
currentTime = time.monotonic()
previousTime = currentTime
interval = 60.0
red = (10, 0, 0)
green = (0, 10, 0)
isActive = None

activate()

while True:
    currentTime = time.monotonic()

    if (currentTime - previousTime) >= interval:
        if isActive:
            mic.record(samples, len(samples))
            sound = normalized_rms(samples)
            print("OK", cp.temperature * 9 / 5 + 32, cp.light, sound, sep=",")
        else:
            print("STOP")
        previousTime = currentTime

    if cp.button_a:
        activate()
    elif cp.button_b:
        deactivate()

