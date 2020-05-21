class StateCarrier:
    def __init__(self, states):
        self._state = None
        self.states = states

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in self.states:
            self._state = value
        else:
            raise ValueError("Value can only be one of the following ", self.states)

    # for command attribute in tkinter widgets
    def saveVal(self, value):
        self.state = value

