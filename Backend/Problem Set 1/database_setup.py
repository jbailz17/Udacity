import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'Shelter'
    name = Column(String(80))
    address = Column(String(250))
    city = Column(String(250))
    state = Column(String(250))
    zipCode = Column(Integer)
    website = Column(String(250))
    id = Column(Integer, primary_key = True)

class Puppy(Base):
    __tablename__ = 'Puppy'
    name = Column(String(80))
    date_of_birth = Column(String(80))
    gender = Column(String(7))
    weight = Column(Integer)
    shelter_id = Column(Integer, ForeignKey('Shelter.id'))
    picture = Column(String(80), primary_key=True)

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)
