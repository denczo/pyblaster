import time


class Env:

    def __init__(self, a=0, d=0, s=0, r=0, g=1):
        self.attack_phase = a
        self.decay_phase = d
        self.sustain_level = s
        self.release_phase = r

        self.gain = g
        self.reached_level = 0
        # current level, when key is pressed
        self.asc_level = 0
        # current level, when key is released
        self.desc_level = 0

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
        #print(a,d,s,r)

    def apply(self, pressed):

        if pressed:
            self.pressed_time = time.time() - self.p_start_time
            self.r_start_time = time.time()
            self.released_time = 0

            # attack
            if self.pressed_time <= self.attack_phase:
                self.asc_level = self.pressed_time / self.attack_phase * self.gain
            # decay
            elif self.pressed_time <= self.attack_phase + self.decay_phase:
                self.asc_level = self.gain - (self.pressed_time - self.attack_phase) / self.decay_phase * (
                        self.gain - (self.gain * self.sustain_level))
            # sustain
            elif self.pressed_time > self.attack_phase + self.decay_phase:
                self.asc_level = self.gain * self.sustain_level

            self.reached_level = self.asc_level
            self.desc_level = self.asc_level

        else:
            self.released_time = time.time() - self.r_start_time
            self.p_start_time = time.time()
            self.pressed_time = 0
            fraction = self.asc_level / self.gain

            # release
            if self.desc_level > 0.001 and self.release_phase > 0:
                self.desc_level = (self.release_phase * fraction - self.released_time) / (
                            self.release_phase * fraction) * self.asc_level
            else:
                self.desc_level = 0

            self.reached_level = self.desc_level

        return self.reached_level
