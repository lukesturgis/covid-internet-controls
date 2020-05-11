import logging

import requests
from fake_useragent import UserAgent

log = logging.getLogger(__name__)


def request_webpage(
    target: str, timeout: int = 10, path: str = "/", use_tls: bool = False
):

    if use_tls and not target.startswith("https://"):
        target = "https://" + target

    else:
        if not target.startswith("http://") and not target.startswith("https://"):
            target = "http://" + target

    headers = {"User-Agent": UserAgent().random}

    data = {"success": False, "status_code": -1, "headers": "", "content": ""}

    try:
        response = requests.get(
            target, headers=headers, timeout=timeout, allow_redirects=False
        )

    except requests.ConnectionError as e:
        content = e

    except requests.RequestException as e:
        content = e

    except requests.TooManyRedirects as e:
        content = e

    except requests.RequestException as e:
        content = e

    except Exception as e:
        log.error(f"Unknown exception for {target}: {e}")
        content = str(e)

    else:

        headers = response.headers
        data["headers"] = dict(headers)
        data["status_code"] = response.status_code
        data["success"] = True
        data["path"] = path

        try:
            content = response.content.decode(response.encoding or "utf-8")

        except UnicodeDecodeError:
            content = response.text

    finally:
        data["content"] = content

    return data
