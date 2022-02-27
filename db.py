from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///biudzetas.db")
Base = declarative_base()


class Biudzeto(Base):
    __tablename__ = "Biudzetas"
    id = Column(Integer, primary_key=True)
    tipas = Column("Tipas", String)
    suma = Column("Suma", Float)
    comments = Column("Komentaras", Integer)

    def __init__(self, tipas, suma, comments):
        self.tipas = tipas
        self.suma = suma
        self.comments = comments

    def __repr__(self):
        return f"{self.id}.{self.tipas}: {self.suma}, {self.comments}"



Base.metadata.create_all(engine)

