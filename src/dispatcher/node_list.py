import time
import logging
from node import Node
class listNodes:
    #Class constructor, generates a list of nodes
    def __init__(self):
        self.listOfNodes = []
        self.numberOfNodes = 0
    
    #Get the real time description of the list of nodes as an string
    def showList(self):
        for Node in self.listOfNodes:
            print(Node)
    
    #Searches the disconnected nodes and deletes them from either the cluster and the list of
    #sends a QCM (quit cluster message) to the node so he doesn't reconnect again after he reconnects to the network
    def checkNodes(self, listOfClusters):
        for Node in self.listOfNodes:
            if(Node.getStatus() == 0):
                self.listOfNodes.remove(Node)
                listOfClusters.deleteNode(Node)
                self.numberOfNodes = self.numberOfNodes - 1
    
    #Getter listOfNodes
    def getNodeList(self):
        return self.listOfNodes
    
    #Getter number of active nodes
    #Needs list of clusters to verify the active nodes and delete them if necessary from the clusters
    def getNumberOfNodes(self, listOfClusters):
        self.checkNodes(listOfClusters)
        return self.numberOfNodes
    
    #Adds a node to the list of nodes, also adds it to a cluster and updates the number of nodes on the list
    # 0 => Node already in, 1 => Success
    def addNode(self,idNode, chiefID,listOfClusters,MessageServer, periodicity):
        for node in self.listOfNodes:
            if(node.getNodeID() == str(idNode)):
                node.updateTimestamp()
                node.setActivesNodes(listOfClusters.getNumNodesCluster(node.getNodeID()))
                node.notifyjoinCluster()
                node.updatePeriodicity(periodicity)
                listOfClusters.addNode(node)
                return 0 #node already in
        newNode = Node(id = idNode, idChief = chiefID, messageServer = MessageServer, periodicityNode = periodicity)
        self.numberOfNodes = self.numberOfNodes + 1
        self.listOfNodes.append(newNode)
        listOfClusters.addNode(newNode)
        return 1 #Success
