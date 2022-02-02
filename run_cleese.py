#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Usage examples.
'''

from PIL import Image
import numpy as np

import cleese_stim as cleese

inputFile = './tutorial/sounds/female_anniversaire_isochrone.wav'
imgFile = './tutorial/pics/monalisa.jpg'
dfmFile = './tutorial/dfm/default.dfm'
dfmxyFile = './tutorial/dfm/monalisa.random.dfmxy'
landmarksFile = './tutorial/dfm/monalisa.landmarks.txt'
configFile = './cleeseConfig_all.py'
tomlConfig = './cleese-phase-vocoder.toml'
mediapipeConfig = './cleese-mediapipe.toml'

# example 1: run with random BPFs
# cleese.generate_stimuli(cleese.engines.PhaseVocoder, inputFile, tomlConfig)

# # example 2: run with given BPF
# # FIXME Second 0. (value) triggers a crash
# givenBPF = np.array([[0., 0.], [3., 500.]])
# cleese.generate_stimuli(cleese.Engine.PHASE_VOCODER,
#                         inputFile,
#                         tomlConfig,
#                         BPF=givenBPF)

# # example 3: run with given scalar factor
# FIXME Overly slow and RAM consuming
# givenBPF = 200
# cleese.generate_stimuli(cleese.Engine.PHASE_VOCODER,
#                         inputFile,
#                         tomlConfig,
#                         BPF=givenBPF)

# # example 4: array input and output
# waveIn, sr, __ = cleese.engines.PhaseVocoder.wavRead(inputFile)
# waveOut, BPFout = cleese.process_data(cleese.engines.PhaseVocoder,
#                                       waveIn,
#                                       tomlConfig,
#                                       sample_rate=sr)

# # example 5: example with given time vector
# givenTimeVec = np.array([0.1, 0.15, 0.3])
# cleese.generate_stimuli(cleese.engines.PhaseVocoder,
#                         inputFile,
#                         tomlConfig,
#                         timeVec=givenTimeVec)

# example 6: deform a single image
# img = cleese.process_file(cleese.engines.Mediapipe, imgFile, mediapipeConfig)
# Image.fromarray(img).show()

# example 7: Generate randomly deformed images
# cleese.generate_stimuli(cleese.engines.Mediapipe, imgFile, mediapipeConfig)

# example 8: Apply existing .dfm
# dfm = cleese.engines.Mediapipe.load_dfm(dfmFile)
# img = cleese.process_file(cleese.engines.Mediapipe,
#                           imgFile,
#                           mediapipeConfig,
#                           dfm=dfm)
# Image.fromarray(img).show()

# example 9: Apply existing .dfmxy
# dfmxy = cleese.engines.Mediapipe.load_dfmxy(dfmxyFile)
# img = cleese.process_file(cleese.engines.Mediapipe,
#                           imgFile,
#                           mediapipeConfig,
#                           dfmxy=dfmxy)
# Image.fromarray(img).show()

# example 10: Convert dfmxy to dfm
# cleese.engines.Mediapipe.dfmxy_to_dfm(dfmxyFile,
#                                       landmarksFile,
#                                       output_dfm_file='./converted.dfm')
