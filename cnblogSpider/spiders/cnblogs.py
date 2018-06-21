# -*- coding: utf-8 -*-
import scrapy
from cnblogSpider.items import CnblogspiderItem
from scrapy.selector import Selector

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://www.cnblogs.com/qiyeboy/default.html?page=1']

    def parse(self, response):
        # 实现网页的解析
        # 首先抽取所有的文章
        papers = response.xpath(".//*[@class='day']")
        # 从每篇文章中抽取数据
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            # print(url,title,time,content)
            item = CnblogspiderItem(url=url,time=time,title=title,content=content)
            yield item
        next_page = Selector(response).re('<a href="(\S*)">下一页</a>')
        # print(next_page)
        if next_page:
            yield scrapy.Request(url=next_page[0],callback=self.parse)