import sqlite3
import re
import os

con = sqlite3.connect('binary.db')
cursorObj = con.cursor()

def parseArticle(article):
    stripped = article.strip().replace("\r", "")
    combineNl =  re.sub("\n+", "\n", stripped)
    pList = combineNl.split("\n")
    return (pList[0], pList[len(pList)-1])
    
def newArticle(link, title, text, source, category, time):
    (head, tail) = parseArticle(text)
    try:
        cursorObj.execute("INSERT INTO article VALUES(?, ?, ?, ?, ?, ?, ?, ?)", 
                    (link, title, head, tail, text, source, category, time))
        res = con.commit()
        print(title)
    except:
        print(title, "failed")

def check(link):
    print(link)
    query=("select exists(select 1 from article where url like '%s') limit 1")%link
    check=cursorObj.execute(query) 
    return check.fetchone()[0]==0



if(__name__ == "__main__"):
    test = parseArticle("\n\r\nadd ge ewgw g3g3g gwg3g \n\n\n\n wdwd g4 qrqr uku ef \n\n wdwdwdwf wqfq g4g4g4g")
    print(test)