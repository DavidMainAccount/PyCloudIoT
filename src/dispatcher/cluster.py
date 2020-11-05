import time
import logging
class Cluster:
    #Class constructor, generates a cluster instance.
    #needs the cluster ID and the capacity
    def __init__(self, clustID, capacit):
        self.capacity = capacit
        self.clusterID = clustID
        self.nodesInside = 0 #number of active nodes inside
        self.listOfNodes = []
        self.status = 1 #1 => not full; 0 => full
        self.activeLeader = 0 #0 => no leader, 1 => leader
        self.leaderId = "null"
    
    #Getter ClusterID
    def getClusterID(self):
        return self.clusterID
    
    #Getter Cluster Dedicated Chanel
    def getCDCH(self):
        return self.clusterID + "DCH"
    
    #Getter Cluster Leader Dedicated Channel
    def getCLDCH(self):
        return self.clusterID + "DCHLeader"
    
    #Getter leader status
    #0 => no leader, 1 => leader
    def getLeaderActive(self):
        return self.activeLeader
    
    #Getter list of nodes in the cluster
    def getListOfNodes(self):
        return self.listOfNodes
    
    #Getter the places left in the cluster
    def getNodesLeft(self):
        return self.capacity - self.nodesInside
    
    #Getter the places in the cluster
    def getCapacity(self):
        return self.capacity
    
    #Getter cluster occupacy status
    #1 => not full; 0 => full
    def getStatus(self):
        return self.status
    
    #Get current leader
    def getOldLeader(self):
        for node in self.listOfNodes:
            if(str(node.getLeader()) == str(1)):
                return node
    
    #Getter the number of active nodes in the cluster
    def getNumNodesInisde(self):
        return self.nodesInside
        
    #If there's enough place in the cluster adds the node, otherwise refuses to add it. Changes the counter of nodes inside of the cluster and the occupacy status.
    #Requires from a node as an imput
    #Returns: 1 Success, 0 Error, 2 Node inside
    def addNode(self, Node):
        if (self.nodesInside < self.capacity):
            for nodeInList in self.listOfNodes:
                if(nodeInList.getNodeID() == Node.getNodeID()):
                    logging.debug("node already inside")
                    return 2
            self.listOfNodes.append(Node)
            self.nodesInside = self.nodesInside + 1
            Node.setCluster(self.clusterID,0)
            self.chooseLeader()
            if (self.nodesInside == self.capacity):
                self.status = 0
            return 1
        else:
            for nodeInList in self.listOfNodes:
                if(nodeInList.getNodeID() == Node.getNodeID()):
                    logging.debug("node already inside")
                    return 2
            logging.debug("Cluster Full")
            return 0
    
    #Deletes a node from the cluster list
    #Searchs if the node is inside the cluster and deletes it if it is
    #Returns 1 if it succeded and 0 if there was an error
    def deleteNode(self, Node):
        if(self.nodesInside > 0):
            for node in self.listOfNodes:
                if(node.getNodeID() == Node.getNodeID()):
                    if(node.getLeader() == 1):
                        self.leaderId = "null"
                        self.activeLeader = 0
                    node.quitCluster()
                    self.listOfNodes.remove(node)
                    self.status = 1
                    self.nodesInside = self.nodesInside - 1
                    return 1
            return 0

    #Change the capacity of the cluster
    def updateCapacity(self, newCap):
        self.capacity = newCap
    
    #Get the node with the smaller periodicity
    def getFastestNode(self):
        fastests = "null"
        periodFastest = 200
        for node in self.listOfNodes:
            if (int(node.getPeriodicity()) < int(periodFastest)):
                fastests = node
                periodFastest = int(node.getPeriodicity())
        return fastests
    
    #If the cluster has no leader chooses a new leader and sends the notification to the node.
    #Takes the fastest node in the cluster
    def chooseLeader(self):
        if(self.getNodesLeft()==self.getCapacity()):
            return None
        leader_node = self.getFastestNode()
        if(int(self.activeLeader) == int(1)):
            ancient_leader = self.getOldLeader()
            if(ancient_leader.getNodeID() == leader_node.getNodeID()):
                #print("The node was already leader") #debug
                 leader_node = ancient_leader
            else:
                self.leaderId = str(leader_node.getNodeID())
                leader_node.setLeader()
                self.activeLeader = 1
                ancient_leader.setLeaderOut()
        else:
            self.leaderId = str(leader_node.getNodeID())
            leader_node.setLeader()
            self.activeLeader = 1
        
    #Get the real time description of the cluster as an string
    def __repr__(self):
        stringRet = ("Cluster "+ self.clusterID + " Capacity: " + str(self.nodesInside) + "/" + str(self.capacity)+ " Status: " + str(self.getStatus()) +" Active Leader: " + str(self.activeLeader) +"\nNodes inside: \n")
        i = 1
        for node in self.listOfNodes:
            stringRet = stringRet + "\t" + str(i) + "/" + str(self.capacity) +" Board "+ node.getNodeID() + " Last_KAM " + str(node.getTimestamp()) + " periodicity " + str(node.getPeriodicity())
            if node.getLeader() == 1 :
                stringRet = stringRet + " ******* LEAD"
            stringRet = stringRet + "\n"
            i = i + 1
        return stringRet
