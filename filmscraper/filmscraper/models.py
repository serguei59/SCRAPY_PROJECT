from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 
import csv

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ISBN = Column(String, unique=True, nullable=False)
    Book_Title = Column(String, nullable=False)
    Book_Author = Column(String, nullable=False)
    Year_Of_Publication = Column(Integer, nullable=False)
    Publisher = Column(String, nullable=False)
    Image_URL_S = Column(String)
    Image_URL_M = Column(String)
    Image_URL_L = Column(String)

# Configuration de la base de données
#engine = create_engine('postgresql+psycopg2://sergebuasa:Rebirth2024+@:buasaserver.postgres.database.azure.com/flexibleserverdb')
engine = create_engine('postgresql+psycopg2://sergebuasa:Rebirth2024+@buasaserver.postgres.database.azure.com/buasa_bdd')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def import_books_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        csvreader =  csv.DictReader(csvfile, delimiter=';', quotechar='"', escapechar='\\')
        for row in csvreader:
            book = Book(
                ISBN=row['ISBN'],
                Book_Title=row['Book-Title'],
                Book_Author=row['Book-Author'],
                Year_Of_Publication=int(row['Year-Of-Publication']),
                Publisher=row['Publisher'],
                Image_URL_S=row['Image-URL-S'],
                Image_URL_M=row['Image-URL-M'],
                Image_URL_L=row['Image-URL-L']
            )
            session.add(book)
        session.commit()

# Chemin vers le fichier CSV
csv_file_path = 'postgre_basics/data/books.csv'
import_books_from_csv(csv_file_path)

#un_livre = Book()

""" def add_book(db: Session, un_livre = Book):
    un_livre = Book(ISBN='0002005018', Book_Title='Become', Book_Author='M.Obama', Year_Of_Publication='2018', )
 """