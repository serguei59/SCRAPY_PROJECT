import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AllocinespiderSpider(CrawlSpider):
    name = "allocinespider"
    allowed_domains = ["www.allocine.fr"]

    start_urls = [f"https://www.allocine.fr/films/?page={i}" for i in range(1,100)]

    allocine_films_details = LinkExtractor(restrict_xpaths="//h2/a")
    rules_allocine_details = Rule(allocine_films_details,
             callback="parse_item", 
             follow=False)

    rules = (
        rules_allocine_details,
    )

    def parse_item(self, response):
        yield{
            'title' : response.xpath("//h1[@class='item']/text()").get(),
            'titre_original' : response.xpath("//div[@class='meta-body']//span[@class='dark-grey']/text()").get(),
            'score_presse' : response.xpath("//div[@class='rating-item-content']//span[@class='stareval-note']/text()").get(),
            'score_spectateur' : response.xpath("(//div[@class='rating-item-content']//span[@class='stareval-note']/text())[2]").get(),
            'genre' : response.xpath("//span[text()='|']/following-sibling::span[contains(@class,'dark-grey-link')]/text()").getall(),
            'annee' : response.xpath("//span[contains(@class,'date blue-link')]/text()").get() if response.xpath("//span[contains(@class,'date blue-link')]/text()").get() != None else response.xpath("(//span[contains(@class,'date')]/text())[1]").get(),
            'duree' : response.xpath("(//span[@class='spacer']/following-sibling::text())[1]").get(),
            'description' : response.xpath("//p[@class='bo-p']/text()").get(),
            'acteurs' : response.xpath("//div[@class='meta-body-item meta-body-actor']//span[contains(@class,'dark-grey-link')]/text()").getall(),
            'realisateur' : response.xpath("//span[text()='De']/following-sibling::span/text()").get(),
            'public' : response.xpath("//span[@class='certificate-text']/text()").get(),
            'pays_d_origine' : response.xpath("//span[contains(@class,'nationality')]/text()").getall(),
            'langue_d_origine' : response.xpath("(//span[@class='that']/text())[10]").get()

        }
        
        """ item = 
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return item
 """