from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    direction = Column(String)
    entry = Column(Float)
    tp = Column(Float)
    sl = Column(Float)
    ote_min = Column(Float)
    ote_max = Column(Float)
    confidence = Column(Float)
    confluences = Column(String)
    hit_tp = Column(Boolean, default=False)
    hit_sl = Column(Boolean, default=False)
    timeframe = Column(String)
    tipo = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
