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
        item = self.clean_annee(item)
        item = self.clean_duree(item)
        item = self.clean_langue(item)
        item = self.clean_realisateur(item)
        item = self.clean_title(item)
        item = self.clean_titreOriginal(item)
        return item

    def clean_annee(self,item):
        adapter = ItemAdapter(item)
        annee = adapter.get('annee')
        print(annee)
        #supprimer le /n 1
        cleaned_annee = annee.strip()
        print(cleaned_annee)
        adapter['annee']= cleaned_annee
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
    
    def clean_langue(self,item):
        adapter = ItemAdapter(item)
        langue = adapter.get('langueOrigine')
        cleaned_langue = langue.strip()
        adapter['langueOrigine'] = cleaned_langue
        return item
    
    def clean_realisateur(self,item):
        adapter = ItemAdapter(item)
        realisateur = adapter.get('realisateur')
        cleaned_realisateur = realisateur.strip()
        adapter['realisateur'] = cleaned_realisateur
        return item
    
    def clean_title(self,item):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        cleaned_title = title.strip()
        adapter['title'] = cleaned_title
        return item
    
    def clean_titreOriginal(self,item):
        adapter = ItemAdapter(item)
        titreOriginal = adapter.get('titreOriginal')
        cleaned_titreOriginal = titreOriginal.strip() if titreOriginal else titreOriginal
        adapter['titreOriginal'] = cleaned_titreOriginal
        return item    
    
    

class SeriesAllocinescraperPipeline:
    def process_item(self, item, spider):
        item = self.clean_annee(item)
        item = self.clean_duree(item)
        item = self.clean_title(item)
        item = self.clean_titreOriginal(item)
        return item
    
    def clean_annee(self,item):
        adapter = ItemAdapter(item)
        annee = adapter.get('annee')
        print(annee)
        #supprimer le /n 1
        cleaned_annee = annee.strip()
        print(cleaned_annee)
        adapter['annee']= cleaned_annee
        return item
    
    def clean_duree(self,item):
        adapter = ItemAdapter(item)
        duree = adapter.get('duree')
        cleaned_duree = duree.strip()
        adapter['duree'] = cleaned_duree
        return item
    
    
    def clean_title(self,item):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        cleaned_title = title.strip()
        adapter['title'] = cleaned_title
        return item
    
    def clean_titreOriginal(self,item):
        adapter = ItemAdapter(item)
        titreOriginal = adapter.get('titreOriginal')
        cleaned_titreOriginal = titreOriginal.strip() if titreOriginal else titreOriginal
        adapter['titreOriginal'] = cleaned_titreOriginal
        return item 
    



