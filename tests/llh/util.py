import math


def clog2(x):
    if x <= 1:
        return 0
    return math.ceil(math.log2(x))


def makeCounter():
    cnt = 0

    def innerCounter():
        nonlocal cnt
        cnt += 1
        return cnt

    return innerCounter


def makeAutoName():
    cnt = 0

    def autoName():
        nonlocal cnt
        cnt += 1
        return f"auto{cnt}"

    return autoName


autoName = makeAutoName()
