#!/usr/bin/python3

import scipy.io.wavfile as wav
import time
import sys
import numpy
from matplotlib import pyplot 

# Read wav file
sample_rate, wav_data = wav.read('dixon.wav')
print('sample rate: {}'.format(sample_rate))

N = wav_data.shape[0]
print('length in samples (N): {}'.format(N))

# Determine length of wave in seconds
wav_time_seconds = N / sample_rate
print('time (s): {}'.format(wav_time_seconds))

# Extract 8 seconds from the middle of the wav
middle_sample_i = int(N / 2)
print('Middle sample: {}'.format(middle_sample_i))

# 8 seconds in number of samples at sample_rate samples per secnod
j_8_seconds = sample_rate * 8
print('8 seconds of samples: {}'.format(j_8_seconds))

sample= wav_data[middle_sample_i:middle_sample_i + j_8_seconds]
print(sample.shape)

# Plot and play each sample
# import ossaudiodev
# snddev = ossaudiodev.open('/dev/audio', 'w')
# snddev.setfmt(ossaudiodev.AFMT_S16_LE)
# snddev.channels(1)
# snddev.speed(sample_rate)
# snddev.close()

print('Left channel')
left_channel = sample[:, 0]

print('Right channel')
right_channel = sample[:, 1]

# Normalize each channel
left_max = numpy.absolute(left_channel).max()
print('Left max: {}'.format(left_max))

normalized_left_sample = left_channel * 1. / left_max

right_max = numpy.absolute(right_channel).max()
print('Right max: {}'.format(right_max))

normalized_right_sample = right_channel * 1. / right_max

pyplot.subplot(221)
pyplot.title('Left Channel Un-normalized')
pyplot.plot(left_channel)

pyplot.subplot(222)
pyplot.title('Right Channel Un-normalized')
pyplot.plot(right_channel)

pyplot.subplot(223)
pyplot.title('Left Channel Normalized')
pyplot.plot(normalized_left_sample)

pyplot.subplot(224)
pyplot.title('Right Channel Normalized')
pyplot.plot(normalized_right_sample)

pyplot.show()

