import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database and tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_telegram_message(setup_database):
    response = client.post(
        "/telegram_messages/",
        json={"message": "Test message"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Test message"

def test_read_all_telegram_messages(setup_database):
    response = client.get("/telegram_messages/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_detection_result(setup_database):
    response = client.post(
        "/detection_results/",
        json={"result": "Test result"}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "Test result"

def test_read_all_detection_results(setup_database):
    response = client.get("/detection_results/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_telegram_message(setup_database):
    # First, create a new message
    response = client.post(
        "/telegram_messages/",
        json={"message": "Original message"}
    )
    message_id = response.json()["id"]
    
    # Update the message
    response = client.put(
        f"/telegram_messages/{message_id}",
        json={"message": "Updated message"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Updated message"

def test_delete_telegram_message(setup_database):
    # First, create a new message
    response = client.post(
        "/telegram_messages/",
        json={"message": "Message to delete"}
    )
    message_id = response.json()["id"]
    
    # Delete the message
    response = client.delete(f"/telegram_messages/{message_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Telegram message with id {message_id} deleted successfully"
    
    # Verify deletion
    response = client.get(f"/telegram_messages/{message_id}")
    assert response.status_code == 404
