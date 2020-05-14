import pytest

from src.worker.run_worker import app


@pytest.fixture
def worker():
    app.config["TESTING"] = True

    with app.test_client() as worker:
        yield worker


def test_get_request(worker):
    """Test get request instead of post."""

    req = worker.get("/new_target")
    assert req.status_code == 405


def test_empty_request(worker):
    """Test an empty post request."""

    req = worker.post("/new_target")
    assert req.get_json()["status"] == "error"


def test_invalid_request(worker):
    """Test a request with an invalid key."""

    data = {"invalid": "format"}
    req = worker.post("/new_target", data=data)
    assert req.get_json()["status"] == "error"


def test_ping(worker):
    """Test a ping check."""

    req = worker.get("/ping")
    assert req.get_json()["status"] == "success"
    assert req.get_json()["data"] == "pong"


def test_new_target_http_redirect(worker):
    """Test a new target, getting a 301 to the HTTPS version."""

    data = {"target": "google.com"}
    req = worker.post("/new_target", data=data)
    assert req.get_json()["status_code"] == 301


def test_new_target(worker):
    """Test a new target."""

    data = {"target": "https://www.google.com"}
    req = worker.post("/new_target", data=data)
    assert req.get_json()["status_code"] == 200
