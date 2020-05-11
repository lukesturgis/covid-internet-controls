#!/usr/bin/env python3

import argparse
import logging
import sys

import coloredlogs

from src.utils.worker_utils import (
    get_all_workers_status,
    print_status_of_workers,
    send_targets_to_all_workers,
)
from src.worker.utils.input_file_utils import read_txt_input_file
from workers import workers

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")

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
    input_method.add_argument("-f", "--file", type=str, help="Path to input text file.")
    input_method.add_argument("-t", "--target", type=str, help="Individual target.")

    parser.add_argument("--worker", type=str, help="Send targets to a specific worker.")

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    if args.send_targets:

        if args.file:
            targets = read_txt_input_file(args.file)

        elif args.target:
            targets = [args.target]

        else:
            log.error("You must provide either an input file or a target. Exiting...")
            sys.exit(1)

        if args.worker:
            target_worker = None

            for worker in workers:
                if worker["country"].lower() == args.worker.lower():
                    target_worker = worker

            if not target_worker:
                log.error(f"{args.worker} is not valid.")
                sys.exit(1)

            workers = [target_worker]

        send_targets_to_all_workers(workers, targets)

    worker_status = get_all_workers_status(workers)
    print_status_of_workers(worker_status)
