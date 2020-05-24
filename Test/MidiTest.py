# import time
# import rtmidi
#
# midiout = rtmidi.MidiOut()
# midi_in = rtmidi.MidiIn()
#
# ports_in = midi_in.get_ports()
# available_ports = midiout.get_ports()
#
# print(available_ports, ports_in)
#
# if available_ports:
#     midiout.open_port(0)
# else:
#     midiout.open_virtual_port("My virtual output")
#
# with midiout:
#     # channel 1, middle C, velocity 112
#     note_on = [0x90, 60, 112]
#     note_off = [0x80, 60, 0]
#     midiout.send_message(note_on)
#     time.sleep(0.5)
#     midiout.send_message(note_off)
#     time.sleep(0.1)
#
# del midiout

#!/usr/bin/env python
#
# midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

# from __future__ import print_function
#
# import logging
# import sys
# import time
#
# import rtmidi
# from rtmidi.midiutil import open_midiinput
#
# midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
# if available_ports:
#     midiout.open_port(0)
# else:
#     midiout.open_virtual_port("My virtual output")
#
# log = logging.getLogger('midiin_poll')
# logging.basicConfig(level=logging.DEBUG)
#
# # Prompts user for MIDI input port, unless a valid port number or name
# # is given as the first argument on the command line.
# # API backend defaults to ALSA on Linux.
# port = sys.argv[1] if len(sys.argv) > 1 else None
#
# try:
#     midiin, port_name = open_midiinput(port)
# except (EOFError, KeyboardInterrupt):
#     sys.exit()
#
# print("Entering main loop. Press Control-C to exit.")
# try:
#     #timer = time.time()
#     while True:
#         msg = midiin.get_message()
#
#         if msg:
#             message, deltatime = msg
#             #timer += deltatime
#             midiout.send_message(message)
#             #print("[%s] @%0.6f %r" % (port_name, timer, message))
#
#         time.sleep(0.00001)
# except KeyboardInterrupt:
#     print('')
# finally:
#     print("Exit.")
#     midiin.close_port()
#     del midiin



#!/usr/bin/env python
#
# midiin_callback.py
#
from __future__ import print_function

import rtmidi

"""Show how to receive MIDI input by setting a callback function."""

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput


#midiout = rtmidi.MidiOut()
# available_ports = midiout.get_ports()
# if available_ports:
#     midiout.open_port(0)
# else:
#     midiout.open_virtual_port("My virtual output")

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()
        self.midiout = rtmidi.MidiOut()
        self.available_ports = self.midiout.get_ports()
        if self.available_ports:
            self.midiout.open_port(0)
        else:
            self.midiout.open_virtual_port("My virtual output")


    def __call__(self, event, data=None):
        message, deltatime = event
        #self._wallclock += deltatime
        self.midiout.send_message(message)
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))


# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
