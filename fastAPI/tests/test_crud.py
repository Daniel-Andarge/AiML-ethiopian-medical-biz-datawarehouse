import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from models import Base, DetectionResult, TelegramMessage
from schemas import DetectionResultCreate, TelegramMessageCreate, TelegramMessageUpdate
import crud

#  In-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_get_all_telegram_messages(setup_database, db_session):
    message = TelegramMessage(message="Test message")
    db_session.add(message)
    db_session.commit()
    messages = crud.get_all_telegram_messages(db_session)
    assert len(messages) == 1
    assert messages[0].message == "Test message"

def test_get_all_detection_results(setup_database, db_session):
    result = DetectionResult(result="Test result")
    db_session.add(result)
    db_session.commit()
    results = crud.get_all_detection_results(db_session)
    assert len(results) == 1
    assert results[0].result == "Test result"

def test_create_detection_result(setup_database, db_session):
    detection_result_data = DetectionResultCreate(result="New detection result")
    detection_result = crud.create_detection_result(db_session, detection_result_data)
    assert detection_result is not None
    assert detection_result.result == "New detection result"

def test_create_telegram_message(setup_database, db_session):
    telegram_message_data = TelegramMessageCreate(message="New telegram message")
    telegram_message = crud.create_telegram_message(db_session, telegram_message_data)
    assert telegram_message is not None
    assert telegram_message.message == "New telegram message"

def test_update_telegram_message(setup_database, db_session):
    message = TelegramMessage(message="Original message")
    db_session.add(message)
    db_session.commit()
    telegram_message_update = TelegramMessageUpdate(message="Updated message")
    updated_message = crud.update_telegram_message(db_session, message.id, telegram_message_update)
    assert updated_message is not None
    assert updated_message.message == "Updated message"

def test_delete_telegram_message(setup_database, db_session):
    message = TelegramMessage(message="Message to delete")
    db_session.add(message)
    db_session.commit()
    deleted = crud.delete_telegram_message(db_session, message.id)
    assert deleted is True
    message = db_session.query(TelegramMessage).filter(TelegramMessage.id == message.id).first()
    assert message is None
