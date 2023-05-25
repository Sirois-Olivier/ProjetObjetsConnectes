import time
import datetime
from azure.iot.device import IoTHubDeviceClient, MethodResponse

CONNECTION_STRING = "HostName=iothubserre.azure-devices.net;DeviceId=deviceserre;SharedAccessKey=BDWKJV/+KR6BKaWZsIHGdThmvT/jFy5Wi91ZxSstolQ="


class ReceivedMessageManager:

    def __init__(self):
        self.messageEnCours = None
        self.client = None
        self.create_client()

    def GetMessageEnCours(self):
        return self.messageEnCours
    
    def SetMessageEnCours(self, value: tuple[bool, float, bool]):
        self.messageEnCours = value

    def create_client(self):
        # Instantiate the client
        self.client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        # Define the handler for method requests

        def method_request_handler(method_request):
            request = str(method_request.name).split(",")
            print(request[0])
            if request[0] == "Open":

                self.messageEnCours = (False, 100.0, False)

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

            elif request[0] == "Close":

                self.messageEnCours = (False, 10.0, True)

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)
            
            elif request[0] == "Manuel":

                self.messageEnCours = (False, float(request[1]), False)

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

            elif request[0] == "Automatique":

                self.messageEnCours = (True, 0.0, False)

                # Create a method response indicating the method request was resolved
                resp_status = 200
                resp_payload = {"Response": "This is the response from the device"}
                method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

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


if __name__ == "__main__":
    test = ReceivedMessageManager()
    try:
        while True:
            i = 1
    except KeyboardInterrupt:
        print("Stop")

