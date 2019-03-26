
from multiprocessing import Process
import os, signal, time, random


def receiveSignal(signalNumber, frame):
		i=random.randint(0,5)
		if i==0 :
			coef_ext=coef_ext*0.1 #communisme
		elif i==2 :
			coef_ext=coef_ext*0.5 #invention du nucléaire
		elif i==3 :
			coef_ext=coef_ext*0.8 #cadeaux
		elif i==4 :
			coef_ext=coef_ext*1.5 #monopole
		else :
			coef_ext=coef_ext*5 #guerre
        price()


def External():
    while True:
        i=random.randint(0,100)
        if (i==1):
            os.kill(os.getppid(), signal.SIGUSR1)


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, receiveSignal)
    child = Process(target=External ,args=())
    child.start()
