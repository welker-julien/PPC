from multiprocessing import Process
import threading
import os,signal, time, sys, random

 
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
def Home(i,nb,A,B,temp):
	print("home",i,"connected",temp)
	Conso=temp*A
	Prod=temp*B
	if Prod >Conso:
		Surprod =Prod-Conso
		while Surprod!=0:
			#routine de vente
			sys.wait(1)
			mqh=sysv_ipc.MessageQueue(1000)
			message,typ,timeout= mqh.receive()
			if message !=0:
				value= message.decode()
				#value parse on
				qttdemande=value(2)
				if value(0)==1:#type recherche d'energie
					if value(2)<Surpod:
						mqh=sysv_ipc.MessageQueue(1000)
						message=str((3;i;timeout)).encode()
						mqh.send(message)
						sys.wait(1)
						message,typ,timeout=mqh.receive()
						Surrod=Surprod-qttdemande
			else:
				mqm=sysv_ipc.MessageQueue(1100)
				message=str(2;i;Surprod).encode()#2=VENTE AU MARKET
				mqm.send(message)
				message,typ,timeout=mqm.receive()
				while message!=4:
					message,typ,timeout=mqm.receive()
				Surprod=0
	elif P<C:
		mqh=sysv_ipc.MessageQueue(1000)
		message=str((1;i;C-P)).encode()#1= j'ia besoin d'energie
		mqh.send(message)
		message,typ,timeout=mqh.receive()
		if message ==2:
			value= message.decode()
			#value parse on
			print(P-C, i,value(1))

			mqh=sysv_ipc.MessageQueue(1000)
			message= str(3;i;C-P)).encode()
			mq.send(message)
		else:
			mqm=sysv_ipc.MessageQueue(1100)
			message=str(1;i;C-P)).encode()#on vend au marché
			mqm.send(message)
	else:
		#nada car on est à l'équilibre



	

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
		#m=Process(target=Market,args=(temp,))
		#m.start()
		#m.join()		
		
		w = Process(target=weather, args=(temp,))
		w.start()
		w.join()
		
		h=Process(target=houses,args=(nb,temp))
		h.start()
		h.join()
		
		#mqh=sysv_ipc.MessageQueue(1000,sysv_ipc.IPC_CREAT)#message queue des homes

		#mqm=sysv_ipc.MessageQueue(1100,sysv_ipc.IPC_CREAT)#message queue du market

#garbage collector des messages queues

       
