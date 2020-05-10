from utils.dns_lookup import dns_lookup


def test_dns_lookup_valid():
    # test we can reverse lookup an actual address
    dns = dns_lookup("8.8.8.8")
    assert dns == "dns.google."


def test_dns_lookup_invalid():
    # test that invalid address doesnt come up
    assert dns_lookup("gjiojtgiojo") is None
