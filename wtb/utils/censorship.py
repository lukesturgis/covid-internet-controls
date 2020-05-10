from redis_utils import redis_connect, redis_get_record


def find_censorship():
    connection = redis_connect()

    # go through each website
    for key in connection.keys():

        website = key.decode()
        record = redis_get_record(connection, website)

        # get each protocol and all of the traceroutes that have
        # ever been run under that protocol
        for protocol, results in record["protocol"].items():

            valid_response = -1

            # for each traceroute in the list of traceroute results
            for traceroute in results:

                # go through each hop in the given traceroute
                for hop in traceroute["hops"]:

                    # find where we got the first valid response
                    if (
                        hop["response"]
                        and hop["response"] != "*"
                        and hop["response"] != "time-exceeded"
                    ):
                        valid_response = ""


if __name__ == "__main__":
    find_censorship()
