import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FilmspiderSpider(CrawlSpider):
    name = "filmspider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?adult=include"]

    #rules = (Rule(LinkExtractor(allow=r"Items/"), callback="parse_item", follow=True),)
    #the_film_details = LinkExtractor(restrict_xpaths="//a[@class='ipc-title-link-wrapper']")
    the_film_details =LinkExtractor(allow=r".+/title/tt\d+/\?ref_=sr_t_.+", )
    rule_film_details = Rule(the_film_details,
                             callback="parse_item",
                             follow=True)
    rules = (
        rule_film_details,
    )

    def parse_item(self, response):
        yield{
            'title' : response.xpath("//h1/span/text()").get(),
            'url' : response.url
            

        }



        #item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        #return item
