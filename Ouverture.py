import RPi.GPIO as GPIO
import time

motorPins = (12, 11, 13, 15)
CCWStep = (0x01, 0x02, 0x04, 0x08)
CWStep = (0x08, 0x04, 0x02, 0x01)


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in motorPins:
        GPIO.setup(pin, GPIO.OUT)


def moveOnePeriod(direction, ms):
    for j in range(0, 4, 1):
        for i in range(0, 4, 1):
            GPIO.output(motorPins[i], ((CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
        if ms < 3:
            ms = 3
        time.sleep(ms * 0.001)


def moveSteps(direction, ms, steps):
    for i in range(steps):
        moveOnePeriod(direction, ms)


def motorStop():
    for i in range(0, 4, 1):
        GPIO.output(motorPins[i], GPIO.LOW)


def loop():
    while True:
        moveSteps(0, 3, 100)  # rotating 360 deg anticlockwise
        time.sleep(0.5)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
