from multiprocessing import Process
import os,signal, time, sys, random, sysv_ipc,datetime



def Weather(temp_courant):
    while True:
        Maj_Temp=random.randint(-5,5)
        if -20<=(temp_courant.value + Maj_Temp)<=20:
            temp_courant.value=temp_courant.value+Maj_Temp

def External():
    while True: #1 == 1 ?
        i=random.randint(0,100)
        if (i==1):
            os.kill(os.getppid(), signal.SIGUSR1)

def Price(prix_courant,val_ext):
    coef_ext=[-200,-150,80,120,150,200]
    tot = 0
    for i in range (0,5):
        tot=tot+prix_courant[i]*coef_ext*val_ext[i]
    return tot
#TODO : fonction transaction 
def Transaction():
    


def receiveSignal(signalNumber, frame):
    tab_ext = list(map(lambda : random.randint(0,1),tab_ext))

def Market():
    Process(target=Weather,args=()).start()
    Quantite_energie = 0
    prix_courant = 0.14
    tab_ext = Array('i', range(10))
    ext=Process(target=External,args=())
    price(prix_courant,tab_ext,temperature,totaux)
    signal.signal(signal.SIGUSR1, receiveSignal)

def Houses():
    for i in range(NB_HOME):
        A,B = (random.randint(0,10) for x in range(0,2))
        home = Process(target=Home,args=(i,A,B,))
        home.start()
    home.join()

def Home(homeNumber,A,B):
    print("home",homeNumber,"connected")
    #defining conso and prod using random numbers
    homeConso = temperature * A
    homeProd = temperature * B

    if homeConso < homeProd:
        Surproduction(homeNumber,homeConso,homeProd)

    elif homeConso > homeProd:
        Surconsommation(homeNumber,homeConso,homeProd)

def Surproduction(homeNumber,homeConso,homeProd):
    print("Surprod", homeNumber)
    surproduction = homeProd - homeConso
    while surproduction != 0:
        #time.sleep(10)
        if HOME_QUEUE.current_messages != 0:
            message,messageType = HOME_QUEUE.receive()
        else: #TODO : GERER MARKET 
            return 
        if message != None:
            data = message.decode().split(',')
            qttDemande = int(data[1])
            if messageType == 1:
                if qttDemande < surproduction:
                    if  int(data[2].split(".")[0]) + 20 >  time.time():
                        HOME_QUEUE.send(type = 2) #ACK
                    time.sleep(21)    
                    #Waitin for answer
                    if HOME_QUEUE.current_messages != 0:
                        message,messageType = HOME_QUEUE.receive()
                    
                    
                    #newMessage,newMessageType = HOME_QUEUE.receive()
                    if newMessageType == 3:
                        surproduction = surproduction - qttDemande
        else:
            MARKET_QUEUE.send(str((homeNumber,surconsommation)).encode(),type=1)
            surproduction = 0
            #TODO : Verification du print dans le thread

def Surconsommation(homeNumber,homeConso,homeProd):
    print("Surconso", homeNumber)
    surconsommation = homeConso - homeProd
    print("surconsommation de ", surconsommation)
    HOME_QUEUE.send(str((homeNumber,surconsommation,time.time())).encode(),type=1)
    #time.sleep(20)
    if HOME_QUEUE.current_messages != 0:
        message,messageType = HOME_QUEUE.receive()
    else: #TODO : GERER MARKET 
            return 

    if messageType == 2:
        data = message.decode().split(',')
        print("home",data[0],"vend",data[1],"Kwh",homeNumber) #process vendeur, quantite
        HOME_QUEUE.send(type=3) #ACK
    else: 
        MARKET_QUEUE.send(str((homeNumber,surconsommation)).encode(),type=1)
        surconsommation = 0
        #TODO : Verification du print dans le thread.

if __name__ == '__main__':
    NB_HOME = 5
    temperature = 20
    HOME_QUEUE = sysv_ipc.MessageQueue(1000,sysv_ipc.IPC_CREAT)
    MARKET_QUEUE = sysv_ipc.MessageQueue(1100,sysv_ipc.IPC_CREAT)
    tab_ext = [0 for x in range(6)]
    # Market processing
    Process(target=Market,args=()).start() 
    Process(target=Houses,args=()).start() 
