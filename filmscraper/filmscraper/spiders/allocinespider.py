import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from filmscraper.items import FilmsAllocinescraperItem


class AllocinespiderSpider(CrawlSpider):
    name = "allocinespider"
    allowed_domains = ["www.allocine.fr"]

    start_urls = [f"https://www.allocine.fr/films/?page={i}" for i in range(1,100)]

    custom_settings = {
        "ITEM_PIPELINES" : {
    "filmscraper.pipelines.FilmsAllocinescraperPipeline":100,

}

    }

    allocine_films_details = LinkExtractor(restrict_xpaths="//h2/a")
    rules_allocine_details = Rule(allocine_films_details,
             callback="parse_item", 
             follow=False)

    rules = (
        rules_allocine_details,
    )

    def parse_item(self, response):
        item = FilmsAllocinescraperItem()
        
        item['title'] = response.xpath("//h1[@class='item']/text()").get()
        item['titreOriginal'] = response.xpath("//div[@class='meta-body']//span[@class='dark-grey']/text()").get()
        item['scorePresse'] = response.xpath("//div[@class='rating-item-content']//span[@class='stareval-note']/text()").get()
        item['scoreSpectateur'] = response.xpath("(//div[@class='rating-item-content']//span[@class='stareval-note']/text())[2]").get()
        item['genre'] = response.xpath("//span[text()='|']/following-sibling::span[contains(@class,'dark-grey-link')]/text()").getall()
        item['annee'] = response.xpath("//span[contains(@class,'date blue-link')]/text()").get() if response.xpath("//span[contains(@class,'date blue-link')]/text()").get() != None else response.xpath("(//span[contains(@class,'date')]/text())[1]").get()
        item['duree'] = response.xpath("(//span[@class='spacer']/following-sibling::text())[1]").get()
        item['description'] = response.xpath("//p[@class='bo-p']/text()").get()
        item['acteurs'] = response.xpath("//div[@class='meta-body-item meta-body-actor']//span[contains(@class,'dark-grey-link')]/text()").getall()
        item['realisateur'] = response.xpath("//span[text()='De']/following-sibling::span/text()").get()
        item['public'] = response.xpath("//span[@class='certificate-text']/text()").get()
        item['paysOrigine'] = response.xpath("//span[contains(@class,'nationality')]/text()").getall()
        item['langueOrigine'] = response.xpath("(//span[@class='that']/text())[10]").get()

        yield item