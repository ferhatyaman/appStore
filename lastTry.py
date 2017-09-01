import urllib.request
from bs4 import BeautifulSoup
import string, sys, sqlite3, time
"""
def takeAppIDandStatus(url):
	i = url.rfind("id")
	k = url.rfind("?mt=8")
	appID = int(url[i+2:k])
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	status = soup.find(class_ ='release-date')
	lastDate = status.contents[1]['content']
	status = status.contents[0].contents[0]
	print(appID)
	#f.write("AppID: {}	Status: {}		Date: {} \n".format(appID,status,lastDate))
"""
def dataEntry(newUrl,name,genreid,letter, genreName):
	i = newUrl.rfind("id")
	k = newUrl.rfind("?mt=8")
	appID = int(newUrl[i+2:k])
	c.execute("INSERT OR IGNORE INTO apps VALUES(?,?,?,?,?)",(appID,name,genreid,genreName,letter))
	conn.commit()

def openAppLinks(url,genreid,letter, genreName):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	ul_letters = soup.findAll(class_ ='column')
	for i in range(3):
		a_tags = ul_letters[i]
		if not a_tags.findAll('a', href=True):
			return False
		for link in a_tags.findAll('a', href=True):
			name = link.contents[0]
			newUrl = link['href']
			dataEntry(newUrl, name, genreid,letter, genreName)
	return True

def openPageNumber(a,genreid, letter,genreName):
	infinity= sys.maxsize
	for num in range(1,infinity):
		url = a + "&page="+str(num) +"#page"
		if not openAppLinks(url,genreid,letter,genreName):
			break
def getGenreName(url):
	page = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(page,'html.parser')
	genreList = soup.select('.breadcrumb > li')[1].contents[1]
	genreName = genreList.contents[0]
	return genreName



def generateURL():
	alphabet = string.ascii_uppercase + '*'
	for i in range(6017,6026):
		if i == 6019:
			continue
		for char in alphabet:
			url = "https://itunes.apple.com/us/genre/id"+ str(i) +"?mt=8&letter=" + char
			print(url)
			genreName = getGenreName(url)
			openPageNumber(url, i, char, genreName)


conn = sqlite3.connect('appStore.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS apps(appID INT PRIMARY KEY, appName TEXT, genreID INT, genre TEXT, genre_letter TEXT)")
generateURL()
c.close()
conn.close()