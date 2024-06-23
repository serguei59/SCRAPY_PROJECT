import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from filmscraper.items import SeriesAllocinescraperItem


class AllocineSerieSpiderSpider(CrawlSpider):
    name = "allocine_serie_spider"

    allowed_domains = ["www.allocine.fr"]

    start_urls = [f"https://www.allocine.fr/series-tv/?page={j}" for j in range(1,2)]

    custom_settings ={
            "ITEM_PIPELINES" : {
    "filmscraper.pipelines.SeriesAllocinescraperPipeline":100,

}
        
    }

    allocine_serie_details = LinkExtractor(restrict_xpaths="//h2/a")
    rules_allocine_serie_details = Rule(allocine_serie_details, 
                                        callback="parse_item",
                                        follow=False)

    rules = (
        rules_allocine_serie_details,
        )

    def parse_item(self, response):
        item = SeriesAllocinescraperItem()
        
        item['title'] = response.xpath("//h1[@class='item']/text()").get()
        item['titreOriginal'] = response.xpath("//span[@class='light']/following-sibling::strong/text()").get()
        item['scorePresse'] = response.xpath("//div[@class='rating-item-content']//span[@class='stareval-note']/text()").get()
        item['scoreSpectateur'] = response.xpath("(//div[@class='rating-item-content']//span[@class='stareval-note']/text())[2]").get()
        item['genre'] = response.xpath("//span[text()='|']/following-sibling::span[contains(@class,'dark-grey-link')]/text()").getall()
        item['annee'] = response.xpath("(//span[@class='spacer']/preceding-sibling::text())[1]").get()
        item['duree']= response.xpath("(//span[@class='spacer']/following-sibling::text())[1]").get()
        item['description']= response.xpath("//p[@class='bo-p']/text()").getall()
        item['acteurs'] =  response.xpath("//span[text()='Avec']/following-sibling::span/text()").getall()
        item['realisateur'] = response.xpath("//a[@class='dark-grey-link']/text()").getall()
        ##Public
        item['paysOrigine'] = response.xpath("//span[text()='Nationalité']/following-sibling::span/text()").get() or response.xpath("//div[@class='meta-body-item meta-body-nationality']//span[contains(@class,'dark-grey-link')]/text()").getall()
        ##Langue d’origine :
        item['nombreDeSaisons'] = response.xpath("(//div[@class='stats-item']/text())[1]").get()
        item['nombreEpisodes'] = response.xpath("(//div[@class='stats-item']/text())[2]").get()
            
        yield item
