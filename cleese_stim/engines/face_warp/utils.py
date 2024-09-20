#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CLEESE toolbox
v1.0: mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS
v2.0: jan 2022, Lara Kermarec <lara.git@kermarec.bzh> for CNRS

Audio utils functions for CLEESE's phase vocoder engine
'''

import scipy
import numpy as np
import math

def generate_gif(base_file, dfm_file, gains):

    #dfm = FaceWarp.load_dfm(dfm_file)

    #for index,gain in enumerate(gain_series):
    #    deformed = cleese.process_file(FaceWarp,
    #                                base_frame,
    #                                config_file,
    #                                dfm=dfm)
    #FaceWarp.img_write(deformed, "./pics/monalisa_transformed_4.jpg")

