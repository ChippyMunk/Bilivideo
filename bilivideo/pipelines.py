# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from bilivideo.items import BilivideoItem

class BilivideoPipeline(object):

    def process_item(self, item, spider):
        # Headers for the video source request
        headers={
        'Origin': 'https://www.bilibili.com',
        'Referer': item['video_url'],
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
        }

        v=requests.get(url=item['video_src'],headers=headers,verify=False, stream=True)
        fileav=item['video_url'].split('/')[-1]

        # Write streaming binary data to local mp4 file
        if v.status_code==200:
            print('========================Start Downloading=========================')
            for data in v.iter_content(chunk_size=2048):
                with open(fileav + '.mp4','ab') as f:
                    f.write(data)

            f.close()
            print "========================Downloading Complete========================="
        else:
            print "Downloading Aborted"
            print "Code: " + str(v.status_code)
