import argparse
import signal

import numpy as np
import soundfile
import av

from .encoder import encode_color, encode_bw

shutdown = False

def handler(signum, frame):
	print("Got SIGINT, quitting…")
	global shutdown
	shutdown = True

def main():
	parser = argparse.ArgumentParser(
		description="Video Cassette Encoder",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument("infile", help="input video", type=argparse.FileType("rb"))
	parser.add_argument("outfile", help="output audio file", type=argparse.FileType("wb"))

	parser.add_argument("-r", "--rate", help="sample rate", default=96000, type=int)
	parser.add_argument("-b", "--bw", help="black and white mode for mono audio", default=False, action="store_true")
	parser.add_argument("-s", "--settings", help="print decoder settings", default=False, action="store_true")
	parser.add_argument("-f", "--fps", help="frames per second", default=3, type=float)
	parser.add_argument("-l", "--lines", help="lines of resolution", default=150, type=int)
	parser.add_argument("-p", "--pulselength", dest="pulse_length", help="length of sync pulses in ms", default=0.2, type=float)
	parser.add_argument("-o", "--oversample", dest="over_sample", help="oversampling amount", default=1, type=int)

	args = parser.parse_args()

	sample_rate = args.rate
	over_sample = args.over_sample
	pulse_length = args.pulse_length/1000

	fps = args.fps
	lines = args.lines
	h_time = (1/fps/lines)*2
	width = h_time-(pulse_length*4)

	if width <= 0:
		print("Not time for image data, try reducing frame rate, lines, or pulse length.")
		exit(1)

	if args.settings:
		print(f"color: {"false" if args.bw else "true"},")
		print(f"hFreq: {1.0/h_time:g},")
		print(f"vFreq: {args.fps:g},")
		print(f"overScan: {width/h_time:g},")
		print(f"hOffset: {(pulse_length*1.45)/h_time:g},")
		print(f"pulseLength: {pulse_length:g},")

	width *= sample_rate

	outFile = soundfile.SoundFile(args.outfile, "w", samplerate=sample_rate, channels=2)
	outFile.write(np.zeros((sample_rate, 2)))

	container = av.open(args.infile)

	print("Encoding...")
	signal.signal(signal.SIGINT, handler)

	for index, frame in enumerate(container.decode(video=0)):
		print(f"\rProcessing frame {index}", end="")

		image = frame.to_image()

		if index % 2 == 0:
			field = 0
		else:
			field = 1

		if args.bw:
			frame = encode_bw(image, field, width, lines, pulse_length, sample_rate, over_sample)
		else:
			frame = encode_color(image, field, width, lines, pulse_length, sample_rate, over_sample)

		outFile.write(frame * 0.5)

		if shutdown:
			break

	print("\nDone!")

	outFile.write(np.zeros((sample_rate, 2)))
	outFile.close()
