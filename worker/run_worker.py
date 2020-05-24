#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

import coloredlogs
import requests
from fake_useragent import UserAgent
from flask import Flask, jsonify, request

app = Flask(__name__)
log = logging.getLogger(__name__)
logging.getLogger("scapy").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.WARNING)
coloredlogs.install(level="INFO", fmt="%(message)s")


def request_webpage(target: str, timeout: int = 10):
    """ Request a given webpage, returning the received response. """

    if not target.startswith("http://") and not target.startswith("https://"):
        target = f"http://{target}"

    headers = {"User-Agent": UserAgent().random}

    data = {"success": False}

    try:
        response = requests.get(
            target, headers=headers, timeout=timeout, allow_redirects=False
        )

    except requests.RequestException as e:
        error_message = f"Request exception for {target}: {str(e)}"
        log.error(error_message)
        data["data"] = error_message

    else:

        try:
            content = response.content.decode(response.encoding or "utf-8")

        except UnicodeDecodeError:
            content = response.text

        data = {
            "target": target,
            "headers": dict(response.headers),
            "status_code": response.status_code,
            "success": True,
            "content": content,
        }

    finally:
        return data


def make_response(status: str, data: str = ""):
    """ Make a simple response. """
    return jsonify({"status": status, "data": data})


@app.route("/ping", methods=["GET"])
def ping():
    """ Respond to a given ping request. """
    return make_response("success", "pong")


@app.route("/new_target", methods=["POST"])
def new_target():
    """ Respond to a new target request. """
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
