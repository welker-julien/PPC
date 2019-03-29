from multiprocessing import Process,Value,Array
import os,signal, time, sys, random, sysv_ipc,datetime,threading



def Weather():
    # while True:
        Maj_Temp=random.randint(-5,5)
        if -20<=(temperature.value + Maj_Temp)<=20:
            temperature.value=temperature.value+Maj_Temp
            time.sleep(1)

def transaction(lock,semaphore_thread):
	message,messageType = MARKET_QUEUE.receive()
	data = message.decode().split(',')
	global Quantite_energie
	#print(data)
	qtt=data[1]
	homeNum=data[0]
	if ')'in data[0] or '(' in data[0]:
		print("modif taille")
		qttlen=len(qtt)-1
	else:
		qttlen=len(qtt)
	print("taille",qttlen)
	qttDemande = int(qtt[0:qttlen])
	#print(homeNum," ",qttDemande)
	#homeNumber = int(data[0])
	if messageType==2:#on vend aux maison
		with lock:
			Quantite_energie=Quantite_energie-qttDemande

		print(qttDemande," vendue a : ",homeNum)
	if messageType==1:#on achete le surplus des maison
		with lock:
			Quantite_energie=Quantite_energie+qttDemande

		print(qttDemande," achete a : ",homeNum)
	print("quantité d'energie ayant transité par market",Quantite_energie)
	semaphore_thread.release()


def External():
    while True: #1 == 1 ?
        i=random.randint(0,100)
        if (i==1):
            os.kill(os.getppid(), signal.SIGUSR1)

def Price(prix_courant,val_ext):
    coef_ext=[-200,-150,80,120,150,200]
    tot = 0
    for i in range (0,5):
        tot=tot+prix_courant*coef_ext[i]*val_ext[i]
    return tot
#TODO : fonction transaction

def receiveSignal(signalNumber, frame):
    tab_ext = list(map(lambda : random.randint(0,1),tab_ext))

def Market():
    Process(target=Weather,args=()).start()
    lock=threading.Lock()
    semaphore_thread=threading.Semaphore(3)
    prix_courant = 0.14
    tab_ext = Array('i', range(10))
    ext=Process(target=External,args=())
    while True:
        semaphore_thread.acquire()
        trans=threading.Thread(target=transaction,args=(lock,semaphore_thread))
        trans.start()
        prix_courant=Price(prix_courant,tab_ext)
        signal.signal(signal.SIGUSR1, receiveSignal)

def Houses():
    for i in range(NB_HOME):
        A,B = (random.randint(-10,10) for x in range(0,2))
        home = Process(target=Home,args=(i,A,B,))
        home.start()
    home.join()

def Home(homeNumber,A,B):
    print("home",homeNumber,"connected")
    #defining conso and prod using random numbers
    while True:
        time.sleep(1)
        homeConso = temperature.value * A
        homeProd = temperature.value * B

        if homeConso < homeProd:
            Surproduction(homeNumber,homeConso,homeProd)

        elif homeConso > homeProd:
            Surconsommation(homeNumber,homeConso,homeProd)

def Surproduction(homeNumber,homeConso,homeProd):
    print("Surprod", homeNumber)
    surproduction = int(homeProd - homeConso)
    print("surproduction de ", surproduction," par ",homeNumber)
    while surproduction != 0:
        print("A")
        # time.sleep(10)
        if HOME_QUEUE.current_messages != 0:
            print("B")
            message,messageType = HOME_QUEUE.receive()
        else:
            print ("surprod vendue MARKET")
            MARKET_QUEUE.send(str((homeNumber,surproduction)).encode(),type=1)
            surproduction = 0
            #TODO : Verification du print dans le thread

        if message != None:
            print("C")
            data = message.decode().split(',')
            qttDemande = int(data[1])
            if messageType == 1:
                print("D")
                if qttDemande < surproduction:
                    print("E")
                    if  int(data[2].split(".")[0]) + 20 >  time.time():
                        print("F")
                        message=str(homeNumber)+","+str(qttDemande)
                        HOME_QUEUE.send(message.encode(),type = 2) #ACK
                        time.sleep(3)
                    if HOME_QUEUE.current_messages != 0:
                        message,messageType = HOME_QUEUE.receive()
                        print("G")
                        print (messageType)
                        if messageType == 3:
                            surproduction = int(surproduction - qttDemande)
                            print("sell")

        else:
            valeurs=str(homeNumber)+','+str(surproduction)
            MARKET_QUEUE.send(valeurs.encode(),type=1)
            surproduction = 0

def Surconsommation(homeNumber,homeConso,homeProd):
    print("Surconso", homeNumber)
    surconsommation = int(homeConso - homeProd)
    print("surconsommation de ", surconsommation," par ",homeNumber)
    while surconsommation !=0:
        HOME_QUEUE.send(str((homeNumber,surconsommation,time.time())).encode(),type=1)
        time.sleep(5) #ne pas toucher!
        if HOME_QUEUE.current_messages != 0:
            print("conso 1")
            message,messageType = HOME_QUEUE.receive()
        else: #TODO : GERER MARKET
                pass

        if messageType == 2:
            print("conso 1")
            data = message.decode().split(',')
            print (data)
            print("home",data[0],"vend",data[1],"Kwh à",homeNumber) #process vendeur, quantite
            HOME_QUEUE.send("",type=3) #ACK
        else:
            valeurs= str(homeNumber)+','+str(surconsommation)
            MARKET_QUEUE.send(valeurs.encode(),type=2)
            surconsommation = 0

if __name__ == '__main__':
    NB_HOME = 2
    Quantite_energie = 0
    temperature = Value('d',20)
    HOME_QUEUE = sysv_ipc.MessageQueue(1000,sysv_ipc.IPC_CREAT)
    MARKET_QUEUE = sysv_ipc.MessageQueue(1100,sysv_ipc.IPC_CREAT)
    tab_ext = [0 for x in range(6)]
    # Market processing
    Process(target=Market,args=()).start()
    Process(target=Houses,args=()).start()
