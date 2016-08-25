#coding: utf8
import datetime
import requests
import mysql.connector
from bs4 import BeautifulSoup
import time
from collections import OrderedDict
import re
import qicheset
#from  multiprocessing.dummy import Pool

conn = mysql.connector.connect(user='root', password='123', database='test3',charset ='utf8mb4')

cur = conn.cursor()
cur.execute(
    'create table if not exists postcontent1(ReplyTime varchar(100), NickName varchar(100) ,RegTime varchar(100), Local varchar(100) ,Car varchar(100), Content text) default charset = utf8mb4')


#时间转换为时间戳
def process(t):
    timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp



#取出所有bbs 链接
def get_bbs_link():
    # SELECT Link  FROM qichelink AS r1 JOIN (SELECT ROUND(RAND() * (SELECT MAX(id) FROM qichelink)) AS id) AS r2 WHERE r1.id >= r2.id ORDER BY r1.id ASC LIMIT 500
    cur.execute('select Link from qichelink limit 150 ,20')
    all_bss_link = cur.fetchall()
    for  bbs in all_bss_link:
       yield bbs[0]



topic_set=set()

def get_lastmodify( link ):#抓取链接
    global topic_set

    # for i in range(1,6):  # 6页之前的内容
    #     link = link[:-6] +'i'+'.html'
    with  requests.get (link).text  as html:
    # res = requests.get (link)
    # html = res.text
        bs = BeautifulSoup(html ,'html.parser')
        for topic in bs.select('div.carea dl.list_dl'):

            modify_time =topic.select('span.ttime')
            if modify_time  and  process(modify_time[0].text +':00') >last_crawl_timestamp :
                # tlt =topic.select('dt a')[0].text
                tlt_link ='http://club.autohome.com.cn/'+topic.select('dt a')[0].get('href')
                topic_set.add(tlt_link)


k = 0  # 抓取个数
def  get_new_reply(link):  #参数为帖子网址
    with requests.get(link).text as html:
    # res =requests.get(link)
    # html =res.text
        bs = BeautifulSoup(html ,'html.parser')
        if bs.select('span.fs'):
            page_info =bs.select('span.fs')[0].text
            page_num = page_info.split(' ')[2]

            # print page_num
            flag=True
            for i in range(1,int(page_num) +1)[::-1]:
                if flag ==True:
                     url = link[:-6] + str(i)+ link[-5:]   #这个帖子各页的url 从最后一页开始向前检索
                     # print url
                     html =requests.get(url).text
                     bsj=BeautifulSoup(html,'html.parser')
                     for div in  bsj.select('.clearfix.contstxt.outer-section')[::-1]: #从最后一个回复向上检索
                        item =OrderedDict()
                        reply_time =div.select('span[xname]')[0].text
                        if process(reply_time) > last_crawl_timestamp:
                            # print "".join(div.select('div.rconten')[0].text.split())
                            cont=div.select('div.rconten')[0].text
                            cont_no_space =re.sub('\s+','',cont)  # 灭空格
                            content= re.sub('.*?:\d\d:\d\d','',cont_no_space)  #截断前面用户信息内容
                            item['time'] = reply_time

                            item['nickname'] =(div.select('.txtcenter.fw')[0].text).strip()

                            if div.select('ul.leftlist > li:nth-of-type(5)'):
                                item['reg_time'] = div.select('ul.leftlist > li:nth-of-type(5)')[0].text
                            else:
                                item['reg_time'] =''
                            if div.select('ul.leftlist > li:nth-of-type(6)'):
                                 item['local'] =  div.select('ul.leftlist > li:nth-of-type(6)')[0].text
                            else:
                                item['local'] =''
                            if div.select('ul.leftlist > li:nth-of-type(7)'):
                                item['car'] =div.select('ul.leftlist > li:nth-of-type(7)')[0].text
                            else:
                                item['car'] =''
                            item['content'] = content



                            try:
                                # cursor =conn.cursor()

                                cur.execute('insert into  postcontent1() values (%s,%s,%s,%s,%s,%s)',item.values())
                                global k
                                k =k+1

                            except :

                                print (item)
                                continue

                        else:
                            flag = False

def log_time(timeStamp):

    timeArray = time.localtime(timeStamp)
    format_Time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return  format_Time





if __name__ == '__main__':
    start_crawl_time =time.time()
    last_crawl_timestamp = process('2016-8-20 12:00:00')
    pool =Pool(10)
    #
    # pool.map(get_lastmodify, get_bbs_link())
    pool.map(get_new_reply,topic_set)
    c = 1    # 提交次数
    try:
        pool.map(get_lastmodify,get_bbs_link())
        for i in topic_set:
            try:
                get_new_reply(i)
                if time.time() -start_crawl_time >1800* c: # 每隔 半个小时 写入一次
                        conn.commit()
                c = c + 1

            except:
                continue

    finally:
        f = open('log.txt','a')
        f.write(
        '{}\t帖子更新开始时间:{},抓取时间:{},结束时间：{},耗时：{} h ,抓取{}条信息\n '.format(str(datetime.date.today()),
                                                        log_time(last_crawl_timestamp),log_time(start_crawl_time),log_time(time.time()),round((time.time()-start_crawl_time)/3600 ,2),k))
        f.close()
        conn.commit()
        conn.close()
