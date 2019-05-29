# -*- coding: utf-8 -*-
from maitian1.items import Maitian1Item
import hashlib
import scrapy
from scrapy_redis.spiders import RedisSpider


class ZufangSpider(RedisSpider):
    name = 'zufangredis'
    # start_urls = ['http://bj.maitian.cn/zfall/PG1']
    # 执行命令lpush zufang:start_urls http://fz.maitian.cn/zfall/PG1
    redis_key = 'zufang:start_urls'

    def parse(self, response):
        title_list = response.xpath("//div[@class='list_title']")

        for quote in title_list:
            item = Maitian1Item()
            title = quote.xpath('./h1/a/text()').extract_first().strip().replace('\r\n\r\n', '')
            id = self.get_md5(title)
            item["id"] = id
            item["title"] = title
            yield item
        next_page_url = response.xpath('//div[@id="paging"]/a[@class="down_page"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def get_md5(self, key):
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        a = m.hexdigest()
        return a
