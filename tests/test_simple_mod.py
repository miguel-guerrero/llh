import llh as L


class SomeMod(L.Module):
    def __init__(self, insName):
        super().__init__('SomeMod', insName)

    def interface(self):
        self.x = self.createInput(name='port_x')
        self.y = self.createInput(name='port_y')
        self.z = self.createOutput(name='port_z')

    def logic(self):
        self.and_1 = L.And()
        self.and_1.a /= self.x
        self.and_1.b /= self.y

        w0 = self.and_1.z

        self.not_1 = L.Not()
        self.not_1.a /= w0
        self.z /= self.not_1.z

        print('and.a.driver', self.and_1.a.driver)
        print('and.a.loads', self.and_1.a.loads)


def test1():
    L.gSim.resetSim()

    mod1 = SomeMod('mod1')
    mod1.elaborate()

    # drive some inputs
    mod1.x.post(L.LV(W=1, val=1))
    mod1.y.post(L.LV(W=1, val=0))

    L.gSim.run(mod1)

    print(L.gSim.currentSimTime())
    print('not_1.y', mod1.not_1.z)
    print('port_z', mod1.z.getVal())

    assert mod1.z.getVal() == L.LV(W=1, val=1)

    mod1.x.post(L.LV(W=1, val=1))
    mod1.y.post(L.LV(W=1, val=1))

    L.gSim.run(mod1)

    print(L.gSim.currentSimTime())
    print('not_1.y', mod1.not_1.z)
    print('port_z', mod1.z.getVal())

    assert mod1.z.getVal() == L.LV(W=1, val=0)


if __name__ == "__main__":
    # import pdb
    # pdb.set_trace()
    test1()
