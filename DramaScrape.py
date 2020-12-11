import requests
import re
import urllib.request
import sys
import os
import shutil
import json
import time
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from datetime import datetime

def download_url(url):
  # print("downloading: ",url)
  # assumes that the last segment after the / represents the file name
  # if url is abc/xyz/file.txt, the file name will be file.txt
  file_name_start_pos = url.rfind("dramacool)") + 10
  file_name = url[file_name_start_pos:]

  r = requests.get(url, stream=True)
  if r.status_code == 200:
    with open(downloadPath+file_name, 'wb') as f:
      #for data in r:
      #  f.write(data)
        #print ("\rDownloading %s" % file_name)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                #update download status every 5 seconds
                #time.sleep(5)

                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                print("\r%s[%s%s]" % (file_name,'=' * done, ' ' * (50-done)))
  return url

#Load JSON for Variables
with open('config.json','r') as read_file:
    data = json.load(read_file)

#config variable settings
URLStart = data["URLStart"]
URLEnd = data["URLEnd"]
    
start = data["LoopStartEnd"][0]
end = data["LoopStartEnd"][1]

outputURLList = data["OutputURLName"]
loggerFile = data["LoggerFile"]

downloadInPython = data["DownloadInPython"]
downloadPath = data["DownloadPath"]
if (downloadPath[-1] != '/'):
    downloadPath = downloadPath + '/'

threadNum = data["ThreadNum"]

##Only Delete a Folder created by US. a.k.a check for a DramaScrapeLogger file
if(os.path.exists(downloadPath + loggerFile)):
    try:
        print("Deleting Folder: " + downloadPath)
        shutil.rmtree(downloadPath)
    except:
        print ("Deletion Of Folder Failed at " + downloadPath)

##Try to Create Folder and Insert Validation Txt if Needed
if(not os.path.exists(downloadPath)):
    try:
        os.mkdir(downloadPath)
        print("Creating Folder: " + downloadPath)
    except:
        print ("Creation Of Folder Failed at " + downloadPath)
    
    ##Create the LoggerFile.txt only when the Folder is Created
    try:
        open(downloadPath + loggerFile,'a').close()
        print("Created LoggerFile Txt: " + downloadPath + loggerFile)
    except:
        print ("Creation of LoggerFile Txt Failed at " + downloadPath + loggerFile)

if(os.path.exists(downloadPath) and not os.path.exists(downloadPath + loggerFile)):
    print("Error: Logger File does not Exist in this Folder")
    print("Please Validate the Folder Path, and if needed manually create the " + loggerFile + " file")
    print("Otherwise you can Delete the Folder as the Logger File is added on Creation of the Folder")
    sys.exit()

#Start Code
f = open(outputURLList,'w')
try:
    cookies = cookielib.MozillaCookieJar()
    cookies.load(filename='DramaCoolCookies.txt')

    url = ""

    for i in range(start,end):
        #Debug Print just to keep track during Compilation
        #print(i)

        urlArray = []

        for k in range(1,len(URLStart)+1):
            urlArray.append(URLStart[k-1]+str(i)+URLEnd[k-1])

        #In Cases where we have multiple base URLs for a show, let's loop through it and exit if we get a valid link
        for url in urlArray:
            #print(url)
            r = requests.get(url,cookies=cookies)

            if(r.status_code == 200):
                break

        soup = BeautifulSoup(r.text,"html.parser")

        #Need to Emulate the Javascript Call to find all the Download Links: document.getElementsByClassName('cf-download')[0].children[2].getAttribute("href").toString()
        try:
            mydivs = soup.find("div", {"class": "cf-download"}).findAll("a", href=True, text=True, recursive=False)
            f.write(mydivs[len(mydivs) - 1]['href']+'\n')

        except:
            print("Unexpected Error:", sys.exc_info()[0])

except:
    print("Unexpected Error:", sys.exc_info()[0])

f.close()

##After URLList.txt is generated, do a parallel download as an option instead of only doing xargs
##i.e xargs -n 1 -P ${jobs} wget < /PathToFile/URLList.txt
if(downloadInPython):
    print("start download")

    #Open File and Mark Start of Thread Downloads
    with open(downloadPath + loggerFile,'a') as finished_urls:
        finished_urls.writelines(datetime.now().strftime("%Y/%m/%d %I:%M:%S %p") + ": Starting Download Tasks of " + str(end-start) + " Files: " + "\n")

    #Open the List of HTTP Download URLs for Thread Downloading
    with open(outputURLList,'r') as read_file:
        downloadArray = read_file.read().splitlines()

    #Start Threaded Downloads
    results = ThreadPool(threadNum).imap_unordered(download_url,downloadArray)

    #Print Results
    for r in results:
        #print(r)
        
        #Write the Finished HTTP URL's to finished Download File
        with open(downloadPath + loggerFile,'a') as finished_urls:
            finished_urls.writelines(datetime.now().strftime("%Y/%m/%d %I:%M:%S %p") + ": Finished File: " + r[(r.rfind("dramacool)") + 10):] + "\n")

    print("Finished All Threads")
    
            
        

    