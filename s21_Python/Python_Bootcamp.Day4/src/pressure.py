import random
import time


def emit_gel(step):
    pressure = 50
    while True:
        step_size = random.uniform(0, step)
        pressure += round(step_size)
        if pressure > 100 or pressure < 0:
            break
        if pressure < 20 or pressure > 80:
            step = -step
        if pressure > 90 or pressure < 10:
            break
        time.sleep(0.5)
        yield pressure


def valve():
    step = 50
    gel_gen = emit_gel(step)
    try:
        while True:
            pressure = next(gel_gen)
            if pressure > 90 or pressure < 10:
                break
            if pressure < 20 or pressure > 80:
                step = -step
                gel_gen.send(step)
            print(f"Pressure: {pressure}")
    except StopIteration:
        print("Emergency break - Pressure out of range")


valve()
