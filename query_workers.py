#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from itertools import repeat
from multiprocessing.pool import Pool

import coloredlogs
import mysql.connector
import requests
from dotenv import load_dotenv

from workers import workers

load_dotenv()
log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")

REQUEST_KEY = os.getenv("REQUEST_KEY")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"


def ping(worker: str):
    """ Ping a worker for connectivity. """

    log.debug(f"Pinging {worker}...")

    pingable = False

    try:
        response = requests.get(f"http://{worker}:42075/ping", timeout=5)

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


def send_target_to_worker(worker: dict, target: str):
    """ Send a target to a single worker. """

    data = {"key": REQUEST_KEY, "target": target}
    log.debug(f"Sending {target} to {worker['country_name']}...")
    address = f"http://{worker['ip']}:42075/new_target"

    try:
        response = requests.post(address, data=data, timeout=10).json()

    except requests.RequestException as e:
        response = {"success": False, "data": str(e)}

    log.debug(f"{json.dumps(response, indent=4)}")
    response["worker"] = worker
    return response


def setup_db():

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWORD,
        database="covid_internet_controls",
    )
    if conn.is_connected():
        return conn

    log.error("Unable to establish a connection to the database.")
    return None


def create_country(conn, cursor, country_code: str, country_name: str, continent: str):
    inserted = False
    sql = "INSERT IGNORE INTO countries VALUES (%s, %s, %s)"
    val = (country_code, country_name, continent)
    cursor.execute(sql, val)
    conn.commit()

    # assure that it was inserted properly
    sql = "SELECT * FROM countries WHERE country_code = '%s'"
    val = (country_code,)
    cursor.execute(sql, val)
    cursor.fetchall()
    if cursor.rowcount != 1:
        log.error(f"Country {country_code} was not inserted properly.")
    else:
        inserted = True

    return inserted


def send_to_db(results):
    db = mysql.connector.connect(
        host="localhost", user="yourusername", passwd="yourpassword"
    )

    cursor = db.cursor()

    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = ("John", "Highway 21")
    cursor.execute(sql, val)


def send_target_to_workers(target: str, workers: list):
    """ Send a target to all workers in a multiprocessing pool. """

    with Pool(processes=20) as pool:
        results = list(
            pool.starmap(send_target_to_worker, zip(workers, repeat(target)))
        )

        # put all results into respective lists so that we can print successes
        # first, then the failures
        successes = []
        failures = []

        for result in results:
            status_line = f"{BOLD}{result['worker']['country_name']:<20}{RESET}"

            if result["success"]:
                successes.append(
                    status_line + f"{GREEN}SUCCESS - {result['status_code']}{RESET}"
                )

            else:

                # if we did not have success, verify that the worker
                # is not just offline
                if not ping(result["worker"]["ip"]):
                    status_line += f"{RED}ERROR - Worker is offline{RESET}"

                else:
                    status_line += f"{RED}ERROR - {result['data']}{RESET}"

                failures.append(status_line)

        for success in successes:
            print(success)

        for failure in failures:
            print(failure)


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

        # if sending targets, see if we are targeting a specific worker.
        # if so, we need to parse the workers file for the corresponding
        # server location to get its IP address
        if args.worker:

            target_worker = None
            for worker in workers:
                if worker["country_name"].lower() == args.worker.lower():
                    target_worker = worker

            if not target_worker:
                log.error(f"Worker '{args.worker}' does not exist.")
                sys.exit(1)

            workers = [target_worker]

        # otherwise, default to sending target to all workers
        else:
            workers = workers

        send_target_to_workers(args.target, workers)

        for worker in workers:


    # if we are not sending targets, then just ping all workers
    else:

        for worker in workers:
            if ping(worker["ip"]):
                print(f"{worker['country_name']:<20} OK")
            else:
                print(f"{worker['country_name']:<20} OFFLINE")
