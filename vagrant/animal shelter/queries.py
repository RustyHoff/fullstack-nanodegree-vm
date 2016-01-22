from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
