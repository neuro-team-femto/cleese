![cleese](docs/docs/images/silly-walk.jpg)

CLEESE ("Ministry of Silly Speech") is a sound and image manipulation tool
designed to generate an infinite number of possible stimuli; be it
natural-sounding expressive variations around an original speech recording, or
variations on the expression of a human face.

More precisely, CLEESE is currently composed of two engines: `PhaseVocoder` and
`Mediapipe`.
* `PhaseVocoder` allows one to create random fluctuations around an audio
  file’s original contour of pitch, loudness, timbre and speed (i.e. roughly
  defined, its prosody). One of its foreseen applications is the generation of
  very many random voice stimuli for reverse correlation experiments.
* `Mediapipe` uses [mediapipe](https://google.github.io/mediapipe/)'s Face Mesh
  API to introduce random or precomputed deformation in the expression of a
  visage on an image. This engine was designed to produce batches of deformed
  faces for reverse correlation experiments.

CLEESE is a free, standalone Python module, distributed under an open-source
MIT Licence on the IRCAM Forumnet plateform. It was designed by Juan José
Burred, Emmanuel Ponsot and Jean-Julien Aucouturier (STMS, IRCAM/CNRS/Sorbonne
Université, Paris), with collaboration from Pascal Belin (Institut des
Neurosciences de la Timone, Aix-Marseille Université), with generous funding
from the European Research Council (CREAM 335536, 2014-2019, PI: JJ
Aucouturier), and support for face deformation was added by Lara Kermarec
(2022).

Jupyter notebooks are available as tutorials form
[sound manipulation](tutorial_audio.ipynb) and
[image manipulation](tutorial_images.ipynb).

The user manual in PDF format is available
[here](https://github.com/creamlab/cleese/raw/master/doc/CLEESE_manual_v2.0.pdf).
