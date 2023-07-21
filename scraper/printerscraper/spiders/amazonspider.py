import scrapy
from datetime import date
from printerscraper.items import PrinterItem


class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com/s?k=3d+printer"]
    source_name = "Amazon"
    scraped_date = date.today()

    custom_settings = {
        "FEEDS": {
            f"{source_name}_{scraped_date}.json" : {"format": "json", "encoding": "utf8", "overwrite": True}
        }
    }

    def start_requests(self):
        base_url = 'https://www.amazon.com/s?k=3d+printer&i=industrial&rh=n%3A6066127011&dc&page={}&crid=3JH3PIODP5BR1&qid=1689950585&rnid=2941120011&sprefix=%2Caps%2C158&ref=sr_pg_{}'
        num_pages = 50
        
        for page_num in range(1, num_pages + 1):
            yield scrapy.Request(base_url.format(page_num, page_num-1), callback=self.parse)


    def parse(self, response):
        urls = response.css("h2 a::attr(href)").getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_printer_page)

        
    def parse_printer_page(self, response):
        printer_item = PrinterItem(
            fonte=self.source_name,
            date=self.scraped_date,
            name=response.css("div#ppd span#productTitle::text").get(default="Unknow"),
            brand=response.css("div#productOverview_feature_div table td.a-span9 span::text").get(default="Unknow"),
            price=response.css("div#ppd span.a-price span::text").get(default="0"),
            currency="$",
            rating=response.css("div#customerReviews div.AverageCustomerReviews span::text").get(default="0"),
            num_reviews=response.css("div#customerReviews div.averageStarRatingNumerical span::text").get(default="0"),
            url=response.url
        )
    
        yield printer_item