from llh.types import LV


def test_and_lv():
    W = 8
    a = LV(W)
    b = LV(W)
    aVal = 0xF3
    bVal = 0xA1
    a.setVal(aVal)
    b.setVal(bVal)
    c = a & b
    assert c.V() == (aVal & bVal)
    assert c.X() == 0
    c = a | b
    assert c.V() == (aVal | bVal)
    assert c.X() == 0
    c = a ^ b
    assert c.V() == (aVal ^ bVal)
    assert c.X() == 0
    c = ~a
    assert c.V() == ~aVal & 0xFF
    assert c.X() == 0
