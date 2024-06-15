from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import DetectionResult, TelegramMessage
from schemas import DetectionResultCreate, TelegramMessageCreate, TelegramMessageUpdate

def get_all_telegram_messages(db: Session):
    try:
        return db.query(TelegramMessage).all()
    except SQLAlchemyError as e:
        print(f"Error fetching telegram messages: {e}")
        return []

def get_all_detection_results(db: Session):
    try:
        return db.query(DetectionResult).all()
    except SQLAlchemyError as e:
        print(f"Error fetching detection results: {e}")
        return []

def create_detection_result(db: Session, detection_result: DetectionResultCreate):
    try:
        db_detection_result = DetectionResult(**detection_result.dict(exclude_unset=True))
        db.add(db_detection_result)
        db.commit()
        db.refresh(db_detection_result)
        return db_detection_result
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating detection result: {e}")
        return None

def create_telegram_message(db: Session, telegram_message: TelegramMessageCreate):
    try:
        db_telegram_message = TelegramMessage(**telegram_message.dict(exclude_unset=True))
        db.add(db_telegram_message)
        db.commit()
        db.refresh(db_telegram_message)
        return db_telegram_message
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating telegram message: {e}")
        return None

def update_telegram_message(db: Session, message_id: int, telegram_message_update: TelegramMessageUpdate):
    try:
        db_message = db.query(TelegramMessage).filter(TelegramMessage.id == message_id).first()
        if db_message:
            for field, value in telegram_message_update.dict(exclude_unset=True).items():
                setattr(db_message, field, value)
            db.commit()
            return db_message
        return None
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating telegram message: {e}")
        return None

def delete_telegram_message(db: Session, message_id: int):
    try:
        telegram_message = db.query(TelegramMessage).filter(TelegramMessage.id == message_id).first()
        if telegram_message:
            db.delete(telegram_message)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting telegram message: {e}")
        return False
