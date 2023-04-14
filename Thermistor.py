import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *

adc = ADCDevice()

def setup():
    global adc

    if(adc.detectI2C(0x4b)):
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n Please use command 'i2cdetect -y 1' to check the I2C address! \nProgram Exit. \n")
        exit(-1)

def getTemperature() -> float :
    value = adc.analogRead(0)
    voltage = voltage = value / 255.0 * 3.3 
    Rt = 10 * voltage / (3.3 - voltage)
    return (1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0)) - 273.15

def destroy():
    adc.close()