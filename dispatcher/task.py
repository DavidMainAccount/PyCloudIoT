import time
class task:
    #Init method, needs the buffer list and the size.
    #type 0 => library
    #type 1 => script
    def __init__(self, typeTask, functionNameTask, scriptContentTask, ownerTask):
        self.type = typeTask
        self.functionName = str(functionNameTask)
        self.scriptContent = str(scriptContentTask)
        self.owner = ownerTask
        self.executing = 0
        self.done = 0
        self.executingTime = None
    
    #gets if the task have taken a lot of time
    def reExecute(self):
        if (self.executingTime != None):
            newTime = int(round(time.time() * 1000))
            result = newTime - self.executingTime
            if(result > 50000):
                return 1
        return 0
    
    def resetExecTime(self):
        self.executingTime = None
        
    #setter Executing time
    def setExecutingTime(self):
        self.executingTime = int(round(time.time() * 1000))
        
    #getter executing
    def getExecuting(self):
        return self.executing
        
    #getter done
    def getDone(self):
        return self.done
        
    #setter done
    def setDone(self):
        self.done = 1
    
    #setter executing
    def setExecuting(self):
        self.executing = 1
        self.setExecutingTime()
        
    #setter not executing
    def setNotExecuting(self):
        self.executing = 0
        
    #getter type
    def getType(self):
        return self.type
    
    #getter functionName
    def getFunctionName(self):
        return self.functionName
        
    #getter scriptContent
    def getSciptContents(self):
        return self.scriptContent
    
    #Checks the type of the function and generates the payload to be sent
    def generatePayload(self,messageServer):
        if(self.type == 0):
            return messageServer.produceLPMList(self.functionName, self.scriptContent)
        else:
            return messageServer.produceFSMList(self.functionName, self.scriptContent)
            
            
