from sqlalchemy import Column, Integer, String, ARRAY, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import csv
from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint
import os
from os import environ
from dotenv import load_dotenv
load_dotenv

Base = declarative_base()

# import des variables d environnement

# Configuration de la base de données
#engine = create_engine('postgresql+psycopg2://sergebuasa:Rebirth2024+@:buasaserver.postgres.database.azure.com/flexibleserverdb')
# azure
#azureengine = create_engine('postgresql+psycopg2://sergebuasa:Rebirth2024+@buasaserver.postgres.database.azure.com/buasa_bdd')
#creation config base de donnes dans serveur postgtreysql local
#engine = create_engine('jdbc:postgresql://localhost:5432/buasa_allocinescrapping_bdd')

def db_connect():
    """
    connection to database
    return of sqlalchemy engine instance
    """
    username = os.getenv("DB_USERNAME")
    hostname = os.getenv("DB_HOSTNAME")
    port = os.getenv("DB_PORT")
    database_name = os.getenv("DB_NAME")
    password = os.getenv("DBSERVER_PASSWORD")
    bdd_path = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database_name}"
    #return create_engine('postgresql+psycopg2://sergebuasa:Rebirth2024+@localhost:5432/buasa_allocinescrapping_bdd')
    return create_engine(bdd_path)

def create_table(engine):
    """
    database creation  by sqlalchemy engine instance
    """
    Base.metadata.create_all(engine)

#Session = sessionmaker(bind=engine)
#session = Session()


#film est en association one to many avec film_genre, film_origine et film langue
class Film(Base):
    __tablename__ = 'films'
    film_id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String)
    titre_original = Column(String)
    score_presse = Column(String)
    score_spectateur = Column(String)
    annee = Column(String)
    duree = Column(String)
    description = Column(String)
    public = Column(String)
    #rajouter la mention one to many avec filmsgenre filmsorigine filmslangue
    un_film = relationship('GenreFilm', backref='films')
    un_film = relationship('LangueFilm', backref='films')
    un_film = relationship('OrigineFilm', backref='films')
    real_films = relationship('RealisateurFilm', back_populates='mapper_film')



#serie est en association many to one avec serie_genre et avec serie_origine
class Serie(Base):
    __tablename__ = 'series'
    serie_id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String)
    titre_original = Column(String)
    score_presse = Column(String)
    score_spectateur = Column(String)
    annee = Column(String)
    duree = Column(String)
    description = Column(String)
    nombre_episodes = Column(String)
    nombre_saisons= Column(String)
    #rajouter la mention one to many avec seriesgenre et origineserie
    une_serie = relationship('GenreSerie', backref='films')
    une_serie = relationship('OrigineSerie', backref='films')
    #rajout relation back_populates avec realisateur serie
    real_series = relationship("RealisateurSerie", back_populates="mapper_serie")




class Personne(Base):
    __tablename__ = 'personnes'
    personne_id = Column(Integer, primary_key=True, autoincrement=True)
    prenom = Column(String)
    nom = Column(String)
    #serie = relationship("Serie", back_populates="personnes") relation avec realisateur film
    #real_films = relationship('RealisateurFilm', back_populates=)
    #relation avec realisateur serie
    real_series = relationship('RealisateurSerie', back_populates='mapper_personne')
    real_films = relationship('RealisateurFilm', back_populates='mapper2_personne')
    __table_args__ = (
        UniqueConstraint('prenom', 'nom'),
    )

#tables association entre film / serie et personnes

class ActeursFilm(Base):
    __tablename__ = 'acteurs_films'
    film_id = Column(Integer, ForeignKey('films.film_id'), primary_key=True)
    personne_id = Column(Integer,ForeignKey('personnes.personne_id'), primary_key=True)
    film = relationship("Film", backref="personnes")
    personne = relationship("Personne", backref="films")

    __table_args__ = (
        PrimaryKeyConstraint('film_id', 'personne_id'),
    )

class RealisateurFilm(Base):
    __tablename__ = 'realisateur_films'
    film_id = Column(Integer,ForeignKey('films.film_id'), primary_key=True)
    personne_id = Column(Integer,ForeignKey('personnes.personne_id'), primary_key=True)
    mapper_film = relationship("Film", back_populates="real_films")
    mapper2_personne = relationship("Personne", back_populates="real_films")

    __table_args__ = (
        PrimaryKeyConstraint('film_id', 'personne_id'),
    )

class ActeursSerie(Base):
    __tablename__ = 'acteurs_series'
    serie_id = Column(Integer, ForeignKey('series.serie_id'), primary_key=True)
    personne_id = Column(Integer,ForeignKey('personnes.personne_id'), primary_key=True)
    serie = relationship("Serie", backref="personnes")
    personne = relationship("Personne", backref="series")

    __table_args__ = (
        PrimaryKeyConstraint('serie_id', 'personne_id'),
    )

class RealisateurSerie(Base):
    __tablename__ = 'realisateur_series'
    serie_id = Column(Integer, ForeignKey('series.serie_id'), primary_key=True)
    personne_id = Column(Integer, ForeignKey('personnes.personne_id'), primary_key=True)
    mapper_serie = relationship("Serie", back_populates="real_series")
    mapper_personne = relationship("Personne", back_populates="real_series")

    __table_args__ = (
        PrimaryKeyConstraint('serie_id', 'personne_id'),
    ) 
#tables en many to one avec film et serie

class GenreFilm(Base):
    __tablename__ = 'genre_films'
    film_id = Column(Integer, ForeignKey('films.film_id'), primary_key=True) #many genrefilm to one film
    genre = Column(String, primary_key=True)
        
    __table_args__ = (
        PrimaryKeyConstraint('film_id', 'genre'),
    )
class LangueFilm(Base):
    __tablename__ = 'langue_films'
    film_id = Column(Integer, ForeignKey('films.film_id'), primary_key=True) #many languefilm to one film
    langue = Column(String, primary_key=True)
        
    __table_args__ = (
        PrimaryKeyConstraint('film_id', 'langue'),
    )

class OrigineFilm(Base):
    __tablename__ = 'origine_films'
    film_id = Column(Integer, ForeignKey('films.film_id'), primary_key=True) #many originefilm to one film
    pays = Column(String, primary_key=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('film_id', 'pays'),
    )

#tables en many to one avec serie

class GenreSerie(Base):
    __tablename__ = 'genre_series'
    serie_id = Column(Integer, ForeignKey('series.serie_id'), primary_key=True) #many genreserie to one serie
    genre = Column(String, primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('serie_id', 'genre'),
    )



class OrigineSerie(Base):
    __tablename__ = 'origine_series'
    serie_id = Column(Integer, ForeignKey('series.serie_id'), primary_key=True) #many origineserie to one serie
    pays = Column(String, primary_key=True)
    
    __table_args__ = (
        PrimaryKeyConstraint('serie_id', 'pays'),
    )

 
