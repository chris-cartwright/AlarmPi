from threading import Thread, Event


class RepeatingTimer(Thread):
    def __init__(self, freq, f):
        Thread.__init__(self)
        self.signal = Event()
        self.freq = freq
        self.func = f

    def run(self):
        while not self.signal.wait(self.freq):
            self.func()