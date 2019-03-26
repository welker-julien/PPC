from multiprocessing import Process, Manager
 
def weather():
	p=1
	while True:
		temp=293
		for i in range(60):
			temp=temp+1
			print(temp) 
		for i in range(60):
			temp=temp-1
			print(temp)
		if (p<3):
			p=p+1
		else:
			break
 

if __name__ == "__main__":
	

	
		p = Process(target=weather, args=())
		p.start()
		p.join()

 
       
