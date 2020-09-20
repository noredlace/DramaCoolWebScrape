from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import sys
import os
import json

def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies


#Start Code
try:
    cookies = parseCookieFile('DramaCoolCookies.txt')
    url = ""
    f = open('URLList.txt','w')

    #Load JSON for Variables
    with open('config.json','r') as read_file:
        data = json.load(read_file)

    URLStart = data["URLStart"]
    URLEnd = data["URLEnd"]
    
    start = data["LoopStartEnd"][0]
    end = data["LoopStartEnd"][1]

    for i in range(start,end):
        #Debug Print just to keep track during Compilation
        print(i)

        urlArray = []
        
        for k in range(1,len(URLStart)+1):
            urlArray.append(URLStart[k-1]+str(i)+URLEnd[k-1])

        #In Cases where we have multiple base URLs for a show, let's loop through it and exit if we get a valid link
        for url in urlArray:
            r = requests.get(url, cookies=cookies)

            if(r.status_code == 200):
                break

        soup = BeautifulSoup(r.text,"html.parser")

        #Need to Emulate the Javascript Call to find all the Download Links: document.getElementsByClassName('cf-download')[0].children[2].getAttribute("href").toString()
        try:
            mydivs = soup.find("div", {"class": "cf-download"}).findAll("a", href=True, text=True, recursive=False)
            f.write(mydivs[len(mydivs) - 1]['href']+'\n')

        except:
            print("Unexcepted Error:", sys.exc_info()[0])

except:
    print("Unexcepted Error:", sys.exc_info()[0])

f.close()

    