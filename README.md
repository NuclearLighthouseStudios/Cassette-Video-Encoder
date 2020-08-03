# Welcome to the world of Cassette Video!

This is the encoder for the cassette video format, a way to turn videos into audio to put them on normal compact audio cassettes.


## Installation

This script requires NumPY/SciPy, Pillow and SoundFile to run. You can install all of them by running
```
pip install -r requirements.txt
```

I recommend running this script inside a virtualenv.


## Usage

```
usage: enc.py [-h] -i INPUTS [-r RATE] [-f FPS] [-l LINES] [-p PULSELENGTH] [-o OVERSAMPLE] outfile

positional arguments:
  outfile

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTS, --input INPUTS
                        input file pattern(s)
  -r RATE, --rate RATE  sample rate
  -f FPS, --fps FPS     frames per second
  -l LINES, --lines LINES
                        lines of resolution
  -p PULSELENGTH, --pulselength PULSELENGTH
                        length of sync pulses in ms
  -o OVERSAMPLE, --oversample OVERSAMPLE
                        oversampling amount
```

The script reads image sequences as input which can be specified using standard unix shell glob patterns. Just make sure you put them in `""` so they don't get expanded by your shell. You can specify multiple inputs which will be concatenated.

The frames per second and lines options specify the resolution of the video. The horizontal resolution is calculated automatically from these parameters to be as high as possible.

The pulse length option sets the length of the synchronization pulses between lines and frames. Making these longer than the default 0.2ms helps with tracking but decreases the resolution. Making them shorter increases resolution but might lead to playback problems on some players.

The amount of oversampling helps keep timing accurate at higher values like the default of 10, but increases processing time. Only touch this if you know what you're doing.

When running the script it will output a number of configuration variables which are required by the decoder script. These can be used directly in the decoder options parameter.

## Examples

```
./enc.py -i "intro/*.jpg" intro.wav
```
Encode all jpeg images from the intro directory into an intro.wav file with the default settings of 3fps, 150 lines, and 0.2ms sync pulses.


```
./enc.py -i "intro/*.jpg" -f 10 -l 100 -p 0.1 Intro.wav
```
Encode the same frames but at 10 frames per second, 100 lines of resolution and 0.1ms sync pulses.