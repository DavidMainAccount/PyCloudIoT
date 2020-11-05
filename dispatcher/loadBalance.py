class LoadBalancer:
    
    #Class constructor, generates a list of nodes
    def __init__(self):
        self.next = 0
        
    def roundRobin(self, numberOfClusters):
        if(numberOfClusters == 0):
            return 0
        nextOne = self.next%numberOfClusters
        self.next = self.next + 1
        return nextOne
