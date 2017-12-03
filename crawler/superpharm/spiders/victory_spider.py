import scrapy
import urlparse
import re

class VictorySpider(scrapy.Spider):
    name = 'victory'
    start_urls = ['http://matrixcatalog.co.il/NBCompetitionRegulations.aspx']

    chain_id_to_name = {
        '7290058148776': 'ShukHaIr',
        '7290661400001': 'MahsaneiHaShuk',
        '7290696200003': 'Victory',
        '7290696200690': 'Victory'
    }

    def parse(self, response):
        links = response.xpath("//a[@href]")
        self.logger.info("Num urls {}".format(len(links)))
        for link in links:
            name = link.xpath("../../td[1]/text()").extract_first()
            if name is None:
                continue
            name = name.lower()
            if 'pricefull' in name or 'promofull' in name or 'store' in name:
                chain_id = re.search('[a-zA-Z]*(\d+)', name).group(1)
                yield {'file_urls': [urlparse.urljoin(response.url, link.xpath('@href').extract_first())],
                       'name': name,
                       'store': VictorySpider.chain_id_to_name[chain_id]}