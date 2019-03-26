from multiprocessing import Process
import threading
import os,signal, time, sys, random, sysv_ipc

 
def weather(temp):
	print("weather connected")
	p=1
	while True:
		temp=293
		for i in range(60):
			temp=temp+1
			#print(temp) 
		for i in range(60):
			temp=temp-1
			#print(temp)
		if (p<3):
			p=p+1
		else:
			break
#mq plante
def Home(i,nb,A,B,temp):
	#while true:
	print("home",i,"connected")
	Conso=temp*A
	Prod=temp*B
	if Prod >Conso:
		print("Surproduction de ", Prod-Conso)
		Surprod =Prod-Conso
		print (Surprod,"ici")
		while Surprod!=0:
			#routine de vente
			print("while")
			#time.sleep(1)
			mqh=sysv_ipc.MessageQueue(1000)
			print("a")
			message,t=mqh.receive()
			print("ae")#erreur après
			if message !=0:
				value= message.decode()
				#value parse on
				qttdemande=value[1]
				if t==1:#type recherche d'energie
					if int(value[1])<Surprod:
						mqh=sysv_ipc.MessageQueue(1000)
						message=str((i,timeout)).encode()
						mqh.send(message,type=3)
						time.sleep(1)
						message,t=mqh.receive()
						Surprod=Surprod-qttdemande
			else:
				mqm=sysv_ipc.MessageQueue(1100)
				message=str((i,Surprod)).encode()#2=VENTE AU MARKET
				mqm.send(message,type=2)
				message,t=mqm.receive()
				while message!=4:
					message,t=mqm.receive()
				Surprod=0
	elif Prod<Conso:
		print("Surconsomation de ",Conso-Prod)
		mqh=sysv_ipc.MessageQueue(1000)
		message=str((i,Conso-Prod)).encode()#1= j'ai besoin d'energie
		mqh.send(message,type=1)
		message,t=mqh.receive()
		if type ==2:
			value= message.decode()
			#value parse on
			print(P-C, i,t)
			mqh=sysv_ipc.MessageQueue(1000)
			message= str((i,Conso-Prod)).encode()
			mq.send(message,type=3)
		else:
			mqm=sysv_ipc.MessageQueue(1100)
			message=str((i,Conso-Prod)).encode()#on achète au marché donc 1
			mqm.send(message,type=1)
	else:
		#nada car on est à l'équilibre
		print("equilibre")


	

	print(i,"nb de maison: ",nb,"constantes de calcul: ",Conso-Prod)


def houses(nb,temp):

	
	for i in range(nb):
		A=random.randint(0,10)#pour calculer les consommations et productions
		B=random.randint(0,10)
		C=random.randint(0,10)

		ho=Process(target=Home,args=(i,nb,A,B,temp))
		ho.start()
	ho.join()


if __name__ == "__main__":
	
	nb=5 #Nombre de maison	
	temp=293
	mqh=sysv_ipc.MessageQueue(1000,sysv_ipc.IPC_CREAT)#message queue des homes

	mqm=sysv_ipc.MessageQueue(1100,sysv_ipc.IPC_CREAT)#message queue du market
	#m=Process(target=Market,args=(temp,))
	#m.start()
	#m.join()		
		
	w = Process(target=weather, args=(temp,))
	w.start()
	w.join()
		
	h=Process(target=houses,args=(nb,temp))
	h.start()
	h.join()
		
		

#garbage collector des messages queues

       
