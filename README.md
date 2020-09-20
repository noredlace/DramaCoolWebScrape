# DramaCoolWebScrape

Basic Functionality to Extract VODs on DramaCool

Cookies.text is accessed from Logging into Site and generating the Cookies.TXT Chrome Extension

config.json is used to pass the URLs (as an array if there are multiple URLs to support) and Loop Start/End

Executing the Python Scripts writes to a file URLList.txt

We can utilize XARGS to pipe all the URLs to be batch downloaded

i.e xargs -n 1 -P ${jobs} wget < /PathToFile/URLList.txt

