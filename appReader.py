import urllib.request
from bs4 import BeautifulSoup
import string, sys, sqlite3, time

#if connection lost or server waits the program
#try to catch error and sleep until error is gone
def htmlRequest(url):
	success= False
    while not success:
        try:
            page = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(page,'html.parser')
            return soup
            success= True
        except HTTPError as e:
            time.sleep(random.random()*3)
            success =False
        except URLError as e:
            time.sleep(random.random()*3)
            success =False


#Insert data entries which are appid, name, genre, genreid and letter which is belong to into table 
def dataEntry(newUrl,name,genreid,letter, genreName):
	i = newUrl.rfind("id")
	k = newUrl.rfind("?mt=8")
	appID = int(newUrl[i+2:k])
	c.execute("INSERT OR IGNORE INTO apps VALUES(?,?,?,?,?)",(appID,name,genreid,genreName,letter))
	conn.commit()
#Extract apps info from list for example: category Business,letter A, 5th page,
#take whole apps from that page
def openAppLinks(url,genreid,letter, genreName):
	soup = htmlRequest(url)
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
#iterate over page number
#Example: Category Books, Letter D, Page number 1,2,3,...... until cannot find this page number
def openPageNumber(a,genreid, letter,genreName):
	infinity= sys.maxsize
	for num in range(1,infinity):
		url = a + "&page="+str(num) +"#page"
		if not openAppLinks(url,genreid,letter,genreName):
			break

#Extract Category name from that page
def getGenreName(url):
	soup = htmlRequest(url)
	genreList = soup.select('.breadcrumb > li')[1].contents[1]
	genreName = genreList.contents[0]
	return genreName


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
	soup = htmlRequest(url)
	ul_letters = soup.find(class_ ='list alpha')
	for link in ul_letters.find_all('a', href=True):
		getCatIDLetters(l,link['href'])

def takeAllCat(l):
	soup = htmlRequest('https://itunes.apple.com/us/genre/ios/id36?mt=8')
	for link in soup.find_all('a',class_="top-level-genre"):
		openCategories(l, link['href'])
"""
# Use generateURL instead of using these three functions 
#however it can change over time but it is faster
"""

#Itereate over known genre ids and letters 
def generateURL():
	alphabet = string.ascii_uppercase + '*' #for numbers add '*' character
	for i in range(6000,6026):
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