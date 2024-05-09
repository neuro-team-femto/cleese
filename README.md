![cleese](docs/docs/images/silly-walk.jpg)

[[Paper]](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0205943)
[[Documentation]](https://neuro-team-femto.github.io/cleese)
[[Tutorials]](https://neuro-team-femto.github.io/cleese/tutorials/speech/)

CLEESE ("Ministry of Silly Talks") is a Python toolbox to help the generation of randomized sound and image stimuli for neuroscience research. It was originally created to generate arbitrary many random variations around an original speech recording (hence, "silly talks"). It has now been extended to provide a variety of sound and image transformation algorithms (so-called Engines) also able e.g. to create random expressive variations on a human face. 

# Setup

You can download and install the latest version of CLEESE with the following
command:

```Bash
pip install cleese-stim
```

# Available Engines

CLEESE is currently composed of two transformation engines: `PhaseVocoder` and
`FaceWarp`.
* `PhaseVocoder` allows one to create random fluctuations around an audio
  file’s original contour of pitch, loudness, timbre and speed (i.e. roughly
  defined, its prosody). One of its foreseen applications is the generation of
  very many random voice stimuli for reverse correlation experiments.
* `FaceWarp` uses [mediapipe](https://google.github.io/mediapipe/)'s Face Mesh
  API to introduce random or precomputed deformation in the expression of a
  visage on an image. This engine was designed to produce batches of deformed
  faces for reverse correlation experiments.

# Basic Usage

CLEESE runs in completely in Python. Python 3.8.10 was used for the most recent testing.

## PhaseVocoder
```Python
import cleese_stim as cleese
from cleese_stim.engines import PhaseVocoder

inputFile  = 'path_to_input_sound.wav'
configFile = 'path_to_config_file.toml'

cleese.generate_stimuli(PhaseVocoder, inputFile, configFile)
```

The `config_file` controls the parameters of the manipulation. For more information and further functionality see the [documentation](https://neuro-team-femto.github.io/cleese).

# Acknowledgements

CLEESE was originally designed in 2018 by [Juan José Burred](https://www.jjburred.com), [Emmanuel Ponsot](https://www.stms-lab.fr/person/emmanuel-ponsot) and [Jean-Julien Aucouturier](https://www.femto-st.fr/fr/personnel-femto/jeanaucouturier) at [STMS Lab](https://www.stms-lab.fr) (IRCAM/CNRS/Sorbonne Université, Paris - France), and released on the [IRCAM Forum](https://forum.ircam.fr/) platform. As of 2021, CLEESE is now developed and maintained by the [Neuro Team](https://neuro-team-femto.github.io/) [FEMTO-ST Institute](https://www.femto-st.fr/) (CNRS/Université Bourgogne Franche-Comté) in Besançon - France.

CLEESE's development was originally funded by the [European Research Council](https://erc.europa.eu) ([CREAM](https://neuro-team-femto.github.io/cream/) 335536, 2014-2019, PI: JJ Aucouturier), and has since then received support from [Agence Nationale de la Recherche](https://anr.fr/) (ANR SEPIA, AND Sounds4Coma), [Fondation pour l'Audition](https://www.fondationpourlaudition.org) (DASHES) and [Région Bourgogne-Franche Comté](https://www.bourgognefranchecomte.fr/) (ASPECT).


If you use CLEESE in academic work, please cite it as :

```
Burred, JJ., Ponsot, E., Goupil, L., Liuni, M. & Aucouturier, JJ. (2019).
CLEESE: An open-source audio-transformation toolbox for data-driven experiments in speech and music cognition.
PLoS one, 14(4), e0205943.
```

# License

CLEESE is a free, standalone Python module, distributed under an open-source MIT Licence on the FEMTO Neuro team [github page](https://github.com/neuro-team-femto/cleese).
