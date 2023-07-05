import llh as L


class SomeMod(L.Module):
    def __init__(self, insName):
        super().__init__('SomeMod', insName)

    def interface(self):
        self.x = self.createInput('port_x')
        self.y = self.createInput('port_y')
        self.z = self.createOutput('port_z')

    # out = ~(x & y)
    def logic(self):
        self.and_1 = L.And()
        self.and_1.a /= self.x
        self.and_1.b /= self.y
        w0 = self.and_1.z

        self.not_1 = L.Not()
        self.not_1.a /= w0
        self.z /= self.not_1.z


class Top(L.Module):
    def __init__(self, insName):
        super().__init__('Top', insName)

    def interface(self):
        self.a = self.createInput('port_a')
        self.z = self.createOutput('port_z')

    # out = a
    def logic(self):
        self.mod1 = SomeMod('SomeMod1')
        self.mod1.x /= self.a
        self.mod1.y /= self.a

        self.mod2 = SomeMod('SomeMod2')
        self.mod2.x /= self.mod1.z
        self.mod2.y /= self.mod1.z

        self.z /= self.mod2.z


def test1():
    L.gSim.resetSim()

    top1 = Top('top1')
    top1.elaborate()

    # drive some inputs
    top1.a.post(L.LV(W=1, val=1))

    print(L.gSim.currentSimTime())

    L.gSim.run(top1)

    print(L.gSim.currentSimTime())
    print('top1.z', top1.z)

    assert top1.mod2.z.getVal() == L.LV(W=1, val=1)

    print(top1.emitMod())


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    test1()
