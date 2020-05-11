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
    global is_active
    global previous_time
    
    if not is_active:
        is_active = True
        current_time = time.monotonic()
        previous_time = current_time
        cp.pixels.fill(green)
        print("START")


def deactivate():
    global is_active
    global previous_time
    
    if is_active == None or is_active:
        is_active = False
        previous_time = None
        cp.pixels.fill(red)
        print("STOP")


def read_sensors(mic, samples):
    mic.record(samples, len(samples))
    sound = normalized_rms(samples)
    print("OK", cp.temperature * 9 / 5 + 32, cp.light, sound, sep=",")


mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)
previous_time = None
interval = 60 * 1 # seconds * minutes
red = (10, 0, 0)
green = (0, 10, 0)
is_active = None

deactivate()

while True:
    current_time = time.monotonic()

    if is_active and abs(current_time - previous_time) >= interval:
        read_sensors(mic, samples)
        previous_time = current_time        

    if cp.button_a:
        activate()
        
    elif cp.button_b:
        deactivate()