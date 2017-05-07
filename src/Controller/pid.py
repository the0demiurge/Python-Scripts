class PID(object):

    def __init__(self, Kp=1, Ki=.1, Kd=0, T_sample=1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.T_sample = T_sample

        self.u_prev = 0
        self.e_prev = 0
        self.e_prev_prev = 0

    def step(self, e):
        u = (self.u_prev + self.Kp * (e - self.e_prev) + self.Ki * self.T_sample * e + self.Kd * (e - 2 * self.e_prev + self.e_prev_prev))
        self.u_prev, self.e_prev, self.e_prev_prev = u, e, self.e_prev
        return u
