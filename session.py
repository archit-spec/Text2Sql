# dbengine/session.py
from sqlalchemy.orm import sessionmaker
from .db import engine

Session = sessionmaker(bind=engine)