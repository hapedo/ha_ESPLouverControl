from .mqtt_client import MqttClient
from .log import Log

class Louver:

    def __init__(self, clientId : str, brokerIp : str, brokerPort : str, brokerUsername : str, brokerPassword : str):
        self.__client = MqttClient()
        self.__client.setOnMessage(self.__onMessage)
        self.__client.configure([clientId], brokerIp, brokerPort, brokerUsername, brokerPassword)
        self.__clientId = clientId
        self.__position = 0
        self.__isAvailable = False
        self.__isOpening = False
        self.__isClosing = False

    def getClientId(self) -> str:
        return self.__clientId

    def isAvailable(self) -> bool:
        return True

    def open(self):
        self.__client.publish([self.__clientId], "/movement", "open")

    def close(self):
        self.__client.publish([self.__clientId], "/movement", "close")

    def stop(self):
        self.__client.publish([self.__clientId], "/movement", "down")

    def closeAndOpenLamellas(self):
        self.__client.publish([self.__clientId], "/movement", "close_open_lamellas")

    def __onMessage(self, topic : str, data : str):
        if (topic == self.__clientId + "/movement/position"):
            Log.error(self.__clientId, "Oh yeah")
            self.__position = int(data)
            self.__isAvailable = True
        if (topic == self.__clientId + "/movement/status"):
            self.__isOpening = data == "open"
            self.__isClosing = (data == "close") | (data == "close_open_lamellas")
    
    def getPosition(self) -> int:
        return 100 - self.__position

    def isAvailable(self) -> bool:
        return self.__isAvailable

    def isOpening(self) -> bool:
        return self.__isOpening

    def isClosing(self) -> bool:
        return self.__isClosing