from multiprocessing import Process
import os,signal, time, sys, random, sysv_ipc,datetime


def Weather():
    print(temperature)

def Market():
    Process(target=Weather,args=()).start() 

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
    print("C la suproD")
    surproduction = homeProd - homeConso
    while surproduction != 0:
        time.sleep(10)
        message,messageType = HOME_QUEUE.receive()
        if message != None:
            data = message.decode().split(',')
            qttDemande = int(data[1])
            if messageType == 1:
                if qttDemande < surproduction:
                    if  datetime.strptime(data[2]) + 20 >  datetime.datetime.now():
                        HOME_QUEUE.send(type = 2) #ACK
                    time.sleep(21)    
                    #Waitin for answer
                    newMessage,newMessageType = HOME_QUEUE.receive()
                    if newMessageType == 3:
                        surproduction = surproduction - qttDemande
        else:
            MARKET_QUEUE.send(str((homeNumber,Surconsommation)).encode(),type=1)
            surproduction = 0
            #TODO : Verification du print dans le thread

def Surconsommation(homeNumber,homeConso,homeProd):
    print("Il est sur-con Welker :)")
    surconsommation = homeConso - homeProd
    print("surconsommation de ", surconsommation)
    HOME_QUEUE.send(str((homeNumber,Surconsommation,datetime.datetime.now())).encode(),type=1)
    time.sleep(20)
    message,messageType = HOME_QUEUE.receive()

    if messageType == 2:
        data = message.decode().split(',')
        print("home",data[0],"vend",data[1],"Kwh",homeNumber) #process vendeur, quantite
        HOME_QUEUE.send(type=3) #ACK
    else: 
        MARKET_QUEUE.send(str((homeNumber,Surconsommation)).encode(),type=1)
        surconsommation = 0
        #TODO : Verification du print dans le thread.

if __name__ == '__main__':
    NB_HOME = 5
    temperature = 20
    HOME_QUEUE = sysv_ipc.MessageQueue(1000,sysv_ipc.IPC_CREAT)
    MARKET_QUEUE = sysv_ipc.MessageQueue(1100,sysv_ipc.IPC_CREAT)

    # Market processing
    Process(target=Market,args=()).start() 
    Process(target=Houses,args=()).start() 
