from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from isbullshit.items import IsbullshitItem


class IsBullshitSpider(CrawlSpider):
    """General configuration of the Crawl Spider """
    name = 'isbullshit'
    start_urls = ['http://isbullsh.it']
    allowed_domains = ['isbullsh.it']
    rules = [
        Rule(SgmlLinkExtractor(
            allow=[r'http://isbullsh\.it/\d{4}/\d{2}/\w+'], unique=True),
            callback='parse_blogpost')
    ]

    def parse_blogpost(self, response):
        """ Callback function scraping data from the response html """
        hxs = HtmlXPathSelector(response)
        item = IsbullshitItem()
        item['title'] = hxs.select('//header/h1/text()').extract()[0]
        item['author'] = hxs.select('//header/p/a/text()').extract()[0]
        item['date'] = hxs.select(
            '//header/div[@class="post-data"]'
            '/p[contains(text(), "20")]/text()').extract()[0]
        item['url'] = response.url

        return item
