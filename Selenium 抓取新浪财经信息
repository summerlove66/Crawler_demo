import time

from bs4 import BeautifulSoup
from selenium import webdriver

k = 2
driver = webdriver.Chrome()
driver.get('http://vip.stock.finance.sina.com.cn/q/go.php/vIR_RatingNewest/index.phtml')

while k < 6:
    time.sleep(6)
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    for tr in range(2, 42):
        bsj = bs.select('tr:nth-of-type({})'.format(tr))[0]
        # print(bsj.select('td:nth-of-type(2)')[0].text,bsj.select('td:nth-of-type(2) span')[0]['id'][5:],bsj.select('[id^="price"]')[0].text)
        bj = bsj.select('[id]')
        print(bj[0].text, '\t', bj[0].get('id')[5:], '\t', bj[1].text, '\t', bj[2].text)

    driver.find_element_by_link_text("{}".format(k)).click()
    k = k + 1
