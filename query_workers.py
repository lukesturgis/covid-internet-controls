#!/usr/bin/env python3

import argparse
import logging
import sys

import coloredlogs
import requests

from workers import workers

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")


def ping(worker: str) -> bool:
    """ Ping a worker for connectivity. """

    log.debug(f"Pinging {worker}...")

    pingable = False

    try:
        response = requests.get(f"http://{worker}/ping", timeout=5)

    except requests.ConnectionError as e:
        log.debug(f"Connecting to {worker} yielded: {e}")

    else:

        data = response.json()

        try:
            if data["status"] == "success":
                pingable = True

        except KeyError:
            log.error("Invalid response.")

    finally:
        return pingable


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose logging.",
    )
    parser.add_argument(
        "--send-targets",
        action="store_true",
        default=False,
        help="Send targets to workers.",
    )

    input_method = parser.add_mutually_exclusive_group()
    input_method.add_argument("-t", "--target", type=str, help="Individual target.")

    parser.add_argument("--worker", type=str, help="Send targets to a specific worker.")

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    for worker in workers:
        worker_url = f"{worker['ip_address']}:{worker['port']}"
        if ping(worker_url):
            print(f"{worker['country']:<10} OK")
        else:
            print(f"{worker['country']:<10} OFFLINE")
