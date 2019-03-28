#!user/bin/bash/env python 3

from multiprocessing import Process,Value
import sys,time,os,random

def Weather(temp_courant):
    while True:
        Maj_Temp=random.randint(-5,5)
        if -20<=(temp_courant.value + Maj_Temp)<=20:
            temp_courant.value=temp_courant.value+Maj_Temp

def Market(temp):
    Process(target=Weather,args=(temp,)).start()



def Home(temp):
    while True:
        print("température:",temp.value)
        time.sleep(1)


if __name__ == "__main__":
    print("il faut initialiser la shared memory dans le main comme ça tout le monde y a accès HomeX et Market")
    print('comme ça les modi de weather sont dispo dispo pour tout le monde')
    print("nb: il faut passer la variable partagé en paramètre de toutes les fonctions")
    Temperature=Value('d',0)
    Process(target=Market,args=(Temperature,)).start()
    Process(target=Home,args=(Temperature,)).start()
