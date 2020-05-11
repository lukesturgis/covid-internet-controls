from src.worker.classes.traceroute import Traceroute


def test_icmp():
    traceroute = Traceroute("www.google.com", protocol="icmp", global_ip="0.0.0.0")
    results = traceroute.run()
    for hop in results["hops"]:
        print(hop)
    assert results is None


def test_tcp():
    traceroute = Traceroute("www.google.com", protocol="tcp", global_ip="0.0.0.0")
    results = traceroute.run()
    for hop in results["hops"]:
        print(hop)
    assert results is None


def test_http():
    traceroute = Traceroute("www.google.com", protocol="http", global_ip="0.0.0.0")
    results = traceroute.run()
    for hop in results["hops"]:
        print(hop)
    assert results is None


def test_https():
    traceroute = Traceroute("www.google.com", protocol="https", global_ip="0.0.0.0")
    results = traceroute.run()
    for hop in results["hops"]:
        print(hop)
    assert results is None
