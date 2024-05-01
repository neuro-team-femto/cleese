

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
```

Enabling the `generateExpFolder` option will generate a new folder inside `outPath` for each subsequent experiment. Whereas if this option
is disabled, all experiment results are written directly in `outPath`.


