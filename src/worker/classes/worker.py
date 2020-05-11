import logging
import pickle
import socket

from src.worker.classes.process_pool import MyProcessPoolExecutor
from src.worker.classes.traceroute import Traceroute
from src.worker.utils.get_global_ip import get_global_ip
from src.worker.utils.redis_utils import send_results_to_redis
from src.worker.utils.socket_utils import recvall

log = logging.getLogger(__name__)


class Worker:
    def __init__(self, address: str = "0.0.0.0", port: int = 42075):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.pool = MyProcessPoolExecutor(max_workers=10)
        self.global_ip = get_global_ip()
        self.futures = []
        self.live = True

    def bind(self) -> bool:
        """ Attempt to make a bind, spawning a thread listening for all connections. """

        successful_bind = False
        try:
            self.sock.bind((self.address, self.port))

        except OSError as e:
            log.error(f"Error opening socket: {e}")

        except Exception as e:
            log.error(f"Unknown exception: {e}")

        else:
            successful_bind = True

        finally:
            return successful_bind

    def keep_alive(self) -> None:
        """ Keep server alive infinitely. """

        while self.live:
            self.listen()

        self.shutdown()

    def listen(self) -> None:
        """ Listen for new connections. """

        self.sock.listen(1)
        conn, addr = self.sock.accept()

        data = recvall(conn)
        log.debug(f"Receiving transmission from: {addr}\n {data}")
        response = self.process_transmission(data)
        conn.send(response)
        conn.close()

    def process_transmission(self, data: dict) -> str:
        """ Process a transmission, handing the command appropriately."""

        response = self.make_response("NOT OK")

        try:
            command = data["command"]

        except KeyError:
            log.error(f"Invalid key: received {data}")
            response = self.make_response("ERROR: invalid key")

        except Exception as e:
            log.error(f"Unknown exception: {e}")
            response = self.make_response(e)

        else:

            if command == "ping":
                response = self.make_response("OK")

            elif command == "num_targets":
                num_targets = self.get_number_of_pending_targets()
                response = self.make_response("OK", num_targets)

            elif command == "add_new_targets":
                response = self.process_new_targets(data)
                response = self.make_response(response)

            else:
                response = self.make_response(f"ERROR: Invalid command '{command}'.")

        return response

    def get_number_of_pending_targets(self) -> int:
        """ Get the total number of remaining targets. """

        pending = len(self.futures)
        for future in self.futures:
            if future.done():
                pending -= 1

        return pending

    def process_new_targets(self, data: dict) -> str:
        """ Process the new target payload. """

        response = "Unknown error occured."

        try:
            for protocol in data["protocol"]:
                for target in data["targets"]:
                    self.add_new_target(target, protocol)

        except KeyError as e:
            response = f"Invalid key: {e}"

        except Exception as e:
            response = f"Unknown exception: {e}"

        else:
            response = "OK"
            total_targets = len(data["targets"])
            log.info(f"{total_targets} new targets added.")

        finally:
            return response

    def make_response(self, status: str, data: str = ""):
        """ Make a simple response. """

        response = {"status": status, "data": data}
        return pickle.dumps(response)

    def add_new_target(self, target: str, protocol: str) -> None:
        """ Add a new target. """

        log.debug(f"Adding new traceroute for {target} via {protocol}...")

        traceroute = Traceroute(target, protocol, self.global_ip)
        future = self.pool.submit(traceroute.run)
        future.add_done_callback(self.worker_callback)
        self.futures.append(future)

    def worker_callback(self, future) -> None:
        """ Callback for the traceroute function to send results to Redis. """

        results = future.result()
        if results:
            protocol = results["protocol"]
            target = results["target"]

            log.info(f"\033[1mTraceroute complete for {target} via {protocol}. ")
            send_results_to_redis(target, results)

    def shutdown(self) -> None:
        """ Shut down the worker and listening socket. """

        log.info(f"Worker shutting down...")
        self.pool.shutdown(wait=False)
        self.sock.close()
