import pytest
import allure
from utils.helpers import generate_user
from utils.api_client import ApiClient


@allure.feature("Authentication")
class TestAuth:

    @allure.story("Register")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_register_success(self, api_client):
        """POST /api/auth/register — should register a new user successfully"""
        user = generate_user()

        with allure.step("Send register request"):
            response = api_client.post("/api/auth/register", user)

        with allure.step("Verify 200 status and success message"):
            assert response.status_code == 200
            assert "success" in response.text.lower() or \
                   "registered" in response.text.lower()

    @allure.story("Register - Duplicate User")
    @pytest.mark.auth
    def test_register_duplicate_user(self, api_client):
        """POST /api/auth/register — should fail when username already exists"""
        user = generate_user()

        first = api_client.post("/api/auth/register", user)
        assert first.status_code == 200

        second = api_client.post("/api/auth/register", user)
        assert second.status_code in [400, 403, 409, 500]

    @allure.story("Register - Validation")
    @pytest.mark.parametrize("payload,description", [
        ({}, "empty body"),
    ])
    @pytest.mark.auth
    def test_register_invalid_inputs(self, api_client, payload, description):
        """POST /api/auth/register — should reject completely empty body"""
        response = api_client.post("/api/auth/register", payload)
        assert response.status_code in [400, 403, 500], \
            f"Expected error for {description}, got {response.status_code}"

    @allure.story("Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_success(self, api_client):
        """POST /api/auth/login — should return JWT token"""
        user = generate_user()

        api_client.post("/api/auth/register", user)

        with allure.step("Send login request"):
            response = api_client.post("/api/auth/login", user)

        with allure.step("Verify 200 status"):
            assert response.status_code == 200

        with allure.step("Verify token is returned"):
            token = response.text.strip()
            assert token is not None
            assert len(token) > 20
            assert "." in token

    @allure.story("Login - Wrong Password")
    @pytest.mark.auth
    def test_login_wrong_password(self, api_client):
        """POST /api/auth/login — should fail with wrong password"""
        user = generate_user()
        api_client.post("/api/auth/register", user)

        wrong_creds = {"username": user["username"], "password": "wrongpassword"}
        response = api_client.post("/api/auth/login", wrong_creds)
        assert response.status_code in [401, 403]

    @allure.story("Login - Non-existent User")
    @pytest.mark.auth
    def test_login_nonexistent_user(self, api_client):
        """POST /api/auth/login — should fail for unknown user"""
        fake_user = {"username": "ghost_user_xyz999", "password": "somepassword"}
        response = api_client.post("/api/auth/login", fake_user)
        assert response.status_code in [401, 403]

    @allure.story("Protected Route - No Token")
    @pytest.mark.auth
    def test_access_protected_route_without_token(self):
        """GET /api/tasks — should return 401 or 403 without token"""
        client = ApiClient()
        response = client.get("/api/tasks")
        assert response.status_code in [401, 403]

    @allure.story("Protected Route - Invalid Token")
    @pytest.mark.auth
    def test_access_protected_route_with_invalid_token(self):
        """GET /api/tasks — should return 401 or 403 with fake token"""
        client = ApiClient(token="this.is.not.a.valid.token")
        response = client.get("/api/tasks")
        assert response.status_code in [401, 403]

    @allure.story("Protected Route - Valid Token")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_access_protected_route_with_valid_token(self, auth_client):
        """GET /api/tasks — should return 200 with valid JWT token"""
        response = auth_client.get("/api/tasks")
        assert response.status_code == 200