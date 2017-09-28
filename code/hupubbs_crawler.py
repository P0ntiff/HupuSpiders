# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.exporters import XmlItemExporter
#.encode('UTF-8')
import re
def process_div(floor_s):
    text = floor_s.extract()
    if ((text is None) or ('<blockquote>' not in text)):
        return None
    ori_id = floor_s.css(".author .u::attr(href)").extract_first()
    ori_floor = floor_s.css(".f666 a::attr(id)").extract_first()
    if not ori_floor:
        return None
    ori_floor = int(ori_floor)
    ori_message_s = floor_s.css(".quote-content")
    if not ori_message_s:
        return None
    ori_message = ori_message_s[0].xpath("text()").extract()
    if len(ori_message) != 2:
        return None
    ori_message = ori_message[1] #just a wired convention...
    quote_s = floor_s.css("blockquote")[0]
    pos_id = quote_s.css(".u::attr(href)").extract_first()
    pos_floor = quote_s.css("b").extract_first()
    prefix = "<b>引用"
    #if (pos_floor[:5] != prefix):
    #    print prefix + "!"
    #    print pos_floor[:5] + "!"
    #    return None
    if not pos_floor:
        return None
    pos_floor = pos_floor[5:]
    r = re.compile("[0-9]+")
    pos_floor = r.match(pos_floor)
    if not pos_floor:
        return None
    pos_floor = int(pos_floor.group())
    pos_message = quote_s.css("p").xpath("text()").extract()[1]
    return {
        "ori_id": ori_id,
        "ori_floor" : ori_floor,
        "ori_message" : ori_message,
        "pos_id" : pos_id,
        "pos_floor" : pos_floor,
        "pos_message" : pos_message
    }

def process_page(response):
    floors = response.css(".floor_box")
    if not floors:
        return None
    infos = [process_div(floor) for floor in floors]
    infos = [it for it in infos if it is not None]
    if not infos:
        return None
    ans = {
        'tid': response.css('div.floor a::attr(tid)').extract()[0],
        'reply_infos': infos,
        #'replies_string_array': [s.encode('UTF-8') for s in replies]
    }
    return ans

class HupubbsSpider(scrapy.Spider):
    name = 'hupubbs'
    allowed_domains = ['bbs.hupu.com']
    start_urls = ['http://bbs.hupu.com/']

    def parse(self, response):
        url = response.url
        full_url = response.urljoin(url)
        data = process_page(response)
        yield data

        next_pages = response.css("a::attr(href)").extract()
        for next_page in next_pages:
            if next_page is not None:
                next_page = response.urljoin(next_page)
                data = scrapy.Request(next_page, callback=self.parse)
                yield data
