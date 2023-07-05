import llh as L
from lib import FullAdder


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


class Cntr2(L.Module):
    def __init__(self, insName):
        super().__init__('Cntr2', insName)

    def interface(self):
        self.clk = self.createInput('clk', L.ClockPosT())
        self.rstn = self.createInput('rstn', L.AsyncRstNegT())
        self.inc = self.createInput('inc')
        self.cnt0 = self.createOutput('cnt0')
        self.cnt1 = self.createOutput('cnt1')

    def logic(self):
        zero = L.Const(L.LV(W=1, val=0))
        adder2 = Adder2('adder2_0')
        dff0 = L.Next()
        dff1 = L.Next()

        dff0.clk /= self.clk
        dff0.rst /= self.rstn
        dff1.clk /= self.clk
        dff1.rst /= self.rstn

        adder2.cin /= zero.z   # L.f_not(self.inc)
        adder2.a0 /= self.inc
        adder2.a1 /= zero.z    # L.f_not(self.inc)
        adder2.b0 /= dff0.q
        adder2.b1 /= dff1.q

        dff0.d /= adder2.sum0
        dff1.d /= adder2.sum1

        self.cnt0 /= dff0.q
        self.cnt1 /= dff1.q


def test1():
    L.gSim.resetSim()

    V0 = L.LV(W=1, val=0)
    V1 = L.LV(W=1, val=1)

    dut = Cntr2('Cntr2_0')
    dut.elaborate()

    # set inc=1
    dut.inc.post(V1)

    # reset assert
    dut.rstn.post(V0)
    L.gSim.advance(dut, 50)
    # reset de-assert
    dut.rstn.post(V1)
    L.gSim.advance(dut, 50)

    # clock few cycles
    for n in range(10):
        dut.clk.post(V0)

        L.gSim.advance(dut, 50)
        assert L.gSim.pendingEventCount() == 0

        dut.clk.post(V1)

        L.gSim.advance(dut, 50)
        assert L.gSim.pendingEventCount() == 0

        print("------", L.gSim.currentSimTime().get(),
              'cnt:', dut.cnt1.getVal(), dut.cnt0.getVal())

        exp = n + 1
        assert dut.cnt0.getVal().V() == ((exp >> 0) & 1)
        assert dut.cnt1.getVal().V() == ((exp >> 1) & 1)

    print(dut.emitMod())


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    test1()
