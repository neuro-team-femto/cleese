

## Common configuration

In order to configure the different tools it provides, CLEESE uses `toml` configuration files. Most sections in these file are specific to
certain engines, but here are a few variables shared among all engines:

```toml
[main]

# output root folder
outPath = "./CLEESE_output_data/"

# number of output files to generate (for random modifications)
numFiles = 10

# generate experiment folder with name based on current time
generateExpFolder = true

# parameter file extension (default: '.txt')
param_ext = '.txt'
```

Enabling the `generateExpFolder` option will generate a new folder inside `outPath` for each subsequent experiment. Whereas if this option
is disabled, all experiment results are written directly in `outPath`.

CLEESE engines store parameter files alongside each stimulus. By default, the name of these files are the same as the corresponding stimulus, with the `.txt` extention (ex. for `PhaseVocoder`, `file001.wav` and the corresponding `file001.txt`). This extension (and end of the file name) can be changed with the `param_ext` option (ex. `param_ext = '_bpf.txt` will store parameter files as e.g. `file001_bpf.txt`). 


