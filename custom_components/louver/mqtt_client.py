from paho.mqtt import client as mqttClient
import random
import time, threading
from .log import Log
from typing import List

class MqttClient:

    def __init__(self):
        self.__broker = "localhost"
        self.__username = ""
        self.__password = ""
        self.__port = 1883
        self.__clientId = f'python-mqtt-{random.randint(0, 1000)}'
        self.__louverClientIdList = []
        self.__client = mqttClient.Client(self.__clientId)
        self.__client.on_connect = self.__onConnect
        self.__client.on_disconnect = self.__onDisconnect
        self.__client.on_message = self.__onMessage
        self.__timer = None
        self.__onMessageCallback = None

    def configure(self, louverClientIdList : List[str], brokerIp : str, brokerPort : int = 1883, username : str = "", password : str = ""):
        if (self.__client.is_connected()):
            Log.info("MQTT", "Disconnecting from broker, host=\"{}:{}\"".format(self.__broker, self.__port))
            self.__client.disconnect()
        self.__louverClientIdList = louverClientIdList
        self.__broker = brokerIp
        self.__port = brokerPort
        self.__username = username
        self.__password = password
        self.__timer = threading.Timer(30, self.__periodicConnect).start()
        self.__periodicConnect()
        Log.error("MQTT", "Configured, clientId={}, broker=\"{}\", port={}, username=\"{}\", password=\"*\"".format(self.__clientId, self.__broker, self.__port, self.__username))

    def setOnMessage(self, onMessageCallback : callable):
        self.__onMessageCallback = onMessageCallback

    def publish(self, clientList : List[str], topic : str, value : str):
        if (not self.__client.is_connected()):
            Log.error("MQTT", "Error publishing topic \"{}\"=\"{}\" (not connected)".format(topic, value))
        for client in clientList:
            Log.info("MQTT", "Trying to publish topic \"{}{}\"=\"{}\"".format(client, topic, value))
            info = self.__client.publish(client + topic, value)
            info.wait_for_publish(3000)
            if (info.rc != 0):
                Log.error("MQTT", "Unable to publish topic \"{}{}\"=\"{}\"".format(client, topic, value))

    def __onConnect(self, client, userData, flags, result):
        if (result == 0):
            Log.info("MQTT", "Connected to broker")
        else:
            Log.error("MQTT", "Failed to connect, result={}, username=\"{}\"".format(result, self.__username))
        topics = []
        for clientId in self.__louverClientIdList:
            topics.append((clientId + "/#", 0))
        Log.debug("MQTT", "Subscribing following topics: {}".format(topics))
        for topic in topics:
            self.__client.subscribe(topic)

    def __onDisconnect(self,client, userdata, result):
        if (result == 0):
            Log.info("MQTT", "Disconnected from broker")
        else:
            Log.error("MQTT", "Disconnected from broker, result={}".format(result))

    def __onMessage(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        Log.info("MQTT", "Message received, topic {}: data: {}".format(msg.topic, payload))
        if (callable(self.__onMessageCallback)):
            self.__onMessageCallback(msg.topic, payload)

    def __periodicConnect(self):
        if (not self.__client.is_connected()):
            self.__client.username_pw_set(self.__username, self.__password)
            Log.info("MQTT", "Trying to connect to broker, host=\"{}:{}\"".format(self.__broker, self.__port))
            self.__client.connect_async(self.__broker, self.__port)
            self.__client.loop_start()
        
if __name__ == "__main__":
    Log.configure("koupelna")
    client = MqttClient()
    louvers = []
    louvers.append("koupelna")
    client.configure(louvers, "192.168.0.207", 1883, "louver", "louverpass")
    while(True):
        pass