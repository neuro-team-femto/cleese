#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Usage examples.
'''

from PIL import Image
import numpy as np

import cleese_stim as cleese

sound_file = './sounds/female_anniversaire_isochrone.wav'
img_file = './pics/monalisa.jpg'
dfm_file = './dfm/default.dfm'
dfmxy_file = './dfm/monalisa.random.dfmxy'
landmarks_file = './dfm/monalisa.landmarks.txt'
phase_vocoder_config = './configs/random_pitch_profile.toml'
mediapipe_config = './configs/cleese-mediapipe.toml'

# example 1: run with random BPFs
#cleese.generate_stimuli(cleese.engines.PhaseVocoder, sound_file, phase_vocoder_config)

# # example 2: run with given BPF
#given_BPF = np.array([[0., 0.], [1.5, 500.], [3., -500.]])
#cleese.generate_stimuli(cleese.engines.PhaseVocoder,
#                         sound_file,
#                         phase_vocoder_config,
#                         BPF=given_BPF)

# # example 3: run with given scalar factor
# FIXME Overly slow and RAM consuming
#given_BPF = 200
#cleese.generate_stimuli(cleese.engines.PhaseVocoder,
#                         sound_file,
#                         phase_vocoder_config,
#                         BPF=given_BPF)

# # example 4: array input and output
#wave_in, sr, __ = cleese.engines.PhaseVocoder.wavRead(sound_file)
#wave_out, BPF_out = cleese.process_data(cleese.engines.PhaseVocoder,
#                                       wave_in,
#                                       phase_vocoder_config,
#                                       sample_rate=sr)

# # example 5: example with given time vector
#given_time_vec = np.array([0.1, 0.15, 0.3])
#cleese.generate_stimuli(cleese.engines.PhaseVocoder,
#                         sound_file,
#                         phase_vocoder_config,
#                         timeVec=given_time_vec)

# example 6: deform a single image
#img = cleese.process_file(cleese.engines.Mediapipe, img_file, mediapipe_config)
#Image.fromarray(img).show()

# example 7: Generate randomly deformed images
#cleese.generate_stimuli(cleese.engines.Mediapipe, img_file, mediapipe_config)

# example 8: Apply existing .dfm
# dfm = cleese.engines.Mediapipe.load_dfm(dfmFile)
# img = cleese.process_file(cleese.engines.Mediapipe,
#                           img_file,
#                           mediapipe_config,
#                           dfm=dfm)
# Image.fromarray(img).show()

# example 9: Apply existing .dfmxy
#dfmxy = cleese.engines.Mediapipe.load_dfmxy(dfmxy_file)
#img = cleese.process_file(cleese.engines.Mediapipe,
#                           img_file,
#                           mediapipe_config,
#                           dfmxy=dfmxy)
#Image.fromarray(img).show()

# example 10: Convert dfmxy to dfm
#cleese.engines.Mediapipe.dfmxy_to_dfm(dfmxy_file,
#                                       landmarks_file,
#                                       output_dfm_file='./output/converted.dfm')
