def strip_protocol(url: str):
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    return url


def get_domain_name_from_url(url: str):
    """
    Parse a URL and extract the domain name without any extras (port, etc.)
    """

    # HOTFIX: getting rid of tldextract dependency for pyinstaller build,
    # need to build more robust version of url processing but this is good
    # for now

    # strip protocol
    url = url.replace("http://", "")
    url = url.replace("https://", "")

    # now strip path
    url = url.split("/")
    url = url[0]

    # strip port, if existing
    url = url.split(":")[0]

    if not url.startswith("www."):
        url = "www." + url

    return url


def get_path_from_url(url: str):
    url = strip_protocol(url)

    url_split = url.split("/")
    path = "/"
    if len(url_split) > 1:
        path = path + "/".join(url_split[1:])

    return path
