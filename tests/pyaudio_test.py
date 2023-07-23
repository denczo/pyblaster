import pyaudio

pa = pyaudio.PyAudio()

print('\navailable devices:', pa.get_device_count())
for i in range(pa.get_device_count()):
    dev = pa.get_device_info_by_index(i)
    name = dev['name'].encode('utf-8')
    print(i, name, dev['maxInputChannels'], dev['maxOutputChannels'])

print('\ndefault input & output device:')
try:
    print(pa.get_default_input_device_info())
except:
  print("No default input device available")

try:
    print(pa.get_default_output_device_info())
except:
  print("No default output device available")

print(pa.get_default_host_api_info())
print(pa.get_device_count())