import pytest
from dotenv import load_dotenv
from utils.api_client import ApiClient
from utils.helpers import generate_user

load_dotenv()


@pytest.fixture(scope="session")
def api_client():
    """Base unauthenticated client — for public endpoints"""
    return ApiClient()


@pytest.fixture(scope="session")
def auth_client():
    """Registers a fresh user and returns an authenticated client"""
    client = ApiClient()
    user = generate_user()

    # Register returns plain text "User registered successfully!"
    reg_response = client.post("/api/auth/register", user)
    assert reg_response.status_code == 200, \
        f"Registration failed: {reg_response.text}"

    # Login returns raw JWT token string directly
    login_response = client.post("/api/auth/login", user)
    assert login_response.status_code == 200, \
        f"Login failed: {login_response.text}"

    # Token is the raw response text, not JSON
    token = login_response.text.strip()
    assert token is not None and len(token) > 0, "No token returned from login"

    client.set_token(token)
    return client


@pytest.fixture(scope="function")
def created_task(auth_client):
    """Creates a fresh task before each test, cleans up after"""
    from utils.helpers import generate_task
    task_data = generate_task()
    response = auth_client.post("/api/tasks", task_data)
    assert response.status_code == 201
    task = response.json()

    yield task

    auth_client.delete(f"/api/tasks/{task['id']}")