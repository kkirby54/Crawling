from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from socket import timeout
import requests
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='kmhak540611!', db='mysql', charset='utf8')

cur = conn.cursor()
cur.execute("USE newsscraping")

url = "https://news.naver.com/main/ranking/popularDay.naver"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" }
response = requests.get(url, headers=headers)
bs = BeautifulSoup(response.text, 'html.parser')


boxes = bs.findAll('div', class_='rankingnews_box')
for box in boxes:
    # 여기서 cur 움직여
    company = box.find(class_='rankingnews_name').text
    titles = box.findAll(class_='list_title')

    for i in range(0, 3):
        title = titles[i].text
        cur.execute("SELECT * FROM news WHERE title = %s", (title))
        if cur.rowcount == 0:
            cur.execute('INSERT INTO news (company, title) VALUES (%s, %s)', (company, title))
            conn.commit()

    #
    # print("================{}================".format(company))
    # for i in range(0, 2):
    #     print("{}번째 : ".format(i) + titles[i].text)


cur.close()
conn.close()