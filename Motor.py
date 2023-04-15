import RPi.GPIO as GPIO
import time

motorPins = (12, 11, 13, 15)
CCWStep = (0x01, 0x02, 0x04, 0x08)
CWStep = (0x08, 0x04, 0x02, 0x01)


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in motorPins:
        GPIO.setup(pin, GPIO.OUT)


def moveOnePeriod(ms, direction):
    for j in range(0, 4, 1):
        for i in range(0, 4, 1):
            if direction == 1:
                GPIO.output(motorPins[i], ((CCWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
            else:
                GPIO.output(motorPins[i], ((CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
        if ms < 3:
            ms = 3
        time.sleep(ms * 0.001)


def moveSteps(ms, steps, direction):
    for i in range(steps):
        moveOnePeriod(ms, direction)
