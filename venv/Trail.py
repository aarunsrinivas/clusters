# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:04:24 2020

@author: Saatvik Korisepati
"""

#import requests
#from bs4 import BeautifulSoup
#
#class Search:
#    def __init__(self, phrase):
#        self.phrase = phrase
#        
#        self.url = 'https://www.google.com/search?q={0}'.format(self.phrase)
#        
#    def scrape(self):
#        html = requests.get(self.url)
#        #print(html.text)
#        soup = BeautifulSoup(html.text, 'html.parser')
#        allDiv = soup.find_all('div')
#        for div in allDiv:
#            #if 'wa:/description' in div:
#            print(div.text)
#            print('\n')
#            #f = open("trial.txt", "a")
#            #f.write(div.text)
#            #f.write('\n')
#        #f.close()
#        
#a = Search('why+is+sky+blue')
#a.scrape()
import requests

class Search:
    def __init__(self, phrase):
        self.phrase = phrase
        
        self.url = 'https://api.duckduckgo.com/?q={0}&format=json'.format(self.phrase)
        
    def scrape(self):
        tempDict = {}
        
        r = requests.get(self.url)
        data = r.json()
        
        
        if len(data['AbstractText']) != 0:
            tempDict[self.phrase] = data['AbstractText']
        elif len(data['Answer']) != 0:
            tempDict[self.phrase] = data['Answer']
            
        print(tempDict)
        
a = Search('valley+forge+national+park')
a.scrape()
