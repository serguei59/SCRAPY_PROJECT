# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FilmsAllocinescraperItem(scrapy.Item):
    title = scrapy.Field()
    titreOriginal = scrapy.Field()
    scorePresse = scrapy.Field()
    scoreSpectateur = scrapy.Field()
    genre = scrapy.Field()
    annee = scrapy.Field()
    duree = scrapy.Field()
    description = scrapy.Field()
    acteurs = scrapy.Field()
    realisateur = scrapy.Field()
    public = scrapy.Field()
    paysOrigine = scrapy.Field()
    langueOrigine = scrapy.Field()
    

class SeriesAllocinescraperItem(scrapy.Item):
    title = scrapy.Field()
    titreOriginal = scrapy.Field()
    scorePresse = scrapy.Field()
    scoreSpectateur = scrapy.Field()
    genre = scrapy.Field()
    annee = scrapy.Field()
    duree = scrapy.Field()
    description = scrapy.Field()
    acteurs = scrapy.Field()
    realisateur = scrapy.Field()
    paysOrigine = scrapy.Field()
    nombreDeSaisons = scrapy.Field()
    nombreEpisodes = scrapy.Field()

    

  