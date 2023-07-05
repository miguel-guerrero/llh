class SimTime:
    def __init__(self, t, dt=0):
        self.t = t
        self.dt = dt

    def __lt__(self, rhs):
        return (self.t == rhs.t and self.dt < rhs.dt) or (self.t < rhs.t)

    def __eq__(self, rhs):
        return (self.t == rhs.t) and (self.dt == rhs.dt)

    def __le__(self, rhs):
        return self.__lt__(rhs) or self.__eq__(rhs)

    def __add__(self, rhs):
        if isinstance(rhs, int):
            return SimTime(self.t + rhs, self.dt)
        elif isinstance(rhs, SimTime):
            return SimTime(self.t + rhs.t, self.dt + rhs.dt)
        else:
            raise Exception(f"I can't add SimTime and {rhs}")

    def get(self):
        return self.t

    def __repr__(self):
        return f"#{self.t}(dt={self.dt})"
        return f"SimTime({self.t}, {self.dt})"
