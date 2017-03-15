#! python3
# getSyosetu.py - Using first chapter of a novel on Syosetu, downloads
# all of the chapters as named text documents in a folder
import requests, sys, os
from bs4 import BeautifulSoup as bs

# make sure url is included
if not sys.argv[1]:
    print("Please include link to first chapter as argument.")
    sys.exit()

# make sure url returns a response and create a soup if it does
res = requests.get(sys.argv[1])
res.raise_for_status() # make sure it finds it otherwise exits
soup = bs(res.content, "lxml")

# check if DownloadedNovels dir exists, if not make it
if not os.path.exists('DownloadedNovels'):
    os.makedirs('DownloadedNovels')

# make new directory in DownloadedNovels if necessary
novel_title = soup.select('title')[0].get_text().split(" ")[0]
chapter_title = soup.select('.novel_subtitle')[0].get_text()
chapter_number = soup.select('#novel_no')[0].get_text().split("/")[0]
chapter_total = soup.select('#novel_no')[0].get_text().split("/")[1]
if int(chapter_number) < 10:
    chapter_number = '00' + chapter_number
elif int(chapter_number) < 100:
    chapter_number = '0' + chapter_number

if not os.path.exists('DownloadedNovels/' + novel_title):
    os.makedirs('DownloadedNovels/' + novel_title)
# download each page and write chapter number as Chapter 001 - {title}.txt

# loop until final chapter downloaded

# loop checks to see if chapter is downloaded already and can update with
# only new chapters?
