#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CLEESE toolbox
v1.0: mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS
v2.0: jan 2022, Lara Kermarec <lara.git@kermarec.bzh> for CNRS

Main functions for CLEESE's phase vocoder engine
'''

import os
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import time
import shutil

from .bpf import (
        createBPFtimeVec,
        createBPFfreqs,
        createBPF,
        create_BPF_header)
from .audio_engine import (
        stft,
        istft,
        istft_resamp,
        phaseVocoder_varHop,)
from ..engine import Engine
from ...cleese import log, load_config

from .utils import load_file, wav_read, wav_write, extract_pitch, extract_spectral_env, extract_rms


class PhaseVocoder(Engine):

    @staticmethod
    def generate_stimuli(soundData, config, BPF=None, sample_rate=None,
                         sample_format=None,
                         timeVec=None):
        PhaseVocoder.process(
                soundData, config, BPF=BPF, sample_rate=sample_rate,
                sample_format=sample_format, timeVec=timeVec,
                file_output=True)

    @staticmethod
    def process(soundData, config, BPF=None, sample_rate=None,
                sample_format=None, timeVec=None,
                file_output=False):

        doCreateBPF = False
        if BPF is None:
            doCreateBPF = True

        try:
            BPF_EXT = config["main"]["param_ext"]
        except KeyError as e:
            BPF_EXT = '.txt' # default bpf extension
  

        if not sample_rate:
            log("ERROR: missing sample rate")
            return

        if file_output:
            if not sample_rate or not sample_format:
                log("ERROR: missing sample format")
                return

        sr = sample_rate
        sampleFormat = sample_format

        waveIn = soundData
        numFiles = 1

        if len(waveIn.shape) == 2:
            log('WARN: stereo file detected. Reading only left channel.')
            waveIn = np.ravel(waveIn[:, 0])

        config["main"]['inSamples'] = len(waveIn)
        config["main"]['sr'] = sr

        if doCreateBPF and file_output:

            numFiles = config["main"]['numFiles']

        else:

            numFiles = 1
            if np.isscalar(BPF):
                BPF = np.array([[0., float(BPF)]])

        currOutFile = []
        for t in range(0, len(config["main"]['transf'])):

            tr = config["main"]['transf'][t]

            if config["main"]['chain']:
                if t == 0:
                    currTrString = tr
                else:
                    currTrString = currTrString+'_'+tr
            else:
                currTrString = tr

            if doCreateBPF:

                if file_output:
                    config["main"]['currOutPath'] = os.path.join(config['main']['expBaseDir'], currTrString)

                # create BPF time vector
                duration = config["main"]['inSamples']/float(sr)
                BPFtime, numPoints, endOnTrans = createBPFtimeVec(
                        duration, config[tr], timeVec=timeVec)

            else:
                config["main"]['currOutPath'] = config["main"]['outPath']
                duration = config["main"]['inSamples']/float(sr)
                numPoints = BPF.shape[0]

            # create output folder
            if file_output:
                if not os.path.exists(config["main"]['currOutPath']):
                    os.makedirs(config["main"]['currOutPath'])
                path, inFileNoExt = os.path.split(config["main"]["filename"])
                inFileNoExt = os.path.splitext(inFileNoExt)[0]

            # create frequency bands for random EQ
            eqFreqVec = None
            if tr == 'eq':
                eqFreqVec = createBPFfreqs(config)

            for i in range(0, numFiles):

                log(currTrString+' variation '+str(i+1)+'/'+str(numFiles))
                currFileNo = "%08u" % (i+1)

                if config["main"]['chain'] and t > 0:
                    if file_output:
                        waveIn, sr, sampleFormat = PhaseVocoder.wav_read(
                                currOutFile[i])
                    else:
                        waveIn = waveOut
                    config["main"]['inSamples'] = len(waveIn)
                    config["main"]['sr'] = sr
                    duration = len(waveIn) / float(sr)
                    BPFtime, numPoints, endOnTrans = createBPFtimeVec(
                            duration, config[tr], timeVec=timeVec)

                # generate random BPF
                if doCreateBPF:
                    BPF = createBPF(tr, config, BPFtime, numPoints,
                                    endOnTrans, eqFreqVec)

                # export BPF as text file
                if file_output:
                    currBPFfile = os.path.join(
                            config["main"]['currOutPath'],
                            inFileNoExt+'.'+currFileNo+'.'+currTrString+BPF_EXT)
                    BPF_header = create_BPF_header(tr, config)

                    np.savetxt(currBPFfile, BPF, '%.8f', delimiter = ',', header = BPF_header, comments='')

                    if t == 0:
                        currOutFile.append(os.path.join(
                                config["main"]['currOutPath'],
                                inFileNoExt+'.'+currFileNo+'.'+currTrString+'.wav'))
                    else:
                        currOutFile[i] = os.path.join(
                                config["main"]['currOutPath'],
                                inFileNoExt+'.'+currFileNo+'.'+currTrString+'.wav')

                if tr in ['stretch', 'pitch']:

                    if tr == 'stretch':
                        doPitchShift = False
                    elif tr == 'pitch':
                        doPitchShift = True

                    # call processing with phase vocoder
                    waveOut = processWithPV(waveIn=waveIn,
                                            config=config,
                                            BPF=BPF,
                                            doPitchShift=doPitchShift)

                    # remove trailing zero-pad
                    if tr == 'pitch':
                        waveOut = np.delete(
                                waveOut,
                                range(
                                    config["main"]['inSamples'],
                                    len(waveOut)))

                elif tr == 'eq':

                    waveOut = processWithSTFT(
                            waveIn=waveIn, config=config, BPF=BPF)

                    # remove trailing zero-pad
                    waveOut = np.delete(
                            waveOut,
                            range(config["main"]['inSamples'], len(waveOut)))

                elif tr == 'gain':

                    if numPoints == 1:
                        waveOut = waveIn * BPF[:, 1]
                    else:
                        gainVec = np.interp(np.linspace(
                                0, duration, config["main"]['inSamples']),
                                BPF[:, 0], BPF[:, 1])
                        waveOut = waveIn * gainVec

                # if gain > 1.0, normalize to avoid clipping
                if np.max(np.abs(waveOut)) >= 1.0:
                    waveOut = waveOut/np.max(np.abs(waveOut))*0.999
                
                if file_output:            
                    PhaseVocoder.wav_write(waveOut, file_name=currOutFile[i],
                                          sr=sr, sample_format=sampleFormat)

        if not file_output:
            return waveOut, BPF

    @staticmethod
    def name():
        return "phase_vocoder"

    @staticmethod
    def load_file(file_name): 
        return load_file(file_name)

    @staticmethod
    def wav_read(file_name):
        return wav_read(file_name)

    @staticmethod
    def wav_write(wave_out, file_name, sr, sample_format='int16'):
        return wav_write(wave_out, file_name, sr, sample_format)

    @staticmethod
    def extract_pitch(x, sr, win=.02, bounds=[70,400], harmo_thresh=0.1, interpolate=True):
       return extract_pitch(x, sr, win, bounds=bounds, harmo_thresh = harmo_thresh, interpolate = interpolate)

    @staticmethod
    def extract_spectral_env(x, sr, lpc_order=50, pe_thresh=1000, freq_limit = 20000):
        return extract_spectral_env(x, sr, lpc_order, pe_thresh, freq_limit)

    @staticmethod
    def extract_rms(x,sr,win, thresh=0.02, interpolate=True):
        return extract_rms(x,sr,win, thresh, interpolate)

    @staticmethod
    def create_BPF(trans, config_file, time_points, num_points, end_on_transition, eq_freqs=None):
        config = load_config(config_file)
        if config is None:
            return
        return createBPF(trans, config, time_points, num_points, end_on_transition, eq_freqs)


def processWithSTFT(waveIn, config, BPF):

    sr = config["main"]['sr']
    inSamples = config["main"]['inSamples']

    winLen = config["analysis"]["window"]["len"]        # in seconds
    n_fft = int(2**np.ceil(np.log2(winLen*sr)))   # next pow 2
    overlapFactor = config["analysis"]["oversampling"]
    synHop = n_fft//overlapFactor

    win = np.hamming(n_fft)

    numFrames = int(round(inSamples/synHop)) + overlapFactor
    anaHopVec = np.ones(numFrames, dtype=int) * synHop

    stftMat = stft(waveIn, win, n_fft, anaHopVec)
    stftMat = np.squeeze(stftMat)
    stftMat = stftMat[0:n_fft//2+1, :]

    # interpolate BPF matrix to generate filter mask
    numSeg = BPF.shape[0]
    numBands = (BPF.shape[1]-2)//2

    freqMat = BPF[:, 2::2]
    amplMat = BPF[:, 3::2]
    timeVec = BPF[:, 0]

    # interpolate in frequency
    interpBPF = np.zeros((n_fft//2+1, numSeg))
    for i in range(0, numSeg):
        currBinVec = freqMat[i, :]/sr*2 * (n_fft//2+1)
        # piecewise-linear spectral envelope
        interpBPF[:, i] = np.interp(np.arange(0, n_fft//2+1),
                                    currBinVec, amplMat[i, :],
                                    left=0, right=0)

    # interpolate in time
    filterMat = np.zeros(stftMat.shape)
    if numSeg == 1:
        filterMat = np.tile(interpBPF, (1, stftMat.shape[1]))
    else:
        frameVec = timeVec*sr/synHop
        for i in range(0, n_fft//2+1):
            filterMat[i, :] = np.interp(np.arange(0, numFrames),
                                        frameVec, interpBPF[i, :])

    stftMat *= np.power(10,filterMat/20)

    waveOut = istft(stftMat, win, n_fft, synHop)

    return waveOut


def processWithPV(waveIn, config, BPF, doPitchShift=False):

    sr = config["main"]["sr"]
    inSamples = config["main"]["inSamples"]

    if not doPitchShift:

        # static stretch
        if BPF.size == 2:
            rateVec = 1/BPF[0, 1]  # >1: dilation (stretching), <1: compression
            numSeg = 1
        else:
            sampleVec = np.rint(BPF[:, 0]*sr)   # in samples
            rateVec = BPF[:, 1]
            numSeg = BPF.shape[0]

    else:

        bins_per_octave = 12

        # static pitch shift
        if BPF.size == 2:
            # in libRosa, pitch shifting factors are in semitones.
            # In CLEESE, in cents.
            rateVec = 2.0 ** (-float(BPF[0, 1]/100.0) / bins_per_octave)
            numSeg = 1
        else:
            sampleVec = np.rint(BPF[:, 0]*sr)   # in samples
            rateVec = 2.0 ** (BPF[:, 1] / float(100*bins_per_octave))

            numSeg = BPF.shape[0]

    winLen = config["analysis"]["window"]["len"]  # in seconds
    n_fft = int(2**np.ceil(np.log2(winLen*sr)))   # next pow 2
    overlapFactor = config["analysis"]["oversampling"]
    synHop = n_fft//overlapFactor

    if numSeg == 1:

        anaHop = int(round(synHop*rateVec))
        numFrames = int(round(inSamples/anaHop)) + overlapFactor
        anaHopVec = np.ones(numFrames, dtype=int) * anaHop

    else:

        pos = 0
        currHop = int(round(synHop/rateVec[0]))
        anaHopVec = currHop
        allRatesVec = rateVec[0]

        while pos <= inSamples:
            pos += currHop
            sampledBPF = np.interp(pos, sampleVec, rateVec)
            currHop = int(round(synHop/sampledBPF))
            anaHopVec = np.append(anaHopVec, currHop)
            allRatesVec = np.append(allRatesVec, sampledBPF)

    win = np.hamming(n_fft)

    stftMat = stft(waveIn, win, n_fft, anaHopVec)

    stftMat = np.squeeze(stftMat)
    stftMat = stftMat[0:n_fft//2+1, :]

    phase_locking = 1

    stft_stretch = phaseVocoder_varHop(stftMat,
                                       anaHopVec=anaHopVec,
                                       synHop=synHop,
                                       phase_locking=phase_locking)

    if doPitchShift == 0:

        waveOut = istft(stft_stretch, win, n_fft, synHop)

    else:
        if numSeg == 1:

            waveOut = istft(stft_stretch, win, n_fft, synHop)
            n_samples = int(np.ceil(len(waveOut) * rateVec))
            waveOut = sig.resample_poly(waveOut, n_samples, len(waveOut))

        else:

            waveOut = istft_resamp(stft_stretch, win, n_fft,
                                   synHop, allRatesVec, inSamples)

    return waveOut
