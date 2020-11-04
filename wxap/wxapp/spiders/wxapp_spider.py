# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxap.wxapp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True), #不保存数据不需要回调
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback="parse_item", follow=False)
    )

    def parse_item(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').get()
        author_p = response.xpath('//p[@class="authors"]')
        author = author_p.xpath('./a/text()').get()
        pub_time = author_p.xpath('./span/text()').get()
        print("author%s/pub_time:%s" % (author, pub_time))
        article_content = response.xpath('//td[@id="article_content"]//text()').getall()
        article_content = "".join(article_content).strip()
        item = WxappItem(title=title,author=author,pub_time=pub_time,content=article_content)
        yield item
