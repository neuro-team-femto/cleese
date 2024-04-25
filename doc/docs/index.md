# Welcome to CLEESE

CLEESE ("Ministry of Silly Speech") is a sound and image manipulation tool designed to generate an infinite number of possible stimuli; be it natural-sounding expressive variations around an original speech recording, or variations on the expression of a human face.

More precisely, CLEESE is currently composed of two engines: `PhaseVocoder` and `Mediapipe`.

* PhaseVocoder allows one to create random fluctuations around an audio file’s original contour of pitch, loudness, timbre and speed (i.e. roughly defined, its prosody). One of its foreseen applications is the generation of very many random voice stimuli for reverse correlation experiments.
* Mediapipe uses mediapipe's Face Mesh API to introduce random or precomputed deformation in the expression of a visage on an image. This engine was designed to produce batches of deformed faces for reverse correlation experiments.

CLEESE is a free, standalone Python module, distributed under an open-source MIT Licence on the IRCAM Forumnet plateform. It was originally designed by Juan José Burred, Emmanuel Ponsot and Jean-Julien Aucouturier at STMS Labs (IRCAM/CNRS/Sorbonne Université, Paris), with generous funding from the European Research Council (CREAM 335536, 2014-2019). Development is now continued at the FEMTO-ST Institute (CNRS/Université Bourgogne Franche-Comté), in collaboration with developper Lara Kermarec (face deformation, 2022). 
