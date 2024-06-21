# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class FilmscraperPipeline:
    #un process item par spider
    def process_item(self, item, spider):
        item = self.clean_duree(item)
        return item
    
class FilmsAllocinescraperPipeline:
    def process_item(self, item, spider):
        item = self.clean_duree(item)
        return item


    def clean_duree(self,item):
        adapter = ItemAdapter(item)
        duree = adapter.get('duree')
        #recuperer les heures
        h = int(re.search(r"\d+(?=h)", duree).group(0))
        #recuperer les min
        mn = int(re.search(r"\d+(?=min)", duree).group(0))
        #calculer le total de mn
        cleaned_duree = h*60 + mn
        adapter['duree'] = cleaned_duree
        return item

class SeriesAllocinescraperPipeline:
    def process_item(self,item,spider):
        return item


