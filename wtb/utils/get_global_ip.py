import requests


def get_global_ip():
    return requests.get("https://api.ipify.org").text
