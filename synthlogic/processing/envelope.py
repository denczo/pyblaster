import time


class Env:

    def __init__(self, a=0, d=0, s=0, r=0, g=1):
        self.attack_phase = a
        self.decay_phase = d
        self.sustain_level = s
        self.release_phase = r

        self.gain = g
        self.reached_gain = 0

        self.p_start_time = 0
        self.r_start_time = 0
        self.pressed_time = 0
        self.released_time = 0

    def settings(self, a, d, s, r, g):
        self.attack_phase = a
        self.decay_phase = d
        self.sustain_level = s
        self.release_phase = r
        self.gain = g

    def apply(self, pressed):

        if pressed:
            self.pressed_time = time.time() - self.p_start_time
            self.r_start_time = time.time()
            self.released_time = 0

            # attack
            if self.pressed_time <= self.attack_phase:
                self.reached_gain = self.pressed_time / self.attack_phase * self.gain
            # decay TODO: what happens, when attack is 0?
            elif self.pressed_time <= self.attack_phase + self.decay_phase:
                self.reached_gain = self.gain - (self.pressed_time - self.attack_phase) / self.decay_phase * (
                        self.gain - self.sustain_level)
            # sustain
            elif self.pressed_time > self.attack_phase + self.decay_phase:
                self.reached_gain = self.sustain_level

        else:
            self.released_time = time.time() - self.r_start_time
            self.p_start_time = time.time()
            self.pressed_time = 0

            # release
            if self.reached_gain > 0.001 and self.release_phase > 0:
                self.reached_gain = (self.release_phase - self.released_time) / self.release_phase * self.reached_gain
            else:
                self.reached_gain = 0

        return self.reached_gain
