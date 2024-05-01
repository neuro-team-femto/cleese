#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CLEESE toolbox
v1.0: mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS
v2.0: jan 2022, Lara Kermarec <lara.git@kermarec.bzh> for CNRS

Audio utils functions for CLEESE's phase vocoder engine
'''

import scipy.io.wavfile as wav
import numpy as np
import math

from ...third_party.yin import compute_yin


def load_file(file_name):

    sampleRate, wave = wav.read(file_name)
    sampleFormat = wave.dtype
    if sampleFormat in ('int16', 'int32'):
        # convert to float
        if sampleFormat == 'int16':
            n_bits = 16
        elif sampleFormat == 'int32':
            n_bits = 32
        wave = wave/(float(2**(n_bits - 1)))
        wave = wave.astype('float32')

    attributes = {
        "sample_rate": sampleRate,
        "sample_format": sampleFormat,
    }
    return wave, attributes

def wav_read(file_name):
    wave, attr = load_file(file_name)
    return wave, attr["sample_rate"], attr["sample_format"]

def wav_write(wave_out, file_name, sr, sample_format='int16'):

    if sample_format == 'int16':
        wave_out_format = wave_out * 2**15
    elif sample_format == 'int32':
        wave_out_format = wave_out * 2**31
    else:
        wave_out_format = wave_out
    wave_out_format = wave_out_format.astype(sample_format)
    wav.write(file_name, sr, wave_out_format)

def extract_pitch(x, sr, win=.02, bounds=[70,400], interpolate=True):
    
    # extract raw pitch with yin
    hop_size = int(np.floor(sr * win))
    min_f0, max_f0 = bounds
    # YIN assumes the analysis window is longer than the min_f0 period 
    if hop_size < int(sr / min_f0): 
        hop_size = int(sr / min_f0) + 1
    pitch, harmonic_rates, argmins, times = compute_yin(x, sr, 
        dataFileName=None, w_len=hop_size, w_step=hop_size, f0_min=min_f0, f0_max=max_f0, harmo_thresh=0.1)
    
    # third-party yin returns lists; convert to nparray
    pitch = np.array(pitch)
    times = np.array(times)

    # clean up unvoiced areas
    # flag unvoiced as nan
    pitch[np.where(pitch == 0)[0]] = np.nan
    # trim beginning and end nans
    notnans = np.flatnonzero(~np.isnan(pitch))
    if notnans.size:
        pitch = pitch[notnans[0]: notnans[-1]+1]
        times = times[notnans[0]: notnans[-1]+1]
    else: 
        pitch = times = []
    
    if(interpolate):  # interpolate nans
        start_value = end_value = np.mean(pitch[np.nonzero(~np.isnan(pitch))])
        pitch = interpolate_pitch(pitch, start_value = start_value, end_value = end_value)
    
    return pitch, times

def interpolate_pitch(x, start_value, end_value): 
    """Interpolate zeros in pitch series. Method = spline (order-3 polynomial), linear or none. 
    Provide start_value, end_value to fix bounds. 
    """
    xp=np.where(np.invert(list(map(math.isnan, x))))[0]
    fp=np.array(x)[np.where(np.invert(list(map(math.isnan, x))))]
    return np.interp(x=range(len(x)), xp=xp,fp=fp)



