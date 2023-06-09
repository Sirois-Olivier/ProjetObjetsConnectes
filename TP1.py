import json
import RPi.GPIO as GPIO
import uuid
import time
import math
import ReceivedMessageManager
import Motor
import UltrasonicSensor
import Thermistor
import GUI
import MySqlConnector
import statistics
import threading
import datetime
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message

porteFermeeOuOuverte = False


def setup():
    global motorSpeed
    global receivedMessageManager
    receivedMessageManager = ReceivedMessageManager.ReceivedMessageManager()
    motorSpeed = (5 / 3) * 1000
    print(motorSpeed)

    Thermistor.setup()
    UltrasonicSensor.setup()
    Motor.setup()
    GUI.setup()

    global distanceMax

    distanceMax = calculateDistance()

    communicateAzure()
    

def loop():
    global FermerPorte
    global porteFermeeOuOuverte

    while True:
        if receivedMessageManager.GetMessageEnCours() is not None:
            isAutomatic, ManualPercentage, FermerPorte = receivedMessageManager.GetMessageEnCours()
            print(isAutomatic)
            print(ManualPercentage)
            receivedMessageManager.SetMessageEnCours(None)
        else:
            isAutomatic, ManualPercentage, FermerPorte = GUI.getInformationGUI()

        distance = calculateDistance()
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
            setDoor(distanceMax, ManualPercentage)


def setDoor(distanceMax: float, pourcentage: float):
    global FermerPorte

    distanceActuelle = float('{0:.2f}'.format(UltrasonicSensor.getDistance()))
    distanceObjectif = float('{0:.2f}'.format(distanceMax * (float('{0:.2f}'.format(pourcentage)) / 100.0)))

    temperature = Thermistor.getTemperature()

    updateGUI(distanceActuelle, temperature, "Immobile", 0.0)
    while not (distanceObjectif - 0.5 <= distanceActuelle <= distanceObjectif + 0.5):
        if FermerPorte:
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

        distanceActuelle = calculateDistance()
        updateGUI(distanceActuelle, temperature, direction, vitesse)

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
    global threadAzure
    
    try:
        conn_str = "HostName=iothubserre.azure-devices.net;DeviceId=deviceserre;SharedAccessKey=bSyoNmN6YQ1E4QnviMOoZd0B1jnHhWzdJJ0npmcc4WM"
        device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        device_client.connect()
        distance = calculateDistance()

        lstDataASynchroniser = MySqlConnector.loadDataSerreASynchronizer()

        for dataASynchroniser in lstDataASynchroniser:
            data = {
                "temperature": dataASynchroniser[1],
                "percentageDoorOpen": dataASynchroniser[2],
                "distance": dataASynchroniser[3],
                "dateTime": dataASynchroniser[4]
            }
            msg = Message(json.dumps(data))
            msg.message_id = uuid.uuid4()
            msg.correlation_id = "correlation-1234"
            msg.custom_properties["tornado-warning"] = "yes"
            msg.content_encoding = "utf-8"
            msg.content_type = "application/json"
            print("sending message", data)
            device_client.send_message(msg)

        MySqlConnector.clearDataSerreASynchronizer()
        
        data = {
            "temperature": Thermistor.getTemperature(),
            "percentageDoorOpen": (distance - 5.0) / (distanceMax - 5.0) * 100.0,
            "distance": distance,
            "dateTime": f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}'
            
        }
        msg = Message(json.dumps(data))
        msg.message_id = uuid.uuid4()
        msg.correlation_id = "correlation-1234"
        msg.custom_properties["tornado-warning"] = "yes"
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        print("sending message", data)
        MySqlConnector.saveDataSerre(data)
        device_client.send_message(msg)
        device_client.shutdown()
    except KeyboardInterrupt:
        print("user exit")
    except Exception:
        distance = calculateDistance()
        data = {
            "temperature": Thermistor.getTemperature(),
            "percentageDoorOpen": (distance - 5.0) / (distanceMax - 5.0) * 100.0,
            "distance": distance,
            "dateTime": f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}'
            
        }
        MySqlConnector.saveDataSerre(data)
        MySqlConnector.saveDataSerreASynchroniser(data)
    finally:
        threadAzure = threading.Timer(60.0, communicateAzure).start()


def calculateDistance() -> float:
    listDistance = []

    for i in range(5):
        listDistance.append(float('{0:.2f}'.format(UltrasonicSensor.getDistance())))

    return statistics.median(listDistance)


def destroy():
    Thermistor.destroy()


if __name__ == "__main__":
    print('Program is starting ... ')
    setup()

    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
        receivedMessageManager.client.shutdown()
        GPIO.cleanup()
        
