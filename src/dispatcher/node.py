import time
import logging
import paho.mqtt.publish as publish
class Node:
    #Class constructor, generates a node instance.
    #Needs the nodeId, the maxTimeBefore considering that it's disconected, the chiefId and the MQTT settings
    def __init__(self,id = "null", seuilDisconnection = 15000, idChief = "DISP_1", broker_addressMQTT = "52.15.170.43", portMQTT = "1883", splitt = "$PyIoTCloud$", messageServer = None, periodicityNode = 5):
        
        #Declared on init
        self.nodeID = id
        self.chiefID = idChief
        self.clusterAssociated = "null"
        self.maxSilenceInterval = seuilDisconnection
        self.splitter = splitt
        self.MessageServer = messageServer
        self.periodicity = periodicityNode
        self.activeNodesClust = 0

        #MQTT params
        self.broker_address = broker_addressMQTT
        self.port = portMQTT
        
        #Iniciation constants
        self.status = 1 #1 => active, 0=> disconnected
        self.timeStamp = int(round(time.time() * 1000))
        self.SDCH = str(self.nodeID) + "DCH"
        self.leaderBool = 0 #1 => leader, 0=> not a leader
    
    # Set active nodes clust
    def setActivesNodes(self, activeNodesClust):
        self.activeNodesClust = activeNodesClust

    #Getter slave dedicated channel SDCH
    def getSDCH(self):
        return self.SDCH
    
    #Gets the last ping time done by the node
    def getTimestamp(self):
        return self.timeStamp
    
    #Gets the last ping time done by the node
    def getPeriodicity(self):
        return self.periodicity
        
    #Gets the last ping time done by the node
    def updatePeriodicity(self, period):
        self.periodicity = period
        
    #Gets the last ping time done by the node
    def getTimestamp(self):
        return self.timeStamp
    
    #Getter node id
    def getNodeID(self):
        return self.nodeID
    
    #Associate a cluster to the slave
    def setCluster(self, clustChannel, leaderBoolean):
        self.clusterAssociated = clustChannel
        self.leaderBool = leaderBoolean
        self.notifyjoinCluster()
        
    #Dissociates a cluster from the slave
    def quitCluster(self):
        self.notifyQuitCluster()
        self.clusterAssociated = "null"
        self.leaderBool = 0
        
    #Getter clusterAssociated
    def getClusterAssociated(self):
        return clusterAssociated
    
    #Getter leaderBool
    def getLeader(self):
       return self.leaderBool
       
    #Set a node as the cluster's leader and notifies it to the real node
    def setLeader(self):
       self.leaderBool = 1
       self.notifyLead()
    
    #Set a node as the cluster's no-leader and notifies it to the real node
    def setLeaderOut(self):
       self.leaderBool = 0
       self.notifyLead()

    #Set the maxSilenceInterval
    def setMaxSilenceInterval(self, maxSilenceInterval):
       self.maxSilenceInterval = maxSilenceInterval
    
    #Updates the last activity timestamp to verify his status
    def updateTimestamp(self):
       self.timeStamp = int(round(time.time() * 1000))
    
    #Getter current node status
    #if the node hasn't pinged in more than the maxSilenceInterval, it will be considerd disconnected
    def getStatus(self):
        timeNow = int(round(time.time() * 1000))
        if(timeNow - self.timeStamp) > self.maxSilenceInterval:
            self.status = 0
        else:
            self.status = 1
        return self.status
        
    #Get the real time description of the node as an string
    def __repr__(self):
        return "Board "+ self.nodeID + " located at cluster " + self.clusterAssociated + " Status " + str(self.getStatus()) + "Leader: " + str(self.leaderBool) + " Last KAM: " + str(self.timeStamp) + " periodicity " + str(self.periodicity)
    
    #Notifies the real node to become a leader
    def notifyLead(self):
        payload = self.MessageServer.produceMLM(self.clusterAssociated,self.leaderBool)
        logging.info("-----> Message Sent: [" + str(self.SDCH) + "] " + payload)
        publish.single(str(self.SDCH), payload, hostname= self.broker_address, port = int(self.port))
        
    #Notifies the real node to join a cluster
    def notifyjoinCluster(self):
        payload = self.MessageServer.produceJCM(self.clusterAssociated,self.leaderBool,self.activeNodesClust)
        logging.info("-----> Message Sent: [" + str(self.SDCH) + "] " + payload)
        publish.single(str(self.SDCH), payload, hostname= self.broker_address, port = int(self.port))
        
    #Notifies the real node to quit his current cluster
    def notifyQuitCluster(self):
        payload = self.MessageServer.produceQCM(self.clusterAssociated)
        logging.info("-----> Message Sent: [" + str(self.SDCH) + "] " + payload)
        publish.single(str(self.SDCH), payload, hostname= self.broker_address, port = int(self.port))
