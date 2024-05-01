# Tutorial: random speech generation

This tutorial shows how to use CLEESE's `FaceWarp` engine to generate a arbitrary number of random facial expressions around an original image of a face.

<span>
![png](./pics/monalisa_transformed.jpg){ width=20% } ![png](./pics/monalisa_transformed_2.jpg){ width=20% } ![png](./pics/monalisa_transformed_3.jpg){ width=20% } ![png](./pics/monalisa_transformed_4.jpg){ width=20% }

</span>

## Preambule

### Verify your installation

Before starting, please verify that you have a working CLEESE installation, by running the following cell which you return without error. 

``` py title="import cleese"
import cleese_stim as cleese
from cleese_stim.engines import FaceWarp
```
Check the [installation instructions](../../installation) if needed. 

### Useful files

In the following, we'll be a number of files which you'll first need to download and store in your path at the indicated place

- [monalisa.jpg](./pics/monalisa.jpg) :material-arrow-right: `./pics/monalisa.jpg` 
- [random_lips.toml](./configs/random_lips.toml) :material-arrow-right: `./configs/random_lips.toml`
- [monalisa.random.dfmxy](./dfm/monalisa.random.dfmxy) :material-arrow-right: `./dfm/monalisa.random.dfmxy`
- [smile.dfm](./dfm/smile.dfm) :material-arrow-right: `./dfm/smile.dfm`


## Preambule

### Verify your installation¶

Before starting, please verify that you have a working CLEESE installation, by running the following cell which you return without error. 


```python
import cleese_stim as cleese
from cleese_stim.engines import FaceWarp
```

## Basic image manipulation with CLEESE

### Random image deformation

The most basic usage scenario of CLEESE's `FaceWarp` engine is to input a single image (here, a close-up of the Mona Lisa, `pics/monalisa.jpg`)

![Image title](../pics/monalisa.jpg){ width=50% }


and use CLEESE to apply random tranformation to the expression of the face on the image. For this we use the `cleese.process_data` function that generate a single input from existing array data. We provide this function with the engine we want to use for this transformation (here: `FaceWarp`), the data itself, and a configuration file specifying the parameters of the transformation.

```py title="Random face transformation"
monalisa_file = "./pics/monalisa.jpg"
config_file = "./configs/random_lips.toml"

img = FaceWarp.img_read(monalisa_file)
deformed = cleese.process_data(FaceWarp, img, config_file)
FaceWarp.img_write(deformed, "./pics/monalisa_transformed.jpg")

```

![Image title](../pics/monalisa_transformed.jpg){ width=50% }

### Direct file loading

CLEESE can also directly load image files and process them using the  `cleese.process_file` function, like so:

```python
monalisa_file = "./pics/monalisa.jpg"
config_file = "./configs/random_lips.toml"

deformed = cleese.process_file(FaceWarp, monalisa_file, config_file)
FaceWarp.img_write(deformed, "./pics/monalisa_transformed_2.jpg")

```

![Image title](../pics/monalisa_transformed_2.jpg){ width=50% }

<h3> Batched transforms </h3>

Instead of generating output files one at a time, CLEESE can be used to generate large numbers of manipulated files, each randomly generated using parameters specified in config files as above. This is achieved by using the `cleese.generate_stimuli` function. This function does not return the generated images, but directly writes them in the folder specified under `[main] outPath`, and the number of output files generated is given by `[main] numFiles`, all of which are found in the configuration file:
```
[main]

# output root folder
outPath = "output"

# number of output files to generate (for random modifications)
numFiles = 10

# generate experiment folder with name based on current time
generateExpFolder = false
```

```python
monalisa_file = "./pics/monalisa.jpg"
config_file = "./configs/random_lips.toml"

deformed = cleese.generate_stimuli(FaceWarp, monalisa_file, config_file)
```

In addition to generating 10 images containing randomly deformed faces in the ouptut directory, CLEESE also writes for each image a `.dfmxy` file containing the deformation vectors applied to each facial landmarks, as well as a file containing the positions of all the landmarks detected on the original image (`.landmarks.txt`). Additionally, both the original image and configuration files are copied to the output directory.

## Advanced use

### Applying existing deformation

CLEESE's `Mediapipe` is also able to apply a given deformation set -- for example loaded from a `.dfmxy` file -- to an image. This can be useful to gauge the combined results of a reverse correlation experiment.


```python
dfmxy_file = "./dfm/monalisa.random.dfmxy"
monalisa_file = "./pics/monalisa.jpg"
config_file = "./configs/random_lips.toml"

dfmxy = FaceWarp.load_dfmxy(dfmxy_file)
deformed = cleese.process_file(FaceWarp,
                          monalisa_file,
                          config_file,
                          dfmxy=dfmxy)
FaceWarp.img_write(deformed, "./pics/monalisa_transformed_3.jpg")

```

![Image title](../pics/monalisa_transformed_3.jpg){ width=50% }



## Advanced use

### Converting `.dfmxy` to `.dfm`

Other face deformation tools developed by our team use the `.dfm` deformation file format, more suited to applying the same deformation to an arbitrary face. However, by its use of barycentric coordinates in a landmarks triangulation, it isn't suited to any post or pre-processing, which is an area where `.dfmxy` shines. As a result, CLEESE's `Mediapipe` provides a way to convert a given, `.dfmxy` to `.dfm`, provided you also have the original landmarks on hand:


```python
dfmxy_file = "./dfm/monalisa.random.dfmxy"
landmarks_file = "./dfm/monalisa.landmarks.txt"
dfm_file = "./output/converted.dfm"

FaceWarp.dfmxy_to_dfm(dfmxy_file,
                       landmarks_file,
                       output_dfm_file=dfm_file)

```

### Applying a `.dfm`

As another compatibility feature, CLEESE's `Mediapipe` also allow for applying an existing `.dfm` file to an arbitrary image:


```python
dfm_file = "./dfm/smile.dfm"
monalisa_file = "./pics/monalisa.jpg"
config_file = "./configs/random_lips.toml"

dfm = FaceWarp.load_dfm(dfm_file)
deformed = cleese.process_file(FaceWarp,
                          monalisa_file,
                          config_file,
                          dfm=dfm)
FaceWarp.img_write(deformed, "./pics/monalisa_transformed_4.jpg")

```

![png](./pics/monalisa_transformed_4.jpg){ width=50% }
    
