#!/usr/bin/env python3

"""
A class representation of an individual hop on the way to a given target.
"""

import logging

log = logging.getLogger(__name__)


class Hop(dict):
    """ Represents an individual hop en route to a target. """

    def __init__(
        self,
        ttl: int,
        source: str = "",
        sent_time: int = None,
        reply_time: int = None,
        response: str = "",
    ) -> None:
        self.source = source
        self.ttl = ttl
        self.sent_time = sent_time
        self.reply_time = reply_time
        self.response = response
        self.rtt = -1
        self.success = False

    def finalize(self) -> None:
        """ Finalize the hop, calculating RTT. """

        self.calculate_rtt()

    def calculate_rtt(self) -> None:
        """ Compute the total RTT for a packet. """

        if self.sent_time and self.reply_time:
            try:
                self.rtt = round((self.reply_time - self.sent_time) * 1000, 3)

            except Exception as e:
                log.error(
                    f"Unable to calculate RTT for {self.reply_time} - {self.sent_time}: {e}"
                )

    def __repr__(self):
        return (
            f"{self.ttl:<5} "
            f"{self.source:<20.20} "
            f"{str(self.rtt):<8.8} "
            f"{str(self.response):<15.15}"
        )
