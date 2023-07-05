from .wires import In, Out, InArr
from .designlib import gLib
from .simulator import gSim
from .types import LV
import copy
from typing import Optional
from collections import Counter


class Module:
    def __init__(self, modName: str, insName: Optional[str] = None):
        self.modName = modName
        self.insName = insName or gLib.autoInsName(modName)
        self.inputPorts = []
        self.outputPorts = []
        self.parent = None
        self.cntr = Counter()
        gLib.currModAddIns(self)
        self._elaborated = False
        self.clearInstances()
        self.interface()

    def interface(self):
        assert False, \
            f"please override 'interface' method for Module {self.modName}"

    def params(self):
        return []

    def logic(self):
        assert False, \
            f"please override 'logic' method for Module {self.modName}"

    def inputsChanged(self, chgdInput):
        pass  # taken care by connectivity

    def emitMod(self, fmt="verilog", path=None):
        if fmt == "verilog":
            from . import verilog
            if path is None:
                # return as a string
                return verilog.emitModAsStr(self)
            else:
                # if a path is fiven all files are dumped there and
                # we return a file list
                return verilog.emitModSepFiles(self, path)
        else:
            raise Exception(f"unhandled output format '{fmt}' in emitMod")

    def emitInstance(self, fmt):
        if fmt == "verilog":
            from . import verilog
            s = verilog.emitInstance(self)
        else:
            raise Exception(f"unhandled output format '{fmt}' in emitInstance")
        return s

    def __repr__(self):
        return f"Module({self.hierInstanceName()})"

    def generate(self):
        gLib.setCurrMod(self)
        self.logic()
        for ins in self.instances:
            ins.generate()

    def hierInstanceName(self):
        if self.parent is None:
            return self.modName
        else:
            return self.parent.hierInstanceName() + "." + self.insName

    def createInput(self, name: str, T=None):
        T = T or LV(1)
        assert isinstance(T, LV)
        vcdHandle = gSim.vcdRegister(self.hierInstanceName(), name, T.width())
        port = In(name=name, T=copy.deepcopy(T), parent=self,
                  vcdHandle=vcdHandle)
        self.inputPorts.append(port)
        return port

    def createInputArr(self, name: str, T=None, N: int = 1):
        T = T or LV(1)
        assert isinstance(T, LV)
        arr = []
        for i in range(N):
            port = In(name=f"{name}_{i}", T=copy.deepcopy(T), parent=self)
            arr.append(port)
        arrPort = InArr(name, arr)
        self.inputPorts.append(arrPort)
        return arrPort

    def createOutput(self, name: str, T=None):
        T = T or LV(1)
        assert isinstance(T, LV)
        vcdHandle = gSim.vcdRegister(self.hierInstanceName(), name, T.width())
        port = Out(name=name, T=copy.deepcopy(T), parent=self,
                   vcdHandle=vcdHandle)
        self.outputPorts.append(port)
        return port

    def getPortByName(self, name: str):
        for io in self.inputPorts+self.outputPorts:
            if io.name == name:
                return io
        return None

    def clearInstances(self):
        self.instanceNamesSet = set()
        self.instances = []

    def addInstance(self, newInstance):
        if newInstance.insName in self.instanceNamesSet:
            raise RuntimeError(
                f"duplicated instance name found in {self}: {newInstance}")
        newInstance.parent = self
        self.instanceNamesSet.add(newInstance.insName)
        self.instances.append(newInstance)

    def elaborate(self):
        if not self._elaborated:
            self.generate()
            for ins in self.instances:
                ins.validate()
        self._elaborated = True

    def isElaborated(self):
        return self._elaborated

    def _validateInputs(self, inputs):
        for inp in inputs:
            if isinstance(inp, InArr):
                self._validateInputs(inp.getPorts())
            elif inp.driver is None:
                print('ERROR', self, 'has input port', inp, "undriven")
                raise Exception('Floating input Elaboration error')

    def _validateOutputs(self, outputs):
        for outp in outputs:
            if len(outp.loads) == 0:
                print('WARNING', self, 'has output port', outp, "floating")

    def validate(self):
        self._validateInputs(self.inputPorts)
        self._validateOutputs(self.outputPorts)
        return True
