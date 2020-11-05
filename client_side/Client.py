from ..utils.mqtt_functions import clientMQTT
from parser import parserStatic
from ..utils.messageTypesServer import messageTypesServer
import sys
import time
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the asked key as a string from the os env
# PARAMS: 
# - key: key needed (must be on the ../ennvironments/.env file)
# RETRUN: sting key demanded    
def getFromEnv(key):
    try:
        key_to_retrieve_string = os.getenv(key)
        return key_to_retrieve_string
    except Exception:
        print("Error retrieving TTN key")
        print(sys.exc_info())
        sys.exit()

def loadEnv(env_file_name):
    try:
        env_path = Path('../environment/') / env_file_name
        load_dotenv(dotenv_path=env_path)
    except Exception:
        print("Couldnt load ENV")
        print(sys.exc_info())
        sys.exit()

def on_message(client, userdata, message):
    global init_time
    received = str(message.payload.decode("utf-8"))
    #print("-----> Message arrived : [" + message.topic + "] " + received)
    end_time = time.perf_counter()
    total_time = str(end_time-start_time).replace(".",",")
    print("Total time: " + str(total_time))

#log level
#Level CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10
logging.basicConfig(level=10)

#Load env
loadEnv('.env')

#Broker MQTT settings
broker_address=getFromEnv("BROKER_ADDR")
port = 1883

#Chief Configuration
idDisp = "CLIENT_1"

#Channel configuration
CDCH = idDisp + "DCH" #Client DCH

#messageTypesServer
splitter = "$PyIoTCloud$"
MessageServer = messageTypesServer(idDisp = idDisp, splitt = splitter)

#MQTT client connection
mqttFunctions = clientMQTT(broker_address,port,idDisp)
client = mqttFunctions.clientConnect(on_message)
client = mqttFunctions.subscribeTopic(client,CDCH)
client = mqttFunctions.startLoop(client)

filesToProcess = []
index = 0
parser = parserStatic(MessageServer,client,mqttFunctions)
for arg in sys.argv:
    if(arg != "Client.py"):
        filesToProcess.append(arg)
        index = index + 1

parser.showFilesToProcess(filesToProcess)

start_time = time.perf_counter()
for archive in filesToProcess:
    parser.treatFile(archive)

#Ending the dispatcher
time.sleep(10000000) # wait
client = mqttFunctions.stopLoop(client)


