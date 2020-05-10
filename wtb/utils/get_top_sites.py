#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys

BASE_URL = "https://www.alexa.com/topsites/countries"

if __name__ == "__main__":

    country_code = sys.argv[1].upper()
    url = BASE_URL + "/" + country_code
    response = requests.get(url)

    soup = BeautifulSoup(response.text, features="lxml")
    bullets = soup.find_all("div", {"class": "site-listing"})

    for bullet in bullets:
        items = bullet.find("div", {"class": "DescriptionCell"})
        print(items.text.strip())
