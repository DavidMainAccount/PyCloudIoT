import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.publish as publish

class clientMQTT:
    #Class constructor, generates a clientMQTT
    #needs the mqtt parametters and the node's id
    def __init__(self, broker_address, port, clientID = "null"):
        self.broker_addressMQTT = broker_address
        self.portMQTT = port
        self.clientMQTTID = clientID
    
    #Connects to the MQTT broker and returns the client instance
    #Adds the on_message callback
    def clientConnect(self,on_message):
        print("--------------------------------------------")
        print("Creating Dispatcher Connection")
        client = mqtt.Client(self.clientMQTTID)
        client.on_message=on_message
        print("Connecting to broker")
        client.connect(self.broker_addressMQTT, self.portMQTT)
        return client
    
    #Subscribe to a topic, needs the client and the topic to subscribe
    def subscribeTopic(self,client,topicToSubscribe):
        print("Subscribing to topic " + topicToSubscribe)
        client.subscribe(topicToSubscribe)
        return client
    
    #Subscribe to a topic, needs the client and the topic to subscribe
    def unsubscribeTopic(self,client,topicToSubscribe):
        print("Unsubscribing topic " + topicToSubscribe)
        client.unsubscribe(topicToSubscribe)
        return client
        
    #Starts client loop, needs a client
    def startLoop(self,client):
        client.loop_start()
        return client
    
    #Stops client loop, needs a client
    def stopLoop(self,client):
        client.loop_stop()
        return client
    
