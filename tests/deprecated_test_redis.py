import pytest

from src.worker.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from src.worker.utils.redis_utils import RedisConnection


@pytest.fixture()
def redis_connection():

    connection = RedisConnection(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
    yield connection
    connection.close()


def test_redis_connection(redis_connection):
    """ Assert that we can connect with valid credentials. """
    assert redis_connection is not None


def test_redis_invalid_host():
    """ Assert that we cannot connect with invalid host. """
    connection = RedisConnection(
        REDIS_HOST="", REDIS_PORT=REDIS_PORT, REDIS_PASSWORD=REDIS_PASSWORD
    )
    assert connection.connection is None


def test_redis_invalid_password():
    connection = RedisConnection(
        REDIS_PASSWORD="", REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT
    )
    assert connection.connection is None


def test_redis_invalid_port():
    connection = RedisConnection(
        REDIS_PORT=1, REDIS_HOST=REDIS_HOST, REDIS_PASSWORD=REDIS_PASSWORD
    )
    assert connection.connection is None


def test_redis_set(redis_connection):
    assert redis_connection.set("test", "test")


def test_redis_get(redis_connection):
    assert redis_connection.get("test") == "test"


def test_redis_delete(redis_connection):
    assert redis_connection.delete("test")
