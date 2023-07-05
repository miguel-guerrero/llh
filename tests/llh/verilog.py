from .module import Module
from .primitive import Primitive
from .wires import InArr


def emitModSepFiles(
        mod: Module,
        path: str,
        prefix: str = "${PREFIX}/",
        fileListName: str = "filelist.f") -> list:
    done = set()
    fileList = []
    _emitModSepFiles(mod, path, prefix, fileListName, done, fileList)
    return fileList


def _emitModSepFiles(
        mod: Module,
        path: str,
        prefix: str,
        fileListName: str,
        done: set,
        fileList: list):

    # dump child instance modules prior to module itself
    for m in mod.instances:
        if m.modName not in done:
            _emitModSepFiles(m, path, prefix, fileListName, done, fileList)

    # emit this one
    if mod not in done:
        if not isinstance(mod, Primitive):
            filePath = path+"/"+mod.modName+".v"
            with open(filePath, "w") as f:
                f.write(_emitOneModAsStr(mod))
            fileList.append(filePath)
            done.add(mod.modName)

    # emit file list
    with open(path + "/" + fileListName, "w") as f:
        f.write("\n".join(prefix + fn for fn in fileList) + "\n")


def emitModAsStr(mod: Module) -> list:
    done = set()
    return _emitModAsStr(mod, done)


def _emitModAsStr(mod: Module, done: set) -> str:
    s = ""
    # emit lower level modules (out of instances)
    for m in mod.instances:
        if m.modName not in done:
            s += _emitModAsStr(m, done)
    # emit this one
    if mod not in done:
        if not isinstance(mod, Primitive):
            s = _emitOneModAsStr(mod)
            done.add(mod.modName)
    return s


def _emitOneModAsStr(mod: Module) -> str:
    s = _emitHeader(mod)
    s += _emitBody(mod)
    s += _emitFooter(mod)
    return s


def _emit(ind: int, txt: str) -> str:
    s = "    " * ind
    s += txt
    return s


def _emitln(ind: int, txt: str) -> str:
    return _emit(ind, txt) + "\n"


def _emitHeader(mod: Module) -> str:
    s = "// " + ("-" * 70) + "\n"
    s += f"// Module {mod.modName}" + "\n"
    s += "// " + ("-" * 70) + "\n"
    s += _emitln(0, f"module {mod.modName}(")

    ports = []
    for port in mod.inputPorts + mod.outputPorts:
        ports.append(_emit(1, f"{port.name}"))
    s += _emitln(0, ",\n".join(ports))

    s += _emitln(0, f");")

    for port in mod.inputPorts:
        msb = port.width() - 1
        s += _emitln(0, f"input [{msb}:0] {port.name};")
    for port in mod.outputPorts:
        msb = port.width() - 1
        s += _emitln(0, f"output [{msb}:0] {port.name};")
    s += _emitln(0, "")
    return s


def _emitFooter(mod: Module) -> str:
    return _emitln(0, "endmodule\n")


def _emitBody(mod: Module) -> str:
    instancesStr = ""
    declares = []
    for ins in mod.instances:
        insStr, wires = emitInstance(ins, mod)
        declares += wires
        instancesStr += insStr

    declStr = ""
    for net in sorted(set(declares)):  # to set to remove duplicates
        netName, w = net
        declStr += _emitln(0, f"wire [{w-1}:0]  {netName};")

    s = declStr + "\n" + instancesStr
    return s


def getOutPortNetName(port, mod):
    # if the port is unloaded, don't connect it to any net
    if len(port.loads) == 0:
        netName = ""
    else:
        # assume by default the net name is provided by insta+portName
        netName = port.wireName()
        # but if one of the loads is a primary output, that one provides
        # the name
        for load in port.loads:
            if load in mod.outputPorts:
                netName = load.name
    return netName


def getInPortNetName(port, mod):
    return getOutPortNetName(port.driver, mod)


def emitInstance(ins, mod: Module) -> str:
    nets = []
    ports = []

    # handle inputs and arrayed inputs (lists)
    for port in ins.inputPorts:
        if isinstance(port, InArr):
            wLst = []
            for w in port.getPorts():
                wName = w.driver.wireName()
                wLst.append(wName)
                if w.driver not in mod.inputPorts:
                    nets.append((f"{wName}", w.driver.width()))
            netName = "{" + (", ".join(reversed(wLst))) + "}"
        else:
            netName = getInPortNetName(port, mod)
            if (port.driver not in mod.inputPorts
                    and port.driver not in mod.outputPorts):
                nets.append((f"{netName}", port.driver.width()))
        ports.append(_emit(1, f".{port.name}({netName})"))

    for port in ins.outputPorts:
        netName = getOutPortNetName(port, mod)
        ports.append(_emit(1, f".{port.name}({netName})"))

    # create pass down parameter string
    paramStr = ""
    paramLst = [f".{p[1]}({p[0]})" for p in ins.params()]
    if len(paramLst) > 0:
        paramStr = f" #({', '.join(paramLst)})"

    s = f"{ins.modName}{paramStr} {ins.insName} (\n"
    s += ",\n".join(ports)
    s += _emitln(0, "\n);\n")
    return s, nets
