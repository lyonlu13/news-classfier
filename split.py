# 分割資料集
import sqlite3
con = sqlite3.connect('articles.db')
cursorObj = con.cursor()

types = ['finance', 'global', 'society', 'sport', 'star']
sources = ['udn', 'chinatimes', 'tvbs']


def idType(item):
    tmp = list(item)
    tmp[6] = types.index(tmp[6])
    return tuple(tmp)

def idSource(item):
    tmp = list(item)
    tmp[5] = sources.index(tmp[5])
    return tuple(tmp)


def splitType(t):
    query = "select * from article where type='%s' ORDER BY RANDOM()"%t
    check = cursorObj.execute(query) 
    res = check.fetchall()
    cursorObj.executemany('INSERT INTO train VALUES(?, ?, ?, ?, ?, ?, ?, ?);', res[:450])
    cursorObj.executemany('INSERT INTO test VALUES(?, ?, ?, ?, ?, ?, ?, ?);', res[450:])
    con.commit()

for type in types:
    splitType(type)