import urllib.request
from bs4 import BeautifulSoup
import string, sys, subprocess, shlex, pickle

"""
# Functions which are 3 functions below from here gives exact URL
# however it is little bit slower 
"""
def getCatIDLetters(l,url):
	i = url.rfind("id")
	catID = int(url[i+2:i+6])
	k = url.rfind('letter')
	letter = url[k+7]
	l.append([catID,letter])

def openCategories(l,url):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	ul_letters = soup.find(class_ ='list alpha')
	for link in ul_letters.find_all('a', href=True):
		getCatIDLetters(l,link['href'])

def takeAllCat(l):
	page = urllib.request.urlopen('https://itunes.apple.com/us/genre/ios/id36?mt=8').read()
	soup = BeautifulSoup(page,'html.parser')
	for link in soup.find_all('a',class_="top-level-genre"):
		openCategories(l, link['href'])
"""
# Use generateURL instead of using these three functions 
#however it can change over time but it is faster
"""
def openAppLinks(url):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	ul_letters = soup.findAll(class_ ='column')
	for i in range(3):
		a_tags = ul_letters[i]
		if not a_tags.findAll('a', href=True):
			return False
		for link in a_tags.findAll('a', href=True):
			return True
	return True

def openPageNumber(a,l):
	infinity= sys.maxsize
	for num in range(1,infinity):
		url = a + "&page="+str(num) +"#page"

		if openAppLinks(url):
			l.append(url+'\n')
		else:
			break

def generateURL():
	alphabet = string.ascii_uppercase + '*'
	for i in range(6017,6026):
		if i == 6019:
			continue
		for char in alphabet:
			l = list()
			url = "https://itunes.apple.com/us/genre/id"+ str(i) +"?mt=8&letter=" + char
			filename = str(i) + char+".pickle"
			f = open(filename,'wb')
			openPageNumber(url,l)
			pickle.dump(f,l)
			f.close()



#listofTuples = list()


#takeAllCat(listofTuples)
generateURL()

"""
for tuples in listofTuples:
	cmd = "qsub -q bme.q -cwd qsub-job.sh {} {}".format(tuples[0],tuples[1])
	args = shlex.split(cmd)
	result = subprocess.run(args,stdout=subprocess.PIPE)
	result.stdout

"""

