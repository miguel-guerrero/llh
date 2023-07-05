

class LV:
    def __init__(self, W: int = 1, val: int = 0, x: int = 0):
        assert isinstance(W, int)
        assert isinstance(val, int)
        assert isinstance(x, int)
        self.W = W
        self.val = val
        self.x = x

    def mask(self):
        return (1 << self.W) - 1

    def __and__(self, rhs):
        assert isinstance(rhs, LV)
        assert self.W == rhs.W
        val = self.val & rhs.val
        return LV(self.W, val, val & (self.x | rhs.x))

    def __or__(self, rhs):
        assert isinstance(rhs, LV)
        assert self.W == rhs.W
        val = self.val | rhs.val
        return LV(self.W, val, ~val & (self.x | rhs.x))

    def __xor__(self, rhs):
        assert isinstance(rhs, LV)
        assert self.W == rhs.W
        val = self.val ^ rhs.val
        return LV(self.W, val, (self.x | rhs.x))

    def __invert__(self):
        val = (~self.val) & self.mask()
        return LV(self.W, val, self.x)

    def __eq__(self, rhs):
        assert isinstance(rhs, LV)
        return (self.W == rhs.W and
                self.val == rhs.val and
                self.x == rhs.x)

    def isVal(self, val: int):
        assert isinstance(val, int)
        return (self.val == val) and (self.x == 0)

    def __ne__(self, rhs):  # TODO is this needed?
        assert isinstance(rhs, LV)
        return not self.__eq__(rhs)

    def setVal(self, val, x=0):
        if isinstance(val, int):
            assert val & ~self.mask() == 0, \
                   "setVal({val}) assigns too many bits for {self} size"
            self.val = val
            self.x = x
        else:
            assert isinstance(val, LV)
            assert self.width() == val.width()
            self.val = val.val
            self.x = val.x

    def V(self):
        return self.val  # & self.mask()

    def X(self):
        return self.x  # self.mask()

    def defaultVal(self):  # used as default reset on DFF
        return 0

    def width(self):
        return self.W

    def getBit(self, n: int):
        assert isinstance(n, int)
        return LV(W=1,
                  val=1 & (self.val >> n),
                  x=1 & (self.x >> n))

    def __repr__(self):
        return f"{self.W}'d{self.val}"
        return f"{self.val}"
        return f"LV(W={self.W}, val={self.val}, x={self.x})"


class ClockPosT(LV):
    def __init__(self):
        super().__init__()

    def name(self):
        return "clk"

    def active(self, val: int):
        return val == 1


class AsyncRstNegT(LV):
    def __init__(self):
        super().__init__()

    def name(self):
        return "rstn"

    def active(self, val: int):
        return val == 0

    def asyn(self):
        return True
