import llh as L
from lib import Counter


def test_counter(W=4):
    L.gSim.resetSim()

    mask = (1 << W) - 1

    V0 = L.LV(W=1, val=0)
    V1 = L.LV(W=1, val=1)

    dut = Counter(W)
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
    for n in range(2 + (1 << W)):
        dut.clk.post(V0)
        L.gSim.advance(dut, 50)
        assert L.gSim.pendingEventCount() == 0

        dut.clk.post(V1)
        L.gSim.advance(dut, 50)
        assert L.gSim.pendingEventCount() == 0

        print("------", L.gSim.currentSimTime().get(),
              'cnt:', dut.cnt.getVal())

        exp = n + 1
        assert dut.cnt.getVal().V() == (exp & mask)

    dut.emitMod(path="work/verilog")


if __name__ == "__main__":
    test_counter()
