import scrapy
from scrapy_splash import SplashRequest


class TgddSpider(scrapy.Spider):
    name = "tgdd"
    allowed_domains = ["www.thegioididong.com"]
    start_urls = ["https://www.thegioididong.com/dtdd"]
    crawled_data = set()

    def parse(self, response):
        for product in response.xpath("//ul[@class='listproduct']/li"):
            link_phone_tgdd = product.xpath(".//a[@class='main-contain ']/@href").get()
            name_phone_tgdd = product.xpath(".//a[@class='main-contain ']/h3/text()").get()
            clean_name = name_phone_tgdd.strip()
            # yield{
            #     "link_phone_tgdd": link_phone_tgdd,
            #     "name_phone_tgdd": clean_name
            # }
            self.crawled_data.add(link_phone_tgdd)
            if clean_name == "Samsung Galaxy A14 4G":
                yield scrapy.Request(url=response.urljoin(link_phone_tgdd), callback=self.parse_phone_page)

    def parse_phone_page(self, response):
        link_phone_tgdd = response.url
        print(response)
        cmtphone_tgdd = response.xpath("//div[@class='box-border']/div")
        link_cmt = cmtphone_tgdd.xpath(".//a[@class='comment-btn__item right-arrow']/@href").get()
        yield scrapy.Request(url=response.urljoin(link_cmt), callback=self.parse_cmtphone_page)
        
    def parse_cmtphone_page(self, response):
        link_cmtphone_tgdd = response.url
        print(response)
        total_rating = response.xpath("//div[@class='rating-star rating-viewall']/div/p/text()").get()
        total_cmt = response.xpath("//div[@class='content-wrap']/input/@value").get()
        five_rating = response.xpath("//ul[@class='rating-list']/li/p/text()").get()
        
        yield{
            "total_rating": total_rating,
            "total_cmt": total_cmt,
            "five_rating": five_rating
        }
        for product in response.xpath("//div[@class='comment comment--all ratingLst']/div"):
            cmt_phone_tgdd = product.xpath(".//div[@class='comment-content']/p/text()").get()
            date_buy = product.xpath(".//div[@class='item-click']")
            date_buy = date_buy.xpath("./a[@class='click-use']/div/div/div/p/text()").getall()
            if cmt_phone_tgdd and date_buy:
                yield{
                    "title_phone_tgdd": cmt_phone_tgdd.strip(),
                    "date_buy": date_buy
                }
        # i=1
        # total_page = response.xpath("//div[@class='pagcomment']/a[4]/text()").get()
        # total_page = int(total_page)
       
        # next_page = "https://www.thegioididong.com/dtdd/samsung-galaxy-a14/danh-gia?s=5&p=" + str(i)
        # yield scrapy.Request(url=next_page, callback=self.parse_cmtphone_page)
    
    
        
        
