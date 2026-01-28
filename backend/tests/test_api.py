import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "llm_providers" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_get_llm_providers(client):
    """Test LLM providers endpoint."""
    response = client.get("/api/config/llm-providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert isinstance(data["providers"], list)


def test_analyze_code_missing_fields(client):
    """Test analyze endpoint with missing fields."""
    response = client.post("/api/analyze", json={})
    assert response.status_code == 422  # Validation error


def test_analyze_code_invalid_provider(client):
    """Test analyze endpoint with invalid provider."""
    response = client.post("/api/analyze", json={
        "code": "print('hello')",
        "language": "python",
        "llm_provider": "invalid_provider"
    })
    # Should return 400 or 500 depending on provider availability
    assert response.status_code in [400, 500]


def test_document_code_missing_fields(client):
    """Test document endpoint with missing fields."""
    response = client.post("/api/document", json={})
    assert response.status_code == 422  # Validation error


def test_get_reviews_empty(client):
    """Test get reviews with empty database."""
    response = client.get("/api/reviews")
    assert response.status_code == 200
    data = response.json()
    assert "reviews" in data
    assert "pagination" in data
    assert len(data["reviews"]) == 0
    assert data["pagination"]["total"] == 0


def test_get_reviews_pagination(client):
    """Test reviews pagination parameters."""
    response = client.get("/api/reviews?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["limit"] == 5


def test_get_review_not_found(client):
    """Test get review with non-existent ID."""
    response = client.get("/api/reviews/non-existent-id")
    assert response.status_code == 404


def test_delete_review_not_found(client):
    """Test delete review with non-existent ID."""
    response = client.delete("/api/reviews/non-existent-id")
    assert response.status_code == 404
