from sqlalchemy.orm import Session
from models import DetectionResult, TelegramMessage
from schemas import DetectionResultCreate, TelegramMessageCreate, TelegramMessageUpdate


def get_all_telegram_messages(db: Session):
    return db.query(TelegramMessage).all()

def get_all_detection_results(db: Session):
    return db.query(DetectionResult).all()

def create_detection_result(db: Session, detection_result: DetectionResultCreate):
    db_detection_result = DetectionResult(**detection_result.dict(exclude_unset=True))
    db.add(db_detection_result)
    db.commit()
    db.refresh(db_detection_result)
    return db_detection_result

def create_telegram_message(db: Session, telegram_message: TelegramMessageCreate):
    db_telegram_message = TelegramMessage(**telegram_message.dict(exclude_unset=True))
    db.add(db_telegram_message)
    db.commit()
    db.refresh(db_telegram_message)
    return db_telegram_message

def update_telegram_message(db: Session, message_id: int, telegram_message_update: TelegramMessageUpdate):
    db_message = db.query(TelegramMessage).filter(TelegramMessage.id == message_id).first()
    if db_message:
        for field, value in telegram_message_update.dict(exclude_unset=True).items():
            setattr(db_message, field, value)
        db.commit()
        return db_message
    return None


def delete_telegram_message(db: Session, message_id: int):
    telegram_message = db.query(TelegramMessage).filter(TelegramMessage.id == message_id).first()
    if telegram_message:
        db.delete(telegram_message)
        db.commit()
        return True
    return False
