import json
import RPi.GPIO as GPIO
import uuid
import time
import math
import Motor
import UltrasonicSensor
import Thermistor
import GUI
import statistics
import threading
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message

porteFermeeOuOuverte = False


def setup():
    global motorSpeed

    motorSpeed = (5 / 3) * 1000
    print(motorSpeed)

    Thermistor.setup()
    UltrasonicSensor.setup()
    Motor.setup()
    GUI.setup()

    global distanceMax

    listDistance = []

    for i in range(5):
        listDistance.append(float('{0:.2f}'.format(UltrasonicSensor.getDistance())))

    distanceMax = statistics.median(listDistance)
    # print("", distanceMax)
    communicateAzure()


def loop():
    # time.sleep(5.0)
    global FermerPorte
    global porteFermeeOuOuverte

    # while True:
    #     print(float('{0:.2f}'.format(UltrasonicSensor.getDistance())))

    while True:
        isAutomatic, ManualPercentage, FermerPorte = GUI.getInformationGUI()

        if not FermerPorte:
            porteFermeeOuOuverte = False

        listDistance = []

        for i in range(5):
            listDistance.append(float('{0:.2f}'.format(UltrasonicSensor.getDistance())))

        distance = statistics.median(listDistance)
        temperature = Thermistor.getTemperature()
        updateGUI(distance, temperature, "Immobile", 0.0)

        if isAutomatic:
            if temperature < 20.0:
                setDoor(distanceMax, 0.0)
            elif 20.0 <= temperature < 35.0:
                setDoor(distanceMax, ((temperature / 35.0) * 100.0))
            elif temperature >= 35.0:
                setDoor(distanceMax, 100.0)
        else:
            # print("Mode Manuel active")
            setDoor(distanceMax, ManualPercentage)

        # print("Temperature = %.2f C | Distance = %.2f cm" %(temperature, distance))
        # Motor.moveSteps(3, 5, 1)


def setDoor(distanceMax: float, pourcentage: float):
    global porteFermeeOuOuverte

    distanceActuelle = float('{0:.2f}'.format(UltrasonicSensor.getDistance()))
    distanceObjectif = float('{0:.2f}'.format(distanceMax * (float('{0:.2f}'.format(pourcentage)) / 100.0)))

    temperature = Thermistor.getTemperature()

    updateGUI(distanceActuelle, temperature, "Immobile", 0.0)
    while not (distanceObjectif - 0.5 <= distanceActuelle <= distanceObjectif + 0.5):
        if porteFermeeOuOuverte:
            break

        temperature = Thermistor.getTemperature()
        direction = "Immobile"
        vitesse = 0

        if distanceActuelle < distanceObjectif:
            Motor.moveSteps(3, 3, 0)
            direction = "Ouverture"
            vitesse = motorSpeed
        else:
            Motor.moveSteps(3, 3, 1)
            direction = "Fermeture"
            vitesse = motorSpeed

        listDistance = []

        for _ in range(5):
            listDistance.append(float('{0:.2f}'.format(UltrasonicSensor.getDistance())))

        # print("check")
        distanceActuelle = statistics.median(listDistance)
        updateGUI(distanceActuelle, temperature, direction, vitesse)
        # print(distanceObjectif, " - ", pourcentage, "%")
        # print(distanceActuelle, " - clean")

    if FermerPorte:
        porteFermeeOuOuverte = True


def updateGUI(distance: float, temperature: float, direction: str, vitesse: float):
    try:
        GUI.app.update()
        GUI.app.updateCurrentOpening((distance - 5.0) / (distanceMax - 5.0) * 100.0)
        GUI.app.updateCurrentTemperature(temperature)
        GUI.app.updateCurrentSpeed(vitesse)
        GUI.app.updateCurrentDirection(direction)

    except Exception:
        destroy()
        GPIO.cleanup()


def communicateAzure():
    conn_str = "HostName=internetobjethubtest.azure-devices.net;DeviceId=collect_temperature;SharedAccessKey=AQK7Cua8C5xvyDbeWm2GBDbgsoVst4SHm5eKHUcTOa4="
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    listDistance = []

    for i in range(5):
        listDistance.append(float('{0:.2f}'.format(UltrasonicSensor.getDistance())))

    distance = statistics.median(listDistance)

    try:
        device_client.connect()
        data = {
            "temperature": Thermistor.getTemperature(),
            "pourcentageOuverturePorte": (distance - 5.0) / (distanceMax - 5.0) * 100.0,
            "distance": distance
        }
        msg = Message(json.dumps(data))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-1234"
        msg.custom_properties["tornado-warning"] = "yes"
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        print("sending message")
        device_client.send_message(msg)
    except KeyboardInterrupt:
        print("user exit")
    except Exception:
        print("Error")
        raise
    finally:
        device_client.shutdown()

    threading.Timer(60.0, communicateAzure).start()


def destroy():
    Thermistor.destroy()


if __name__ == "__main__":
    print('Program is starting ... ')
    setup()

    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        GPIO.cleanup()
