from ..primitive import Primitive
# from ..wires import Wire
from ..simtime import SimTime
from ..types import LV, ClockPosT, AsyncRstNegT
from typing import Optional


class Next(Primitive):
    def __init__(self, T=None, initVal=None,
                 clkT=None, rstT=None, insName: Optional[str] = None):
        self.T = T or LV(1)
        assert isinstance(self.T, LV)
        self.initVal = initVal or self.T.defaultVal()
        self.clkT = clkT or ClockPosT()
        self.rstT = rstT or AsyncRstNegT()
        modName = 'Next'
        modName += "AsyncRst" if self.rstT.asyn() else "SyncRst"
        modName += "n" if self.rstT.active(0) else ""
        modName += "NegClk" if self.clkT.active(0) else ""
        super().__init__(modName, insName)
        self.delay = SimTime(1, 1)

    def interface(self):
        self.clk = self.createInput(self.clkT.name(), self.clkT)
        self.rst = self.createInput(self.rstT.name(), self.rstT)
        self.d = self.createInput('d', self.T)
        self.q = self.createOutput('q', self.T)

    def params(self):
        return [(self.T.width(), 'W')]

    # TODO how to avoid getting called when only d changes
    def inputsChanged(self, chgdInput):
        if chgdInput is self.rst:
            if self.rst.T.active(self.rst.getVal().V()):
                out = self.initVal
                self.q.post(LV(W=self.T.W, val=out), self.delay)
        elif chgdInput is self.clk:
            if self.clk.T.active(self.clk.getVal().V()):
                out = self.d.getVal()
                self.q.post(out, self.delay)


