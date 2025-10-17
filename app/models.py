from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class TrackedObject(Base):
    __tablename__ = 'tracked_objects'

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    x_coordinate = Column(Integer)
    y_coordinate = Column(Integer)
    speed_mps = Column(Float)