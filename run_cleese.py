#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Usage examples.
'''

import cleese
import cv2

inputFile = './tutorial/sounds/female_anniversaire_isochrone.wav'
imgFile = './tutorial/pics/monalisa.jpg'
dfmFile = './tutorial/dfm/default.dfm'
configFile = './cleeseConfig_all.py'
tomlConfig = './cleese-phase-vocoder.toml'
mediapipeConfig = './cleese-mediapipe.toml'

# example 1: run with random BPFs
# cleese.process(soundData=inputFile, configFile=configFile)
#cleese.generate_stimuli(cleese.engines.PhaseVocoder, inputFile, tomlConfig)
#cleese.process_file(cleese.engines.PhaseVocoder, inputFile, tomlConfig)
# waveIn, sr, __ = cleese.cleeseProcess.wavRead(inputFile)
#waveOut, BPFout = cleese.process_data(cleese.engines.PhaseVocoder, waveIn, tomlConfig, sample_rate=sr)

# # example 2: run with given BPF
# import numpy as np
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
# waveIn,sr,__ = cleese.wavRead(inputFile)
# waveOut,BPFout = cleese.process(soundData=waveIn, configFile=configFile, sr=sr)

# # example 5: example with given time vector
# import numpy as np
# givenTimeVec = np.array([0.1, 0.15, 0.3])
# cleese.generate_stimuli(cleese.Engine.PHASE_VOCODER, inputFile, tomlConfig, timeVec=givenTimeVec)

# example 6: deform a single image
# img = cleese.process_file(cleese.engines.Mediapipe, imgFile, mediapipeConfig)
# cv2.imshow("Cleese v2", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# k = cv2.waitKey(0)

# example 7: Generate randomly deformed images
#cleese.generate_stimuli(cleese.engines.Mediapipe, imgFile, mediapipeConfig)

# example 8: Apply existing .dfm
dfm = cleese.engines.Mediapipe.load_dfm(dfmFile)
img = cleese.process_file(cleese.engines.Mediapipe,
                          imgFile,
                          mediapipeConfig,
                          dfm=dfm)
cv2.imshow("Cleese v2", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
k = cv2.waitKey(0)
