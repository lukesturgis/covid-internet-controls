import json
import logging
import pickle
import socket

log = logging.getLogger(__name__)


def recvall(sock: socket.socket):
    """
    Receive a data transmission, unpickling the response.
    """

    BUFF_SIZE = 1024
    data = b""

    try:
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break

    except socket.error as e:
        log.error(f"Socket error receiving transmission: {e}")

    else:
        try:
            data = pickle.loads(data)

        except pickle.PickleError as e:
            log.error(f"Unable to unserialize transmission: {e}")

        else:
            log.debug(f"Received data: \n{json.dumps(data, indent=4)}")

    finally:
        return data
