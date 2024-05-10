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

from ...third_party.yin import compute_yin


def load_file(file_name):

    sampleRate, wave = scipy.io.wavfile.read(file_name)
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
    scipy.io.wavfile.write(file_name, sr, wave_out_format)

def extract_pitch(x, sr, win=.02, bounds=[70,400], interpolate=True):
    """
    Extract pitch from x waveform with the YIN algorithm
    """
    
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
    
    return times, pitch

def interpolate_pitch(x, start_value, end_value): 
    """
    Interpolate zeros in pitch series. Method = spline (order-3 polynomial), linear or none. 
    Provide start_value, end_value to fix bounds. 
    """
    xp=np.where(np.invert(list(map(math.isnan, x))))[0]
    fp=np.array(x)[np.where(np.invert(list(map(math.isnan, x))))]
    return np.interp(x=range(len(x)), xp=xp,fp=fp)

def lpc_env(x, sr, order=6):
    """
    Compute spectral enveloppe with linear prediction coefficient (LPC) algorithm. 
    order is the number of poles (rule of thumb: 6 poles to extract 3 formants)
    """
    
    n_samples=len(x)

    #compute Mth-order autocorrelation function
    rx=[]
    for i in range(order+1):
        rx.append(x[:n_samples-i].dot(x[i:n_samples]))

    #construct Toeplitz matrix
    rx = np.array(rx)
    
    #solve toeplitz matrix
    a_coeffs = scipy.linalg.solve_toeplitz((-rx[0:order],-rx[0:order]),rx[1:order+1])

    #get complete polynomial A(z)
    a_lp = np.insert(a_coeffs,0,1)
    
    #get curve
    freqs, env = scipy.signal.freqz(1, a_lp, fs=sr)
    env_db = 20*np.log10(abs(env))
    
    return freqs, env_db

def extract_spectral_env(x, sr, lpc_order=50, pe_thresh=1000, freq_limit = 20000):
    """
    Extract spectral envelope from waveform x using LPC algorithm
    Plot as plot(freqs,env_db)
    """
    # pre-emphasis filter s[n] = s[n] - a*s[n-1]
    a = np.exp(-2*np.pi*pe_thresh/sr)
    x_pe = scipy.signal.lfilter([1, -a], [1], x)
    
    # resample at 2*freq_limit
    new_sr = 2*freq_limit 
    new_n = round(len(x_pe) * new_sr / sr)
    x_rs = scipy.signal.resample(x_pe, new_n)
    
    # normalize
    x_rs = x_rs/max(abs(x_rs))
        
    # extract LPC envelope
    freqs, env_db = lpc_env(x_rs,new_sr,lpc_order)
    
    return freqs, env_db