#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Usage examples.
'''

import cleese

inputFile = './example.wav'
configFile = './cleeseConfig_all.py'

# example 1: run with random BPFs
cleese.process(soundData=inputFile, configFile=configFile)

# # example 2: run with given BPF
# import numpy as np
# givenBPF = np.array([[0.,0.],[3.,500.]])
# cleese.process(soundData=inputFile, configFile=configFile, BPF=givenBPF)

# # example 3: run with given scalar factor
# givenBPF = 200
# cleese.process(soundData=inputFile, configFile=configFile, BPF=givenBPF)

# # example 4: array input and output
# waveIn,sr = cleese.wavRead(inputFile)
# waveOut,BPFout = cleese.process(soundData=waveIn, configFile=configFile, sr=sr)

# # example 5: example with given time vector
# import numpy as np
# givenTimeVec = np.array([0.1,0.15,0.3])
# cleese.process(soundData=inputFile, configFile=configFile, timeVec=givenTimeVec)
