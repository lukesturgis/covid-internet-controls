#!/usr/bin/env python3

"""
A class representation of an individual traceroute to a given target.
"""


import logging
import socket
from datetime import datetime
from time import time

from scapy.all import DNS, DNSQR, ICMP, IP, TCP, UDP, sr1

from src.worker.classes.hop import Hop
from src.worker.utils.request_webpage import request_webpage
from src.worker.utils.url_parse import get_domain_name_from_url, get_path_from_url

log = logging.getLogger(__name__)


class Traceroute(dict):
    """ Represents an individual traceroute to a target. """

    def __init__(
        self,
        target,
        protocol: str,
        global_ip: str,
        max_ttl: int = 30,
        timeout: int = 5,
    ) -> None:

        self.hops = []
        self.protocol = protocol
        self.max_ttl = max_ttl
        self.timeout = timeout
        self.time = str(datetime.now())
        self.global_ip = global_ip

        self.target = get_domain_name_from_url(target)
        if self.protocol == "http" or self.protocol == "https":
            self.path = get_path_from_url(target)

        payloads = {
            "icmp": ICMP(),
            "tcp": TCP(dport=53, flags="S"),
            "udp": UDP() / DNS(qd=DNSQR(qname=self.target)),
            "http": TCP(dport=80, flags="S"),
            "https": TCP(dport=443, flags="S"),
        }
        self.payload = payloads.get(self.protocol)

    def run(self) -> None:
        """ Run the traceroute to the target. """

        log.debug(
            f"Initializing traceroute to {self.target} "
            f"via {self.protocol.upper()}..."
        )

        for ttl in range(1, self.max_ttl + 1):

            try:
                pkt = IP(dst=self.target, ttl=ttl) / self.payload
                reply = sr1(pkt, verbose=0, timeout=self.timeout)

            except socket.gaierror as e:
                log.error(f"Unable to resolve IP for {self.target}: {e}")
                return

            except Exception as e:
                log.error(f"Non-socket exception occured: {e}")
                return

            else:

                # no response, endpoint is likely dropping this traffic
                hop = Hop(ttl=ttl, sent_time=pkt.sent_time)
                if reply is None:
                    hop.source = "*"

                else:
                    hop.source = reply.src
                    hop.reply_time = reply.time

                    # reply type is ICMP means we either got back a destination
                    # unreachable, time expired, or actual ICMP reply
                    if reply.haslayer(ICMP):
                        hop.response = reply.sprintf("%ICMP.type%")

                        if reply.type == 3 or reply.type == 0:
                            hop.success = True

                    else:
                        # if we received a response back that is not ICMP,
                        # we likely received back a SYN/ACK for an HTTP request.

                        if self.protocol == "http" or self.protocol == "https":

                            tls = self.protocol == "https"
                            hop.sent_time = time()

                            response = request_webpage(
                                self.target, self.timeout, path=self.path, use_tls=tls
                            )

                            hop.response = response["status_code"]
                            hop.http_content = response
                            hop.reply_time = time()
                            if response["success"]:
                                hop.success = True

                # finally, calculate metrics for the hop and add it to our results
                hop.finalize()
                self.hops.append(hop)

                if hop.success:
                    break

        # represent each hop as a dictionary instead of as a class object
        hops = [vars(hop) for hop in self.hops]

        results = {
            "target": self.target,
            "protocol": self.protocol,
            "max_ttl": self.max_ttl,
            "timeout": self.timeout,
            "time": self.time,
            "global_ip": self.global_ip,
            "hops": hops,
        }

        return results

    def write_to_stdout(self):
        """ Write the results of the traceroute to stdout. """

        log.debug(
            (
                f"\033[1m"
                f"{'TTL':<5} "
                f"{'IP':<20} "
                f"{'RTT':<8} "
                f"{'RESPONSE':<25}"
                f"\033[0m"
            )
        )
        for hop in self.hops:
            log.debug(hop)
