# import pyaudio

# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#     if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#         print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

# import pyaudio

################################################################################################

# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
# for i in range (0,numdevices):
#         if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
#                 print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))

#         if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
#                 print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))

# devinfo = p.get_device_info_by_index(1)
# # print("Selected device is ",devinfo.get('name'))
# print("Selected device is ",devinfo)
# if p.is_format_supported(44100.0,  # Sample rate
#                          input_device=devinfo["index"],
#                          input_channels=devinfo['maxInputChannels'],
#                          input_format=pyaudio.paInt16):

#   p.terminate()

################################################################################################

import pyaudio
import wave
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

DEVICE_NAME = "scala_mic_i2c_sw_vol"
CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "voice.wav"

input_device_index = -1

for i in range(0, numdevices):
  if(p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')):
    if (p.get_device_info_by_host_api_device_index(0, i).get('name') == DEVICE_NAME):
      input_device_index = i    

print(DEVICE_NAME, "found on device id:", input_device_index)

if (input_device_index < 0):
  print("Device not found, make sure it's connected")
  exit(1)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index=input_device_index,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("Now sleeping...")
import time
time.sleep(5)
print("Now playing...")

from subprocess import Popen, PIPE
#subprocess.call(["play", "-v", self.volume, file])
# subprocess.call(["aplay", WAVE_OUTPUT_FILENAME])
#amazon polly returns mpg, in test we have wav
process = Popen(["aplay", WAVE_OUTPUT_FILENAME], stdout=PIPE, stderr=PIPE)
# process = Popen(["mpg123", WAVE_OUTPUT_FILENAME], stdout=PIPE, stderr=PIPE)
process.wait()