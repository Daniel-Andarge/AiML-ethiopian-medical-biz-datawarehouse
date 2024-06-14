from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DetectionResultBase(BaseModel):
    class_label: int
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float

class DetectionResultCreate(DetectionResultBase):
    pass

class DetectionResult(DetectionResultBase):
    id: int

    class Config:
        orm_mode = True

class TelegramMessageBase(BaseModel):
    channel: str
    message_id: int
    content: Optional[str]
    timestamp: Optional[datetime]
    views: Optional[float]
    message_link: Optional[str]

class TelegramMessageCreate(TelegramMessageBase):
    pass

class TelegramMessage(TelegramMessageBase):
    id: int

    class Config:
        orm_mode = True

class TelegramMessageUpdate(BaseModel):
    channel: Optional[str]
    content: Optional[str]
    views: Optional[float]
    message_link: Optional[str]