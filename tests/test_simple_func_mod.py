import llh as L


class SomeMod(L.Module):
    def __init__(self, insName):
        super().__init__('SomeMod', insName)

    def interface(self):
        self.x = self.createInput(name='port_x')
        self.y = self.createInput(name='port_y')
        self.z = self.createOutput(name='port_z')

    def logic(self):
        w0 = L.f_and(self.x, self.y)
        self.z /= L.f_not(w0)


def test1():
    L.gSim.resetSim()

    mod1 = SomeMod('mod1')
    mod1.elaborate()

    # drive some inputs
    mod1.x.post(L.LV(W=1, val=1))
    mod1.y.post(L.LV(W=1, val=0))

    L.gSim.run(mod1)

    print(L.gSim.currentSimTime())
    print('port_z', mod1.z.getVal())

    assert mod1.z.getVal() == L.LV(W=1, val=1)


if __name__ == "__main__":
    import pdb
    pdb.set_trace()
    test1()
