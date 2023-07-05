from ..primitive import Primitive
from ..wires import Wire
from ..simtime import SimTime
from ..types import LV
from typing import Optional


class Or(Primitive):
    def __init__(self, T=None, insName: Optional[str] = None):
        self.T = T or LV(1)
        assert isinstance(self.T, LV)
        super().__init__('Or', insName)
        self.delay = SimTime(1, 1)

    def interface(self):
        self.a = self.createInput('a', self.T)
        self.b = self.createInput('b', self.T)
        self.z = self.createOutput('z', self.T)

    def params(self):
        return [(self.T.width(), 'W')]

    def inputsChanged(self, chgdInput):
        a = self.a.getVal()
        b = self.b.getVal()
        assert isinstance(a, LV)
        assert isinstance(b, LV)
        out = a | b
        assert isinstance(out, LV)
        self.z.post(out, self.delay)


def f_or(a: Wire, b: Wire):
    assert isinstance(a, Wire)
    assert isinstance(b, Wire)
    assert isinstance(a.T, LV)
    assert isinstance(b.T, LV)
    assert a.width() == b.width()
    ins = Or()
    ins.a /= a
    ins.b /= b
    return ins.z
