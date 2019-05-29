# -*- coding: utf-8 -*-
import scrapy


class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    start_urls = ['http://fz.maitian.cn/zfall/PG1']

    def parse(self, response):
        title_list = response.xpath("//div[@class='list_title']")
        for quote in title_list:
            yield {'title': quote.xpath('./h1/a/text()').extract_first().strip().replace('\r\n\r\n', '')}
        next_page_url = response.xpath('//div[@id="paging"]/a[@class="down_page"]/@href').extract_first()
        print(next_page_url)
        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))
