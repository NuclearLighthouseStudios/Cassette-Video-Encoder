# Welcome to the world of Cassette Video!

This is the encoder for the cassette video format, a way to turn videos into audio to put them on normal compact audio cassettes.


## Installation

```
pipx install .
```

## Usage

```
usage: vc-enc [-h] [-r RATE] [-b] [-s] [-f FPS] [-l LINES] [-p PULSE_LENGTH] [-o OVER_SAMPLE] infile outfile

Video Cassette Encoder

positional arguments:
  infile                input video
  outfile               output audio file

options:
  -h, --help            show this help message and exit
  -r, --rate RATE       sample rate (default: 96000)
  -b, --bw              black and white mode for mono audio (default: False)
  -s, --settings        print decoder settings (default: False)
  -f, --fps FPS         frames per second (default: 3)
  -l, --lines LINES     lines of resolution (default: 150)
  -p, --pulselength PULSE_LENGTH
                        length of sync pulses in ms (default: 0.2)
  -o, --oversample OVER_SAMPLE
                        oversampling amount (default: 1)
```

The script should be able to read most videos supported by libav.
The frames per second and lines options specify the resolution of the video. The horizontal resolution is calculated automatically from these parameters to be as high as possible.

The pulse length option sets the length of the synchronization pulses between lines and frames. Making these longer than the default 0.2ms helps with tracking but decreases the resolution. Making them shorter increases resolution but might lead to playback problems on some players.

The amount of oversampling helps keep timing accurate at higher values like the default of 10, but increases processing time. Only touch this if you know what you're doing.

When running the script with the -s option it will output a number of configuration variables which are required by the decoder script. These can be used directly in the decoder options parameter.


## Examples

```
vc-enc video.mp4 video.wav
```
Encode the video video.mp4 into a sound file named video.wav with the default settings of 3fps, 150 lines, and 0.2ms sync pulses.


```
vc-enc -s -f 10 -l 100 -p 0.1 video.mov video.wav
```
Encode the video video.mov at 10 frames per second, 100 lines of resolution, and 0.1ms sync pulses and print the matching decoder settings to the console.