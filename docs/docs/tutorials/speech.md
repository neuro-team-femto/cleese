# Tutorial: random speech generation

This tutorial shows how to use CLEESE's `PhaseVocoder` engine to generate a arbitrary number of expressive variations around an original speech recording.

## Preambule

### Verify your installation

Before starting, please verify that you have a working CLEESE installation, by running the following cell which you return without error. 

``` py
import cleese_stim as cleese
from cleese_stim.engines import PhaseVocoder
```
Check the [installation instructions](../../installation) if needed. 

### Useful imports

The following code imports all the python packages that are needed in the rest of this tutorial. 

```py
import numpy as np
from IPython.display import Markdown, display, Audio
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import matplotlib.pyplot as plt
%matplotlib inline
from pylab import rcParams
rcParams['figure.figsize'] = 5, 2
```

### Useful files

In the following, we'll be a number of files which you'll first need to download and store in your path at the indicated place

- [male_vraiment_flattened.wav](./sounds/male_vraiment_flattened.wav) :material-arrow-right: `./sounds/male_vraiment_flattened.wav` 
- [random_pitch_profile.toml](./configs/random_pitch_profile.toml) :material-arrow-right: `./configs/random_pitch_profile.toml`
- [female_anniversaire_isochrone.wav](./sounds/female_anniversaire_isochrone.wav) :material-arrow-right: `./sounds/female_anniversaire_isochrone.wav`
- [random_speed_profile.toml](./configs/random_speed_profile.toml) :material-arrow-right: `./configs/random_speed_profile.toml`
- [chained_pitch_stretch.toml](./configs/chained_pitch_stretch.toml) :material-arrow-right `./configs/chained_pitch_stretch.toml`
- [male_vraiment_original.wav](./sounds/male_vraiment_original.wav) :material-arrow-right: `./sounds/male_vraiment_original.wav` 

## Basic sound manipulation with CLEESE

### Random pitch profile in a single utterance

The most basic usage scenario of CLEESE is to input a single recording (ex. the French word "vraiment" - "really", recorded by a single male speaker)

<audio controls src="../sounds/male_vraiment_flattened.wav"></audio><br>
<a href="../sounds/male_vraiment_flattened.wav"> Download audio </a>

and use CLEESE to transform the sound with a random pitch profile. This, like all cleese operations, is done by passing to the main cleese function `cleese.process_data` a configuration file ([random_pitch_profile.toml](./configs/random_pitch_profile.toml)) which specifies the manipulation we want. Here: cut the file in `pitch.window.count = 6` time segments, draw a random pitch shift factor at each segment boundary from a Gaussian distribution centered on 0 and standard deviation `pitch.std = 300`cents, and interpolate between segment boundaries using linear `pitch.BPFType = "ramp"`. (See [PhaseVocoder](../../api/phase-vocoder/) documentation for more information)

```toml
[pitch]
# pitch transposition window in seconds. If 0 : static transformation
window.len = 0.11

# number of pitch transposition windows. If 0 : static transformation
window.count = 6

# 's': force winlength in seconds,'n': force number of windows (equal length)
window.unit = 'n'

# standard deviation (cents) for random transposisiton (Gaussian distrib for now)
std = 300

# truncate distribution values (factor of std)
trunc = 1

# type of breakpoint function:
#      'ramp': linear interpolation between breakpoints
#      'square': square BPF, with specified transition times at edges
BPFtype = 'ramp'

# in s: transition time for square BPF
trTime = 0.02
```

The following code is pretty much all there is to call: `cleese.process_data` takes in the `Engine` that is called on to do the transformation (here, `PhaseVocoder` - see the [Image tutorial](../face) for a similar call to image-transformation engine `FaceWarp`), the array `wave_in` of audio data obtained from `PhaseVocoder.wav_read` and its sampling rate `sr`, and the path to the configuration file `config_file` that tells the `PhaseVocoder` engine what to do with it all. 

```python
input_file = "./sounds/male_vraiment_flattened.wav"
config_file = "./configs/random_pitch_profile.toml"

# read input wavefile, and extract pitch for display (unnecessary for cleese.process below)
wave_in, sr, _ = PhaseVocoder.wav_read(input_file)

# transform sound
wave_out,bpf_out = cleese.process_data(PhaseVocoder, wave_in, config_file, sample_rate=sr)

# save file if necessary
output_file = "./sounds/male_vraiment_flattened_transformed.wav"
PhaseVocoder.wav_write(wave_out, output_file, sr)
```

<audio controls src="../sounds/male_vraiment_flattened_transformed.wav"></audio><br>
<a href="../sounds/male_vraiment_flattened_transformed.wav"> Download audio </a>

CLEESE's `PhaseVocoder` includes a utility for extracting pitch in speech/audio files (`PhaseVocoder.extract_pitch`), which uses the YIN pitch extraction algorithm, and can be used to visualize the pitch profile of sounds before and after manipulation. This is just for visualization purposes, and isn't necessary for the working of the main `cleese.process` function above. 

``` py
# extract pitch before transformation
pitch_in,times_in = PhaseVocoder.extract_pitch(wave_in,sr)

# extract pitch after transformation
pitch_out,times_out = PhaseVocoder.extract_pitch(wave_out,sr)

# display 
plt.plot(times_in, pitch_in, 'k:', label='pre')
plt.plot(times_out, pitch_out, 'k', label='post')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch (Hz)')
plt.ylim([70,120])
```

![Image title](../images/speech_tutorial_1.png)


### Random speed profile in a song 

CLEESE can process longer files than a single word and, instead of manipulating pitch, can manipulate the duration of each portion of the file. To demonstrate this, we use CLEESE to randomly stretch each note in a recording of a song (the French song "Joyeux Anniversaire" / "Happy Birthday", sung by a female singer)

<audio controls src="../sounds/female_anniversaire_isochrone.wav"></audio><br>
<a href="../sounds/female_anniversaire_isochrone.wav"> Download audio </a>

This, as above, is done by passing to `cleese.process_data` a configuration file which specifies the manipulation we want. Here: cut the file in `stretch.window.len = 0.5` second time segments, draw a random stretch shift factor at each segment boundary from a Gaussian distribution centered on 1.0 and standard deviation `stretch.std = 1.5` (where factors >1 correspond to a time stretch, and factors <1 correspond to a time compression), and interpolate between segment boundaries using linear `stretch.BPFType = "ramp"`. 

```toml
[stretch]

window.len = 0.1
window.count = 5
window.unit = 'n'

# stretching factor. >1: expansion, <1: compression
std = 1.5
trunc = 1
BPFtype = 'ramp'
trTime = 0.05
```

The following code runs the transformation

```python
input_file = "./sounds/female_anniversaire_isochrone.wav"
config_file = "./configs/random_speed_profile.toml"

# read input wavefile
wave_in, sr, _ = PhaseVocoder.wavRead(input_file)

# CLEESE
wave_out,bpf_out = cleese.process_data(PhaseVocoder, wave_in, config_file, sample_rate=sr)

# save file if necessary
output_file = "./sounds/female_anniversaire_isochrone_transformed.wav"
PhaseVocoder.wav_write(wave_out, output_file, sr)
```

<audio controls src="../sounds/female_anniversaire_isochrone_transformed.wav"></audio><br>
<a href="../sounds/female_anniversaire_isochrone_transformed.wav"> Download audio </a>

Display pre and post pitch profile: notice pitch values weren't changed, but only how they appear in time)

```py
# extract pitch before transformation
pitch_in,times_in = PhaseVocoder.extract_pitch(wave_in,sr)

# display 
plt.plot(times_in, pitch_in, 'k')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch (Hz)')
plt.ylim([70,120])

```

![Image title](../images/speech_tutorial_2.png)

```py
# extract pitch after transformation
pitch_out,times_out = PhaseVocoder.extract_pitch(wave_out,sr)

# display 
plt.plot(times_out, pitch_out, 'k', label='post')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch (Hz)')
plt.ylim([70,120])
```

![Image title](../images/speech_tutorial_3.png)


### Batched transforms 

Instead of generating output files one at a time, CLEESE can be used to generate large numbers of manipulated files, each randomly generated using parameters specified in config files as above. This is achieve by pusing cleese.generate_stimuli `cleese.generate_stimuli(PhaseVocoder, input_file, config_file)`. Output files are not returned by the function, but directly written in `main.outPath`, and the number of output files generated is given by `main.numFiles`, all of which are found in the configuration file:

```toml
[main]

# output root folder
outPath = "./output/"

# number of output files to generate (for random modifications)
numFiles = 10

# apply transformation in series (True) or parallel (False)
chain = true

# transformations to apply
transf = ["pitch"]

# generate experiment folder with name based on current time
generateExpFolder = true
```

The following code will create 10 random transformations of the `input_file`, each with random parameters generated from `config_file`, and store both files and parameters in the `outPath` folder designated in `config_file` 

!!! warning
    Depending on how you run this code, you may want to ensure the `outPath` folder exists in your path before running this code 

```python
input_file = "./sounds/male_vraiment_flattened.wav"
config_file = "./configs/random_pitch_profile.toml"

# CLEESE
cleese.generate_stimuli(PhaseVocoder, input_file, config_file)

```

<audio controls src="../sounds/male_vraiment_flattened_transformed_1.wav"></audio> 
<a href="../sounds/male_vraiment_flattened_transformed_1.wav"> Download audio </a> <br>
<audio controls src="../sounds/male_vraiment_flattened_transformed_2.wav"></audio>
<a href="../sounds/male_vraiment_flattened_transformed_2.wav"> Download audio </a> <br>
<audio controls src="../sounds/male_vraiment_flattened_transformed_3.wav"></audio>
<a href="../sounds/male_vraiment_flattened_transformed_3.wav"> Download audio </a> <br>
<audio controls src="../sounds/male_vraiment_flattened_transformed_4.wav"></audio>
<a href="../sounds/male_vraiment_flattened_transformed_4.wav"> Download audio </a> <br>


### Chained transforms 

CLEESE can process files with a series of transformations that follow each other, e.g. first time-stretch the file, then pitch-shift it. This is done by specifying keyword `chain = true` under the configuration section `[main]`, as well as the list of transformations to be applied, e.g. here `transf = ['pitch','stretch']`.  

```toml
[main]

# output root folder
outPath = "./output/"

# number of output files to generate (for random modifications)
numFiles = 10

# apply transformation in series (True) or parallel (False)
chain = true

# transformations to apply
transf = ["pitch", "stretch"]

# generate experiment folder with name based on current time
generateExpFolder = true
```

The following code runs a chained transformation (notice the change of `config_file`) on 10 files, and stores them all in the `outPath` folder designated in `config_file`

```python
input_file = "./sounds/male_vraiment_flattened.wav"
config_file = "./configs/chained_pitch_stretch.toml"

# CLEESE
cleese.generate_stimuli(PhaseVocoder, input_file, config_file)
```


<audio controls src="../sounds/male_vraiment_flattened_transformed_5.wav"></audio> 
<a href="../sounds/male_vraiment_flattened_transformed_5.wav"> Download audio </a> <br>
<audio controls src="../sounds/male_vraiment_flattened_transformed_6.wav"></audio>
<a href="../sounds/male_vraiment_flattened_transformed_6.wav"> Download audio </a> <br>
<audio controls src="../sounds/male_vraiment_flattened_transformed_7.wav"></audio>
<a href="../sounds/male_vraiment_flattened_transformed_7.wav"> Download audio </a> <br>
<audio controls src="../sounds/male_vraiment_flattened_transformed_8.wav"></audio>
<a href="../sounds/male_vraiment_flattened_transformed_8.wav"> Download audio </a> <br>

## Advanced use

### Flattening files

When applying CLEESE to generate stimuli for reverse correlation, it is often advisable to use base stimuli that are as flat as possible (e.g., if randomizing pitch, start with a sound that has constant pitch). CLEESE can be used to flatten an existing recording, using the trick of not letting the tool generate its own random breakpoint function, but rather providing it with a custom function that inverts the natural pitch variations found in the original file. We demonstrate this with an original, non flattened recording of the word "vraiment". 

Start with a normal, non-flat recording of the same word ``vraiment'' as above: 

<audio controls src="../sounds/male_vraiment_original.wav"></audio><br>
<a href="../sounds/male_vraiment_original.wav"> Download audio </a>

The file has a soft, down-ward pitch contour, as show here

``` py
input_file = "./sounds/male_vraiment_original.wav"
wave_in, sr, _ = PhaseVocoder.wav_read(input_file)
pitch_in,times_in = PhaseVocoder.extract_pitch(wave_in,sr, win=0.02, bounds=[50, 200])
plt.plot(times_in, pitch_in, 'k')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch')
```

![Image title](../images/speech_tutorial_4.png)

To flatten this existing contour, we construct a custom break-point function (bpf) that passes through the pitch shift values needed to shift the contour down to a constant pitch value, arbitrarily set here at 110Hz. 


```py
mean_pitch = 110.
def difference_to_cents(pitch, ref_pitch):
    if pitch >0:
        return -1200*np.log2(pitch/ref_pitch)
    else:
        return 1
bpf_times = times
bpf_val = np.array([difference_to_cents(hz, mean_pitch) for hz in pitch])
# display original file
plt.plot(1000*bpf_times, bpf_val, 'k')
plt.xlabel('time in file (ms)')
plt.ylabel('BPF')
```

![Image title](../images/speech_tutorial_5.png)
    

We then apply this custom BPF to the original file, using `cleese.process_data(PhaseVocoder, wave_in, config_file, sample_rate=sr, BPF=bpf)` (passing audio data as input, because we don't need batch mode here). 

```python
config_file = "./configs/random_pitch_profile.toml"

# CLEESE
bpf = np.column_stack((bpf_times,bpf_val))
wave_out,bpf_out = cleese.process_data(PhaseVocoder, wave_in, config_file, sample_rate=sr, BPF=bpf)
```

<audio controls src="../sounds/male_vraiment_flattened.wav"></audio><br>
<a href="../sounds/male_vraiment_flattened.wav"> Download audio </a>

Compare pitch profile before and after transformation: 

```py 
# display transformed file
pitch_out,times_out = PhaseVocoder.extract_pitch(wave_out,sr, win=0.005, bounds=[50, 200])
plt.plot(times_in, pitch_in, 'k')
plt.plot(times_out, pitch_out, 'b')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch')
```

![Image title](../images/speech_tutorial_6.png)


### Using custom breakpoints

Instead of generating linearly spaced time windows (or, as called here, breakpoints), CLEESE supports a list of externally provided time positions. To demonstrate this, we use CLEESE to stretch the duration of each note in the song "Joyeux Anniversaire" (which we already used above). 

<audio controls src="../sounds/female_anniversaire_isochrone.wav"></audio><br>
<a href="../sounds/female_anniversaire_isochrone.wav"> Download audio </a>

To find note boundaries, we can e.g. use an external audio editor such as [Audacity](https://www.audacityteam.org), and measure time positions between notes as `[0.027, 0.634, 1.137, 1.647, 2.185, 2.649, 3.181]`.

![Image title](../images/speech_tutorial_7.png)

We can then generate a breakpoint function with `cleese.create_BPF` which uses these time points and parameters loaded from the stretch config file `config_file`. This BPF can then be passed to `cleese.process_data` as argument. 


```python
input_file = "./sounds/female_anniversaire_isochrone.wav"
config_file = "./configs/random_speed_profile.toml"

wave_in, sr, _ = PhaseVocoder.wavRead(input_file)

time_points = np.array([0.027, 0.634, 1.137, 1.647, 2.185, 2.649, 3.181]) # values found in audacity
num_points = len(time_points)
bpf = PhaseVocoder.create_BPF(
    'stretch',config_file,time_points,num_points,0)   

wave_out,bpf_out = cleese.process_data(
    PhaseVocoder, wave_in, config_file, sample_rate=sr, BPF=bpf)
```

<audio controls src="../sounds/female_anniversaire_isochrone_transformed_2.wav"></audio><br>
<a href="../sounds/female_anniversaire_isochrone_transformed_2.wav"> Download audio </a>

```py 
pitch_in,times_in = PhaseVocoder.extract_pitch(wave_in,sr)
plt.plot(times_in, pitch_in, 'k')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch')

# display transformed file
pitch_out,times_out = PhaseVocoder.extract_pitch(wave_out,sr)
plt.plot(times_out, pitch_out, 'b')
plt.xlabel('time in file (ms)')
plt.ylabel('pitch')
```

![Image title](../images/speech_tutorial_8.png)

