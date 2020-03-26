#!/usr/bin/env python

import argparse
import glob
import math

import numpy as np
import soundfile
from PIL import Image
from scipy import signal

def encode(image, field):
	image = image.resize((round(width * oversample), lines))
	image = image.convert('YCbCr')

	data = np.asarray(image)

	left = np.zeros(0)
	right = np.zeros(0)

	if field == 0:
		left = np.append(left, pulse * -1)
		right = np.append(right, pulse)

		left = np.append(left, pulse)
		right = np.append(right, pulse * -1)
	else:
		left = np.append(left, pulse)
		right = np.append(right, pulse * -1)

		left = np.append(left, pulse * -1)
		right = np.append(right, pulse)

	left = np.append(left, quiet)
	right = np.append(right, quiet)

	for line in range(0, data.shape[0] // 2):

		if line != 0:
			if line % 2 == 0:
				left = np.append(left, pulse)
				right = np.append(right, pulse)

				left = np.append(left, pulse * -1)
				right = np.append(right, pulse * -1)
			else:
				left = np.append(left, pulse * -1)
				right = np.append(right, pulse * -1)

				left = np.append(left, pulse)
				right = np.append(right, pulse)

			left = np.append(left, quiet)
			right = np.append(right, quiet)

		left = np.append(left, data[line * 2 + field, :, 0] / 255.0 - 0.5)

		if line % 2 == 0:

			right = np.append(
				right, data[line * 2 + field, :, 1] / 255.0 - 0.5)
		else:
			right = np.append(
				right, data[line * 2 + field, :, 2] / 255.0 - 0.5)

		left = np.append(left, quiet)
		right = np.append(right, quiet)

	left = signal.resample_poly(left, 1, oversample)
	right = signal.resample_poly(right, 1, oversample)

	return np.stack([left, right], 1)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--input', required=True, action='append', dest='inputs', help='input file pattern(s)', type=str )
	parser.add_argument('outfile', type=argparse.FileType( 'wb' ) )

	parser.add_argument('-r', '--rate', dest='rate', action='store', help='sample rate', default=96000, type=int)
	parser.add_argument('-f', '--fps', dest='fps', action='store', help='frames per second', default=3, type=float)
	parser.add_argument('-l', '--lines', dest='lines', action='store', help='lines of resolution', default=150, type=int)
	parser.add_argument('-p', '--pulselength', dest='pulselength', action='store', help='length of sync pulses in ms', default=0.2, type=float)
	parser.add_argument('-o', '--oversample', dest='oversample', action='store', help='oversampling amount', default=10, type=int)

	args = parser.parse_args()

	sample_rate = args.rate
	oversample = args.oversample

	pulse_length = args.pulselength/1000

	fps = args.fps
	lines = args.lines
	h_time = (1/fps/lines)*2
	width = h_time-(pulse_length*4)

	if width <= 0:
		print("Not time for image data, try reducing frame rate, lines, or pulse length.")
		exit(1)

	print("hFreq: {},".format(1.0/h_time))
	print("vFreq: {},".format(args.fps))
	print("overScan: {},".format(width/h_time))
	print("hOffset: {},".format((pulse_length*1.45)/h_time))
	print("pulseLength: {},".format(pulse_length))

	width *= sample_rate

	pulse = np.full(round(pulse_length * sample_rate * oversample), 1.0)
	quiet = np.zeros(round(pulse_length * sample_rate * oversample))

	images = []

	for infile in args.inputs:
		files = glob.glob(infile)
		files.sort()
		images.extend(files)

	outFile = soundfile.SoundFile(args.outfile, "w", samplerate=sample_rate, channels=2, subtype='FLOAT')

	outFile.write(np.zeros((sample_rate, 2)))

	print("Encoding...")

	count = 0

	for imageFile in images:
		print("\rProcessing {}/{} frames".format(count+1,len(images)), end='')

		image = Image.open(imageFile)

		if count % 2 == 0:
			field = 0
		else:
			field = 1

		frame = encode(image, field)
		outFile.write(frame * 0.5)

		count += 1

	print("\nDone!")

	outFile.write(np.zeros((sample_rate, 2)))

	outFile.close()
