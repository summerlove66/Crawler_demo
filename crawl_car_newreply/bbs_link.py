# coding: utf8
from mysql.connector import connect
import requests

from bs4 import BeautifulSoup

conn = connect(user='root', password='123', database='test3')
cur = conn.cursor()
cur.execute('drop table if exists qichelink')
cur.execute(
    'create table if not exists qichelink(ID int PRIMARY key, Category  varchar(100), Name varchar(100)  ,Link varchar (200)  )')

res = requests.get('http://club.autohome.com.cn/')

html = res.text

bs = BeautifulSoup(html, 'html.parser')

j = 1
for sel in bs.select('.tab-content-item'):
    if sel['id'] != 'tab-7':


        for ele in sel.select('li a'):
            item = {}
            item['link'] = 'http://club.autohome.com.cn' + ele['href']
            item['name'] = ele.text
            if sel['id'] == 'tab-4':
                item['cate'] = '车系论坛'
            elif sel['id'] == 'tab-5':
                item['cate'] = '地方论坛'
            else:
                item['cate'] = '主题论坛'

            sql = 'insert into qichelink (ID,Category,Name ,Link)VALUES (%s,%s,%s,%s)'
            cur.execute(sql, (j, item['cate'], item['name'], item['link']))
            j = j + 1

conn.commit()
conn.close()
