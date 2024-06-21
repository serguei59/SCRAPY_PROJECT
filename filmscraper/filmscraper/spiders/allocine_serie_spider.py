import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AllocineSerieSpiderSpider(CrawlSpider):
    name = "allocine_serie_spider"
    allowed_domains = ["www.allocine.fr"]

    start_urls = [f"https://www.allocine.fr/series-tv/?page={j}" for j in range(1,5)]

    allocine_serie_details = LinkExtractor(restrict_xpaths="//h2/a")
    rules_allocine_serie_details = Rule(allocine_serie_details, 
                                        callback="parse_item",
                                        follow=False)

    rules = (
        rules_allocine_serie_details,
        )

    def parse_item(self, response):
        yield{
            'title' : response.xpath("//h1[@class='item']/text()").get(),
            'titre original' : response.xpath("//span[@class='light']/following-sibling::strong/text()").get(),
            'score_presse' : response.xpath("//div[@class='rating-item-content']//span[@class='stareval-note']/text()").get(),
            'score_spectateur' : response.xpath("(//div[@class='rating-item-content']//span[@class='stareval-note']/text())[2]").get(),
            'genre' : response.xpath("//span[text()='|']/following-sibling::span[contains(@class,'dark-grey-link')]/text()").getall(),
            'annee' : response.xpath("(//span[@class='spacer']/preceding-sibling::text())[1]").get(),
            'duree' : response.xpath("(//span[@class='spacer']/following-sibling::text())[1]").get(),
            'description' : response.xpath("//p[@class='bo-p']/text()").getall(),
            'acteurs' :  response.xpath("//span[text()='Avec']/following-sibling::span/text()").getall(),
            'realisateur' : response.xpath("//a[@class='dark-grey-link']/text()").getall(),
            ##Public
            'pays_d_origine' : response.xpath("//span[text()='Nationalité']/following-sibling::span/text()").get() or response.xpath("//div[@class='meta-body-item meta-body-nationality']//span[contains(@class,'dark-grey-link')]/text()").getall(),
            ##Langue d’origine :
            'nombre_de_saisons' : response.xpath("(//div[@class='stats-item']/text())[1]").get(),
            'nombre_d_episodes' : response.xpath("(//div[@class='stats-item']/text())[2]").get(),
            
        }
        """ item = {}
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        return item """
