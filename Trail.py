# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:04:24 2020

@author: Saatvik Korisepati
"""

# import requests
# from bs4 import BeautifulSoup
#
# class Search:
#    def __init__(self, phrase):
#        self.phrase = phrase
#
#        self.url = 'https://www.google.com/search?q={0}&formatclass=st'.format(self.phrase)
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
# a = Search('why+is+sky+blue')
# a.scrape()
import requests
# from pprint import pprint

from flaskapp import db


class skillsDictionary(db.model):
    __tablename__ = 'skillsDict'


id = db.Column(db.Integer, primary_key=True)
keyPhrase = db.Column(db.String(50))
phraseDefinition = db.Column(db.Text)


#    def __repr__():
#        return f'String Representation: )'


class Search:
    def __init__(self, phrase):
        self.phrase = phrase

        self.url = 'https://api.duckduckgo.com/?q={0}&format=json'.format(self.phrase)

    def scrape(self):
        tempDict = {}

        r = requests.get(self.url)
        data = r.json()

        #        pprint(data)

        if len(data['AbstractText']) != 0:
            response = data['AbstractText']
        elif len(data['Answer']) != 0:
            response = data['Answer']

        print(tempDict)

        #        IF (phrase NOT IN (
        #        SELECT keyPhrase FROM skillsDict ))
        #        THEN INSERT INTO skillsDict (phrase, response)
        #        END IF;

        skills = skillsDictionary(keyPhrase=self.phrase, phraseDefintion=response)
        db.session.add(skills)
        db.session.commit()


a = Search('java+programming+language')
a.scrape()
print(skillsDictionary.query.all())
