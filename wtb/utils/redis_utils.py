#!/usr/bin/env python3

"""
Various utilities for interacting with Redis.
"""

import json
import logging
import os

import redis

from config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, ROOT_DIR

log = logging.getLogger(__name__)


class RedisConnection:
    def __init__(self, REDIS_HOST: str, REDIS_PORT: str, REDIS_PASSWORD: int):
        """ Instantiate a connection to the redis server. """

        CERT_PATH = os.path.join(ROOT_DIR, "certs", "cert.pem")

        self.connection = None
        try:
            conn = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                ssl=True,
                ssl_ca_certs=CERT_PATH,
                decode_responses=True,
            )
            conn.ping()

        except redis.AuthenticationError:
            log.error("Invalid authentication.")

        except redis.ConnectionError:
            log.error("Unable to connect to redis database.")

        except Exception as e:
            log.error(f"Unknown exception occured: {e}")

        else:
            self.connection = conn

    def set(self, target: str, record: dict) -> bool:
        """ Set a record within the redis database. """
        if self.connection.set(target, json.dumps(record)):
            return True
        return False

    def push(self, target: str, record: dict) -> bool:
        """ Append a record to its list within Redis. """
        if self.connection.lpush(target, json.dumps(record)):
            return True
        return False

    def get(self, target: str) -> dict:
        """ Get an existing record from the redis database. """
        data = self.connection.lrange(target, 0, -1)
        decoded_data = []
        for dp in data:
            decoded_data.append(json.loads(dp))
        return decoded_data

    def delete(self, target: str) -> bool:
        return self.connection.delete(target)

    def close(self) -> None:
        self.connection.close()

    def get_keys(self):
        return self.connection.keys()


def send_results_to_redis(target: str, results: dict) -> None:
    """ Send the results of the traceroute to the redis database. """

    log.info(f"Sending results to redis...\033[0m")
    log.debug(f"\n{json.dumps(results, indent=4)}")

    connection = RedisConnection(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

    if not connection.push(target, results):
        log.error("Unable to append results within redis.")
    else:
        log.debug("Results sent to redis successfully.")

    connection.close()
