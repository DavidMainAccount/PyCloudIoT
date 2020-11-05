import time
import math
import logging
from cluster import Cluster

class listClusters:
    #Class constructor, generates a list of nodes
    def __init__(self):
        self.listOfClusters = []
        self.totalCapacity = 0
        
        self.numberOf3NodeClusters = 0
        self.listOf3NodeClusters = []
        
        self.numberOf5NodeClusters = 0
        self.listOf5NodeClusters = []
        
        self.nodesInside = 0
    
    #Recalculates the capacity of the infrastructure
    def refreshCapacity(self):
        self.totalCapacity = self.numberOf3NodeClusters * 3 + self.numberOf5NodeClusters * 5
        return self.totalCapacity
    
    def getNumClusters(self):
        return self.numberOf3NodeClusters + self.numberOf5NodeClusters
    
    #Get next available id to create a cluster, recursively starts from 0 until it finds the lower
    #available number
    def getNextID(self, i):
        newID = "Cluster" + str(i)
        for clust in self.listOfClusters:
            if(clust.getClusterID() == newID):
                return self.getNextID(i+1)
        return newID
    
    #creates a 5 node cluster and adds it to the listOfClusters
    def create5NodeCluster(self):
        newCluster = Cluster(self.getNextID(0), 5)
        self.numberOf5NodeClusters = self.numberOf5NodeClusters + 1
        self.listOf5NodeClusters.append(newCluster)
        self.listOfClusters.append(newCluster)
        self.refreshCapacity()
    
    #creates a 3 node cluster and adds it to the listOfClusters
    def create3NodeCluster(self):
        newCluster = Cluster(self.getNextID(0), 3)
        self.numberOf3NodeClusters = self.numberOf3NodeClusters + 1
        self.listOf3NodeClusters.append(newCluster)
        self.refreshCapacity()
    
    #deletes a whole cluster and redistributes his nodes among the other clusters
    def deleteCluster(self,cluster):
        numberOfNodesRelocated = cluster.getNumNodesInisde()
        nodes_to_relocate = cluster.getListOfNodes()
        if(cluster.getCapacity() == 5):
            if(cluster.getCapacity() == cluster.getNodesLeft()):
                self.listOfClusters.remove(cluster)
                self.listOf5NodeClusters.remove(cluster)
                self.numberOf5NodeClusters = self.numberOf5NodeClusters - 1
            else:
                nodes_to_relocate = cluster.getListOfNodes()
                self.listOfClusters.remove(cluster)
                self.listOf5NodeClusters.remove(cluster)
                self.numberOf5NodeClusters = self.numberOf5NodeClusters - 1
        elif(cluster.getCapacity() == 3):
            if(cluster.getCapacity() == cluster.getNodesLeft()):
                self.listOfClusters.remove(cluster)
                self.listOf3NodeClusters.remove(cluster)
                self.numberOf3NodeClusters = self.numberOf3NodeClusters - 1
            else:
                nodes_to_relocate = cluster.getListOfNodes()
                self.listOfClusters.remove(cluster)
                self.listOf3NodeClusters.remove(cluster)
                self.numberOf3NodeClusters = self.numberOf3NodeClusters - 1
        for node in nodes_to_relocate:
            self.addNode(node)
        return numberOfNodesRelocated
        
    #Get the real time description of the cluster's as an string
    def showClust(self):
        for clust in self.listOfClusters:
            print(clust)
    
    #Adds a node to the first cluster with a free place
    def addNode(self, Node):
        self.refreshCapacity()
        if(self.totalCapacity>self.nodesInside and self.totalCapacity != 0):
            for clust in self.listOfClusters:
                nodeAddResult = clust.addNode(Node)
                if( nodeAddResult == 2):
                    clust.chooseLeader()
                    #print("node already in")
                    return 0
                elif (nodeAddResult == 1):
                    logging.debug("node added correctly to cluster" + clust.getClusterID())
                    self.nodesInside = self.nodesInside + 1
                    return 1
        else:
            logging.debug("Crating new cluster")
            self.create5NodeCluster()
            return self.addNode(Node)
    
    #Deletes a node from the cluster where it is
    def deleteNode(self,Node):
        for clust in self.listOfClusters:
            clust.deleteNode(Node)
            clust.chooseLeader()
            
    #gets the quantity of needed clusters to locate all the active nodes, requires from the preferred size input
    #Can be updated to combine all the permited capacities (3,5 and 7) to generate the clusters in the future
    def getNeededClusters(self, capacity):
        return math.ceil(self.nodesInside/capacity)
    
    #Gets the fastest node of a list
    def getFastestNode(self,list):
        fastests = "null"
        periodFastest = 200
        for node in list:
            if (int(node.getPeriodicity()) < int(periodFastest)):
                fastests = node
                periodFastest = int(node.getPeriodicity())
            elif (int(node.getPeriodicity()) == int(periodFastest)):
                if(int(node.getTimestamp()) < int(fastests.getTimestamp())):
                    fastests = node
                    periodFastest = int(node.getPeriodicity())
        return fastests
    
    #Gets the fastest node of a list
    def getSlowestNode(self,list):
        slowest = "null"
        periodSlowest = 0
        for node in list:
            if (int(node.getPeriodicity()) > int(periodSlowest)):
                slowest = node
                periodSlowest = int(node.getPeriodicity())
            elif (int(node.getPeriodicity()) == int(periodSlowest)):
                if(int(node.getTimestamp()) > int(slowest.getTimestamp())):
                    slowest = node
                    periodSlowest = int(node.getPeriodicity())
        return slowest
        
    #Redistributes the among on the clusters, not to be done all time, it takes both time
    # and computing resources.
    def reDistributeNodes(self):

        #Dont execute the function when there are no connected nodes.
        if(self.nodesInside==0):
            return None

        logging.debug("redistriuting function")
        clusterPreferredSize = 5
        clustersQuantity = self.getNeededClusters(clusterPreferredSize)
        logging.debug("Needed clusters: " + str(clustersQuantity))
        internalListOfNodes = []
        leaders = []
        
        for clust in self.listOfClusters:
            logging.debug("Adding cluster nodes" + str(clust))
            for Node in clust.getListOfNodes():
                self.nodesInside = self.nodesInside - 1
                internalListOfNodes.append(Node)
                Node.quitCluster()
        
        self.listOfClusters = []
        self.listOf5NodeClusters = []
        self.numberOf5NodeClusters = 0
        self.totalCapacity = 0
        self.nodesInside = 0
        
        for i in range(0, int(clustersQuantity)):
            nodeToAdd = self.getFastestNode(internalListOfNodes)
            if(nodeToAdd != "null"):
                leaders.append(nodeToAdd)
                internalListOfNodes.remove(nodeToAdd)
        
        #Añadir if para evitar el caso de que leaders esté vacio
        logging.debug("Leaders:" + str(leaders))
        
        if(self.leaders==[]):
            return None
        
        for i in range(0, int(clustersQuantity)):
            self.addNode(leaders[i])
            for j in range(0,clusterPreferredSize - 1):
                if(j%2 == 0):
                    nodeToAdd = self.getFastestNode(internalListOfNodes)
                    if(nodeToAdd != "null"):
                        self.addNode(nodeToAdd)
                        internalListOfNodes.remove(nodeToAdd)
                else:
                    nodeToAdd = self.getSlowestNode(internalListOfNodes)
                    if(nodeToAdd != "null"):
                        self.addNode(nodeToAdd)
                        internalListOfNodes.remove(nodeToAdd)
        
        
        
        
