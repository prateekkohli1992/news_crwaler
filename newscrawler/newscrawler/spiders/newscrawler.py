import hashlib
import html
import json
import re

import scrapy

from ..items import NewscrawlerItem


def striphtml(data):
    data = html.unescape(data)
    p = re.compile(r'<.*?>')
    data = p.sub(' ', data)

    data = data.replace("\xa0", " ")
    data = re.sub("\s\s+", " ", data)
    return data


class NewsCrawler(scrapy.Spider):
    name = "newsmaker"

    def __init__(self, pages=3, start=1, **kwargs):
        self.start_urls = ['https://www.moneycontrol.com/news/business/']
        with open('./newscrawler/moneycontrol.json') as f:
            data = json.load(f)

        urls = list(data.values())
        self.start_urls.extend(list(data.values())[1:])
        for a in urls:
            for b in range(int(start) + 1, int(pages) + 1):
                self.start_urls.extend([a + "page-" + str(b)])
        # print("______________=---------------------------------------------")
        # print(self.start_urls)

        super().__init__(**kwargs)  # python3

    def parse(self, response):

        dest_urls = response.css("li.clearfix h2 a::attr(href)")

        for url in list(set(dest_urls)):
            # print(url.extract().strip())
            # print("_________________________________________________")
            yield scrapy.Request(url=url.extract().strip(), callback=self.parse_page)

    def parse_page(self, response):
        print("_________________dddddddddddddddddddddddddd")

        rege = r'((\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?)(\d{1,2}(st|nd|rd|th)?)?((\s*[,.\-\/]\s*)\D?)?\s*((19[0-9]\d|20\d{2})|\d{2}).*(IST|AM|\d{1,2})'
        items = NewscrawlerItem()
        date = response.css("#page1 .arttidate::text").extract_first().strip()
        if date is None:
            date = ""
        else:
            date_clean = re.search(rege, date)
            if date_clean[0] is not None:
                date = date_clean[0]

        blogger_name = response.css("#page1 .bloger-name::text")

        if blogger_name is not None and len(blogger_name) > 0:
            blogger_name = response.css("#page1 .bloger-name::text").extract_first().strip()
            blogger_name = re.sub("\s\s+", " ", blogger_name)
            if blogger_name == '':
                blogger_name = response.css("#page1 .bloger-name a::text")
                if len(blogger_name) > 0:
                    blogger_name = response.css("#page1 .bloger-name a::text").extract_first().strip()
                    blogger_name = re.sub("\s\s+", " ", blogger_name)
                else:
                    blogger_name = ""
        else:
            blogger_name = ""

        art_tittle = response.css("#page1 .artTitle::text")

        if art_tittle is not None and len(art_tittle) > 0:
            art_tittle = striphtml(art_tittle.extract_first().strip())
        else:
            art_tittle = ""

        art_subtittle = response.css("#page1 .subhead::text")

        if art_subtittle is not None and len(art_subtittle) > 0:
            art_subtittle = striphtml(art_subtittle.extract_first().strip())
        else:
            art_subtittle = ""

        content_text = response.css("#page1 #article-main p")

        if content_text is not None and len(content_text) > 0:
            content_text = " ".join(
                [striphtml(a.extract().strip()).strip() for a in response.css("#page1 #article-main p")]).strip()
        else:
            content_text = ''

        content_tags = response.css("#page1 .tag_txt a::text")

        if content_tags is not None and len(content_tags) > 0:
            content_tags = ",".join([a.extract().strip() for a in response.css("#page1 .tag_txt a::text")])
        else:
            content_tags = ''

        bread_crum = response.css(".brad_crum a::text")

        if bread_crum is not None and len(bread_crum) > 0:
            bread_crum = ",".join([a.extract().strip() for a in response.css(".brad_crum a::text")])
        else:
            bread_crum = ''

        hash_object = hashlib.md5(response.url.split("/")[-1].replace("html", "").replace("html", "").encode('utf-8'))
        items['key_page'] = hash_object.hexdigest()
        items['date'] = date
        items['blogger_name'] = blogger_name
        items['art_tittle'] = art_tittle
        items['art_subtittle'] = art_subtittle
        items['content_text'] = content_text
        items['content_tags'] = content_tags
        items['bread_crum'] = bread_crum
        print("_________________")
        print(items)
        yield items
