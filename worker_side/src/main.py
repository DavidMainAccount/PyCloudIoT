import time
import os
import network
import time
from Libraries.mqttNew import MQTTClient
from Libraries.messageTypesServer import messageTypesServer

#####################################################################
# Global variables for the execution and configuration of the node: #
#####################################################################

#initializes the wifi connection parametters
ssid = "david"
password = "david333"

#Arduino Identification parameter
idArd = "ARD1"

#MQTT Server Connection parameters
mqtt_server = '52.15.170.43'
port = 1883

#Iniciation constants
status = 1 #1 => active, 0=> disconnected
wdch = "ARD1DCH"
leader_bool = 0 #1 => leader, 0=> not a leader
broadcast_chan = "BroadcastChannel"
cluster_id = "null"
clust_chan = "null"
clust_lead_chan = "null"
chief_id = "null"

#messageTypesServer
splitter = "$PyIoTCloud$"
MessageServer = messageTypesServer(idWork = idArd, splitt = splitter)

#Cluster Settings
splitter = "$PyIoTCloud$"
duty_cycle = 3 #seconds before checking the mqtt for new messages

#Cache results of functions (To implement)
last_results = []

#########################################
# The program functions are under here: #
#########################################
#Function showing the status of the node to debug
def showStatus():
    print("######################")
    print("Worker dedicated channel: " + wdch)
    print("Broadcast channel: " + broadcast_chan)
    print("Cluster subscribed topic: " + clust_chan)
    print("Leader: " + str(leader_bool))
    print("Cluster leader subscribed topic: " + clust_lead_chan)
    print("######################")

#connexion function WIFI, parameters ssid and password of the network TO DO: multi ip later, cath error connecting to avoid the crash
def do_connect(name, psw):
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(name,psw)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

#Function to join a cluster and change the status of leader or not
def joinCluster(new_cluster_id):
    global cluster_id,clust_chan,clust_lead_chan,leader_bool
    cluster_id = str(new_cluster_id)
    clust_chan = str(new_cluster_id) + "DCH"
    print("joining cluster: " + clust_chan)
    client.subscribe(str(clust_chan))

    if(str(leader_bool) == "1"):
        clust_lead_chan = str(new_cluster_id) + "DCHLeader"
        print("joining cluster: " + clust_lead_chan)
        leader_bool = 1
        client.subscribe(str(clust_lead_chan))

#Function to quit a cluster
def quitCluster():
    global cluster_id,clust_chan,clust_lead_chan,leader_bool

    client.unsubscribe(str(clust_chan))
    print("Leaving cluster: " + clust_chan)
    cluster_id = "null"
    clust_chan = "null"

    if(str(leader_bool) == "1"):
        print("Leaving cluster: " + clust_lead_chan)
        client.unsubscribe(str(clust_lead_chan))
        topic_cluster = "null"
        leader_bool = 0

#Keepalive message
def sendKeepalive():
    global MessageServer, duty_cycle, broadcast_chan
    payload = MessageServer.produceKAM(duty_cycle)
    print("-----> Message Sent: [" + str(broadcast_chan) + "] " + payload)
    pub_id = client.publish(str(broadcast_chan), payload, False)

#Set the callback method which is fired when a publish command succeeds.
def unsub_cb(msg_id):
  print('UNSUB ID = %r success' % msg_id)

#Set the callback method which is fired when a publish command succeeds.
def puback_cb(msg_id):
  print('PUBACK ID = %r success' % msg_id)

#Set the callback method which is fired when a subscribe command succeeds.
def suback_cb(msg_id, qos):
  print('SUBACK ID = %r, Accepted QOS = %r' % (msg_id, qos))

#Function runned on connection to the mqtt server 
def con_cb(connected):
    if connected:
        global wdch
        client.subscribe(str(wdch))
    else: 
        #unscubscribe and erease cluster information
        print("MQTT server unjoineable")

#Function runned on message reception from the mqtt server 
def msg_cb(topic, msg):
    global wdch, splitter, chief_id, leader_bool,cluster_id,MessageServer
    print((topic, msg))

    if(topic.decode("utf-8")== str(wdch)):
        messageSplitted = msg.decode("utf-8").split(splitter)
        if(str(messageSplitted[0]) == str(MessageServer.getidMessage("JCM"))):
            chief_id = str(messageSplitted[1])
            new_cluster = str(messageSplitted[2])
            leader_bool = str(messageSplitted[3])
            joinCluster(new_cluster)
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("QCM"))):
            chief_id = str(messageSplitted[1])
            quitCluster()
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("MLM"))):
            if(cluster_id != "null"):
                quitCluster()
            chief_id =str(messageSplitted[1])
            cluster_id = str(messageSplitted[2])
            leader_bool = str(messageSplitted[3])
            joinCluster(cluster_id)
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("MDM"))):
            chief_id  =str(messageSplitted[1])
            duty_cycle = int(messageSplitted[2])
    elif(topic.decode("utf-8")== str(clust_chan)):
        messageSplitted = msg.decode("utf-8").split(splitter)
        if(str(messageSplitted[0]) == str(MessageServer.getidMessage("LPM"))):
            library_name = str(messageSplitted[1])
            library_script =str(messageSplitted[2])
            saveLibrary(library_name,library_script)
        elif(str(messageSplitted[0]) == str(MessageServer.getidMessage("FSM"))):
            function_name = str(messageSplitted[1])
            function_script =str(messageSplitted[2])
            saveScript(function_name,function_script)
            #executeFunction(function_name,function_script)
    if(topic.decode("utf-8") == str(clust_lead_chan)):
        messageSplitted = msg.decode("utf-8").split(splitter)
        if((str(leader_bool) == str(1)) and (str(messageSplitted[0]) == str(MessageServer.getidMessage("CRM")))):
            idAnswer =str(messageSplitted[1])
            functionName = str(messageSplitted[2]).replace(".py","")
            answer = str(messageSplitted[3])
            addAnswerForConsensus(answer, idAnswer, functionName)

#store function to execute
def saveScript(function_name,function_script):
    print('Stocking script chunk: '+ function_name)
    #Writes the script chunk file
    try:
        filename = "/Scripts/" + str(function_name)
        f = open(filename, "a+")
        content_splitted = function_script.split("', ")
        for line in content_splitted:
            line = line.replace("['", "")
            line = line.replace("']", "")
            line = line.replace("'", "")
            line = line.replace("\\n", "\n")
            line = line.replace("\\n", "\n")
            line = line.replace("PYCLEND", "")
            f.write(line)
        f.close()
    except Exception as e: 
        print(e)
    print('Script chunk saved')
    if("PYCLEND" in function_script):
        print('Script saved, all chunks arrived')
        f = open(filename, "a+")
        f.write("\nres="+function_name.replace(".py","")+"() \n")
        f.write('f= open("Results/result'+str(function_name.replace(".py",""))+'.txt","w")\n')
        f.write('f.write(str(res))\n')
        f.write("f.close()")    
        f.close()
        runScript(filename,str(function_name.replace(".py","")))

#manque ajouter la politique de consensus et effacer les fichiers après envoyer la réponse
def runScript(filename,scriptName):
    global leader_bool,last_results
    print("Running script " + scriptName)
    execfile(filename)
    f = open('Results/result'+str(scriptName.replace(".py",""))+'.txt')
    finalResult = f.read()
    f.close()
    if(leader_bool == 1):
        addMyAnswer(scriptName,finalResult)
        os.remove(filename)
        for fxx in os.listdir("/Scripts/Libraries"):
            os.remove("/Scripts/Libraries/"+fxx)
    else:
        sendResultForConsensus(scriptName,finalResult)
        os.remove(filename)
        

#store library associated to the script
def saveLibrary(library_name,library_content):
    print('Stocking library: '+ library_name)
    #Writes the library file
    try:
        filename = "/Scripts/Libraries/" + str(library_name)
        f = open(filename, "a+")
        content_splitted = library_content.split("', ")
        for line in content_splitted:
            line = line.replace("['", "")
            line = line.replace("']", "")
            line = line.replace("'", "")
            line = line.replace("\\n", "\n")
            line = line.replace("\\n", "\n")
            line = line.replace("PYCLEND", "")
            f.write(line)
        f.close()
    except Exception as e: 
        print(e)
    print('Library chunk saved')
    if("PYCLEND" in library_content):
        print('Library saved, all chunks arrived')

#Adds the leader's answer to the last_result
def addMyAnswer(taksname, result):
    global last_results
    print("Adding answer to the cache")
    time_task =  int(round(time.time() * 1000))
    current_result = {'taskname': str(taksname), 'values': [str(result)],'time': time_task}
    last_results.append(current_result)
    print("Answer added to the cache")

#Sends the result to the cluster manager before the task consensus
def sendResultForConsensus(functionName,result):
    global clust_chan, clust_lead_chan, MessageServer
    leaderTopic = clustChan+"Leader"
    print("Sending result for consensus to the " + str(clust_lead_chan))
    payload = MessageServer.produceCRM(functionName,result)
    pub_id = client.publish(str(clust_lead_chan), payload, False)
    print("-----> Message Sent: [" + str(clust_lead_chan) + "] " + payload)

#Creates a new task and offloads it to the last_results array
def createNewTask(taskname, result, time):
    global last_results
    print("Creating new task result entry")
    newTaskResult = {}
    newTaskResult["taskname"] = taskname
    newTaskResult["values"] = [str(result)]
    newTaskResult["time"] = time
    last_results.append(newTaskResult)

#Treates a FAM message and adds it to the last_results table
def addAnswerForConsensus(answer, idArdSender, task_name):
    global last_results
    print("Received answer: " + str(answer) + " from: " +str(idArdSender))
    for i in range(0, len(last_results)):
        if(last_results[i]["taskname"]==task_name):
            last_results[i]["values"].append(answer)
            return 1
    createNewTask(task_name, answer, "null")

def consensusSimple(listAnswers):
    count = 0
    correctAnswer = "null"
    for i in range(0,len(listAnswers)):
        count = 0
        for j in range(0,len(listAnswers)):
            if(str(listAnswers[j]) == str(listAnswers[i])):
                count = count + 1
        if(count >= 2):
            correctAnswer = listAnswers[i]
            return correctAnswer
    return listAnswers[0]

#Funtion Scanning the latest results and sending the result after a time threshold
def checkToSend():
    print("Checking valid answers")
    global last_results,idArd
    Broadcast_sub = "BroadcastChannel"
    for i in range(0, len(last_results)):
        time_now = int(round(time.time() * 1000))
        time_before = last_results[i]["time"]
        resultTime = time_now - int(time_before)
        if(resultTime > 9000 or len(last_results[i]["values"]) >= 2):
            print("Making consensus for function " + last_results[i]["taskname"])
            print(last_results[i])
            listAnswers = last_results[i]["values"]
            ans = consensusSimple(listAnswers)
            messageToSend = "8" + splitter + idArd + splitter + last_results[i]["taskname"] + splitter + ans
            print("Answer sent:" + str(messageToSend))
            pub_id = client.publish(str(Broadcast_sub), messageToSend, False)
            del last_results[i]

#Execute function
def executeFunction(functionName,functionScript):
	try:
		writeFunctionScript(functionName,functionScript)
		runScript(functionName)
	except Exception as e: 
		print(e)
	print("Script executed" + functionName)

#Function used to Connect to the server and to subscribe to a topic on the same time, parameters the client id, mqtt server ip and the topic subscribed
def connect_and_configure(client_id, mqtt_ip):
    global port

    client = MQTTClient(mqtt_ip, port)
    #Callback definitions
    client.set_connected_callback(con_cb)
    client.set_puback_callback(puback_cb) 
    client.set_suback_callback(suback_cb) 
    client.set_message_callback(msg_cb) 
    client.set_unsuback_callback(unsub_cb)

    client.connect(client_id) #Connect the MQTT client to the broker. 
    print('Connected to %s MQTT broker, subscribed to %s topic as %s' % (mqtt_server, wdch, client_id))
    return client

#Function to retry to connect to the server
def restart_and_reconnect(client_id, mqtt_ip):
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(1)
    connect_and_configure(client_id, mqtt_ip)


##################################
# The program starts under here: #
##################################

#initializes the wifi interfaces and connects 
sta_if = network.WLAN(network.STA_IF) 
ap_if = network.WLAN(network.AP_IF)
do_connect(ssid, password)

#Initializes the connection with the mqtt server
try:
  client = connect_and_configure(idArd,mqtt_server)
except OSError as e:
  restart_and_reconnect(idArd,mqtt_server)

###################################################################
# Loop code goes inside the loop here, this is called repeatedly: #
###################################################################
i = 1
while True:
    i = i + 1
    if client.isconnected():
        sendKeepalive()
        checkToSend()
        if (i % 10 == 0):
            showStatus()
            

    time.sleep(duty_cycle) # Delay for 1 second. (no bajar de ahi!!!!!!)



