import urllib.request
from bs4 import BeautifulSoup
import string
import sys


def takeAppIDandStatus(url,f):
	i = url.rfind("id")
	k = url.rfind("?mt=8")
	appID = int(url[i+2:k])
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	status = soup.find(class_ ='release-date')
	lastDate = status.contents[1]['content']
	status = status.contents[0].contents[0]
	
	f.write("AppID: {}	Status: {}		Date: {} \n".format(appID,status,lastDate))


def openAppLinks(url,f):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	ul_letters = soup.findAll(class_ ='column')
	for i in range(3):
		a_tags = ul_letters[i]
		for link in a_tags.findAll('a', href=True):
			takeAppIDandStatus(link['href'],f)

def openPageNumber(url):

	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	nextLink = soup.find(class_ ='paginate-more')
	if nextLink!= None:
		openPageNumber(nextLink['href'])


def openLetters(url,f):
	#url = "https://itunes.apple.com/us/genre/id"+ str(var) +"?mt=8&letter=" + char
	openPageNumber(url,f)
	
f = open("allApps.txt",'w')
openLetters(sys.argv[1],f)