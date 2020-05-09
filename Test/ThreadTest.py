import threading
import time


class A:
    def __init__(self):
        self.running = True
        self.counter = 0

    def doSomething(self):
        while self.running:
            print(self.counter)
            self.counter += 1

            if self.counter >= 50:
                self.running = False


class B:
    def __init__(self):
        pass

    def doSomething(self, A):
        print("ALHAMDULILLAH ", A.counter)

