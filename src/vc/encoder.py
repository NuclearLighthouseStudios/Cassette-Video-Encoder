import numpy as np
from scipy import signal

def encode_color(image, field, width, lines, pulse_length, sample_rate, over_sample):
	image = image.resize((round(width * over_sample), lines))
	image = image.convert('YCbCr')

	pulse = np.full(round(pulse_length * sample_rate * over_sample), 1.0)
	quiet = np.zeros(round(pulse_length * sample_rate * over_sample))

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

	if over_sample > 1:
		left = signal.resample_poly(left, 1, over_sample)
		right = signal.resample_poly(right, 1, over_sample)

	return np.stack([left, right], 1)


def encode_bw(image, field, width, lines, pulse_length, sample_rate, over_sample):
	image = image.resize((round(width * over_sample), lines))
	image = image.convert('L')

	pulse = np.full(round(pulse_length * sample_rate * over_sample), 1.0)
	quiet = np.zeros(round(pulse_length * sample_rate * over_sample))

	data = np.asarray(image)

	out = np.zeros(0)

	for line in range(0, data.shape[0] // 2):
		if field == 0:
			out = np.append(out, pulse)
			out = np.append(out, pulse * -1)
		else:
			out = np.append(out, pulse * -1)
			out = np.append(out, pulse)

		out = np.append(out, quiet)

		out = np.append(out, data[line * 2 + field] / 255.0 - 0.5)

		out = np.append(out, quiet)

	if over_sample > 1:
		out = signal.resample_poly(out, 1, over_sample)

	return np.stack([out, out], 1)
