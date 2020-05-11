from classes.hop import Hop


def test_calculate_rtt():
    hop = Hop(1, sent_time=1582838380.3099, reply_time=1582838380.3109272)
    hop.calculate_rtt()
    assert hop.rtt == 1.027


def test_calculate_rtt_no_sent_time():
    hop = Hop(1, reply_time=1582838380.3109272)
    hop.calculate_rtt()
    assert hop.rtt == -1


def test_calculate_rtt_no_reply_time():
    hop = Hop(1, sent_time=1582838380.3109272)
    hop.calculate_rtt()
    assert hop.rtt == -1
