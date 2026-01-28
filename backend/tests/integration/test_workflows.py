import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base, get_db
from backend.main import app
import os
from unittest.mock import MagicMock, patch

# Use environment variable for test database or fallback to SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_integration.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

def test_full_analysis_workflow(client):
    """
    Test end-to-end code analysis workflow.
    """
    # Mock LLM response to avoid API calls and costs
    mock_analysis = {
        "summary": "Good code",
        "quality_score": 8.5,
        "issues": [],
        "suggestions": [],
        "security_concerns": []
    }
    
    with patch("backend.services.llm_service.GeminiProvider.analyze_code", return_value=mock_analysis):
        # 1. Analyze code
        response = client.post("/api/analyze", json={
            "code": "def hello(): print('world')",
            "language": "python",
            "filename": "hello.py",
            "llm_provider": "gemini"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "review_id" in data
        assert data["analysis"]["quality_score"] == 8.5
        review_id = data["review_id"]
        
        # 2. Retrieve review
        response = client.get(f"/api/reviews/{review_id}")
        assert response.status_code == 200
        assert response.json()["review_id"] == review_id
        
        # 3. List reviews
        response = client.get("/api/reviews")
        assert response.status_code == 200
        assert len(response.json()["reviews"]) >= 1

def test_documentation_workflow(client):
    """
    Test end-to-end documentation workflow.
    """
    mock_docs = {
        "overview": "Test documentation",
        "functions": [],
        "classes": [],
        "usage_examples": []
    }
    
    with patch("backend.services.llm_service.GeminiProvider.generate_documentation", return_value=mock_docs):
        # Generate documentation
        response = client.post("/api/document", json={
            "code": "def test(): pass",
            "language": "python",
            "doc_style": "google",
            "llm_provider": "gemini"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "doc_id" in data
        assert data["documentation"]["overview"] == "Test documentation"
