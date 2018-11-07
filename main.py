from bs4 import BeautifulSoup
from bs4.element import Comment
import time
import datetime
from os import listdir
from os.path import isfile, join
from urllib.parse import urlparse
import urllib
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import string
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


def _Log(text=''):
    print(f'{datetime.datetime.now()}: {text}')
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

    if isfile(fname):
        return

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


_ResultsPerPage = 100

_TermsToSearchFor = [
    "Trump",
    "President Trump",
    "US President",
    "The Donald",
    "President Donald J. Trump"
]

_LiberalTerms = [
    # positive
    "Democrat", "Democrats",
    # "Democratic",
    "Liberal", "Liberals",
    "Left-wing",
    # negative
    "Extremist", "Extremists",
    "Zealot", "Zealots",
    "Ideologue", "Ideologues",
]

_ConservativeTerms = [
    # positive
    "Republican", "Republicans",
    "Conservative", "Conservatives",
    "Right-wing",
    # negative
    "Hack", "Hacks",
    "Elitist", "Elitists",
    "Shill", "Shills",
    "Snowflake", "Snowflakes",
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
#     t = urllib.parse.urlencode({'term': term}).replace('term=', '')
#
#     url = _SearchUrl.format(_ResultsPerPage, t, t)
#     _Log('fetching: ' + url)
#
#     driver.get(url)
#     time.sleep(10)
#     links = driver.find_elements_by_css_selector('g-link')
#
#     SaveGoogleResult(term, driver.page_source)
#
# driver.close()


#######################################################################
#   Extract links from google search results
#######################################################################
# allLinks = []
#
# files = [f for f in listdir('results/') if isfile(join('results/', f)) and '.html' in f ]
# current = 1
# total = len(files)
#
# for file in files:
#     _Log(f'\tprocessing result {current} of {total} ({current/total*100:.4f}%): {file}')
#     current += 1
#
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
# _Log(f'total links extracted: ({len(allLinks)}):')


#######################################################################
#   pull and save linked pages
#######################################################################
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36")
# chrome_options.add_argument("pragma=no-cache")
# driver = webdriver.Chrome(executable_path=_DriverPath, options=chrome_options)
#
# startTime = time.time()
# current = 1
# total = len(allLinks)
#
# _Log(f'Pulling linked pages...')
#
# for l in allLinks:
#     _Log(f'\tfetching linked page {current} of {total} ({current/total*100:.4f}%): {l}')
#     current += 1
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
#   Process websites into known sites (not using)
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



#######################################################################
#   process similarity to samples
#######################################################################
# _Log('loading pages for similarity comparison...')
# files = [f for f in listdir('results/pages/') if isfile(join('results/pages/', f)) and '.html' in f ]
# files.sort()
# pagesForComparison = {}
# current = 1
# total = len(files)
# for f in files:
#     _Log(f'\tloading {current} of {total} ({current/total*100:.4f}%): {f}')
#     current += 1
#     with open('results/pages/' + f, 'r') as infile:
#         pagesForComparison[f] = visible_text(infile.read())
#
# _Log('loading liberal samples...')
# liberalSamplesFiles = [f for f in listdir('results/liberal samples/') if isfile(join('results/liberal samples/', f)) and '.html' in f ]
# lib = {}
# current = 1
# total = len(liberalSamplesFiles)
# for f in liberalSamplesFiles:
#     _Log(f'\tloading {current} of {total} ({current/total*100:.4f}%): {f}')
#     current += 1
#     with open('results/liberal samples/' + f, 'r') as infile:
#         lib[f] = visible_text(infile.read())
#
# _Log('loading conservative samples...')
# con = {}
# conservativeSamplesFiles = [f for f in listdir('results/conservative samples/') if isfile(join('results/conservative samples/', f)) and '.html' in f ]
# current = 1
# total = len(conservativeSamplesFiles)
# for f in conservativeSamplesFiles:
#     _Log(f'\tloading {current} of {total} ({current/total*100:.4f}%): {f}')
#     current += 1
#     with open('results/conservative samples/' + f, 'r') as infile:
#         con[f] = visible_text(infile.read())
#
# rows = len(pagesForComparison) + 1
# columns = len(liberalSamplesFiles) + len(conservativeSamplesFiles) + 1
# comparisonResults = [[0 for x in range(columns)] for y in range(rows)]
#
# startTime = datetime.datetime.now()
# _Log()
# _Log(f'files to process: {len(pagesForComparison)}')
#
#
# # populate row and column headers
# col = 1
# row = 1
# for c in range(0, len(liberalSamplesFiles)):
#     comparisonResults[0][col] = liberalSamplesFiles[c]
#     col += 1
# for c in range(0, len(conservativeSamplesFiles)):
#     comparisonResults[0][col] = conservativeSamplesFiles[c]
#     col += 1
# for k in pagesForComparison.keys():
#     comparisonResults[row][0] = k
#     row += 1
#
#
# # do the comparisons
# spacy.prefer_gpu()
# nlp = spacy.load('en')  # https://spacy.io/usage/models
# current = 1
# total = (len(comparisonResults)-1) * (len(comparisonResults[0])-1)
# startTime = datetime.datetime.now()
#
# for r in range(1, len(comparisonResults)):
#     for c in range(1, len(comparisonResults[r])):
#         f1 = comparisonResults[r][0]
#         f2 = comparisonResults[0][c]
#
#         _Log(f'\tcomparing {current} of {total} ({current/total*100:.4f}%, {datetime.datetime.now() - startTime} elapsed): \'{f1}\', \'{f2}\'')
#         current += 1
#
#         page = pagesForComparison[f1]
#         if f2 in lib:
#             comparison = lib[f2]
#         elif f2 in con:
#             comparison = con[f2]
#         else:
#             raise Exception('This is a problem')
#
#         f1 = nlp(page)
#         f2 = nlp(comparison)
#
#         comparisonResults[r][c] = f1.similarity(f2)
#
#
# # output to CSV
# buffer = ''
# for row in range(0, len(comparisonResults)):
#     for col in range(0, len(comparisonResults[row])):
#         buffer += str(comparisonResults[row][col]) + ','
#     buffer += '\n'
#
# with open('results/similarity.csv', 'w') as outfile:
#     outfile.write(buffer)
#
# _Log(f'complete in {datetime.datetime.now() - startTime}')


#######################################################################
#   count search terms (termcount.csv)
#######################################################################
# files = [f for f in listdir('results/pages/') if isfile(join('results/pages/', f)) and '.html' in f ]
# files.sort()
#
# pages = {}
# current = 1
# total = len(files)
#
# for f in files:
#     _Log(f'\tloading {current} of {total} ({current/total*100:.4f}%): {f}')
#     current += 1
#     with open('results/pages/' + f, 'r') as infile:
#         pages[f] = visible_text(infile.read())
#
# rows = len(files) + 1
# columns = len(_LiberalTerms) + len(_ConservativeTerms) + 1
# comparisonResults = [[0 for x in range(columns)] for y in range(rows)]
#
#
# # populate row and column headers
# col = 1
# row = 1
# for r in range(0, len(files)):
#     comparisonResults[row][0] = files[r]
#     row += 1
# for c in range(0, len(_LiberalTerms)):
#     comparisonResults[0][col] = _LiberalTerms[c]
#     col += 1
# for c in range(0, len(_ConservativeTerms)):
#     comparisonResults[0][col] = _ConservativeTerms[c]
#     col += 1
#
#
# # do the counts
# current = 1
# total = (len(comparisonResults)-1) * (len(comparisonResults[0])-1)
# startTime = datetime.datetime.now()
#
# for r in range(1, len(comparisonResults)):
#     for c in range(1, len(comparisonResults[r])):
#         file = comparisonResults[r][0]
#         term = comparisonResults[0][c]
#
#         _Log(f'\tcomparing {current} of {total} ({current/total*100:.4f}%, {datetime.datetime.now() - startTime} elapsed): \'{term}\', \'{file}\'')
#         current += 1
#
#         page = pages[file]
#
#         comparisonResults[r][c] = page.count(term)
#
#
# # output to CSV
# buffer = ''
# for row in range(0, len(comparisonResults)):
#     for col in range(0, len(comparisonResults[row])):
#         buffer += str(comparisonResults[row][col]) + ','
#     buffer += '\n'
#
# with open('results/termcount.csv', 'w') as outfile:
#     outfile.write(buffer)
