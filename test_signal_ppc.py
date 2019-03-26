
from multiprocessing import Process
import os
import signal
import time
import sys

def receiveSignal(signalNumber, frame):
    print('Received:', signalNumber)
    #aller chercher info weather
    return

def Fils(PPID):
    time.sleep(5)
    # PPID=os.getppid
    os.kill(os.getppid(), signal.SIGUSR1)

if __name__ == '__main__':
    child = Process(target=Fils,args=(os.getpid,))
    print ("o")
    child.start()
    while True:
        signal.signal(signal.SIGUSR1, receiveSignal)
