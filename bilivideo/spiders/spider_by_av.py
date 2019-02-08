# -*- coding: utf-8 -*-
from scrapy import Spider
import re
from scrapy import Request
from scrapy.loader import ItemLoader
from bilivideo.items import BilivideoItem

class SpiderByAvSpider(Spider):
    name = 'spider_by_av'
    allowed_domains = ['www.bilibili.com']

    def __init__(self, *args, **kwargs):

        # Get start_urls from command line input
        super(SpiderByAvSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('url')]

    def start_requests(self):

        # Headers
        headers = {
         #'Host': ,
         'Origin': 'https://www.bilibili.com',
         'Connection': 'keep-alive',
         'Referer' : self.start_urls[0],
         'Upgrade-Insecure-Requests': '1',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
         'Accept': '*/*',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        }
        requests = []
        requests.append(Request(url=self.start_urls[0], headers=headers))
        return requests

    def parse(self, response):

        # The video source is embedded in the <script> tag
        playinfo = response.xpath('//script[contains(.,"window.__playinfo__")]/text()').extract()[0]
        playinfo = playinfo.encode('utf-8')

        # Get the video source url
        patn = re.compile('(?<="url":").+(?=","backup_url")')
        video_src = patn.search(playinfo).group()

        yield {'video_src': video_src, 'video_url': self.start_urls[0],}
