import time
import datetime
from azure.iot.device import IoTHubDeviceClient, MethodResponse

CONNECTION_STRING = "HostName=iothubserre.azure-devices.net;DeviceId=deviceserre;SharedAccessKey=BDWKJV/+KR6BKaWZsIHGdThmvT/jFy5Wi91ZxSstolQ="

class ReceivedMessageManager:

    def __init__(self):
        self.messageEnCours = ""
        self.client = None
        self.create_client()

    def GetMessageEnCours(self):
        return self.messageEnCours
    
    def SetMessageEnCours(self, value: str):
        self.messageEnCours = value

    def create_client(self):
        # Instantiate the client
        self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        # Define the handler for method requests
        def method_request_handler(method_request):
<<<<<<< HEAD
            request = str(method_request.name).split(",")

            if request[0] == "Open":
=======
            if method_request.name == "Open":
>>>>>>> 9777788ba4754d6ea9722c502686054bab0a2774

                self.messageEnCours = "Open"

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

<<<<<<< HEAD
            elif request[0] == "Close":
=======
            elif method_request.name == "Close":
>>>>>>> 9777788ba4754d6ea9722c502686054bab0a2774

                self.messageEnCours = "Close"

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)
<<<<<<< HEAD
            
            elif request[0] == "Manuel":

                self.messageEnCours = request[0] + " -> " + request[1]

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)
=======
>>>>>>> 9777788ba4754d6ea9722c502686054bab0a2774

            else:
                # Create a method response indicating the method request was for an unknown method
                resp_status = 404
                resp_payload = {"Response": "Unknown method"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

            # Send the method response
            self.client.send_method_response(method_response)

        try:
            # Attach the handler to the client
            self.client.on_method_request_received = method_request_handler
        except:
            # In the event of failure, clean up
            self.client.shutdown()
