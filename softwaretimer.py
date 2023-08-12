class softwaretimer:
    MAX_SOFTWARE_TIMER = 10
    TICK = 100

    def __init__(self):
        self.counter = []
        self.flag = []
        for i in range(0, self.MAX_SOFTWARE_TIMER):
            self.counter.append(0)
            self.flag.append(0)
        return

    def set_timer(self, index, value):
        self.counter[index] = value/self.TICK
        self.flag[index] = 0
        return

    def is_timer_expired(self,index):
        return self.flag[index]

    def Timer_Run(self):
        for i in range(0, self.MAX_SOFTWARE_TIMER):
            if(self.counter[i] > 0):
                self.counter[i] -=1
                if self.counter[i] <=0:
                    self.flag[i] = 1
        return