# TVBS
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import  sleep
import json
from bs4 import BeautifulSoup
import requests
from record import newArticle, check
from datetime import datetime
import re

url = "https://news.tvbs.com.tw/sports" 
cate = "global"
max_it = 10

driver = webdriver.Chrome("./chromedriver.exe")
driver.implicitly_wait(10)
driver.get(url)

def height():
  hight = 'return document.body.clientHeight'
  h = driver.execute_script(hight)
  return h
driver.maximize_window()
last_h = 0
same_time = 0
while(same_time<5 and max_it>0):
    h = height()
    if(last_h == h): 
        same_time=same_time+1
        print("Same with", same_time)
    else:
        same_time=0   
    last_h = h
    driver.execute_script("window.scrollBy(0, 10000);", "")
    sleep(0.1)
    max_it -= 1
    print(max_it)
    
news_list = driver.find_element(By.CLASS_NAME, 'news_now2')
news_item = news_list.find_elements(By.TAG_NAME, 'li')
links = list(map(lambda item: item.find_element(By.TAG_NAME, "a"), news_item))
print("%d"%len(list(links)))
news = list(filter(lambda item: item[0] != '', map(lambda item: (item.find_element(By.CLASS_NAME, "txt").text, item.get_attribute("href")), links)))

driver.close()
for (index,(title, link)) in enumerate(news, start=1):
    if(not check(link)):
        continue

    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    author = soup.find("div", class_="author")

    first = soup.find("div", id="let_first_p_here").text
    article = soup.find("div", id="news_detail_div")

    if(article and author):
        pattern = re.compile('([0-9]+\/[0-9]+\/[0-9]+ [0-9]+:[0-9]+)')
        date = datetime.strptime(pattern.findall(author.text)[0], '%Y/%m/%d %H:%M')
        dateInt = int(date.timestamp())
        print(link,"(%d/%d)"%(index, len(news)))
        for interference in article.findAll("div"):
            if(not interference.get('id')=="news_detail_div"):
                interference.clear()
        newArticle(link=link,title=title, text=first+'\n'+article.text, source="tvbs", category=cate, time=dateInt)
    else: print("skip")
