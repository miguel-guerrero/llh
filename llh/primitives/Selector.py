from ..primitive import Primitive
from ..wires import Wire
from ..simtime import SimTime
from ..types import LV
from ..util import clog2
from typing import Optional


# Primitive
class Selector(Primitive):
    def __init__(self, T=None, insName: Optional[str] = None):
        self.T = T
        assert isinstance(self.T, LV)
        self.selW = clog2(self.T.width())
        super().__init__("Selector", insName)
        self.delay = SimTime(1, 1)

    def interface(self):
        self.a = self.createInput("a", self.T)
        self.idx = self.createInput("idx", LV(self.selW))
        self.z = self.createOutput("z")

    def params(self):
        return [(self.T.width(), "W")]

    def inputsChanged(self, chgdInput):
        a = self.a.getVal()
        idx = self.idx.getVal()
        assert isinstance(a, LV)
        assert isinstance(idx, LV)
        out = a.getBit(idx.V())
        assert isinstance(out, LV)
        self.z.post(out, self.delay)


def f_selector(a, idx):
    assert isinstance(a, Wire)
    assert isinstance(idx, Wire)
    assert isinstance(a.T, LV)
    assert isinstance(idx.T, LV)
    ins = Selector(LV(a.width()))
    ins.a /= a
    ins.idx /= idx
    return ins.z
