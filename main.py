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
def Home(i,nb,A,B,C,temp):
	print("home",i,"connected",temp)
	Conso=temp*A
	Prod=temp*B+temp*C
	print(i,"nb de maison: ",nb,"constantes de calcul: ",Conso-Prod)


def houses(nb,temp):

	
	for i in range(nb):
		A=random.randint(0,10)#pour calculer les consommations et productions
		B=random.randint(0,10)
		C=random.randint(0,10)

		ho=Process(target=Home,args=(i,nb,A,B,C,temp))
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

       
