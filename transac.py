from multiprocessing import Process
import threading
import os,signal, time, sys, random, sysv_ipc,datetime

Quantite_energie = 0
def Weather():
	print("weather affiche la  temperature: ",temperature)

def transaction(message,messageType,lock):
	data = message.decode().split(',')
	global Quantite_energie
	#print(data)
	qtt=data[1]
	homeNum=data[0]
	qttlen=len(qtt)
	print("taille",qttlen)
	qttDemande = int(qtt[0:qttlen])
	#print(homeNum," ",qttDemande)
	#homeNumber = int(data[0])
	if messageType==2:#on vend aux maison
		with lock:
			Quantite_energie=Quantite_energie-int((message.decode().split(','))[1])

		print(qttDemande," vendue a : ",homeNum)
	if messageType==1:#on achete le surplus des maison
		with lock:
			Quantite_energie=Quantite_energie+int((message.decode().split(','))[1])

		print(qttDemande," achete a : ",homeNum)
	print("quantité d'energie ayant transité par market",Quantite_energie)
		

def Market():
	Process(target=Weather,args=()).start() 
	
	lock=threading.Lock()
	message,messageType = MARKET_QUEUE.receive()
	while message != None:
		trans=threading.Thread(target=transaction,args=(message,messageType,lock))
		trans.start()
		
		message,messageType = MARKET_QUEUE.receive()
	trans.join()
	

def Houses():
	for i in range(NB_HOME):
		A,B = (random.randint(0,10) for x in range(0,2))
		home = Process(target=Home,args=(i,A,B,))
		home.start()
	home.join()

def Home(homeNumber,A,B):
	#print("home",homeNumber,"connected")
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
	print("surproduction de ", surproduction," par ",homeNumber)
	liste=str(homeNumber)+','+str(surproduction)
	#print(type(liste))
	#print(liste)
	MARKET_QUEUE.send(liste.encode(),type=1)
	surproduction = 0
            #TODO : Verification du print dans le thread

def Surconsommation(homeNumber,homeConso,homeProd):
	print("Surconso", homeNumber)
	surconsommation = homeConso - homeProd
	print("surconsommation de ", surconsommation," par ",homeNumber)
	liste= str(homeNumber)+','+str(surconsommation)
	#print(liste)
	MARKET_QUEUE.send(liste.encode(),type=2)
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
