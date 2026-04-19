import pytest
import allure
from utils.helpers import generate_task


@allure.feature("Task Management")
class TestTaskCRUD:

    @allure.story("Create Task")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.tasks
    def test_create_task_success(self, auth_client):
        """POST /api/tasks — should create a task and return 201"""
        task_data = generate_task(priority="HIGH")

        with allure.step("Send POST request to create task"):
            response = auth_client.post("/api/tasks", task_data)

        with allure.step("Verify response status is 201"):
            assert response.status_code == 201

        with allure.step("Verify response body contains correct data"):
            body = response.json()
            assert body["id"] is not None
            assert body["title"] == task_data["title"]
            assert body["priority"] == "HIGH"
            assert body["completed"] is False

        auth_client.delete(f"/api/tasks/{body['id']}")

    @allure.story("Create Task - Validation")
    @pytest.mark.parametrize("priority", ["LOW", "MEDIUM", "HIGH"])
    @pytest.mark.tasks
    def test_create_task_all_priorities(self, auth_client, priority):
        """POST /api/tasks — should accept all valid priority levels"""
        task_data = generate_task(priority=priority)

        response = auth_client.post("/api/tasks", task_data)
        assert response.status_code == 201
        body = response.json()
        assert body["priority"] == priority

        auth_client.delete(f"/api/tasks/{body['id']}")

    @allure.story("Create Task - Validation")
    @pytest.mark.tasks
    def test_create_task_missing_title(self, auth_client):
        """POST /api/tasks — should return 400 or 403 when title is missing"""
        task_data = {
            "description": "No title provided",
            "priority": "LOW",
            "completed": False
        }
        response = auth_client.post("/api/tasks", task_data)
        assert response.status_code in [400, 403]

    @allure.story("Get Tasks")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.tasks
    def test_get_all_tasks(self, auth_client, created_task):
        """GET /api/tasks — should return list of tasks"""
        response = auth_client.get("/api/tasks")
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) >= 1

    @allure.story("Get Task by ID")
    @pytest.mark.tasks
    def test_get_task_by_id(self, auth_client, created_task):
        """GET /api/tasks/{id} — should return correct task"""
        task_id = created_task["id"]
        response = auth_client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == task_id
        assert body["title"] == created_task["title"]

    @allure.story("Get Task by ID - Not Found")
    @pytest.mark.tasks
    def test_get_task_not_found(self, auth_client):
        """GET /api/tasks/99999 — should return 403 or 404 for non-existent task"""
        response = auth_client.get("/api/tasks/99999")
        assert response.status_code in [403, 404]

    @allure.story("Update Task")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.tasks
    def test_update_task(self, auth_client, created_task):
        """PUT /api/tasks/{id} — should update task fields"""
        task_id = created_task["id"]
        updated_data = {
            "title": "Updated title",
            "description": "Updated description",
            "priority": "LOW",
            "completed": True
        }
        response = auth_client.put(f"/api/tasks/{task_id}", updated_data)
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated title"
        assert body["completed"] is True
        assert body["priority"] == "LOW"

    @allure.story("Delete Task")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.tasks
    def test_delete_task(self, auth_client):
        """DELETE /api/tasks/{id} — should delete task and return 204"""
        task_data = generate_task()
        create_response = auth_client.post("/api/tasks", task_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        delete_response = auth_client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == 204

        get_response = auth_client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code in [403, 404]

    @allure.story("Mark Task Complete")
    @pytest.mark.parametrize("completed_status", [True, False])
    @pytest.mark.tasks
    def test_task_completion_toggle(self, auth_client, created_task, completed_status):
        """PUT /api/tasks/{id} — should set completed status correctly"""
        task_id = created_task["id"]
        updated = {**created_task, "completed": completed_status}
        response = auth_client.put(f"/api/tasks/{task_id}", updated)
        assert response.status_code == 200
        assert response.json()["completed"] == completed_status