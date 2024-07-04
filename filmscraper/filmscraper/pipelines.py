# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

import sqlalchemy

from filmscraper.models import ActeursFilm, ActeursSerie, Film, GenreFilm, GenreSerie, LangueFilm, OrigineFilm, OrigineSerie, Personne, RealisateurFilm, RealisateurSerie, Serie, create_table, db_connect
from sqlalchemy.orm import sessionmaker
import pandas as pd


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
    
class SaveFilmPipeline(object):
    def __init__(self):
        """
        initialization of database connnection and sessionmaker
        creation of tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)        

    def process_item(self, item, spider):
        """
        saving of films in the database
        method called for every item pipeline component            
        """
        session = self.Session()
        film = Film()
        film.titre = item["title"]
        film.titre_original = item["titreOriginal"]
        film.score_presse = item['scorePresse']
        film.score_spectateur = item['scoreSpectateur']
        film.annee = item['annee']
        film.duree = item['duree']
        film.description = item['description']
        film.public = item['public']
        
        session.add(film)
        session.commit()

        # GENREFILM
        for i in range(len(item['genre'])):
            genre_film = GenreFilm()
            genre_film.film_id = film.film_id
            genre_film.genre = item['genre'][i]
            session.add(genre_film)
            session.commit()

        #ORIGINEFILM
        for i in range(len(item['paysOrigine'])):
            origine_film = OrigineFilm()
            origine_film.film_id = film.film_id
            origine_film.pays = item['paysOrigine'][i]
            session.add(origine_film)
            session.commit()

        #LANGUEFILM
        liste_item_langue = item['langueOrigine'].split(",")
        for i in range(len(liste_item_langue)):
            langue_film = LangueFilm()
            langue_film.film_id = film.film_id
            langue_film.langue = liste_item_langue[i]
            session.add(langue_film)
            session.commit()

        #recuperer tous les ACTEURS de FILMS->PERSONNE suivant le spider
        # ->affecter le pipeline dans chacun des spiders: VERIF
        ##type de l item:liste avec val nulles possibles
        ##il faut isoler les couple noms prenoms:ce sont juste les elts de la liste
        ##pour chacun il faut separer le nom du prenom via split avec " " ou ". " comme separateur
        for i in range(len(item['acteurs'])):
            print(item[('acteurs')][i])
            liste_nom_prenom_acteur = item[('acteurs')][i].split(". ", 1) if ". " in item[('acteurs')][i] else item[('acteurs')][i].split(" ", 1)
            print(liste_nom_prenom_acteur)
            #je verifie si la personne existe en base
            verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_acteur[0], nom = liste_nom_prenom_acteur[1]).first()
            print(verif_unicite)
            if verif_unicite is None:
                ## et affecter ensuite [0] a nom et [1] à prenom 
                personne = Personne()
                #personne.personnes_id => autoincrementé
                personne.prenom = liste_nom_prenom_acteur[0]
                personne.nom = liste_nom_prenom_acteur[1] 
                session.add(personne)
                session.commit()

                #ajout a la table ->ACTEURSFILM               
                acteursfilm = ActeursFilm()
                acteursfilm.film_id = film.film_id
                acteursfilm.personne_id = personne.personne_id
                session.add(acteursfilm)
                session.commit()

        # REALISATEUR FILMS->PERSONNE
        #if type(item['realisateur']) == str:
        if isinstance(item['realisateur'], str):
            #si l item est un nom unique == ne contient pas de " "
            if " " not in item['realisateur'] :
                #je verifie si la personne existe en base
                verif_unicite = session.query(Personne).filter_by(nom = item['realisateur']).first()
                print(verif_unicite)
                if verif_unicite is None:
                    ## et affecter ensuite [0] a nom et [1] à prenom 
                    personne = Personne()
                    #personne.personnes_id => autoincrementé
                    personne.nom = item['realisateur'] 
                    session.add(personne)
                    session.commit()

                    #ajout a la table ->REALISATEURFILM               
                    real_film = RealisateurFilm()
                    real_film.film_id = film.film_id
                    real_film.personne_id = personne.personne_id
                    session.add(real_film)
                    session.commit()
               
                          
            # si item contient ". "
            elif ". " in item['realisateur']:
                #alors il faut separer le nom du prenom via split ". "
                liste_nom_prenom_realisateur = item['realisateur'].split(". ", 1)
                print(f"liste realisateurs cas 1: {liste_nom_prenom_realisateur}")
                #je verifie si la personne existe en base
                verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                print(verif_unicite)
                if verif_unicite is None:
                    ## et affecter ensuite [0] a nom et [1] à prenom 
                    personne = Personne()
                    #personne.personnes_id => autoincrementé
                    personne.prenom = liste_nom_prenom_realisateur[0]
                    personne.nom = liste_nom_prenom_realisateur[1] 
                    session.add(personne)
                    session.commit()

                    #ajout a la table ->REALISATEUR FILM               
                    real_film = RealisateurFilm()
                    real_film.film_id = film.film_id
                    real_film.personne_id = personne.personne_id
                    session.add(real_film)
                    session.commit()
               
            # si item contient " " alors
            elif " " in item['realisateur']:
                #alors il faut separer le nom du prenom via split ". "
                liste_nom_prenom_realisateur = item['realisateur'].split(" ", 1)
                print(f"liste realisateurs cas 2: {liste_nom_prenom_realisateur}")
                print(f"liste realisateurs cas 1: {liste_nom_prenom_realisateur}")
                #je verifie si la personne existe en base
                verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                print(verif_unicite)
                if verif_unicite is None:
                    ## et affecter ensuite [0] a nom et [1] à prenom 
                    personne = Personne()
                    #personne.personnes_id => autoincrementé
                    personne.prenom = liste_nom_prenom_realisateur[0]
                    personne.nom = liste_nom_prenom_realisateur[1] 
                    session.add(personne)
                    session.commit()

                    #ajout a la table ->REALISATEUR Film               
                    real_film = RealisateurFilm()
                    real_film.film_id = film.film_id
                    real_film.personne_id = personne.personne_id
                    session.add(real_film)
                    session.commit()
      

        #il faut distinguer les cas 2/2 : list(getall)
        #if type(item['realisateur']) == 'list':
        if isinstance(item['realisateur'], list):
            #iterer sur les elements de la liste et pour chacun reappliquer le raisonnement
            for i in range(len(item['realisateur'])):
                #si l item est un nom unique == ne contient pas de " "
                if " " not in item['realisateur'][i] :
                    #  alors prenom vide et nom == item 
                    #je verifie si la personne existe en base
                    verif_unicite = session.query(Personne).filter_by(nom = item['realisateur'][i]).first()
                    print(verif_unicite)
                    if verif_unicite is None:
                        ## et affecter ensuite [0] a nom et [1] à prenom 
                        personne = Personne()
                        #personne.personnes_id => autoincrementé
                        personne.nom = item['realisateur'][i] 
                        session.add(personne)
                        session.commit()

                        #ajout a la table ->REALISATEUR FILM              
                        real_film = RealisateurFilm()
                        real_film.film_id = film.film_id
                        real_film.personne_id = personne.personne_id
                        session.add(real_film)
                        session.commit()
                          
                # si item contient ". "
                elif ". " in item['realisateur'][i]:
                    #alors il faut separer le nom du prenom via split ". "
                    liste_nom_prenom_realisateur = item[('realisateur')][i].split(". ", 1)
                    print(f"liste realisateurs cas 2.1: {liste_nom_prenom_realisateur}")
                    #je verifie si la personne existe en base
                    verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                    print(verif_unicite)
                    if verif_unicite is None:
                        ## et affecter ensuite [0] a nom et [1] à prenom 
                        personne = Personne()
                        #personne.personnes_id => autoincrementé
                        personne.prenom = liste_nom_prenom_realisateur[0]
                        personne.nom = liste_nom_prenom_realisateur[1] 
                        session.add(personne)
                        session.commit()

                        #ajout a la table ->REALISATEUR FILM               
                        real_film = RealisateurFilm()
                        real_film.film_id = film.film_id
                        real_film.personne_id = personne.personne_id
                        session.add(real_film)
                        session.commit()
                # si item contient " " alors
                elif " " in item['realisateur'][i]:
                    #alors il faut separer le nom du prenom via split " "
                    liste_nom_prenom_realisateur = item[('realisateur')][i].split(" ", 1)
                    print(f"liste realisateurs cas 2.2: {liste_nom_prenom_realisateur}")
                    #je verifie si la personne existe en base
                    verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                    print(verif_unicite)
                    if verif_unicite is None:
                        ## et affecter ensuite [0] a nom et [1] à prenom 
                        personne = Personne()
                        #personne.personnes_id => autoincrementé
                        personne.prenom = liste_nom_prenom_realisateur[0]
                        personne.nom = liste_nom_prenom_realisateur[1] 
                        session.add(personne)
                        session.commit()

                        #ajout a la table ->REALISATEUR FILM              
                        real_film = RealisateurFilm()
                        real_film.film_id = film.film_id
                        real_film.personne_id = personne.personne_id
                        session.add(real_film)
                        session.commit()

        
        
        session.close()

        return item
        
                
class SaveSeriePipeline(object):
    def __init__(self):
        """
        initialization of database connnection and sessionmaker
        creation of tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)        

    def process_item(self, item, spider):
        """
        saving of series in the database
        method called for every item pipeline component            
        """
        session = self.Session()
        serie = Serie()
        serie.titre = item["title"]
        serie.titre_original = item["titreOriginal"]
        serie.score_presse = item['scorePresse']
        serie.score_spectateur = item['scoreSpectateur']
        serie.annee = item['annee']
        serie.duree = item['duree']
        serie.description = item['description']
        serie.nombre_episodes = item['nombreEpisodes']
        serie.nombre_saisons = item['nombreDeSaisons']
        
        session.add(serie)
        session.commit()

        # GENRESERIE
        for i in range(len(item['genre'])):
            genre_serie = GenreSerie()
            genre_serie.serie_id = serie.serie_id
            genre_serie.genre = item['genre'][i]
            session.add(genre_serie)
            session.commit()

        # ORIGINESERIE
        #il faut distinguer les cas : string(get) ou list(getall)
        if type(item['paysOrigine']) == str:
                    origine_serie = OrigineSerie()
                    origine_serie.serie_id = serie.serie_id
                    origine_serie.pays = item['paysOrigine']
                    session.add(origine_serie)
                    session.commit()
        else:
            for i in range(len(item['paysOrigine'])):
                        origine_serie = OrigineSerie()
                        origine_serie.serie_id = serie.serie_id
                        origine_serie.pays = item['paysOrigine'][i]
                        session.add(origine_serie)
                        session.commit()

        #recuperer tous les ACTEURS de SERIES->PERSONNE suivant le spider
        # ->affecter le pipeline dans chacun des spiders: VERIF
        ##type de l item:liste avec val nulles possibles
        ##il faut isoler les couple noms prenoms:ce sont juste les elts de la liste
        ##pour chacun il faut separer le nom du prenom via split avec " " ou ". " comme separateur
        for i in range(len(item['acteurs'])):
            print(item[('acteurs')][i])
            liste_nom_prenom_acteur = item[('acteurs')][i].split(". ", 1) if ". " in item[('acteurs')][i] else item[('acteurs')][i].split(" ", 1)
            print(liste_nom_prenom_acteur)
            #je verifie si la personne existe en base
            verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_acteur[0], nom = liste_nom_prenom_acteur[1]).first()
            print(verif_unicite)
            if verif_unicite is None:
                ## et affecter ensuite [0] a nom et [1] à prenom 
                personne = Personne()
                #personne.personnes_id => autoincrementé
                personne.prenom = liste_nom_prenom_acteur[0]
                personne.nom = liste_nom_prenom_acteur[1] 
                session.add(personne)
                session.commit()

                #ajout a la table ->ACTEURSSERIE                
                acteurserie = ActeursSerie()
                acteurserie.serie_id = serie.serie_id
                acteurserie.personne_id = personne.personne_id
                session.add(acteurserie)
                session.commit()

        # REALISATEUR SERIES->PERSONNE
        #if type(item['realisateur']) == str:
        if isinstance(item['realisateur'], str):
            #si l item est un nom unique == ne contient pas de " "
            if " " not in item['realisateur'] :
                #je verifie si la personne existe en base
                verif_unicite = session.query(Personne).filter_by(nom = item['realisateur']).first()
                print(verif_unicite)
                if verif_unicite is None:
                    ## et affecter ensuite [0] a nom et [1] à prenom 
                    personne = Personne()
                    #personne.personnes_id => autoincrementé
                    personne.nom = item['realisateur'] 
                    session.add(personne)
                    session.commit()

                    #ajout a la table ->REALISATEURSSERIE               
                    real_serie = RealisateurSerie()
                    real_serie.serie_id = serie.serie_id
                    real_serie.personne_id = personne.personne_id
                    session.add(real_serie)
                    session.commit()
               
                          
            # si item contient ". "
            elif ". " in item['realisateur']:
                #alors il faut separer le nom du prenom via split ". "
                liste_nom_prenom_realisateur = item['realisateur'].split(". ", 1)
                print(f"liste realisateurs cas 1: {liste_nom_prenom_realisateur}")
                #je verifie si la personne existe en base
                verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                print(verif_unicite)
                if verif_unicite is None:
                    ## et affecter ensuite [0] a nom et [1] à prenom 
                    personne = Personne()
                    #personne.personnes_id => autoincrementé
                    personne.prenom = liste_nom_prenom_realisateur[0]
                    personne.nom = liste_nom_prenom_realisateur[1] 
                    session.add(personne)
                    session.commit()

                    #ajout a la table ->REALISATEURSSERIE               
                    real_serie = RealisateurSerie()
                    real_serie.serie_id = serie.serie_id
                    real_serie.personne_id = personne.personne_id
                    session.add(real_serie)
                    session.commit()
               
            # si item contient " " alors
            elif " " in item['realisateur']:
                #alors il faut separer le nom du prenom via split ". "
                liste_nom_prenom_realisateur = item['realisateur'].split(" ", 1)
                print(f"liste realisateurs cas 2: {liste_nom_prenom_realisateur}")
                print(f"liste realisateurs cas 1: {liste_nom_prenom_realisateur}")
                #je verifie si la personne existe en base
                verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                print(verif_unicite)
                if verif_unicite is None:
                    ## et affecter ensuite [0] a nom et [1] à prenom 
                    personne = Personne()
                    #personne.personnes_id => autoincrementé
                    personne.prenom = liste_nom_prenom_realisateur[0]
                    personne.nom = liste_nom_prenom_realisateur[1] 
                    session.add(personne)
                    session.commit()

                    #ajout a la table ->REALISATEURSSERIE               
                    real_serie = RealisateurSerie()
                    real_serie.serie_id = serie.serie_id
                    real_serie.personne_id = personne.personne_id
                    session.add(real_serie)
                    session.commit()
      

        #il faut distinguer les cas 2/2 : list(getall)
        #if type(item['realisateur']) == 'list':
        if isinstance(item['realisateur'], list):
            #iterer sur les elements de la liste et pour chacun reappliquer le raisonnement
            for i in range(len(item['realisateur'])):
                #si l item est un nom unique == ne contient pas de " "
                if " " not in item['realisateur'][i] :
                    #  alors prenom vide et nom == item 
                    #je verifie si la personne existe en base
                    verif_unicite = session.query(Personne).filter_by(nom = item['realisateur'][i]).first()
                    print(verif_unicite)
                    if verif_unicite is None:
                        ## et affecter ensuite [0] a nom et [1] à prenom 
                        personne = Personne()
                        #personne.personnes_id => autoincrementé
                        personne.nom = item['realisateur'][i] 
                        session.add(personne)
                        session.commit()

                        #ajout a la table ->REALISATEURSSERIE               
                        real_serie = RealisateurSerie()
                        real_serie.serie_id = serie.serie_id
                        real_serie.personne_id = personne.personne_id
                        session.add(real_serie)
                        session.commit()
                          
                # si item contient ". "
                elif ". " in item['realisateur'][i]:
                    #alors il faut separer le nom du prenom via split ". "
                    liste_nom_prenom_realisateur = item[('realisateur')][i].split(". ", 1)
                    print(f"liste realisateurs cas 2.1: {liste_nom_prenom_realisateur}")
                    #je verifie si la personne existe en base
                    verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                    print(verif_unicite)
                    if verif_unicite is None:
                        ## et affecter ensuite [0] a nom et [1] à prenom 
                        personne = Personne()
                        #personne.personnes_id => autoincrementé
                        personne.prenom = liste_nom_prenom_realisateur[0]
                        personne.nom = liste_nom_prenom_realisateur[1] 
                        session.add(personne)
                        session.commit()

                        #ajout a la table ->REALISATEURSSERIE               
                        real_serie = RealisateurSerie()
                        real_serie.serie_id = serie.serie_id
                        real_serie.personne_id = personne.personne_id
                        session.add(real_serie)
                        session.commit()
                # si item contient " " alors
                elif " " in item['realisateur'][i]:
                    #alors il faut separer le nom du prenom via split " "
                    liste_nom_prenom_realisateur = item[('realisateur')][i].split(" ", 1)
                    print(f"liste realisateurs cas 2.2: {liste_nom_prenom_realisateur}")
                    #je verifie si la personne existe en base
                    verif_unicite = session.query(Personne).filter_by(prenom = liste_nom_prenom_realisateur[0], nom = liste_nom_prenom_realisateur[1]).first()
                    print(verif_unicite)
                    if verif_unicite is None:
                        ## et affecter ensuite [0] a nom et [1] à prenom 
                        personne = Personne()
                        #personne.personnes_id => autoincrementé
                        personne.prenom = liste_nom_prenom_realisateur[0]
                        personne.nom = liste_nom_prenom_realisateur[1] 
                        session.add(personne)
                        session.commit()

                        #ajout a la table ->REALISATEURSSERIE               
                        real_serie = RealisateurSerie()
                        real_serie.serie_id = serie.serie_id
                        real_serie.personne_id = personne.personne_id
                        session.add(real_serie)
                        session.commit()



        session.close()

        return item    

       
        
"""    
class SavePersonnePipeline(object):
    def __init__(self):
        
        initialization of database connnection and sessionmaker
        creation of tables
        
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        
        saving of personne (acteurs & realisateurs from films & serie)in the database
        method called for every item pipeline component            
        
        session = self.Session()
        
        #recuperer tous les ACTEURS de films ou series suivant le spider
        # ->affecter le pipeline dans chacun des spiders: VERIF
        ##type de l item:liste avec val nulles possibles
        ##il faut isoler les couple noms prenoms:ce sont juste les elts de la liste
        ##pour chacun il faut separer le nom du prenom via split avec " " ou ". " comme separateur
        for i in range(len(item['acteurs'])):
            print(item[('acteurs')][i])
            liste_nom_prenom_acteur = item[('acteurs')][i].split(". ", 1) if ". " in item[('acteurs')][i] else item[('acteurs')][i].split(" ", 1)
            ## et affecter ensuite [0] a nom et [1] à prenom 
            personne = Personne()
            #personne.personnes_id => autoincrementé
            personne.prenom = liste_nom_prenom_acteur[0]
            personne.nom = liste_nom_prenom_acteur[1]
            try:
                session.add(personne)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("cette personne existe dejà en base")   
                session.rollback()
                session.close()
                session = self.Session()           
                
        
        #Dude: prend lid de lacteur== personne id
            #acteurfilm = ActeursFilm()
            #acteurfilm.film_id = "?" CHERCHER L
            #acteurfilm.personnes_id = personne.personnes_id

        #recuperer tous les REALISATEURS de films ou series
        ##type de l item 
        #il faut distinguer les cas 1/2: string(get)
        
        #if type(item['realisateur']) == str:
        if isinstance(item['realisateur'], str):
            #si l item est un nom unique == ne contient pas de " "
            if " " not in item['realisateur'] :
                #  alors prenom vide et nom == item 
                personne = Personne() 
                personne.nom = item['realisateur']
                try:
                    session.add(personne)
                    session.commit()
                except sqlalchemy.exc.IntegrityError:
                    print("cette personne existe dejà en base")   
                    session.rollback()
                    session.close()
                    session = self.Session()
                          
            # si item contient ". "
            elif ". " in item['realisateur']:
                #alors il faut separer le nom du prenom via split ". "
                liste_nom_prenom_realisateur = item['realisateur'].split(". ", 1)
                print(f"liste realisateurs cas 1: {liste_nom_prenom_realisateur}")
                personne = Personne()
                personne.prenom = liste_nom_prenom_realisateur[0]
                personne.nom = liste_nom_prenom_realisateur[1]
                try:
                    session.add(personne)
                    session.commit()
                except sqlalchemy.exc.IntegrityError:
                    print("cette personne existe dejà en base")   
                    session.rollback()
                    session.close()
                    session = self.Session()
            # si item contient " " alors
            elif " " in item['realisateur']:
                #alors il faut separer le nom du prenom via split ". "
                liste_nom_prenom_realisateur = item['realisateur'].split(" ", 1)
                print(f"liste realisateurs cas 2: {liste_nom_prenom_realisateur}")
                personne = Personne()
                personne.prenom = liste_nom_prenom_realisateur[0]
                personne.nom = liste_nom_prenom_realisateur[1]
                try:
                    session.add(personne)
                    session.commit()
                except sqlalchemy.exc.IntegrityError:
                    print("cette personne existe dejà en base")   
                    session.rollback()
                    session.close()
                    session = self.Session()
      

        #il faut distinguer les cas 2/2 : list(getall)
        #if type(item['realisateur']) == 'list':
        if isinstance(item['realisateur'], list):
            #iterer sur les elements de la liste et pour chacun reappliquer le raisonnement
            for i in range(len(item['realisateur'])):
                #si l item est un nom unique == ne contient pas de " "
                if " " not in item['realisateur'][i] :
                    #  alors prenom vide et nom == item 
                    personne = Personne() 
                    personne.nom = item['realisateur']
                    try:
                        session.add(personne)
                        session.commit()
                    except sqlalchemy.exc.IntegrityError:
                        print("cette personne existe dejà en base")   
                        session.rollback()
                        session.close()
                        session = self.Session()
                          
                # si item contient ". "
                elif ". " in item['realisateur'][i]:
                    #alors il faut separer le nom du prenom via split ". "
                    liste_nom_prenom_realisateur = item[('realisateur')][i].split(". ", 1)
                    print(f"liste realisateurs cas 2.1: {liste_nom_prenom_realisateur}")
                    personne = Personne()
                    personne.prenom = liste_nom_prenom_realisateur[0]
                    personne.nom = liste_nom_prenom_realisateur[1]
                    try:
                        session.add(personne)
                        session.commit()
                    except sqlalchemy.exc.IntegrityError:
                        print("cette personne existe dejà en base")   
                        session.rollback()
                        session.close()
                        session = self.Session()
                # si item contient " " alors
                elif " " in item['realisateur'][i]:
                    #alors il faut separer le nom du prenom via split " "
                    liste_nom_prenom_realisateur = item[('realisateur')][i].split(" ", 1)
                    print(f"liste realisateurs cas 2.2: {liste_nom_prenom_realisateur}")
                    personne = Personne()
                    personne.prenom = liste_nom_prenom_realisateur[0]
                    personne.nom = liste_nom_prenom_realisateur[1]
                    try:
                        session.add(personne)
                        session.commit()
                    except sqlalchemy.exc.IntegrityError:
                        print("cette personne existe dejà en base")   
                        session.rollback()
                        session.close()
                        session = self.Session()


        session.close()

        return item
    

        #traiter les doublons eventuels
        idee geniale d Arnaud == installer une unique constraint key dans la table personnes
        pb cela genere une integrity error si dans un meme item on a des doublons de personnes
 
        sinon usine a gaz via pandas:
        #obtenir toutes les personnes
        #supprimer les doublons(des le deuxieme usage,cela ne supprimera donc que les doublons supplementaires generes)
        # via pandas? poetry add + import
        #transfo de Personne en dataframe
        connection = session.connection
        df_personne = pd.read_sql_table("Personne", connection)
        #suppression des doublons

        cleaned_df_personne = df_personne.drop_duplicates(keep = 'first', inplace=True) 
        #restitution a l objet table Personne
        cleaned_df_personne.to_sql("Personne", connection, if_exists='append')
        session.commit()
    """

        





