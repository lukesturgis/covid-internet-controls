from utils.url_parse import get_domain_name_from_url, get_path_from_url


def test_get_path_from_url():
    url = "www.google.com/test/hello"
    assert get_path_from_url(url) == "/test/hello"


def test_get_path_from_url_root():
    url = "www.google.com"
    assert get_path_from_url(url) == "/"


def test_get_path_from_url_with_port():
    url = "www.google.com:80/test/hello"
    assert get_path_from_url(url) == "/test/hello"


def test_get_path_from_url_with_prefix():
    url = "http://www.google.com:80/test/hello"
    assert get_path_from_url(url) == "/test/hello"


def test_get_path_from_url_no_path():
    url = "http://google.com:80"
    assert get_path_from_url(url) == "/"


def test_get_domain_name_from_url():
    url = "www.google.com"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_with_path():
    url = "www.google.com/test/hello"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_with_root_path():
    url = "www.google.com/"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_https():
    url = "https://www.google.com"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_no_prefix():
    url = "https://google.com"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_http():
    url = "http://www.google.com"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_http_no_prefix():
    url = "http://google.com"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_no_prefix_no_protocol():
    url = "google.com"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_with_port():
    url = "google.com:80"
    assert get_domain_name_from_url(url) == "www.google.com"


def test_get_domain_name_from_url_with_port_protocol():
    url = "http://www.google.com:80"
    assert get_domain_name_from_url(url) == "www.google.com"
