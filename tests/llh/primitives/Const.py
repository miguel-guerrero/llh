from ..primitive import Primitive
from ..types import LV
from ..util import clog2
from typing import Optional


# Primitive
class Const(Primitive):
    def __init__(self, val, insName: Optional[str] = None):
        assert isinstance(val, LV)
        self.val = val
        super().__init__('Const', insName)
        self.z.post(val)

    def interface(self):
        self.z = self.createOutput('z', self.val)

    def params(self):
        return [(self.val.width(), 'W'), (self.val.V(), "VAL")]

    def inputsChanged(self, chgdInput):
        assert False, \
            "Invalid call to inputsChanged for Const, Const has no inputs"


def f_const(n: int, W=None):
    assert isinstance(n, int)
    assert n >= 0
    if W is None:
        W = max(1, clog2(n+1))
    ins = Const(LV(W=W, val=n))
    return ins.z
