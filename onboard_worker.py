#!/usr/bin/env python3

import argparse
import logging
import subprocess
import sys
import time
from threading import Thread

import coloredlogs
import paramiko
from scp import SCPClient

from query_workers import ping
from workers import workers

log = logging.getLogger(__name__)
coloredlogs.install(level="INFO", fmt="%(message)s")
logging.getLogger("paramiko").setLevel(logging.WARNING)


def initiate_connection(ip: str) -> paramiko.SSHClient:
    """ Initiate an SSH connection to a remote host. """

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log.debug(f"Connecting to {ip}...")

    try:
        client.connect(ip, username="root", timeout=10)

    except paramiko.ssh_exception.AuthenticationException:
        log.error("Invalid credentials.")
        client = None

    except:
        log.error("Unable to connect.")
        client = None

    finally:
        return client


def run_command(client: paramiko.SSHClient, command: str, ignore_error=False) -> bool:
    """ Run a command on a remote host. """

    success = False
    stdin, stdout, stderr = client.exec_command(command)

    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        success = True

    for line in stdout.read().splitlines():
        log.debug(line.decode("utf8"))

    del stdin, stdout, stderr
    return success


def shutdown_client(client: paramiko.SSHClient) -> None:
    """ Shutdown a Paramiko SSH client properly. """
    client.close()
    del client


def copy_files(ip: str) -> bool:
    """ Copy files over to a remote host. """

    subprocess.call(
        ["rsync", "-av", '--exclude=".*"', "worker", f"root@{ip}:/root/worker"]
    )


def check_docker(client: paramiko.SSHClient) -> None:
    installed = False
    if run_command(client, "dpkg -s docker.io"):
        installed = True

    return installed


def docker_cleanup(client: paramiko.SSHClient) -> None:
    """ Cleanup and remove any possible docker containers running already. """
    run_command(client, "docker stop $(docker ps -aq)", ignore_error=True)
    run_command(client, "docker rm $(docker ps -aq)", ignore_error=True)


def verify_connectivity(ip: str) -> bool:
    """ Verify that a worker is online, trying 3 times. """

    online = False
    log.info(f"Checking connectivity to {ip}...")
    for _ in range(3):
        if ping(ip):
            online = True
            break
        time.sleep(3)

    return online


def onboard_worker(ip: str):
    # initiate a connection to the remote host
    log.info("Connecting to remote host...")
    client = initiate_connection(ip)
    if not client:
        sys.exit(1)

    log.info("Connection successful.")

    if not check_docker(client):
        log.info("Updating packages...")
        if not run_command(client, "apt update"):
            sys.exit(1)

        # install docker
        log.info("Package update successful. Installing Docker...")
        if not run_command(client, f"apt install -y docker.io"):
            sys.exit(1)

        log.info("Package installation successful.")

    else:
        # remove any possible docker containers, if they exist from a
        # previous onboarding session, just to be safe.
        log.info("Cleaning up old Docker images...")
        docker_cleanup(client)

    # copy over all of the local files needed to run the worker
    log.info("Copying local files...")
    copy_files(ip)

    # build the docker image, then run it
    log.info("Local files copied. Building Docker image...")
    if not run_command(client, "cd worker && docker build -t worker ."):
        sys.exit(1)

    log.info("Docker image built. Running it now...")
    if not run_command(client, "docker run --publish 42075:42075 -d worker"):
        sys.exit(1)

    # verify that we can ping the newly onboarded worker
    online = verify_connectivity(f"{ip}:42075")
    if online:
        log.info("Ping check successful, worker is online.")
    else:
        log.error("Something went wrong, unable to ping the worker.")

    shutdown_client(client)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Onboard a new worker node.")
    parser.add_argument("-a", "--ip", type=str, help="IP address of worker.")
    parser.add_argument(
        "-u", "--user", type=str, default="root", help="Username to SSH as."
    )
    parser.add_argument("-p", "--password", type=str, help="User password.")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose logging.",
    )
    parser.add_argument(
        "--all", action="store_true", default=False, help="Onboard all workers."
    )

    args = parser.parse_args()

    # set log level to debug if verbose flag is passed
    if args.verbose:
        coloredlogs.install(
            level="DEBUG", fmt="%(asctime)s - %(levelname)s - %(message)s"
        )

    if args.all:
        threads = []
        for worker in workers:
            print(worker)
            log.info(f"Onboarding {worker['country']}...")
            ip = worker["ip_address"]
            thread = Thread(target=onboard_worker, args=(ip,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        for worker in workers:
            if ping(f"{worker['ip_address']}:42075"):
                print(f"{worker['country']:<20} OK")
            else:
                print(f"{worker['country']:<20} ERROR")
