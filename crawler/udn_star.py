# UDN
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import  sleep
import json
from bs4 import BeautifulSoup
import requests
from record import newArticle
from datetime import datetime

url = "https://stars.udn.com/star/cate/10087" 
cate = "star"
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
    
news_list = driver.find_element(By.CLASS_NAME, 'content-list')
links = news_list.find_elements(By.CLASS_NAME, "content-list__link")
news = list(filter(lambda item: item[0] != '', map(lambda item: (item.get_attribute("title"), item.get_attribute("href")), links)))
print("%d"%len(news))

# driver.close()
for (index,(title, link)) in enumerate(news, start=1):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    date = soup.find(class_="article-content__subinfo--time")
    article = soup.find("section", class_="article-content__editor")

    if(article and date):
        date = datetime.strptime(date.text, '%Y-%m-%d %H:%M')
        dateInt = int(date.timestamp())
        print(link,"(%d/%d)"%(index, len(news)))
        for figure in article.findAll("figure"):
            figure.clear()

        blockQuote = article.find(class_="article-blockquote") # 文章推薦被當成內文
        if(blockQuote):
            blockQuote.clear() 

        newArticle(link=link, title=title, text=article.text, source="udn", category=cate, time=dateInt)
    else: print("skip")
