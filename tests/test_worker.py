import pytest

from worker.run_worker import app, request_webpage


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


def test_request_webpage_redirect():
    """ Test that we get a redirect for non-https. """
    website = "www.wikipedia.org"
    assert request_webpage(website)["status_code"] == 301


def test_request_webpage_success():
    """ Test that an HTTPS request works. """
    website = "https://www.wikipedia.org"
    assert request_webpage(website)["status_code"] == 200


def test_request_webpage_success_with_tls():
    """ Test that an HTTPS request without adding a prefix works. """
    website = "www.wikipedia.org"
    assert request_webpage(website, use_tls=True)["status_code"] == 200


def test_request_webpage_failure():
    """ Test that a non-existent website fails. """
    website = "aaaaaaaa"
    assert request_webpage(website, timeout=1)["status_code"] == -1
