import sqlite3, urllib.request,time,random
from multiprocessing import Pool

def fetch(row):
	i = 0
	start_time = time.time()
	for row in data:
		success= False
		while success:
			try:
				url = "https://itunes.apple.com/us/app/id"+ str(row[0]) +"?mt=8"
				print(url)
				page = urllib.request.urlopen(url)
				i+=1
				print(i)
				print ('Done! Time taken: {}'.format(time.time() - start_time))
				success= True
			except urllib.error as e:
				print(e, e.reason)
				sleep(1)
				success =False
			



conn = sqlite3.connect('appStore.db')
c = conn.cursor()
c.execute('SELECT * FROM apps')
data = c.fetchall()

if __name__ == '__main__':
    with Pool(4) as p:
        print(p.map(fetch, data))


		

	
c.close()
conn.close()