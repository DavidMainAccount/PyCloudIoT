class messageTypesServer:
	#Init method, the same for both Chiefs and slaves.
    #The only parameter is the node's id
    #You can however change the splitter
    def __init__(self, idDisp = "null", splitt = "$PyIoTCloud$", idWork = "null"):
        self.idChief = str(idDisp)
        self.splitter = str(splitt)
        self.idSlave = str(idWork)
    
    #Getter message id in function of the kind of message
    def getidMessage(self,messageName):
        idMessage = 0
        if(messageName == "KAM"):
            idMessage = 1
        elif(messageName == "JCM"):
            idMessage = 2
        elif(messageName == "QCM"):
            idMessage = 3
        elif(messageName == "MLM"):
            idMessage = 4
        elif(messageName == "LPM"):
            idMessage = 5
        elif(messageName == "FSM"):
            idMessage = 6
        elif(messageName == "CRM"):
            idMessage = 7
        elif(messageName == "FAM"):
            idMessage = 8
        return idMessage
        
    #Generates a keepalive message with the expected structure.
    #From Slave to Chief. Message type 1. Sent to the BroadcastChannel.
    #Structure: 1+splitter+idSlave+periodicity
    def produceKAM(self, periodicity):
        idMessage = 1
        return str(idMessage) + self.splitter + self.idSlave + self.splitter + str(periodicity)
    
    #Generates a join cluster message. Notifies  to  join  a  cluster.
    #From  chief  to  slave. Message type 2. Send to the slave SDCH
    #The  structure  is 2+idChief+clusterName+leaderBoolean.
    #Where clusterName is the cluster to join
    #And leaderBoolean indicates if the node is the leader (1) or if its not(0)
    def produceJCM(self,clusterName, leaderBoolean):
        idMessage = 2
        return str(idMessage) + self.splitter + self.idChief + self.splitter + str(clusterName) + self.splitter + str(leaderBoolean)
        
    #Generates a Quit  cluster  Message  (QCM). Notifies  to  quit  a  cluster.
    #From  chief  to  slave. Message type 3. Send to the slave SDCH
    #The  message’s  structure  is 3+idChief+clusterName.
    #Where clusterName is the cluster to join
    def produceQCM(self,clusterName):
        idMessage = 3
        return str(idMessage) + self.splitter + self.idChief + self.splitter + str(clusterName)
        
    #Generates a Modify  Leader  Message. Modify   his   leader   value.
    #Its   used   to   define   a   newleader   when   the   old   leader   gets   disconnected.
    #It can also be used to directly connecta channel as a leader
    #From  chief  to  slave. Message type 4. Send to the slave SDCH.
    #Them essage’s  structure  is 4+idChief+clusterName+leaderBoolean.
    def produceMLM(self,clusterName, leaderBoolean):
        idMessage = 4
        return str(idMessage) + self.splitter + self.idChief + self.splitter + str(clusterName) + self.splitter + str(leaderBoolean)
        
    #Generates a Library   Pre-fetching   Message   (LPM).
    # Indicates to memorise  a  library  that  the  chief  finds useful in the cache of the slaves.
    #From   chief   to slave’s  cluster.Message type 5. Send to the cluster CDCH
    #The message’s structure is 5+idChief+libraryName+scriptContent.
    def produceLPMList(self,libraryName, scriptContent):
        idMessage = 5
        payloadMaxSize=100
        prefix = str(idMessage) + self.splitter + str(libraryName) + self.splitter
        payloadMaxSize = 100 - len(prefix)
        payloadChunked = [scriptContent[i:i+payloadMaxSize] for i in range(0, len(scriptContent), payloadMaxSize)]
        LPMList = []
        for chunk in range(0, len(payloadChunked)):
            if(chunk == len(payloadChunked)-1):
                LPMList.append(prefix + payloadChunked[chunk] + "PYCLEND")
            else:
                LPMList.append(prefix + payloadChunked[chunk])
        return LPMList
    
    #Generates a Function  Submission  Message.
    #Transmits  a  function  to  be  executed by the nodes of the cluster.
    #From  the  chiefto  slave’s  cluster. Message type 6. Send to the cluster CDCH
    #The message’s structure is 6+idChief+functionName+scriptContent.
    def produceFSMList(self,functionName, scriptContent):
        idMessage = 6
        payloadMaxSize=100
        prefix = str(idMessage) + self.splitter + str(functionName) + self.splitter
        payloadMaxSize = 100 - len(prefix)
        payloadChunked = [scriptContent[i:i+payloadMaxSize] for i in range(0, len(scriptContent), payloadMaxSize)]
        FSMList = []
        for chunk in range(0, len(payloadChunked)):
            if(chunk == len(payloadChunked)-1):
                FSMList.append(prefix + payloadChunked[chunk] + "PYCLEND")
            else:
                FSMList.append(prefix + payloadChunked[chunk])
        return FSMList
        
    #Consensus  Result  Message  (CRM).#This function transmit theresult  of  the  execution  the
    #the  cluster’s  leader  who  will operate  the  consensus  before  giving  a  final  answer
    #to the  Chief.
    #From  slave’s  on  acluster to the cluster’s leader. Message type 7. Send to the cluster CLDCH.
    #The  message’s  structure  is7+idSlave+taskName+answer.
    def produceCRM(self,functionName, answer):
        idMessage = 7
        return str(idMessage) + self.splitter + self.idSlave + self.splitter + str(functionName) + self.splitter + str(answer)

    #Final  Answer  Message  (FAM). Used  to  answer  the  function  after  the  consensus.
    #From  cluster’s  leader  to chief. Message type 8. Send to the cluster FAM.
    #The message’s structure is 8+idSlave+functionName+answer.
    def produceFAM(self,functionName, answer):
        idMessage = 8
        return str(idMessage) + self.splitter + self.idSlave + self.splitter + str(functionName) + self.splitter + str(answer)
    
    #Modify duty-cycle Message (MDM)
    #From chief to slave.
    #Notifies to change his duty cycle to adapt to the cluster better.
    #The message's structure is 9+idChief+newDutyCycle.
    def produceMDM(self, newPeriod):
        idMessage = 9
        return str(idMessage) + self.splitter + self.idChief + self.splitter + str(newPeriod)

    #Final  Answer  Message Dispatcher (FAMD). Used  to  answer  the  function  after  the  consensus.
    #From  cluster’s  leader  to chief. Message type 8. Send to the cluster FAM.
    #The message’s structure is 8+functionName+answer.
    def produceFAMD(self,functionName, answer):
        idMessage = 10
        return str(idMessage) + self.splitter + str(functionName) + self.splitter + str(answer)
