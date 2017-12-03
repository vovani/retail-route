import scrapy
import json
import datetime
import urlparse
import os
from glob import glob

class SuperpharmSpider(scrapy.Spider):
    name = 'rami_levi'
    queries = [
        {
            'type': 'PriceFull',
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
        },
        {
            'type': 'PromoFull',
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
        },
        {
            'type': 'StoresFull',
            'date': datetime.datetime.now().strftime("%Y-%m-%d"),
        }
    ]

    start_urls = ['http://url.retail.publishedprices.co.il']

    def parse(self, response):
        self.logger.info("Got response from {}".format(response.url))
        import ipdb; ipdb.set_trace()
    #     already_downloaded =map(lambda p: os.path.splitext(os.path.basename(p))[0],
    #                             glob(self.settings['FILES_STORE'] + "/*.xml"))
    #     for l in response.xpath("//a[@class='price_item_link']"):
    #         name = l.xpath("../../td[2]/text()").extract_first()
    #         if os.path.splitext(name)[0] in already_downloaded:
    #             continue
    #         request = response.follow(l.xpath("@href").extract_first(), self.parse_download_link)
    #         request.meta['base'] = response.url
    #         request.meta['name'] = name
    #         yield request
    #
    #     page_links = response.xpath("//div[@class='page_link']/a")
    #     next_page_link = filter(lambda s: s.xpath('text()').extract_first() == '>', page_links)
    #     last_page_link = filter(lambda s: s.xpath('text()').extract_first() == '>>', page_links)
    #     assert len(next_page_link) <= 1
    #     if len(next_page_link) == 1:
    #         yield response.follow(next_page_link[0].xpath('@href').extract_first(), self.parse)
    #     elif len(last_page_link) == 1:
    #         yield response.follow(last_page_link[0].xpath('@href').extract_first(), self.parse)
    #
    # def parse_download_link(self, response):
    #     j = json.loads(response.body)
    #     yield {'file_urls': [urlparse.urljoin(response.meta['base'], j['href'])], 'name': response.meta['name']}

