import scrapy
from scrapy_splash import SplashRequest


class TgddSpider(scrapy.Spider):
    name = "fpt"
    allowed_domains = ["fptshop.com.vn"]
    start_urls = ["https://fptshop.com.vn/dien-thoai"]
    crawled_data = set()

    def parse(self, response):
        print(response)
        print(response.xpath("//div[@class='cdt-product-wrapper m-b-20']").get())
        for product in response.xpath("//div[@class='cdt-product-wrapper m-b-20']/div"):
            link_phone_tgdd = product.xpath(".//div[@class='cdt-product__info']/h3/a/@href").get()
            name_phone_tgdd = product.xpath(".//div[@class='cdt-product__info']/h3/a/text()").get()
            clean_name = name_phone_tgdd.strip()
            yield{
                "link_phone_tgdd": link_phone_tgdd,
                "name_phone_tgdd": clean_name
            }
            # self.crawled_data.add(link_phone_tgdd)
            # if clean_name == "Samsung Galaxy A14 4G":
            #     yield scrapy.Request(url=response.urljoin(link_phone_tgdd), callback=self.parse_phone_page)
