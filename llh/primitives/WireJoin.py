from ..primitive import Primitive
from ..simtime import SimTime
from ..types import LV
from typing import Optional


# Primitive
class WireJoin(Primitive):
    def __init__(self, W, insName: Optional[str] = None):
        assert isinstance(W, int)
        self.T = LV(W)
        self.W = W
        super().__init__("WireJoin", insName)
        self.delay = SimTime(1, 1)

    def interface(self):
        self.a = self.createInputArr("a", N=self.W)
        self.z = self.createOutput("z", self.T)

    def params(self):
        return [(self.W, "W")]

    def inputsChanged(self, chgdInput):
        ports = self.a.getPorts()
        outVal = 0
        outX = 0
        for i in range(self.W):
            k = self.W - 1 - i
            lvVal = ports[k].getVal()
            outVal = lvVal.V() | (outVal << 1)
            outX = lvVal.X() | (outX << 1)
        out = LV(self.W, outVal, outX)
        self.z.post(out, self.delay)


def f_wirejoin(a):
    assert isinstance(a, list)
    ins = WireJoin(len(a))
    ports = ins.inputPorts[0].getPorts()
    for i in range(len(a)):
        ports[i] /= a[i]
    return ins.z
