# UDN 聯合
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import  sleep
import json
from bs4 import BeautifulSoup
import requests
from record import newArticle, check
from datetime import datetime

url = "https://udn.com/rank/newest/2/7227/1" 
cate = "sport"
max_it = 8

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
    sleep(0.3)
    max_it -= 1
    print(max_it)
    
news_list = driver.find_element(By.CLASS_NAME, 'context-box__content')
news_item = news_list.find_elements(By.CLASS_NAME, "story-list__news")
links = map(lambda item: item.find_element(By.CLASS_NAME, "story-list__text").find_element(By.TAG_NAME, "a"), news_item)

news = list(filter(lambda item: item[0] != '', map(lambda item: (item.get_attribute("title"), item.get_attribute("href")), links)))
print("%d"%len(news))

driver.close()
for (index,(title, link)) in enumerate(news, start=1):
    if(not check(link)):
        continue
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    date = soup.find("time", class_="article-content__time")
    article = soup.find("section", class_="article-content__editor")

    if(article and date):
        date = datetime.strptime(date.text, '%Y-%m-%d %H:%M')
        dateInt = int(date.timestamp())
        print(link,"(%d/%d)"%(index, len(news)))
        for figure in article.findAll("figure"):
            figure.clear()
        newArticle(link=link,title=title, text=article.text, source="udn", category=cate, time=dateInt)
    else: print("skip")
