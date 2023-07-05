from .eventqueue import EventQueue
from .simtime import SimTime
from vcd import VCDWriter  # from pyvcd package


class Simulator:
    def __init__(self, verbose=False, vcdOn: bool = True, vcdName='dump.vcd'):
        self.verbose = verbose
        self._vcdOn = vcdOn
        self._vcdName = vcdName
        self._vcdOpened = False
        self.resetSim()

    def __del__(self):
        self._closeVcd()

    def resetSim(self):
        self.events = EventQueue()
        self.time = SimTime(0, 0)
        self._closeVcd()
        self._openVcd()

    def _openVcd(self):
        if self._vcdOn:
            if self.verbose:
                print("Opening VCD", self._vcdName)
            self.dumpFile = open(self._vcdName, "w")
            self.writer = VCDWriter(self.dumpFile, timescale='1 ps',
                                    date='today')
            self._vcdOpened = True

    def _closeVcd(self):
        if self._vcdOpened:
            if self.verbose:
                print("Closing VCD", self._vcdName)
            self.writer.close()
            self.dumpFile.close()
            self._vcdOpened = False

    def insertEvent(self, delay, wire, newVal):
        self.events.insert(self.time+delay, wire, newVal)

    def pendingEventCount(self):
        return self.events.size()

    def currentSimTime(self):
        return self.time

    def run(self, design, maxTime=None):
        assert design.isElaborated()
        # self.resetSim()
        self.resumeSim(maxTime)

    def advance(self, design, deltaTime):
        assert design.isElaborated()
        finalTime = self.time + SimTime(deltaTime)
        self.resumeSim(finalTime)
        if self.time < finalTime:
            self.time = finalTime

    def resumeSim(self, maxTime=None):
        while self.events.size() > 0:
            if self.verbose:
                print('--- EQ ----')
                print(self.events)
                print('-----------')
            time, wire, newVal = self.events.extract()
            if maxTime is None or time <= maxTime:
                self.time = time
                wire.setVal(newVal)
            else:
                break

    def vcdRegister(self, scope: str, wireName: str, width: int):
        if self._vcdOn:
            return self.writer.register_var(
                    scope, wireName, 'wire', size=width)
        return None

    def vcdChange(self, varHandle, val):
        if self._vcdOn:
            self.writer.change(varHandle, self.time.get(), val)


gSim = Simulator()
