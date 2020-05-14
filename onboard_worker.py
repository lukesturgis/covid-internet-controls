#!/usr/bin/env python3

import argparse
import logging
import sys
import time

import coloredlogs
import paramiko
from scp import SCPClient

from query_workers import ping

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")
logging.getLogger("paramiko").setLevel(logging.WARNING)


def initiate_connection(ip: str, user: str, password: str) -> paramiko.SSHClient:
    """ Initiate an SSH connection to a remote host. """

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=user, passphrase=password)

    except paramiko.ssh_exception.AuthenticationException:
        log.error("Invalid credentials.")
        client = None

    finally:
        return client


def run_command(client: paramiko.SSHClient, command: str, ignore_error=False) -> bool:
    """ Run a command on a remote host. """

    success = False
    try:
        stdin, stdout, stderr = client.exec_command(command)

    except paramiko.SSHException as e:
        if not ignore_error:
            log.error(f"Error running {command}: {e}")
        else:
            print("got error, aint doin it")

    else:
        success = True
        for line in stdout.read().splitlines():
            log.debug(line.decode("utf8"))

    finally:
        del stdin, stdout, stderr
        return success


def shutdown_client(client: paramiko.SSHClient) -> None:
    """ Shutdown a Paramiko SSH client properly. """
    client.close()
    del client


def copy_files(client: paramiko.SSHClient) -> bool:
    """ Copy files over to a remote host. """

    # TODO: switch over to rsync
    with SCPClient(client.get_transport()) as scp:
        scp.put("./worker", recursive=True)


def docker_cleanup(client: paramiko.SSHClient) -> None:
    """ Cleanup and remove any possible docker containers running already. """
    run_command(client, "docker stop $(docker ps -aq)", ignore_error=True)
    run_command(client, "docker rm $(docker ps -aq)", ignore_error=True)


def verify_connectivity(ip: str) -> bool:
    """ Verify that a worker is online, trying 3 times. """

    online = False
    log.info("Checking connectivity...")
    for _ in range(3):
        if ping(args.ip):
            online = True
            break
        time.sleep(3)

    return online


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Onboard a new worker node.")
    parser.add_argument(
        "-a", "--ip", type=str, required=True, help="IP address of worker."
    )
    parser.add_argument(
        "-u", "--user", type=str, default="root", help="Username to SSH as."
    )
    parser.add_argument(
        "-p", "--password", type=str, required=True, help="User password."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose logging.",
    )

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    # initiate a connection to the remote host
    log.info("Connecting to remote host...")
    client = initiate_connection(args.ip, args.user, args.password)
    if not client:
        sys.exit(1)

    log.info("Connection successful. Updating packages...")

    # update the packages
    if not run_command(client, "apt update"):
        sys.exit(1)

    # install docker
    log.info("Package update successful. Installing required packages...")
    required_packages = "docker.io"
    if not run_command(client, f"apt install -y {required_packages}"):
        sys.exit(1)

    # remove any possible docker containers, if they exist from a
    # previous onboarding session, just to be safe.
    docker_cleanup(client)

    # copy over all of the local files needed to run the worker
    log.info("Package installation successful. Copying local files...")
    copy_files(client)

    # build the docker image, then run it
    log.info("Local files copied. Building Docker image...")
    if not run_command(client, "cd worker && docker build -t worker ."):
        sys.exit(1)

    log.info("Docker image built. Running it now...")
    if not run_command(client, "docker run --publish 42075:42075 -d worker"):
        sys.exit(1)

    # verify that we can ping the newly onboarded worker
    online = verify_connectivity(args.ip)
    if online:
        log.info("Ping check successful, worker is online.")
    else:
        log.error("Something went wrong, unable to ping the worker.")

    shutdown_client(client)
