from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import pandas as pd
import time
import datetime
from os import listdir
from os.path import isfile, join
from urllib.parse import urlparse
import urllib.parse
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import string
import json
from difflib import SequenceMatcher
import spacy


def visible_tag(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', 'img', 'iframe', '[document']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def visible_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    visibleText = filter(visible_tag, texts)
    return u" ".join(t.strip() for t in visibleText)


def _Log(text):
    print(text)
    with open('results/log.log', 'a') as outfile:
        outfile.write(text + '\r\n')


def ReplaceNonValidCharacters(text):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    for c in text:
        if c not in valid_chars:
            text = text.replace(c, '|')
    return text


def LogGoogleResult(term, link):
    _Log(f'LogGoogleResult("{term}", "{link}")')
    fname = "results/results.csv"

    uri = urlparse(link)

    f = open(fname, 'a')
    f.write(f"{datetime.datetime.now()}, '{term}', '{uri.netloc}', '{link}'\n")
    f.close()


def SaveGoogleResult(link, text):
    _Log(f'SaveGoogleResult("{link}", ...)')
    now = str(datetime.datetime.now()).replace(':', '').replace('-', '').replace('.', '')
    fname = f"results/{now} " + ReplaceNonValidCharacters(link) + ".html"

    f = open(fname, 'w')
    f.write(text)
    f.close()


def SaveWebResult(link, text):
    _Log(f'SaveWebResult("{link}", ...)')
    fname = "results/pages/" + ReplaceNonValidCharacters(link) + ".html"

    f = open(fname, 'w')
    f.write(text)
    f.close()


def ProcessLinks(links, file):
    _Log(f'ProcessLinks({links}, {file})')
    hrefs = []

    for l in links:
        term = file[22:].replace('.html', '')
        hrefs.append(l['href'])
        LogGoogleResult(term, l['href'])

    return hrefs


_ResultsPerPage = 20

_TermsToSearchFor = [
    "Trump",
    "President Trump",
    "US President",
    "The Donald",
    "President Donald J. Trump"
]

_SearchUrl = "https://www.google.com/search?sourceid=chrome&ie=UTF-8&num={}&q={}"

_Headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'pragma': 'no-cache',
    'authority': 'www.google.com',
    'referer': 'https://www.google.com/',
}

_DriverPath = '/Users/dan/Google Drive/School/2018 08 - ECSU-CSC450 Senior Research/CSC450/chromedriver'


#######################################################################
#   pull search results
#######################################################################
# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36")
# chrome_options.add_argument("pragma=no-cache")
# chrome_options.add_argument("authority=www.google.com")
# chrome_options.add_argument("referer=https://www.google.com")
#
# driver = webdriver.Chrome(executable_path=_DriverPath, options=chrome_options)
#
# for term in _TermsToSearchFor:
#
#     t = urllib.parse.urlencode({'term': term}).replace('term=', '')
#     url = _SearchUrl.format(_ResultsPerPage, t, t)
#     _Log('fetching: ' + url)
#
#     driver.get(url)
#     time.sleep(120)
#     links = driver.find_elements_by_css_selector('g-link')
#
#     SaveGoogleResult(term, driver.page_source)
#
#
# driver.close()


#######################################################################
#   Extract links from google search results
#######################################################################
# allLinks = []
#
# files = [f for f in listdir('results/') if isfile(join('results/', f)) and '.html' in f ]
# for file in files:
#     _Log('processing results/' + file + ' ...')
#     text = ''
#     with open('results/' + file, 'r') as f:
#         text = f.read()
#
#     soup = BeautifulSoup(text, 'html.parser')
#
#     links = soup.select('g-link > a')
#     _Log(f'\tg-link > a: {len(links)}')
#     links = ProcessLinks(links, file)
#     allLinks.extend(links)
#
#     links = soup.select('.r > a')
#     _Log(f'\t.r > a: {len(links)}')
#     links = ProcessLinks(links, file)
#     allLinks.extend(links)
#
#     links = soup.select('g-inner-card > a')
#     _Log(f'\tg-inner-card > a: {len(links)}')
#     links = ProcessLinks(links, file)
#     allLinks.extend(links)
#
# _Log(f'allLinks ({len(allLinks)}):')

# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36")
# chrome_options.add_argument("pragma=no-cache")
# driver = webdriver.Chrome(executable_path=_DriverPath, options=chrome_options)
#
# startTime = time.time()
#
# for l in allLinks:
#     _Log('fetching ' + l)
#
#     try:
#         driver.get(l)
#         SaveWebResult(l, driver.page_source)
#     except Exception as ex:
#         _Log(f"An exception of type {type(ex).__name__} occurred. Arguments:\n\t{ex.args}")
#
# driver.close()
# endTime = time.time()
#
# _Log(f'finished in {endTime - startTime}')


#######################################################################
#   Process websites
#######################################################################
# hosts = []
#
# files = [f for f in listdir('results/pages/') if isfile(join('results/pages/', f)) and '.html' in f ]
# for file in files:
#     host = file.split('|')[3]
#     if host.count('.') == 1:
#         host = 'www.' + host
#     host = 'http://' + host
#     hosts.append(host)
#
# hosts = list(set(hosts))
# hosts.sort()
#
# knownsites = {}
#
# for host in hosts:
#     knownsites[host] = 0

knownsites = {}
# with open('results/knownsites.json', 'w') as outfile:
#     json.dump(knownsites, outfile, sort_keys=True, indent=4)


# with open('results/knownsites.json', 'r') as infile:
#     knownsites = json.load(infile)
#
# _Log(knownsites)


# Pull visible text from results file
# with open('results/pages/https|||abc13.com|politics|thousands-of-trump-supporters-wait-in-line-for-maga-rally|4534157|.html', 'r') as infile:
#     html1 = infile.read()
# with open('results/pages/https|||ballotpedia.org|Donald_Trump.html', 'r') as infile:
#     html2 = infile.read()
#
# _Log(f'sequencematch = {SequenceMatcher(None, visible_text(html1), visible_text(html2)).ratio()}')
#
# spacy.prefer_gpu()
# nlp = spacy.load('en')  # https://spacy.io/usage/models
#
# x = nlp(html1)
# y = nlp(html2)
#
# _Log(f'spacy         = {x.similarity(y)}')


results = []
files = [f for f in listdir('results/pages/') if isfile(join('results/pages/', f)) and '.html' in f ]
results.extend(files)
results.sort()

size = len(results)
matrix = [[0 for x in range(size)] for y in range(size)]

startTime = datetime.datetime.now()
_Log(f'files to process: {len(results)}')

# load files into memory
progress = 0
total = len(files)
storedFiles = {}
for f in files:
    progress += 1
    _Log(f'loading file {progress} of {total} ({progress/total*100:.4f}%), {datetime.datetime.now() - startTime} elapsed, {f}')
    with open(f'results/pages/{f}', 'r') as f1:
        storedFiles[f] = visible_text(f1.read())


# add row and column headers
for i in range(1, len(results)):
    matrix[0][i] = results[i]
for i in range(1, len(results)):
    matrix[i][0] = results[i]


# process files
spacy.prefer_gpu()
nlp = spacy.load('en')  # https://spacy.io/usage/models

progress = 0
total = len(matrix)**2
for row in range(1, len(matrix)):
    for col in range(1, len(matrix[row])):
        file1 = matrix[row][0]
        file2 = matrix[0][col]
        progress += 1

        _Log(f'processing {progress} of {total} ({progress / total * 100 :.4f}%), {datetime.datetime.now() - startTime} elapsed')
        _Log(f'\t{file1}')
        _Log(f'\t{file2}')

        html1 = nlp(storedFiles[file1])
        html2 = nlp(storedFiles[file2])
        s = html1.similarity(html2)

        _Log(f'\tsimilarity = {s}')

        matrix[row][col] = s


# output to CSV
buffer = ''
for row in range(0, len(matrix)):
    for col in range(0, len(matrix[row])):
        buffer += str(matrix[row][col]) + ','
    buffer += '\n'

with open('results/similarity.csv', 'w') as outfile:
    outfile.write(buffer)

_Log(f'complete in {datetime.datetime.now() - startTime}')
