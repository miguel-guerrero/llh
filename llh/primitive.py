from .module import Module
from typing import Optional


class Primitive(Module):
    def __init__(self, modName: str, insName: Optional[str] = None):
        super().__init__(modName, insName)

    def interface(self):
        assert False, "please override 'interface' method for Primitive type"

    def logic(self):
        pass  # has built-in behavior and logic

    def inputsChanged(self, chgdInput):
        assert False, "please override 'inputsChanged' mthod for Primitive type"

    def emitMod(self):
        pass  # is a primitive

    def __repr__(self):
        return f"{self.modName}::{self.insName}"
