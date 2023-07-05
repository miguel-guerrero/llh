from collections import Counter

class DesignLib:
    def __init__(self):
        self._allmods = set()
        self.currMod = None
        self.cntr = Counter()

    def setCurrMod(self, mod):
        """invoked by generate to indicate the current module being generated
        before invoking its 'logic' method"""
        self.currMod = mod
        self.currMod.clearInstances()
        self._allmods.add(mod.modName)

    def currModAddIns(self, ins):
        """invoked by Module constructor so we know where new instances
        are rooted"""
        if self.currMod is not None:
            self.currMod.addInstance(ins)

    def autoInsName(self, modName: str) -> str:
        if self.currMod is None:
            cntr = self.cntr
        else:
            cntr = self.currMod.cntr
        insName = f"i{modName}_{cntr[modName]}"
        cntr[modName] += 1
        return insName


gLib = DesignLib()
