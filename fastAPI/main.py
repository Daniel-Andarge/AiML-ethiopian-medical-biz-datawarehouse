from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET all Telegram messages
@app.get("/telegram_messages/", response_model=list[schemas.TelegramMessage])
def read_all_telegram_messages(db: Session = Depends(get_db)):
    return crud.get_all_telegram_messages(db)

# GET  all detection results
@app.get("/detection_results/", response_model=list[schemas.DetectionResult])
def read_all_detection_results(db: Session = Depends(get_db)):
    return crud.get_all_detection_results(db)

# create a detection result
@app.post("/detection_results/", response_model=schemas.DetectionResult)
def create_detection_result(detection_result: schemas.DetectionResultCreate, db: Session = Depends(get_db)):
    return crud.create_detection_result(db=db, detection_result=detection_result)

#  create a telegram message
@app.post("/telegram_messages/", response_model=schemas.TelegramMessage)
def create_telegram_message(telegram_message: schemas.TelegramMessageCreate, db: Session = Depends(get_db)):
    return crud.create_telegram_message(db=db, telegram_message=telegram_message)


@app.put("/telegram_messages/{message_id}", response_model=schemas.TelegramMessage)
def update_telegram_message(message_id: int, telegram_message_update: schemas.TelegramMessageUpdate, db: Session = Depends(get_db)):
    updated_message = crud.update_telegram_message(db, message_id, telegram_message_update)
    if updated_message is None:
        raise HTTPException(status_code=404, detail=f"Telegram message with id {message_id} not found")
    return updated_message

# Delete telegram message
@app.delete("/telegram_messages/{message_id}")
def delete_telegram_message(message_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_telegram_message(db, message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Telegram message with id {message_id} not found")
    return {"message": f"Telegram message with id {message_id} deleted successfully"}
