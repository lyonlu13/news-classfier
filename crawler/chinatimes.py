# ChinaTimes 中時
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import  sleep
import json
from bs4 import BeautifulSoup
import requests
from record import newArticle
from datetime import datetime

url = "https://www.chinatimes.com/sports/total?page=1&chdtv" 
cate = "sport"
max_it = 10

driver = webdriver.Chrome("./chromedriver.exe")
driver.implicitly_wait(10)
driver.get(url)


news_item = []
driver.maximize_window()
while(max_it>0):
    news_list = driver.find_element(By.CLASS_NAME, 'vertical-list')
    items = news_list.find_elements(By.CLASS_NAME, "articlebox-compact")
    links = map(lambda item: item.find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a"), items)
    news = list(filter(lambda item: item[0] != '', map(lambda item: (item.text, item.get_attribute("href")), links)))
    news_item = news_item+news
    try:
        next_page = driver.find_element("xpath","//a[contains(text(),'下一頁')]")
        if(not next_page): break
    except:
        break
    next_page.click()
    sleep(0.2)
    max_it -= 1
    


print("%d"%len(news_item))

driver.close()
for (index,(title, link)) in enumerate(news_item, start=1):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    date = soup.find("time")
    article = soup.find("div", class_="article-body")

    if(article and date):
        date = datetime.strptime(date['datetime'], '%Y-%m-%d %H:%M')
        dateInt = int(date.timestamp())
        print(link,"(%d/%d)"%(index, len(news_item)))
        text = ""
        for p in article.findAll("p"):
            text += p.text
        newArticle(link=link, title=title, text=text, source="chinatimes", category=cate, time=dateInt)
    else: print("skip")
