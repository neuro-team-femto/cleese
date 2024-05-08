![cleese](images/silly-walk.jpg)

CLEESE is a Python toolbox to help the generation of randomized sound and image stimuli for neuroscience research. 

It provides a number of sound and image transformation algorithms (so-called `Engines`) able e.g. to create natural-sounding expressive variations around an original speech recording, or expressive variations on a human face. It also provides a config file interface to automatize the call to these algorithms, in order e.g. to easily create thousands of random variants from a single base file, which can serve as stimuli for neuroscience experiments. 

As of version v2.0.0, CLEESE is composed of two engines: `PhaseVocoder` and `FaceWrap`: 

-  `PhaseVocoder` allows one to create random fluctuations around an audio file’s original contour of pitch, loudness, timbre and speed (i.e. roughly
  defined, its prosody). One of its foreseen applications is the generation of random voice stimuli for reverse correlation experiments in the vein of [Ponsot, Burred, Belin & Aucouturier (2018) Cracking the social code of speech prosody using reverse correlation. PNAS, 115(15), 3972-3977](https://www.pnas.org/content/115/15/3972).
  
- `FaceWarp` uses [mediapipe](https://google.github.io/mediapipe/)'s Face Mesh API to introduce random or precomputed deformation in the expression of a
  visage on an image. This engine was designed to produce batches of deformed faces for reverse correlation experiments in the vein of [Jack, Garrod, Yu, Caldara, & Schyns (2012). Facial expressions of emotion are not culturally universal. PNAS, 109(19), 7241-7244](https://www.pnas.org/doi/10.1073/pnas.1200155109).


