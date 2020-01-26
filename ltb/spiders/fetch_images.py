import scrapy

from ltb.utils import add_url_param, get_url_param
from ltb.items import LtbItem


class ImageSpider(scrapy.Spider):
    name = "images"

    def start_requests(self):
        urls = [
            "https://shop.ltbjeans.com/tr/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        category_xpath = '//ul[@class="top-menu"]/li/a[@class="with-subcategories"]/@href'
        for href in response.xpath(category_xpath).extract():
            if href != "#":
                request = scrapy.Request(response.urljoin(href),
                                         callback=self.follow_next_page)
                yield request
    
    def follow_next_page(self, response):
        nxt_pg_param = 'sayfano'

        for next_page_num in range(2, 100):
            next_page_url = add_url_param(
                response.request.url, {nxt_pg_param: next_page_num}
            )
            request = scrapy.Request(next_page_url, callback=self.fetch_images)
            yield request            

    def fetch_images(self, response):
        image_sources = response.xpath('//img[@class="product-image"]/@src').extract()
        
        item = LtbItem()
        item["image_urls"] = image_sources

        yield item
