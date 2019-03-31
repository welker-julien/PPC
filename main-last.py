from multiprocessing import Process,Value,Array
import os,signal, time, sys, random, sysv_ipc,datetime,threading



def Weather():
    while True:
        Maj_Temp=random.randint(-5,5)
        if -20<=(temperature.value + Maj_Temp)<=20:
            temperature.value=temperature.value+Maj_Temp
            time.sleep(1)

def transaction(lock,semaphore_thread,prix_courant):
	message,messageType = MARKET_QUEUE.receive()
	data = message.decode().split(',')
	global Quantite_energie
	qtt=data[1]
	homeNum=data[0]
	if ')'in data[0] or '(' in data[0]:
		qttlen=len(qtt)-1
	else:
		qttlen=len(qtt)
	qttDemande = int(qtt[0:qttlen])

	if messageType==2:#on vend aux maison
		with lock:
			Quantite_energie=Quantite_energie-qttDemande

		print(qttDemande,"kwh vendue a : ",homeNum,"par Market! a",prix_courant,"euros")
	if messageType==1:#on achete le surplus des maison
		with lock:
			Quantite_energie=Quantite_energie+qttDemande

		print(qttDemande," kwH achete a : ",homeNum,"par Market! a ",prix_courant,"euros")
	semaphore_thread.release()


def External():
    while True:
        i=random.randint(0,10000)
        if (i==1):
            os.kill(os.getppid(), signal.SIGUSR1)

def Price(prix_courant,val_ext,lock):
    coef_ext=[-200,-150,80,120,150,200]
    tot = 0
    with lock:
        qtt=Quantite_energie
    if qtt<0:
        qtt=-1*qtt
    for i in range (0,5):
        tot=tot+coef_ext[i]*val_ext[i]*0.001+0.001*temperature.value*(1/5)
    totfin=0.99*prix_courant+tot+qtt*0.009
    return totfin*0.1 #coef pour faire redimmensionner la prix de manière acceeptable


def receiveSignal(signalNumber, frame):
    tab_ext = list(map(lambda : random.randint(0,1),tab_ext))

def Affichage():
    while True:
        time.delay(30)
        print("quantité d'energie ayant transité par market",Quantite_energie)

def Market():
    Process(target=Weather,args=()).start()
    lock=threading.Lock()
    semaphore_thread=threading.Semaphore(3)
    prix_courant = 0.14
    tab_ext = Array('i', range(10))
    ext=Process(target=External,args=())
    threading.Thread(target=Affichage,args=()).start
    while True:
        semaphore_thread.acquire()
        threading.Thread(target=transaction,args=(lock,semaphore_thread,prix_courant)).start()
        prix_courant=Price(prix_courant,tab_ext,lock)
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
    surproduction = int(homeProd - homeConso)
    print("surproduction de ", surproduction," par ",homeNumber)
    while surproduction != 0:
        time.sleep(2)
        if HOME_QUEUE.current_messages != 0:
            message,messageType = HOME_QUEUE.receive()
            if message != None:
                data = message.decode().split(',')
                qttDemande = int(data[1])
                if messageType == 1:
                    if qttDemande <= surproduction:
                        if  int(data[2].split(".")[0]) + 10 >  time.time():
                            message=str(homeNumber)+","+str(qttDemande)
                            HOME_QUEUE.send(message.encode(),type = 2) #ACK
                            time.sleep(5)
                        if HOME_QUEUE.current_messages != 0:
                            message,messageType = HOME_QUEUE.receive()
                            if messageType == 3:
                                surproduction = int(surproduction - qttDemande)
                    else:
                        valeurs=str(homeNumber)+','+str(surproduction)
                        MARKET_QUEUE.send(valeurs.encode(),type=1)
                        surproduction = 0
                else:
                    valeurs=str(homeNumber)+','+str(surproduction)
                    MARKET_QUEUE.send(valeurs.encode(),type=1)
                    surproduction = 0

            else:
                valeurs=str(homeNumber)+','+str(surproduction)
                MARKET_QUEUE.send(valeurs.encode(),type=1)
                surproduction = 0

        else:
            valeurs=str(homeNumber)+','+str(surproduction)
            MARKET_QUEUE.send(valeurs.encode(),type=1)
            surproduction = 0


def Surconsommation(homeNumber,homeConso,homeProd):
    surconsommation = int(homeConso) - int(homeProd)
    print("surconsommation de ", surconsommation," par ",homeNumber)
    while surconsommation !=0:
        HOME_QUEUE.send(str((homeNumber,surconsommation,time.time())).encode(),type=1)
        time.sleep(5) #ne pas toucher!
        if HOME_QUEUE.current_messages != 0:
            message,messageType = HOME_QUEUE.receive()


            if messageType == 2:
                data = message.decode().split(',')
                print("home number",data[0],"vend",data[1],"Kwh à",homeNumber) #process vendeur, quantite
                HOME_QUEUE.send("",type=3) #ACK
            else:
                valeurs= str(homeNumber)+','+str(surconsommation)
                MARKET_QUEUE.send(valeurs.encode(),type=2)
                surconsommation = 0
        else:
            valeurs= str(homeNumber)+','+str(surconsommation)
            MARKET_QUEUE.send(valeurs.encode(),type=2)
            surconsommation = 0

def signal_handler(sig,frame):
	print("exit")
	HOME_QUEUE.remove()
	MARKET_QUEUE.remove()
	sys.exit(0)


if __name__ == '__main__':
    NB_HOME = 5
    Quantite_energie = 0
    temperature = Value('d',20)
    HOME_QUEUE = sysv_ipc.MessageQueue(1000,sysv_ipc.IPC_CREAT)
    MARKET_QUEUE = sysv_ipc.MessageQueue(1100,sysv_ipc.IPC_CREAT)
    tab_ext = [0 for x in range(6)]
    # Market processing
    Process(target=Market,args=()).start()
    Process(target=Houses,args=()).start()
    signal.signal(signal.SIGINT,signal_handler)
    signal.pause()
