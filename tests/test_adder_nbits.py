import llh as L
from lib import FullAdder, Adder


def test_full_adder():
    L.gSim.resetSim()

    fa1 = FullAdder('fa1')
    fa1.elaborate()

    for a in range(2):
        fa1.a.post(L.LV(W=1, val=a))
        for b in range(2):
            fa1.b.post(L.LV(W=1, val=b))
            for cin in range(2):
                fa1.cin.post(L.LV(W=1, val=cin))
                L.gSim.advance(fa1, 10)
                assert L.gSim.pendingEventCount() == 0
                print("---", L.gSim.currentSimTime().get(),
                      'a:', fa1.a.getVal(),
                      'b:', fa1.b.getVal(),
                      'cin:', fa1.cin.getVal(),
                      'sum:', fa1.sum.getVal(),
                      'cout:', fa1.cout.getVal())
                total = a + b + cin
                assert fa1.sum.getVal().V() == (total & 1)
                assert fa1.cout.getVal().V() == ((total >> 1) & 1)

    print(fa1.emitMod())


def test_adder(W=4):
    L.gSim.resetSim()

    dut = Adder(W, f'Adder{W}')
    dut.elaborate()
    dut.cin.post(L.LV(W=1, val=0))
    mask = (1 << (W+1)) - 1

    for a in range(1 << W):
        dut.a.post(L.LV(W, val=a))
        for b in range(1 << W):
            dut.b.post(L.LV(W, val=b))
            L.gSim.advance(dut, 100)
            assert L.gSim.pendingEventCount() == 0
            print("---", L.gSim.currentSimTime().get(),
                  'a:', dut.a.getVal(),
                  'b:', dut.b.getVal(),
                  'sum:', dut.sum.getVal())
            total = a + b
            assert dut.sum.getVal().V() == (total & mask)

    dut.emitMod(path="adder_nbits")


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    test_adder()
