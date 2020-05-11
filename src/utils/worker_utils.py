import logging
import pickle
import socket
from multiprocessing import Pool
from tqdm import tqdm
from src.worker.utils.socket_utils import recvall

log = logging.getLogger(__name__)

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
reset = "\033[0m"
bold = "\033[1m"


def ping(worker: str, port: int = 42075) -> bool:
    """ Ping a worker for connectivity. """

    log.debug(f"Pinging {worker}:{port}...")
    payload = {"command": "ping"}
    pingable = False

    response = sendrcv(worker, port, payload)

    if response:
        if response["status"] == "OK":
            pingable = True

    return pingable


def send_targets_to_worker(
    worker: str, targets: list, country: str, port=42075, protocol: str = None
) -> bool:
    """ Send a list of targets to a worker. """

    # if no protocol was provided, default to run all protocols
    protocols = []
    if protocol:
        protocols.append(protocol)
    else:
        protocols = ["tcp", "icmp", "http", "https"]

    progress_bar = tqdm(
        total=len(targets),
        desc=country,
        unit=" targets",
        ascii=" ▓",
        bar_format="{l_bar}%s{bar}%s{r_bar}" % ("\033[34m", "\033[0m"),
        leave=False,
    )

    # HOTFIX FOR BUFFER OVERFLOW ERROR:
    # pickling larger than a certain number of bytes on the client end
    # causes the transmission to be split up. unsure of how to resolve this.
    # for now, break the target list up into sublists of 10 targets and send
    # each sublist until all targets have been submitted
    all_submitted = True

    sub_lists = [targets[i : i + 10] for i in range(0, len(targets), 10)]

    for target_sub_list in sub_lists:
        payload = {
            "command": "add_new_targets",
            "protocol": protocols,
            "targets": target_sub_list,
        }
        response = sendrcv(worker, port, payload)

        if response:
            if response["status"] != "OK":
                all_submitted = False
                log.error(
                    f"Received the following response from {worker}:{port}: {response}"
                )

        else:
            all_submitted = False

        progress_bar.update(10)

    return all_submitted


def get_number_of_targets_remaining(worker: str, port=42075) -> int:
    """ Get the number of pending targets a worker has. """

    log.debug(f"Querying {worker}:{port} for number of targets remaining...")
    payload = {"command": "num_targets"}
    response = sendrcv(worker, port, payload)
    num_targets = -1

    if response:
        log.debug(
            f"Received the following response from {worker}:{port} "
            f"for remaining targets: {response}"
        )

        if response["status"] == "OK":
            num_targets = response["data"]

    return num_targets


def sendrcv(worker: str, port: int, data: dict) -> dict:
    """ Send a transmission and receive the response. """

    received_data = None
    connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_sock.settimeout(5)

    try:
        log.debug(f"Opening connection to worker at {worker}:{port}...")
        connect_sock.connect((worker, port))

    except ConnectionRefusedError:
        log.error("Connection refused.")

    except OSError as e:
        log.error(e)

    except socket.timeout:
        log.error(f"Connection to {worker}:{port} timed out.")

    else:

        received_data = None
        pickled_data = pickle.dumps(data)

        try:
            connect_sock.send(pickled_data)
            received_data = recvall(connect_sock)

        except socket.error as e:
            log.error(f"Socket error from {worker}:{port}: {e}")

        except Exception as e:
            log.error(
                f"Unknown exception occured receiving data from {worker}:{port}: {e}"
            )

    finally:
        connect_sock.close()

    return received_data


def print_status_of_workers(results: list) -> None:
    """ Print the status results of all workers. """
    print(
        f"\033[1m"
        f"{'IP ADDRESS':<20} "
        f"{'PORT':<10} "
        f"{'COUNTRY':<15} "
        f"{'STATUS':<10} "
        f"{'PENDING':<15}"
        f"\033[0m"
    )
    for worker in results:
        print(
            f"{worker['ip_address']:<20} "
            f"{worker['port']:<10} "
            f"{worker['country']:<15} "
            f"{worker['status']:<10} "
            f"    {worker['pending']:<15}"
        )


def send_targets_to_all_workers(workers: list, targets: list) -> None:
    """ Send targets to all workers. """

    log.debug(f"{len(targets)} targets received.")

    for worker in workers:
        country = worker["country"]
        log.debug(f"Sending targets to {country}...")

        if send_targets_to_worker(
            worker["ip_address"], targets, country, port=worker["port"]
        ):
            log.info(f"Targets sent to {country} successfully.")

        else:
            log.error(f"error sending workers to {country}")


def get_worker_status(worker: dict) -> dict:
    """ Get the status of a single worker. """

    ip = worker["ip_address"]
    port = worker["port"]
    worker["pending"] = f"{red}ERROR{reset}"
    worker["status"] = f"{red}OFFLINE{reset}"

    pingable = ping(ip, port)
    if pingable:
        worker["status"] = f"{green}ONLINE{reset}"

        num_targets = get_number_of_targets_remaining(ip, port)

        if num_targets != -1:
            worker["pending"] = f"{yellow}{num_targets}{reset}"

    return worker


def get_all_workers_status(workers) -> list:
    """ Get the status of all workers. """
    with Pool(processes=20) as pool:
        results = pool.map(get_worker_status, workers)

    return results
