# dbengine/db.py
from sqlalchemy import create_engine
from .config import DATABASE_URI

engine = create_engine(DATABASE_URI)