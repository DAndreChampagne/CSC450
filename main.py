from bs4 import BeautifulSoup
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


def _Log(text):
    return
    print(text)


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
#     print('fetching: ' + url)
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
#     print('processing results/' + file + ' ...')
#     text = ''
#     with open('results/' + file, 'r') as f:
#         text = f.read()
#
#     soup = BeautifulSoup(text, 'html.parser')
#
#     links = soup.select('g-link > a')
#     print(f'\tg-link > a: {len(links)}')
#     links = ProcessLinks(links, file)
#     allLinks.extend(links)
#
#     links = soup.select('.r > a')
#     print(f'\t.r > a: {len(links)}')
#     links = ProcessLinks(links, file)
#     allLinks.extend(links)
#
#     links = soup.select('g-inner-card > a')
#     print(f'\tg-inner-card > a: {len(links)}')
#     links = ProcessLinks(links, file)
#     allLinks.extend(links)
#
# print(f'allLinks ({len(allLinks)}):')

# chrome_options = Options()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36")
# chrome_options.add_argument("pragma=no-cache")
# driver = webdriver.Chrome(executable_path=_DriverPath, options=chrome_options)
#
# startTime = time.time()
#
# for l in allLinks:
#     print('fetching ' + l)
#
#     try:
#         driver.get(l)
#         SaveWebResult(l, driver.page_source)
#     except Exception as ex:
#         print(f"An exception of type {type(ex).__name__} occurred. Arguments:\n\t{ex.args}")
#
# driver.close()
# endTime = time.time()
#
# print(f'finished in {endTime - startTime}')


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

with open('results/knownsites.json', 'r') as infile:
    knownsites = json.load(infile)


print(knownsites)