from bs4 import BeautifulSoup
import requests
import re
import urllib.request

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

cookies = parseCookieFile('DramaCoolCookies.txt')
url = ""

for i in range(1,42):
    url = 'https://www3.dramacool.movie/1-night-2-days-s04-episode-'+str(i)+'.html'
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text,"html.parser")

    #Need to Emulate the Javascript Call to find all the Download Links: document.getElementsByClassName('cf-download')[0].children[2].getAttribute("href").toString()
    mydivs = soup.find("div", {"class": "cf-download"}).findAll("a", href=True, text=True, recursive=False)

    #Format URL for Powershell Script for youtube-dl. It looks like below
    #Start-Process .\youtube-dl.exe '"http://www.mtv.com/episodes/j8g97l/the-challenge-total-madness-mad-world-season-35-ep-3501" --sub-lang "en,eng" --write-sub -o "\The Challenge S35\%(title)s.%(ext)s"'
    print("Start-Process .\youtube-dl.exe '\"%s\"" % mydivs[len(mydivs) - 1]['href'] + " --sub-lang \"en,eng\" --write-sub -o \"\\2D1N\%(title)s.%(ext)s\"'")
    
    #print("Start-Process .\youtube-dl.exe '""" + mydivs[len(mydivs) - 1]['href'] + """ --sub-lang ""en,eng"" --write-sub -o ""\2D1N\%(title)s.%(ext)s""'""")
    #print("Start-Process .\youtube-dl.exe '\"%s\"" % url + " --sub-lang \"en,eng\" --write-sub -o \"\\2D1N\%(title)s.%(ext)s\"'")