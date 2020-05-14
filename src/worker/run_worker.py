#!/usr/bin/env python3


import logging
import sys
from argparse import ArgumentParser
from src.worker.utils.request_webpage import request_webpage

import coloredlogs
from flask import Flask, request, jsonify


app = Flask(__name__)

log = logging.getLogger(__name__)
logging.getLogger("scapy").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.WARNING)
coloredlogs.install(level="INFO", fmt="%(message)s")


def make_response(status: str, data: str = ""):
    """ Make a simple response. """

    return jsonify({"status": status, "data": data})


@app.route("/ping", methods=["GET"])
def ping():
    return make_response("success", "pong")


@app.route("/new_target", methods=["POST"])
def new_target():
    try:
        requested_target = request.form["target"]

    except KeyError:
        return make_response("error", "Invalid data format. Need target.")

    data = request_webpage(requested_target)
    return data


if __name__ == "__main__":
    parser = ArgumentParser("Listen for targets.")

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose logging.",
    )
    parser.add_argument(
        "-a", "--addr", default="0.0.0.0", help="Address to listen on for connections."
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=42075,
        help="Port for this worker to listen on for remote connections.",
    )

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    app.run(host=args.addr, port=args.port)
