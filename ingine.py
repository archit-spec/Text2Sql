from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrap import scrape_youtube

DATABASE_URL = "sqlite:///youtube_data_english.db"  # Using SQLite for simplicity
engine = create_engine(DATABASE_URL)
Base = declarative_base()
transcript_DATABASE_URL = "sqlite:///youtube_data_transcripts.db"
engine_transcript = create_engine(transcript_DATABASE_URL)

class Transcript(Base):
    __tablename__ = 'transcripts'
    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)
    transcript = Column(String, nullable=False)
    languae = Column(String, nullable=False)





class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    channel_name = Column(String, nullable=False)
    channel_link = Column(String, nullable=False)
    views = Column(String, nullable=False)
    upload_date = Column(String, nullable=False)
    transcript = Column(Text, nullable=True)  # Added transcript field

# Create the table
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

#fucntion to initial db
def init_db(db_name):
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    return session

session = SessionLocal()

def add_video(title, link, channel_name, channel_link, views, upload_date):
    for video in data:
        new_video = Video(
        title=video["title"],
        link=video["link"],
        channel_name=video["channel_name"],
        channel_link=video["channel_link"],
        views=video["views"],
        upload_date=video["upload_date"]
        )
        session.add(new_video)
        session.commit()

def get_video_by_link(link):
    return session.query(Video).filter_by(link=link).first()


def remove_video(link):
    video = get_video_by_link(link)
    if video:
        session.delete(video)
        session.commit()


def update_video(link, title, channel_name, channel_link, views, upload_date):
    video = get_video_by_link(link)
    if video:
        video.title = title

        video.channel_name = channel_name
        video.channel_link = channel_link
        video.views = views
        video.upload_date = upload_date
        session.commit()


session.close()
