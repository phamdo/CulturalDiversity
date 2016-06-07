from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import urllib2
import re
from math import log

countries = []
countries2 = []

class Country(object):
    def __init__(self, name, info):
        self.name = name # name of country
        self.info = info # stores info available on CIA World Factbook
        self.data = [] # stores parsed information (percentages)
        self.entropy = 0

    def parseInfo(self):
        p = self.info.split('\n')[1]
        percents = re.findall('[0-9|.]+%', p)
        if (len(percents) > 0):
            for percent in percents:
                num = str(percent)[:-1]
                n = float(num)/100
                self.data.append(n)
        else:
            self.data = "Not enough data available"
        
    def calculateEntropy(self):
        if (type(self.data) == str):
            self.entropy = self.data
        else:
            total = 0
            for i in self.data:
                total += (i * log(i, 2))
            if (total != 0):
                total *= -1
            
            self.entropy = total

    def display(self):
        print "Country: ", self.name
        print self.info
        print "Data: ", self.data
        print "Entropy: ", self.entropy

class Field(object):
    def __init__(self, name, info, data):
        self.name = name
        self.info = info
        self.data = []
        self.entropy = 0

class Language(Field):

    def __init__(self, info, data):
        Field.init(self, "Language", info, data)


def get_countries():
    url = urllib2.urlopen("https://www.cia.gov/library/publications/the-world-factbook/")
    soup = BeautifulSoup(url.read())
    lst = soup.findAll("option")
    for c in lst:
        countries.append(str(c.text).strip())
    print len(countries)
def languages():
    url = urllib2.urlopen("https://www.cia.gov/library/publications/the-world-factbook/fields/2098.html")
    src = url.read()
    soup = BeautifulSoup(src)

    table = soup.find("table", id = "fieldListing")
    rows = table.findAll("tr")

    cts = []
    data = []

    del rows[0]
    for tr in rows:
        cols = tr.findAll('td')
        country = Country(cols[0].text, cols[1].text)
        countries.append(country)
        cts.append(cols[0].text)
        data.append(cols[1].text)

    for country in countries:
        country.parseInfo()
        country.calculateEntropy()

    
    #c  = sorted(countries, key = lambda x: x.entropy)

    #for i in c:
        #i.display()
        #print "---------------------------------------------------"

def religions(): 
    url = urllib2.urlopen("https://www.cia.gov/library/publications/the-world-factbook/fields/2098.html")
    src = url.read()
    soup = BeautifulSoup(src)

    table = soup.find("table", id = "fieldListing")
    rows = table.findAll("tr")

    cts = []

    del rows[0]
    for tr in rows:
        cols = tr.findAll("td")
        country = Country(cols[0].text, cols[1].text)
        countries2.append(country)
        cts.append(cols[0].text)
    

get_countries()
