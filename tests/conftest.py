# exercises/test-suite/tests/conftest.py
# L11 — Test fixtures
#
# Your task: Set up an isolated test database and override the get_db dependency.

import pytest
from fastapi.testclient import TestClient

# TODO: Import create_engine and StaticPool from sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# TODO: Import sessionmaker and Session from sqlalchemy.orm
from sqlalchemy.orm import sessionmaker, Session

# TODO: Import Base, get_db from app.database
from app.database import Base, get_db

# TODO: Import the app
from app.main import app


# TODO: Create an in-memory SQLite test engine
# Use StaticPool so the same connection is reused (required for :memory: databases)
# Key concept: We use a SEPARATE in-memory DB for tests so tests never touch
# the real database file.
#
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# TODO: Define a client fixture that:
@pytest.fixture
def client():
# 1. Creates all tables in the test DB
    Base.metadata.create_all(bind=test_engine)
# 2. Defines override_get_db() yielding a test session
    def override_get_db(): 
        db = TestingSessionLocal()       
        try: 
            yield db 
        finally: 
            db.close()

# 3. Overrides 
    app.dependency_overrides[get_db] = override_get_db

# 4. Yields TestClient(app)
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)


