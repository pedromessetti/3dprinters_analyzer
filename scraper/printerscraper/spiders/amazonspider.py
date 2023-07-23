import scrapy
from datetime import date
from printerscraper.items import PrinterItem


class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com/s?k=3d+printer&i=industrial&rh=n%3A6066127011"]
    source_name = "test"
    scraped_date = date.today()

    custom_settings = {
        "FEEDS": {
            f"{source_name}_{scraped_date}.json" : {"format": "json", "encoding": "utf8", "overwrite": True}
        }
    }

    def parse(self, response):
        urls = response.css("h2 a::attr(href)").getall()

        for url in urls:
            relative_url = 'https://www.amazon.com' + url
            yield scrapy.Request(relative_url, callback=self.parse_printer_page)

        ## Next Page        
        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.amazon.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)


    def parse_printer_page(self, response):
        printer_item = PrinterItem(
            fonte=self.source_name,
            date=self.scraped_date,
            name=response.css("div#ppd span#productTitle::text").get(default="Unknow"),
            brand=response.css("div#productOverview_feature_div table td.a-span9 span::text").get(default="Unknow"),
            price=response.css("div#ppd span.a-price span::text").get(default="0"),
            currency="$",
            available=True,
            rating=response.css("div#customerReviews div.AverageCustomerReviews span::text").get(default="0"),
            num_reviews=response.css("div#customerReviews div.averageStarRatingNumerical span::text").get(default="0"),
            url=response.url
        )
    
        yield printer_item
