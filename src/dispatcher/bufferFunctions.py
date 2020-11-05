from task import task
import paho.mqtt.publish as publish
import logging
from loadBalance import LoadBalancer

class bufferMethods:
    #Init method, needs the buffer list and the size.
    def __init__(self, bufferList, buffersize):
        self.buffer = bufferList
        self.size = int(buffersize)
        self.countItems = 0
        self.loadBalancer = LoadBalancer()
        self.broker_address ="52.15.170.43"
        self.port =1883

    #Adds a task to the buffer
    #needs type,functionName,scriptContent to create a new Task Object
    def addTask(self,type,functionName,scriptContent, ownerTask):
        logging.debug("Adding task to the buffer")
        if (self.countItems >= self.size):
            return "Buffer full, your task will not be executed"
        self.buffer[self.countItems] = task(type, functionName, scriptContent, ownerTask)
        self.countItems = self.countItems + 1
        return "Task added to the buffer"

    #Deletes task and library
    def taskFinished(self, taskName):
        taskPrefixToDelete = taskName.split('_main.py')[0]
        for task in self.buffer:
            print(task)
            if taskPrefixToDelete in task.getFunctionName():
                task.setDone()

    #Re-execute
    def checkRexecute(self):
        for task in self.buffer:
            if(task != None):
                if(task.reExecute() == 1):
                    task.resetExecTime()
                    task.setNotExecuting()
                    self.countItems = self.countItems + 1
                    print("task" + str(task) + "set for rexecution")
                
    #Gives the payload to send
    #needs a messageServer instance
    def getNextTask(self):
        for task in self.buffer:
            if (task.getExecuting() == 0 or task.reExecute() == 1):
                return task
        return None
    
    def executeTask(self, messageServer, clusterToSend , listOfClusters):
        if(self.countItems > 0):
            nextTask = self.getNextTask()
            print(str(nextTask) + " executing")
            if(nextTask != None):
                payload = nextTask.generatePayload(messageServer)
                nextTask.setExecuting()
                if(clusterToSend == None):
                    clusterToSend = self.loadBalancer.roundRobin(listOfClusters.getNumClusters())
                clusterDCH = "Cluster" + str(clusterToSend) + "DCH"
                for chunk in range(0, len(payload)):
                    logging.info("-----> Message Sent: [" + str(clusterDCH) + "] " + payload[chunk])
                    publish.single(str(clusterDCH), payload[chunk], hostname= self.broker_address, port = self.port)
                self.countItems = self.countItems - 1
                if(nextTask.getType() == 0):
                    self.executeTask(messageServer,clusterToSend, listOfClusters)
        
    
    #Consumes the task and returns the payload
    def consumeTask(self):
        for elementIndex in range(0, self.size-1):
            self.buffer[elementIndex] = self.buffer[elementIndex+1]
        self.buffer[(self.size-1)] = None
        self.countItems = self.countItems - 1
        return payload

    #Shows the status of the buffer
    def showBuffer(self):
        for task in self.buffer:
            if(task != None):
                print("Task type: " + str(task.getType()) + " taskName: " + str(task.getFunctionName()) + " executing: " + str(task.getExecuting()))
