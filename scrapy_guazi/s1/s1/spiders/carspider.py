# coding: utf8
import scrapy
from  scrapy.spiders import CrawlSpider, Rule
from s1.items import S1Item
from scrapy.linkextractors import LinkExtractor


class CarSpider(CrawlSpider):
    name = 'guazi'

    start_urls = ['http://www.guazi.com/www/buy/o1/']

    # rules = [
    #     Rule(LinkExtractor(allow=(r"/www/buy/o\d+?/")),callback='parse_list',follow=True)  # 利用linkextractors 翻页
    # ]

    def parse(self, response):
        domain = 'http://www.guazi.com'

        for car in response.xpath('//div[@class="list-infoBox"]'):
            item = S1Item()

            car_info = car.xpath('.//p[@class="infoBox"]/a/text()').extract()[0].split(' ')
            item['car'] = car_info[0]
            item['addition'] = ','.join(car_info[1:])
            item['link'] = domain + car.xpath('.//p[@class="infoBox"]/a/@href').extract()[0]
            item['price'] = car.xpath('.//i[@class="fc-org priType"]/text()').extract()[0].strip()[:-1]
            item['dirving'] = ''.join(car.xpath('.//p[@class="fc-gray"]/text()').extract()).strip()[2:-3]
            item['data'] = car.xpath('.//p[@class="fc-gray"]/span[2]/text()').extract()[0]
            item['local'] = car.xpath('.//span[@class="ctag-green"]/text()').extract()[0]
            item['img'] = car.xpath('.//img/@src').extract()[0]

            yield scrapy.Request(url=item['link'], callback=self.parse_detail, meta={'item': item})
        if response.xpath('//a[@class="next"]'):
            # if int(response.xpath('//a[@class="next"]/@href').extract()[0][30:-1])  < 10:  #可设定翻页数
            yield scrapy.Request(domain + response.xpath('//a[@class="next"]/@href').extract()[0])

    def parse_detail(self, response):
        item = response.meta['item']

        item['jiaoqiangxian'] = response.xpath('//li[@class="baoxian"]/text()').extract()[0]
        item['shangyexian'] = response.xpath('//li[@class="baoxian"]/text()').extract()[1]
        yield item
