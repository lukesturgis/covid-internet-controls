#!/usr/bin/env python3

import argparse
import logging
import os
import sys

import coloredlogs
import requests
from dotenv import load_dotenv

from workers import workers

load_dotenv()
log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")

REQUEST_KEY = os.getenv("REQUEST_KEY")


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


def send_target_to_workers(target, workers):
    data = {"key": REQUEST_KEY, "target": target}
    for worker in workers:
        address = f"http://{worker['ip']}:42075/new_target"
        response = requests.post(address, data=data)
        log.debug(response)


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
        "-t",
        "--target",
        type=str,
        help="Send a target to a given worker (defaults to all workers).",
    )
    parser.add_argument(
        "-w", "--worker", type=str, help="Send targets to a specific worker."
    )

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    if args.target:
        if args.worker:

            target_worker = None
            for worker in workers:
                if worker["location"].lower() == args.worker.lower():
                    target_worker = worker

            if not target_worker:
                log.error(f"Worker '{args.worker}' does not exist.")
                sys.exit(1)

            workers = [target_worker]
        else:
            workers = workers

        log.info(f"Sending {args.target} to {workers}...")
        send_target_to_workers(args.target, workers)

    for worker in workers:
        worker_url = f"{worker['ip_address']}:{worker['port']}"
        if ping(worker_url):
            print(f"{worker['country']:<10} OK")
        else:
            print(f"{worker['country']:<10} OFFLINE")
