#! python3
# getSyosetu.py - Using first chapter of a novel on Syosetu, downloads
# all of the chapters as named text documents in a folder
import requests, sys, os
from bs4 import BeautifulSoup as bs

# get url of first chapter from command line and make BeautifulSoup

if not sys.argv[1]:
    print("Please include link to first chapter as argument.")
    sys.exit()

res = requests.get(sys.argv[1])
res.raise_for_status() # make sure it finds it otherwise exits
soup = bs(res.content, "lxml")

# make directory named DownloadedNovels in current dir and make new
# dirs in that dir to save novels
novel_title = soup.select('title')[0].get_text().split(" ")[0]
chapter_title = soup.select('.novel_subtitle')[0].get_text()
chapter_number = soup.select('#novel_no')[0].get_text().split("/")[0]
chapter_total = soup.select('#novel_no')[0].get_text().split("/")[1]
print("chapter_number = {}".format(chapter_number))
print("chapter_total = {}".format(chapter_total))
# download each page and write chapter number as Chapter 001 - {title}.txt

# loop until final chapter downloaded

# loop checks to see if chapter is downloaded already and can update with
# only new chapters?
