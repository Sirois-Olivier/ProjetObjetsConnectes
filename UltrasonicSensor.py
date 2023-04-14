import RPi.GPIO as GPIO
import time

trigPin = 16
echoPin = 36
MAX_DISTANCE = 220
timeOut = MAX_DISTANCE*60


def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getDistance():
    GPIO.output(trigPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigPin, GPIO.LOW)
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)
    distance = pingTime * 340.0 / 2.0 / 10000.0
    return distance

def setup():
    GPIO.setmode(GPIO.BOARD) #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT) # set trigPin to output mode
    GPIO.setup(echoPin, GPIO.IN) # set echoPin to input mode































