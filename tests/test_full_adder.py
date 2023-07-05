import llh as L
from lib import HalfAdder, FullAdder


def test1():
    L.gSim.resetSim()
    ha1 = HalfAdder('ha1')
    ha1.elaborate()
    print('ha1.a', ha1.a)
    print('ha1.b', ha1.b)
    print('ha1.instances[0]', ha1.instances[0])
    print('ha1.instances[0].a', ha1.instances[0].a)
    print('ha1.instances[0].b', ha1.instances[0].b)
    for a in range(2):
        ha1.a.post(L.LV(W=1, val=a))
        for b in range(2):
            ha1.b.post(L.LV(W=1, val=b))
            L.gSim.advance(ha1, 10)
            assert L.gSim.pendingEventCount() == 0
            print("---", L.gSim.currentSimTime().get(),
                  'a:', ha1.a.getVal(),
                  'b:', ha1.b.getVal(),
                  'sum:', ha1.sum.getVal(),
                  'cout:', ha1.cout.getVal())
            total = a + b
            assert ha1.sum.getVal().V() == (total & 1)
            assert ha1.cout.getVal().V() == ((total >> 1) & 1)


def test2():
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


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    # test1()
    test2()
    test2()
