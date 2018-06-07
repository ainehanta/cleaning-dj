import utime

class SpeedFilter:
    def __init__(self, ax, ay, az):
        self.lowpass  = [1.0, 1.0, 1.0]
        self.highpass = [1.0, 1.0, 1.0]
        self.filter   = [0.95, 0.95, 0.95]

        self.default  = [float(ax), float(ay), float(az)]
        self.accel    = [float(ax), float(ay), float(az)]
        self.speed    = [1.0, 1.0, 1.0]

        self.prev = utime.ticks_ms()

    def update(self, ax, ay, az):
        self.lowpass[0] = self.lowpass[0] * self.filter[0] + ax * (1.0 - self.filter[0])
        self.lowpass[1] = self.lowpass[1] * self.filter[1] + ay * (1.0 - self.filter[1])
        self.lowpass[2] = self.lowpass[2] * self.filter[2] + az * (1.0 - self.filter[2])

        # self.highpass[0] = ax - self.lowpass[0] - self.default[0]
        # self.highpass[1] = ay - self.lowpass[1] - self.default[1]
        # self.highpass[2] = az - self.lowpass[2] - self.default[2]
        self.highpass[0] = ax - self.lowpass[0]
        self.highpass[1] = ay - self.lowpass[1]
        self.highpass[2] = az - self.lowpass[2]

        now = utime.ticks_ms()
        # self.speed[0] = (self.highpass[0] + self.accel[0]) * (now - self.prev) / 2.0 + self.speed[0]
        # self.speed[1] = (self.highpass[1] + self.accel[1]) * (now - self.prev) / 2.0 + self.speed[1]
        # self.speed[2] = (self.highpass[2] + self.accel[2]) * (now - self.prev) / 2.0 + self.speed[2]
        # self.speed[0] = (self.highpass[0] + self.accel[0]) * (now - self.prev) / 2.0
        # self.speed[1] = (self.highpass[1] + self.accel[1]) * (now - self.prev) / 2.0
        # self.speed[2] = (self.highpass[2] + self.accel[2]) * (now - self.prev) / 2.0
        self.speed[0] = self.highpass[0] * (now - self.prev) / 1000.0
        self.speed[1] = self.highpass[1] * (now - self.prev) / 1000.0
        self.speed[2] = self.highpass[2] * (now - self.prev) / 1000.0

        self.accel[0] = self.highpass[0]
        self.accel[1] = self.highpass[1]
        self.accel[2] = self.highpass[2]

        self.prev = now

        return self.speed
