#! python3
# getSyosetu.py - Using first chapter of a novel on Syosetu, downloads
# all of the chapters as named text documents in a folder
import requests, sys, os
from bs4 import BeautifulSoup as bs

# make sure url is included
if not sys.argv[1]:
    print("Please include link to first chapter as argument.")
    sys.exit()

# strip trailing / if it exists
url = sys.argv[1][:-1] if sys.argv[1][-1] == "/" else sys.argv[1]
if 'ncode.syosetu.com' not in url.split("/"):
    print("Link isn't to Syosetu, please try again.")
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
chapter_total = soup.select('#novel_no')[0].get_text().split("/")[1]
chapter_number = soup.select('#novel_no')[0].get_text().split("/")[0]

if not os.path.exists('DownloadedNovels/' + novel_title):
    os.makedirs('DownloadedNovels/' + novel_title)
# download each page and write chapter number as Chapter 001 - {title}.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
novel_path = dir_path + "/DownloadedNovels/" + novel_title

print("Downloading all {} chapters for {} starting from Chapter {}".format(chapter_total, novel_title, chapter_number))
print("Starting URL = {}".format(url))

while True:
    chapter_title = soup.select('.novel_subtitle')[0].get_text()
    if int(chapter_number) < 10:
        chapter_number = '00' + chapter_number
    elif int(chapter_number) < 100:
        chapter_number = '0' + chapter_number
    current_chapter = "Chapter " + chapter_number + " - " + chapter_title
    print("Downloading {}".format(current_chapter))
    chapter_path = novel_path + "/" + current_chapter + ".txt"
    with open(chapter_path, 'w') as f:
        f.write(chapter_title)
        f.write("\n\n\n")
        for text in soup.select('.novel_view'):
            f.write(text.get_text())
            f.write("\n\n")
    if chapter_number == chapter_total:
        break
    else:
        chapter_number = str(int(chapter_number) + 1)
    url = 'http://ncode.syosetu.com/' + url.split("/")[:-1][-1] + "/" + chapter_number
    try:
        res = requests.get(url)
        # make sure it finds it otherwise HTTPError
        res.raise_for_status()
    except requests.exceptions.HTTPError as error:
        # This will be due to there being no prologue
        sys.exit(1)
    soup = bs(res.content, "lxml")

# To Do:
# loop checks to see if chapter is downloaded already and can update
# with only new chapters?
