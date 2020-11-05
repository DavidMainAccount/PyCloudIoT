# -*- coding: utf-8 -*-
import time
import logging
from ..utils.messageTypesServer import messageTypesServer
from bufferFunctions import bufferMethods
import paho.mqtt.publish as publish
from ..utils.mqtt_functions import clientMQTT
from node_list import listNodes
from clust_list import listClusters
import os
from dotenv import load_dotenv
from pathlib import Path

def loadEnv(env_file_name):
    try:
        env_path = Path('../environment/') / env_file_name
        load_dotenv(dotenv_path=env_path)
    except Exception:
        print("Couldnt load ENV")
        print(sys.exc_info())
        sys.exit()

#Analyses an incomming message and makes the actions.
def on_message(client, userdata, message):
    global buffer
    received = str(message.payload.decode("utf-8"))
    logging.info("-----> Message arrived : [" + message.topic + "] " + received)
    if(str(message.topic) == str(Broadcast_sub)):
        messageSplitted = received.split("$PyIoTCloud$")
        logging.debug(messageSplitted[0])
        if(str(messageSplitted[0]) == str(MessageServer.getidMessage("KAM"))):
            listOfNodes.addNode(messageSplitted[1], idDisp, listOfClusters, MessageServer,messageSplitted[2])
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("FAM"))):
            client_ch = "CLIENT_1DCH"
            idSlave =str(messageSplitted[1])
            functionName = str(messageSplitted[2])
            answer =str(messageSplitted[3])
            payload = MessageServer.produceFAMD(functionName,answer)
            logging.info("-----> Message Sent: [" + str(client_ch) + "] " + payload)
            publish.single(str(client_ch), payload, hostname= broker_address, port = int(port))
            print("trying to delete the fcking tasks")
            buffer.taskFinished(functionName)
            #function to set the annswer to done and delete the task
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("LPM"))):
            logging.debug("New Library incomming")
            clientName =str(messageSplitted[1])
            libraryName = str(messageSplitted[2])
            libraryScript =str(messageSplitted[3])
            buffer.addTask(0, libraryName, libraryScript, clientName)
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("FSM"))):
            logging.debug("New task incomming")
            clientName = str(messageSplitted[1])
            functionName = str(messageSplitted[2])
            functionScript = str(messageSplitted[3])
            buffer.addTask(1, functionName, functionScript, clientName)
    
#log level
#Level CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
logging.basicConfig(level=20)


#Load env
loadEnv('.env')

#Broker MQTT settings
broker_address=getFromEnv("BROKER_ADDR")
port = 1883

#Chief Configuration
idDisp = "DISP_1"

#Channel configuration
Broadcast_sub = "BroadcastChannel"

#Tracking arrays
listOfNodes = listNodes()#list of the nodes that have been connected to the MQTT Server
listOfClusters = listClusters() #list of available clusters and clusters Topics
#listOfClients = [] #list of clients having requested something

#messageTypesServer
splitter = "$PyIoTCloud$"
MessageServer = messageTypesServer(idDisp = idDisp, splitt = splitter)

#Linear buffer initiation
bufferList = [None] * 10
buffer = bufferMethods(bufferList, int(len(bufferList)))

#MQTT client connection
mqttFunctions = clientMQTT(broker_address,port,idDisp)
client = mqttFunctions.clientConnect(on_message)
client = mqttFunctions.subscribeTopic(client,Broadcast_sub)
client = mqttFunctions.startLoop(client)

i = 0
while(1):
    i = i + 1
    if(i % 150 == 0):
        print("****************************")
        logging.debug(i)
        print("****************************")
        print("---------Nodes--------")
        listOfNodes.checkNodes(listOfClusters)
        listOfNodes.showList()
        print("\n-------Clusters------- ")
        listOfClusters.showClust()
    
    if(i == 1500):
        print("Redistributing nodes")
        listOfClusters.reDistributeNodes()
        i = 0
        
    
    if(i % 150 == 0):
        print("\n-------Buffer------- ")
        buffer.checkRexecute()
        buffer.showBuffer()
    
    if(i % 20 == 0):
        buffer.executeTask(MessageServer,None,listOfClusters)
    time.sleep(0.1)

#Ending the dispatcher
time.sleep(10000000) # wait
client = mqttFunctions.stopLoop(client)
