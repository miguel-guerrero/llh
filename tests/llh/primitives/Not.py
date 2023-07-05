from ..primitive import Primitive
from ..wires import Wire
from ..simtime import SimTime
from ..types import LV
from typing import Optional


# Primitive
class Not(Primitive):
    def __init__(self, T=None, insName: Optional[str] = None):
        self.T = T or LV(1)
        assert isinstance(self.T, LV)
        super().__init__('Not', insName)
        self.delay = SimTime(1, 1)

    def interface(self):
        self.a = self.createInput('a', self.T)
        self.z = self.createOutput('z', self.T)

    def params(self):
        return [(self.T.width(), 'W')]

    def inputsChanged(self, chgdInput):
        a = self.a.getVal()
        assert isinstance(a, LV)
        out = ~a
        assert isinstance(out, LV)
        self.z.post(out, self.delay)


def f_not(a):
    assert isinstance(a, Wire)
    assert isinstance(a.T, LV)
    ins = Not()
    ins.a /= a
    return ins.z
