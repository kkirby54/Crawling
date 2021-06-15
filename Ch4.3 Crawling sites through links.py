import requests
import re
from bs4 import BeautifulSoup

# 사이트에 대한 정보를 갖고 있는 Crawler 객체를 만든다.
# 정확히 하자면, Website 객체를 param으로 받는 Crawler 객체.
# 그 사이트에서 찾을 수 있는 링크를 정규표현식을 이용해 찾아서 crawl한다.

class Website:
    def __init__(self, name, url, targetPattern, absolteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absolteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print('============================')
        print('URL : {}'.format(self.url))
        print('TITLE : {}'.format(self.title))
        print('BODY : {}'.format(self.body))

class Crawler:
    def __init__(self, site):
        self.site = site
        self.visited = []

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    # targetPattern에 맞는 놈들을 찾는다.
    def crawl(self):
        bs = self.getPage(self.site.url)
        targetPages = bs.findAll('a', href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.url, targetPage)
                self.parse(targetPage)



reuters = Website('Reuters', 'https://www.reuters.com', '^((/world/)|(/business/))',
                  False, 'title', 'div.ArticleBody__container___D-h4BJ')
crawler = Crawler(reuters)
crawler.crawl()
