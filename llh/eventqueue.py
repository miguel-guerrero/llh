from .simtime import SimTime
import heapq
from .util import makeCounter


# used to ensure ties in time push new events to end of the existing ones
serialNum = makeCounter()


def heapsort(iterableIn):
    iterable = list(iterableIn)
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for _ in range(len(h))]


def heapAsSortedList(hIn):
    h = list(hIn)
    ln = len(hIn)
    srt = [heapq.heappop(h) for _ in range(ln)]
    if False:  # check is in order?
        prevT = None
        prevSerial = None
        for t, serial, ev in srt:
            if prevT is not None:
                assert prevT <= t and prevSerial < serial
            prevT = t
            prevSerial = serial
    return srt


class Event:
    def __init__(self, wire, newVal):
        self.wire = wire
        self.newVal = newVal

    def __repr__(self):
        return f"Event({self.wire}, {self.newVal})"


class EventQueue:
    def __init__(self, verbose=False):
        self.heap = []
        self.verbose = verbose

    def size(self) -> int:
        return len(self.heap)

    def insert(self, time: SimTime, wire, newVal):
        entry = (time, serialNum(), Event(wire, newVal))
        if self.verbose:
            print("scheduling write to", wire, "newVal", newVal, "for", time)
        heapq.heappush(self.heap, entry)

    def extract(self):
        t, _, ev = heapq.heappop(self.heap)
        return t, ev.wire, ev.newVal

    def __repr__(self):
        lst = [
            f"ev({t}, {serial}, {ev.wire}, {ev.newVal})"
            for t, serial, ev in heapAsSortedList(self.heap)
        ]
        return "\n".join(lst)
