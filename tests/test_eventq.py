from llh.eventqueue import EventQueue
from llh.simtime import SimTime
from llh.wires import Wire as WireMain


class WireLocal:
    def __init__(self, name):
        self.name = name

    def __lt__(self, rhs):
        return False

    def __repr__(self):
        return f"Wire({self.name})"


Wire = WireMain
# Wire = WireLocal


def test_monotonic():
    w0 = Wire("wire0")
    w1 = Wire("wire1")
    eq = EventQueue()

    eq.insert(SimTime(9, 0), w0, 0)
    for i in range(100):
        eq.insert(SimTime(10+i, 0), w0, 10+i)
    eq.insert(SimTime(200, 0), w0, 200)
    for i in range(100):
        eq.insert(SimTime(10+i, 0), w1, 10+i)

    prevTime = SimTime(0, 0)
    prevVal = 0
    while eq.size() > 0:
        t, w, val = eq.extract()
        assert prevTime <= t
        assert prevVal <= val
        prevTime = t
        prevVal = val
