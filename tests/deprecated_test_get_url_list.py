import os
from pathlib import Path

from utils.get_url_list import format_csv_results, get_url_list, save_url_list_to_file


def test_get_url_list_valid():
    # test that a valid country code gets a response
    url_list = get_url_list("us")
    assert url_list != ""


def test_get_url_list_invalid():
    # test that an invalid country doesnt exist
    assert get_url_list("no_exist") == ""


def test_get_url_list_is_list():
    # test that formatting the results gives back a list
    url_list = get_url_list("us")
    formatted_results = format_csv_results(url_list)
    assert isinstance(formatted_results, list)


def test_url_list_saves_to_file():
    # test that writing the url list to a file works

    country_code = "us"
    url_list = get_url_list("us")
    formatted_results = format_csv_results(url_list)

    save_url_list_to_file(formatted_results, country_code)

    INPUT_DIRECTORY = os.path.join(Path(__file__).resolve().parents[1], "input")
    file_path = os.path.join(INPUT_DIRECTORY, f"{country_code}.txt")

    assert os.path.exists(file_path)
