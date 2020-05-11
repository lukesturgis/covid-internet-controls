from src.worker.utils.request_webpage import request_webpage


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
