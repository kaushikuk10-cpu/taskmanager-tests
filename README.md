# Task Manager API Test Framework

![CI](https://github.com/kaushikuk10-cpu/taskmanager-tests/actions/workflows/ci.yml/badge.svg)

A production-grade API test automation framework built with **pytest**, **Allure Reports**, and **GitHub Actions CI/CD**. Tests the [Task Manager REST API](https://github.com/kaushikuk10-cpu/taskmanager) — a Spring Boot application with JWT authentication.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core language |
| pytest | Test framework |
| requests | HTTP client |
| Faker | Test data generation |
| Allure | Test reporting |
| GitHub Actions | CI/CD pipeline |
| python-dotenv | Environment config |

---

## Project Structure

```
taskmanager-tests/
├── tests/
│   ├── auth/
│   │   └── test_auth.py        # JWT auth flow tests (9 tests)
│   └── tasks/
│       └── test_tasks.py       # CRUD operation tests (12 tests)
├── utils/
│   ├── api_client.py           # Reusable HTTP client wrapper
│   └── helpers.py              # Faker-based test data generators
├── conftest.py                 # Shared fixtures (auth_client, created_task)
├── pytest.ini                  # Pytest config and custom markers
├── requirements.txt            # Dependencies
└── .github/workflows/ci.yml    # GitHub Actions pipeline
```

---

## Test Coverage

### Auth Tests (9 tests)
- ✅ Register new user successfully
- ✅ Reject duplicate username registration
- ✅ Reject invalid/empty request body
- ✅ Login and receive JWT token
- ✅ Reject wrong password
- ✅ Reject non-existent user login
- ✅ Block unauthenticated access to protected routes
- ✅ Block invalid JWT token
- ✅ Allow valid JWT token access

### Task CRUD Tests (12 tests)
- ✅ Create task successfully
- ✅ Create tasks with all priority levels (LOW/MEDIUM/HIGH) — parametrized
- ✅ Reject task creation with missing title
- ✅ Get all tasks
- ✅ Get task by ID
- ✅ Handle non-existent task ID
- ✅ Update task fields
- ✅ Delete task and verify removal
- ✅ Toggle task completion status — parametrized

---

## Running Locally

### Prerequisites
- Python 3.12+
- The [Task Manager API](https://github.com/kaushikuk10-cpu/taskmanager) running on `localhost:8080`

### Setup

```bash
git clone https://github.com/kaushikuk10-cpu/taskmanager-tests.git
cd taskmanager-tests
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file in the root:

```
BASE_URL=http://localhost:8080
TEST_USERNAME=testuser
TEST_PASSWORD=testpass123
```

### Run all tests

```bash
pytest tests/ -v
```

### Run by marker

```bash
pytest -m smoke        # Quick sanity tests only
pytest -m auth         # Auth tests only
pytest -m tasks        # Task CRUD tests only
pytest -m regression   # Full regression suite
```

### Generate Allure report

```bash
pytest tests/ --alluredir=allure-results -v
allure serve allure-results
```

---

## Allure Report

The framework generates rich visual test reports with:
- Pass/fail overview dashboard
- Test breakdown by feature and story
- Step-by-step execution details
- Severity classification (Critical, Normal, Minor)
- Timeline view

---

## CI/CD Pipeline

Every push to `main` automatically:

1. Spins up an Ubuntu runner on GitHub Actions
2. Installs Java 17 (Temurin) and Python 3.12
3. Clones and starts the Spring Boot API in the background
4. Polls the API health check until it responds
5. Runs all 21 tests with Allure output
6. Uploads test results as downloadable artifacts (7 day retention)

---

## Key Framework Features

**Reusable HTTP client** — `ApiClient` wraps `requests.Session` with automatic JWT header injection, keeping test code clean and DRY.

**Smart fixtures** — `conftest.py` provides session-scoped `auth_client` (registers and logs in a fresh user once per test session) and function-scoped `created_task` (creates a task before each test and deletes it after — no test pollution).

**Parametrized tests** — pytest `@parametrize` decorators run the same test logic across multiple inputs (all 3 priority levels, both completion states) with a single test definition.

**Allure decorators** — every test is annotated with `@allure.feature`, `@allure.story`, and `@allure.severity` producing a navigable, professional test report.

**Environment-driven config** — all URLs and credentials live in `.env`, never hardcoded. CI overrides via environment variables.

---

## Author

**Kaushik Krishnananda Prabhu** — [GitHub](https://github.com/kaushikuk10-cpu)

---

## License

This project is open source and available under the [MIT License](LICENSE).
