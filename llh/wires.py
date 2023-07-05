from .simtime import SimTime
from .util import autoName
from .simulator import gSim
from .types import LV
import copy


# -----------------------------------------------------------------------------
# Wire: Base for In/Out
# -----------------------------------------------------------------------------
class Wire:
    def __init__(self, name=None, T=None, vcdHandle=None):
        self.name = name or "wire_" + autoName()
        self.T = T or LV(1)
        self.vcdHandle = vcdHandle
        self.driver = None
        self.loads = []
        self.delay = SimTime(0, 1)  # one delta
        self.neverDriven = True
        self.lastEvent = None

    def wireName(self):
        return self.name

    # schedules a posted write (deferred assignement)
    def post(self, newVal, delay=None):
        assert isinstance(newVal, LV)
        delay = delay or SimTime(0, 1)
        totalDelay = self.delay + delay
        t = gSim.currentSimTime() + totalDelay
        # NOTE: commented out condition is not guaraanteed to be OK,
        # but it is OK if all arcs of a module have the same delay
        # if (self.lastEvent is None or
        #     self.lastEvent[1] != newVal or
        #     t < self.lastEvent[0]):
        if self.lastEvent is None or self.lastEvent != (t, newVal):
            gSim.insertEvent(totalDelay, self, newVal)
            self.lastEvent = (t, copy.deepcopy(newVal))

    def width(self):
        return self.T.width()

    # reads current value
    def getVal(self):
        return self.T

    def __lt__(self, rhs):
        return False

    # assigns value and propagates events if value differs from previous
    def setVal(self, x):
        assert isinstance(x, LV)
        assert isinstance(self.T, LV)
        if x != self.T or self.neverDriven:
            print(gSim.currentSimTime(), "wire", self, "<-", x)
            if self.vcdHandle is not None:
                val = x.V()
                xval = x.X()
                gSim.vcdChange(self.vcdHandle, val if xval == 0 else "x")
            self.T.setVal(x)
            # propagate to loads
            for load in self.loads:
                load.setVal(x)
                ins = load.parent
                if ins is not None:  # a node within an instance
                    ins.inputsChanged(load)
                else:  # a top level port
                    load.inputsChanged(self)  # TODO
            self.neverDriven = False

    def addLoad(self, load):
        self.loads.append(load)
        assert load.driver is None, f"{load} is already driven"
        load.driver = self

    def __getitem__(self, slc):
        from .primitives.Selector import f_selector

        if isinstance(slc, Wire):
            return f_selector(a=self, idx=slc)
        raise Exception(f"subscripting operator requires an integer, found {slc}")

    def __repr__(self):
        return f"Wire(name={self.name}, val={self.T.val})"


class In(Wire):
    def __init__(self, parent=None, name=None, T=None, vcdHandle=None):
        super().__init__(name=name, T=T, vcdHandle=vcdHandle)
        self.parent = parent

    # port name
    def wireName(self):
        return self.name

    def __itruediv__(self, rhs):
        self.connect(rhs)
        return self

    def connect(self, w):
        if isinstance(w, Wire):  # a wire driving an in port
            w.loads.append(self)
            assert self.driver is None, (
                f"{self} already has a driver {self.driver} "
                + f"when connecting to {w}"
            )
            self.driver = w
        elif isinstance(w, In):  # an in port connecting to an in port
            w.addLoad(self)
        elif isinstance(w, Out):  # an out port connecting to an in port
            raise Exception(f"cannot connect out port {w} to in port {self}")
        else:
            raise Exception(f"cannot connect {w} to in port {self}")

    def inputsChanged(self, chgdInput):
        x = chgdInput.getVal()
        assert isinstance(x, LV)
        self.T.setVal(x)
        for load in self.loads:
            load.post(x)

    def __repr__(self):
        if self.parent is None:
            return f"In(name={self.name}, val={self.T})"
        else:
            return f"In {self.parent}.{self.name}(val={self.T})"


class Out(Wire):
    def __init__(self, parent=None, name=None, T=None, vcdHandle=None):
        super().__init__(name=name, T=T, vcdHandle=vcdHandle)
        self.parent = parent
        self.loads = []

    # name based on driving module and output pin port
    def wireName(self):
        return self.parent.insName + "_" + self.name

    def __itruediv__(self, rhs):
        self.connect(rhs)
        return self

    def connect(self, drivingSubPort):
        if isinstance(drivingSubPort, Out):
            drivingSubPort.addLoad(self)
        else:
            raise Exception(f"cannot connect {drivingSubPort} to out port {self}")

    def inputsChanged(self, chgdInput):
        x = chgdInput.getVal()
        self.T.setVal(x)
        for load in self.loads:
            load.post(x)

    def __repr__(self):
        if self.parent is None:
            return f"Out(name={self.name}, val={self.T})"
        else:
            return f"Out {self.parent}.{self.name}(val={self.T})"


class InArr:
    def __init__(self, name: str, ports: list):
        self.name = name
        self.ports = ports

    def getPorts(self):
        return self.ports

    def __repr__(self):
        return f"InArr(name={self.name}, ports={self.ports})"
