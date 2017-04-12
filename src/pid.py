class PID(object):
    def __init__(self, p=1, i=.1, d=0):
        self.p=p
        self.i=i
        self.d=d
        self.integ=0
    def step(self, observe):
        self.integ += self.i * observe
        return -(self.p*observe + self.integ)
