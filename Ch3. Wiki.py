from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

random.seed(datetime.datetime.now())

pages = set()

def getLinks(pageUrl):
    global pages

    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html.parser')

    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').findAll('p')[1].get_text())
        print(bs.find(id='ca-edit').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something')

    for link in bs.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 새 페이지 발견
                newPage = link.attrs['href']
                print('------------------------\n' + newPage)
                pages.add(newPage)
                getLinks(newPage)


getLinks('/wiki/hearthstone')

# links = getLinks('/wiki/hearthstone')

# while len(links) > 0:
#     newArticle = links[random.randint(0, len(links)-1)].attrs['href']
#     print(newArticle)
#     links = getLinks(newArticle)
# ###