import mysql.connector
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")


@pytest.fixture
def conn():
    conn = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
    )

    yield conn
    conn.close()


def test_mysql_is_connected(conn):
    assert conn.is_connected()


def test_show_databases(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")

    found = False
    for databases in cursor:
        if databases[0] == "covid_internet_controls":
            found = True

    assert found
