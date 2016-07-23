```
# coding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import re
from bs4 import BeautifulSoup
import sqlite3
# from multiprocessing.dummy import  Pool

conn = sqlite3.connect(r'E:\SQL\sqlite\xiaoshuo.db')
cursor =conn.cursor()


i = 0
def getart(url):
    global i
    i = i+1
    res =requests.get(url)
    res.encoding='utf8'
    info =re.search('<div style="clear:both"></div>(.*?)<div style="clear:both"></div>',res.text,re.S).group()
    textinfo =re.sub('<div style="clear:both"></div>|<p>|</p>','',info)
    title =BeautifulSoup(res.text,'lxml').h1.get_text()
    book =title.split(' ')[0]
    zhangjie =''.join(title.split(' ')[1:] )
    a =dict(BOOK=book,ID=i,SECTION=zhangjie,ARTICLE=textinfo)
    global cursor
    sql="INSERT INTO Mingchao  VALUES(:ID , :BOOK , :SECTION , :ARTICLE)"
    cursor.execute(sql,a)

if __name__ == '__main__':

    res = requests.get('http://www.mingchaonaxieshier.com/')
    bsj=BeautifulSoup(res.text,'lxml')
    link_list=[]
    for link  in bsj.select('td > a'):
        link_list.append(link.get('href'))
    # pool =Pool(2)
    map(getart,link_list)
    conn.commit()
    conn.close()
```











