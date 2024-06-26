from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import VECTOR
from .engine import Base

class YoutubeVideo(Base):
    __tablename__ = 'youtube_videos'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    segments = relationship("VideoSegment", back_populates="video")

class VideoSegment(Base):
    __tablename__ = 'video_segments'

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey('youtube_videos.video_id'), nullable=False)
    segment_text = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    embedding = Column(VECTOR(384))

    video = relationship("YoutubeVideo", back_populates="segments")