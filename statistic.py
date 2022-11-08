# 統計資料集組成
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

con = sqlite3.connect('articles.db')
cursorObj = con.cursor()

query="select type, source, count(*) from article group by type, source;"
check=cursorObj.execute(query) 
res = check.fetchall()

udn = filter(lambda x: x[1]=='udn', res)
chinatimes = filter(lambda x: x[1]=='chinatimes', res)
tvbs = filter(lambda x: x[1]=='tvbs', res)


left = np.array([1,2,3,4,5])
height1 = np.array(list(map(lambda x: x[2], udn)))
height2 = np.array(list(map(lambda x: x[2], chinatimes)))
height3 = np.array(list(map(lambda x: x[2], tvbs)))

height1_2=list(height1[i]+height2[i] for i in range(0, len(height1)))
height1_2_3=list(height1_2[i]+height3[i] for i in range(0, len(height1)))

labels = ['財經', '國際', '社會', '體育', '娛樂']


font = fm.FontProperties(fname="C:/Windows/Fonts/msjh.ttc")
plt.bar(left, height1, color='#f46c00', label='聯合報')
plt.bar(left, height2, bottom=height1, color='#d8262c', label='中國時報')
plt.bar(left, height3, bottom=height1_2, color='#044996', label='TVBS')
plt.xticks(left, labels, fontproperties=font)

for index, value in enumerate(height1_2_3):
    plt.text(index+0.9, value+5,
             str(value))


plt.title("資料集構成",fontsize=20, fontproperties=font)

plt.legend(loc='lower right', shadow=True, prop=font) 
plt.show()
