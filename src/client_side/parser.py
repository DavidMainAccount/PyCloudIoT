import sys
from mqtt_functions import clientMQTT
from messageTypesServer import messageTypesServer
import paho.mqtt.publish as publish
import logging
import os

class parserStatic:
    
    def __init__(self, MessageServer, client,mqttFunctions):
        self.MessageServer = MessageServer
        self.client = client
        self.mqttFunctions = mqttFunctions
        self.broker_address="52.15.170.43"
        self.port = 1883
        
    def showFilesToProcess(self,filesToProcess):
        for archive in filesToProcess:
            print(archive)
            
    def sendLibrary(self,libName,scriptContent):
        BroadcasChannel = "BroadcastChannel"
        payload = self.MessageServer.produceLPM(libName,scriptContent)
        #print("-----> Message Sent: [" + str(BroadcasChannel) + "] " + payload)
        publish.single(str(BroadcasChannel), payload, hostname= self.broker_address, port = int(self.port))
        
    def sendFunction(self,funName,scriptContent):
        BroadcasChannel = "BroadcastChannel"
        payload = self.MessageServer.produceFSM(funName,scriptContent)
        #print("-----> Message Sent: [" + str(BroadcasChannel) + "] " + payload)
        publish.single(str(BroadcasChannel), payload, hostname= self.broker_address, port = int(self.port))
        
    def treatFile(self,fileToProcess):
        f= open(fileToProcess, 'r')
        #Search for the functions to offload, main and lib
        line_num = 0
        lookupLibraries = '#PYCLOUDIOT : LIBRARY'
        lineLib = 0
        lookupMain = '#PYCLOUDIOT : MAIN'
        lineMain = 0
        libDetails = 0
        mainDetails = 0
        for line in f.readlines():
            line_num += 1
            if line.find(lookupLibraries) >= 0:
                libDetails = line
                lineLib  = line_num
            elif line.find(lookupMain) >= 0:
                lineMain = line
                mainDetails = line
                f.close()
        self.createLibFile(fileToProcess, libDetails)
        self.createMainFile(fileToProcess,mainDetails)

    def createLibFile(self,fileToProcess, details):
        f= open(fileToProcess, 'r')
        details = details.replace('#PYCLOUDIOT : LIBRARY,','')
        tableDetails = details.split(",")
        beginingLane = tableDetails[0]
        endLane = tableDetails[1]
        nameWithNoPrefix = tableDetails[2]
        prefix = "sent/"
        name = prefix + tableDetails[2]
        line_num = 0
        logging.info("begins at " + beginingLane + " ends at " + endLane + " name " + name)
        os.remove(name)
        fileOutput = open(name,'a')
        for line in f.readlines():
            line_num += 1
            if((line_num >= int(beginingLane)) and (line_num <= int(endLane)) ):
                fileOutput.write(line)
                
        fileOutput.close()
        fileOutputRead = open(name,'r')
        scriptContent = fileOutputRead.readlines()
        print(scriptContent)
        self.sendLibrary(nameWithNoPrefix,scriptContent)
        

    def createMainFile(self,fileToProcess, details):
        
        f= open(fileToProcess, 'r')
        details = details.replace('#PYCLOUDIOT : MAIN,','')
        tableDetails = details.split(",")
        beginingLane = tableDetails[0]
        endLane = tableDetails[1]
        nameWithNoPrefix = tableDetails[2]
        name = "sent/" + tableDetails[2]
        imports = tableDetails[3]
        logging.info("begins at " + beginingLane + " ends at " + endLane + " name " + name +" imports " + imports)
        os.remove(name)
        imports = imports.replace('#IMPORTS :','')
        importTable = imports.split(';')
        fileOutput = open(name,'a')
        #import the necessary
        for importLib in importTable:
            if ".py" in importLib:
                importLib = importLib.replace('.py','')
                importLib = importLib.replace(' ','')
                fileOutput.write("from Scripts.Libraries."+ importLib + " import Fibonacci \n")
            else:
                fileOutput.write("import " + importLib + "\n")
        
        fileOutput.write("def " + nameWithNoPrefix.replace(".py","")+ "():\n")
        fileOutput.write("  " + 'print("Inside main function")\n')
        line_num = 0
        for line in f.readlines():
            line_num += 1
            if((line_num >= int(beginingLane)) and (line_num < int(endLane))):
                fileOutput.write("  " + line)
            if (line_num == int(endLane)):
                fileOutput.write("  " + "return " +  line)
                
        fileOutput.close()
        fileOutputRead = open(name,'r')
        scriptContent = fileOutputRead.readlines()
        self.sendFunction(nameWithNoPrefix,scriptContent)
