from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, Text
from database import Base

class DetectionResult(Base):
    __tablename__ = "yolo_detection_results"

    id = Column(Integer, primary_key=True, index=True)
    class_label = Column(Integer)
    x_center = Column(Float)
    y_center = Column(Float)
    width = Column(Float)
    height = Column(Float)
    confidence = Column(Float)

class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String)
    message_id = Column(Integer)
    content = Column(Text)
    timestamp = Column(TIMESTAMP(timezone=True))
    views = Column(Float)
    message_link = Column(String)
