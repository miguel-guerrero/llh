import llh as L


class FullAdder(L.Module):
    def __init__(self, insName):
        super().__init__('FullAdder', insName)

    def interface(self):
        self.cin = self.createInput('cin')
        self.a = self.createInput('a')
        self.b = self.createInput('b')
        self.sum = self.createOutput('sum')
        self.cout = self.createOutput('cout')

    def logic(self):
        self.sum /= L.f_xor(L.f_xor(self.a, self.b), self.cin)
        self.cout /= L.f_or(L.f_or(
                        L.f_and(self.a, self.b),
                        L.f_and(self.a, self.cin)),
                        L.f_and(self.b, self.cin))


class Adder2(L.Module):
    def __init__(self, insName):
        super().__init__('Adder2', insName)

    def interface(self):
        self.cin = self.createInput('cin')
        self.a0 = self.createInput('a0')
        self.a1 = self.createInput('a1')
        self.b0 = self.createInput('b0')
        self.b1 = self.createInput('b1')
        self.sum0 = self.createOutput('sum0')
        self.sum1 = self.createOutput('sum1')
        self.cout = self.createOutput('cout')

    def logic(self):
        fa0 = FullAdder("fa0")
        fa1 = FullAdder("fa1")

        fa0.cin /= self.cin
        fa0.a /= self.a0
        fa0.b /= self.b0

        fa1.cin /= fa0.cout
        fa1.a /= self.a1
        fa1.b /= self.b1

        self.sum0 /= fa0.sum
        self.sum1 /= fa1.sum
        self.cout /= fa1.cout


def test1():
    L.gSim.resetSim()

    dut = Adder2('adder2_0')
    dut.elaborate()

    for a in range(4):
        dut.a0.post(L.LV(W=1, val=a % 2))
        dut.a1.post(L.LV(W=1, val=(a >> 1) % 2))
        for b in range(4):
            dut.b0.post(L.LV(W=1, val=b % 2))
            dut.b1.post(L.LV(W=1, val=(b >> 1) % 2))
            for cin in range(2):
                dut.cin.post(L.LV(W=1, val=cin))
                L.gSim.advance(dut, 10)
                assert L.gSim.pendingEventCount() == 0
                print("------", L.gSim.currentSimTime().get(),
                      'cin:', dut.cin.getVal(),
                      'a:', dut.a1.getVal(), dut.a0.getVal(),
                      'b:', dut.b1.getVal(), dut.b0.getVal(),
                      'cout:', dut.cout.getVal(),
                      'sum:', dut.sum1.getVal(), dut.sum0.getVal())
                total = a + b + cin
                assert dut.sum0.getVal().V() == (total & 1)
                assert dut.sum1.getVal().V() == ((total >> 1) & 1)
                assert dut.cout.getVal().V() == ((total >> 2) & 1)

    print(dut.emitMod())


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    test1()
