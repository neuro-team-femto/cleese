#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Main functions for CLEESE
'''

import os
import numpy as np
import scipy.io.wavfile as wav
import time
import shutil

from cleese.cleeseBPF import *
from cleese.cleeseEngine import *


def generate_stimuli(soundData, config, BPF=None, sample_rate=None,
                     sample_format=None,
                     timeVec=None):
    if "main" not in config or "numFiles" not in config["main"]:
        print("Missing `main.numFiles` variable from config")
        return

    process(soundData, config, BPF=BPF, sample_rate=sample_rate,
            sample_format=sample_format, timeVec=timeVec,
            file_output=True)


def process(soundData, config, BPF=None, sample_rate=None,
            sample_format=None, timeVec=None,
            file_output=False):

    data = {}
    exec(open("./cleeseConfig_all.py").read(), data)
    pars = data['pars']

    doCreateBPF = False
    if BPF is None:
        doCreateBPF = True

    if not sample_rate:
        print("Error: missing sample rate")
        return

    if file_output:
        if not sample_rate or not sample_format:
            print("Error: missing sample format")
            return

    sr = sample_rate
    sampleFormat = sample_format

    waveIn = soundData
    numFiles = 1

    if len(waveIn.shape) == 2:
        print('Warning: stereo file detected. Reading only left channel.')
        waveIn = np.ravel(waveIn[:, 0])

    pars['main_pars']['inSamples'] = len(waveIn)
    pars['main_pars']['sr'] = sr

    if doCreateBPF and file_output:

        numFiles = pars['main_pars']['numFiles']

    else:

        numFiles = 1
        if np.isscalar(BPF):
            BPF = np.array([[0., float(BPF)]])

    currOutFile = []
    for t in range(0,len(pars['main_pars']['transf'])):

        tr = pars['main_pars']['transf'][t]

        if pars['main_pars']['chain']:
            if t==0:
                currTrString = tr
            else:
                currTrString = currTrString+'_'+tr
        else:
            currTrString = tr

        if doCreateBPF:

            if file_output:
                pars['main_pars']['currOutPath'] = os.path.join(config['main']['expBaseDir'], currTrString)

            # create BPF time vector
            duration = pars['main_pars']['inSamples']/float(sr)
            BPFtime, numPoints, endOnTrans = createBPFtimeVec(duration,pars[tr+'_pars'],timeVec=timeVec)

        else:
            pars['main_pars']['currOutPath'] = pars['main_pars']['outPath']

        # create output folder
        if file_output:
            if not os.path.exists(pars['main_pars']['currOutPath']):
                os.makedirs(pars['main_pars']['currOutPath'])
            path, inFileNoExt = os.path.split(config["main"]["filename"])
            inFileNoExt = os.path.splitext(inFileNoExt)[0]

        # create frequency bands for random EQ
        eqFreqVec = None
        if tr == 'eq':
            eqFreqVec = createBPFfreqs(pars)

        for i in range(0,numFiles):

            print(currTrString+' variation '+str(i+1)+'/'+str(numFiles))
            currFileNo = "%04u" % (i+1)

            if pars['main_pars']['chain'] and t>0:
                if file_output:
                    waveIn,sr,sampleFormat = wavRead(currOutFile[i])
                else:
                    waveIn = waveOut
                pars['main_pars']['inSamples'] = len(waveIn)
                pars['main_pars']['sr'] = sr
                BPFtime, numPoints, endOnTrans = createBPFtimeVec(duration,pars[tr+'_pars'],timeVec=timeVec)

            # generate random BPF
            if doCreateBPF:
                BPF = createBPF(tr,pars,BPFtime,numPoints,endOnTrans,eqFreqVec)

            # export BPF as text file
            if file_output:
                currBPFfile = os.path.join(pars['main_pars']['currOutPath'],inFileNoExt+'.'+currFileNo+'.'+currTrString+'_BPF.txt')
                np.savetxt(currBPFfile,BPF,'%.8f')

                if t==0:
                    currOutFile.append(os.path.join(pars['main_pars']['currOutPath'],inFileNoExt+'.'+currFileNo+'.'+currTrString+'.wav'))
                else:
                    currOutFile[i] = os.path.join(pars['main_pars']['currOutPath'],inFileNoExt+'.'+currFileNo+'.'+currTrString+'.wav')

            if tr in ['stretch','pitch']:

                if tr == 'stretch':
                    doPitchShift = False
                elif tr == 'pitch':
                    doPitchShift = True

                # call processing with phase vocoder
                waveOut = processWithPV(waveIn=waveIn, pars=pars, BPF=BPF, doPitchShift=doPitchShift)

                # remove trailing zero-pad
                if tr == 'pitch':
                    waveOut = np.delete(waveOut, range(pars['main_pars']['inSamples'],len(waveOut)))

            elif tr == 'eq':

                waveOut = processWithSTFT(waveIn=waveIn, pars=pars, BPF=BPF)

                # remove trailing zero-pad
                waveOut = np.delete(waveOut, range(pars['main_pars']['inSamples'],len(waveOut)))

            elif tr == 'gain':

                if numPoints == 1:
                    waveOut = waveIn * BPF[:,1]
                else:
                    gainVec = np.interp(np.linspace(0,duration,pars['main_pars']['inSamples']),BPF[:,0],BPF[:,1])
                    waveOut = waveIn * gainVec

            if file_output:
                # normalize
                if np.max(np.abs(waveOut)) >= 1.0:
                    waveOut = waveOut/np.max(np.abs(waveOut))*0.999
                wavWrite(waveOut,fileName=currOutFile[i],sr=sr,sampleFormat=sampleFormat)

    if not file_output:
        return waveOut,BPF


def load_file(fileName):

    sampleRate, wave = wav.read(fileName)

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


def wavRead(filename):
    wave, attr = load_file(filename)
    return wave, attr["sample_rate"], attr["sample_format"]


def wavWrite(waveOut, fileName, sr, sampleFormat='int16'):

    if sampleFormat == 'int16':
        waveOutFormat = waveOut * 2**15
    elif sampleFormat == 'int32':
        waveOutFormat = waveOut * 2**31
    else:
        waveOutFormat = waveOut
    waveOutFormat = waveOutFormat.astype(sampleFormat)
    wav.write(fileName, sr, waveOutFormat)


def processWithSTFT(waveIn, pars, BPF):

    sr = pars['main_pars']['sr']
    inSamples = pars['main_pars']['inSamples']

    winLen = pars['ana_pars']['anaWinLen']        # in seconds
    n_fft = int(2**np.ceil(np.log2(winLen*sr)))   # next pow 2
    overlapFactor = pars['ana_pars']['oversampling']
    synHop = n_fft//overlapFactor

    win = np.hamming(n_fft)

    numFrames = int(round(inSamples/synHop)) + overlapFactor
    anaHopVec = np.ones(numFrames, dtype=int) * synHop

    stftMat = stft(waveIn,win,n_fft,anaHopVec)
    stftMat = np.squeeze(stftMat)
    stftMat = stftMat[0:n_fft//2+1,:]

    # interpolate BPF matrix to generate filter mask
    numSeg = BPF.shape[0]
    numBands = (BPF.shape[1]-2)//2

    freqMat = BPF[:,2::2]
    amplMat = BPF[:,3::2]
    timeVec = BPF[:,0]

    # interpolate in frequency
    interpBPF = np.zeros((n_fft//2+1,numSeg))
    for i in range(0,numSeg):
        currBinVec = freqMat[i,:]/sr*2 * (n_fft//2+1)
        interpBPF[:,i] = np.interp(np.arange(0,n_fft//2+1),currBinVec,amplMat[i,:])  # piecewise-linear spectral envelope

    # interpolate in time
    filterMat = np.zeros(stftMat.shape)
    if numSeg == 1:
        filterMat = np.tile(interpBPF,(1,stftMat.shape[1]))
    else:
        frameVec = timeVec*sr/synHop
        for i in range(0,n_fft//2+1):
            filterMat[i,:] = np.interp(np.arange(0,numFrames),frameVec,interpBPF[i,:])

    stftMat *= filterMat

    waveOut = istft(stftMat,win,n_fft,synHop)

    return waveOut

def processWithPV(waveIn, pars, BPF, doPitchShift=False):

    sr = pars['main_pars']['sr']
    inSamples = pars['main_pars']['inSamples']

    if doPitchShift == False:

        # static stretch
        if BPF.size == 2:
            rateVec = 1/BPF[0,1]   # >1: dilation (stretching), <1: compression
            numSeg = 1
        else:
            sampleVec = np.rint(BPF[:,0]*sr)   # in samples
            rateVec = BPF[:,1]
            numSeg = BPF.shape[0]

    else:

        bins_per_octave = 12

        # static pitch shift
        if BPF.size == 2:
            rateVec = 2.0 ** (-float(BPF[0,1]/100.0) / bins_per_octave)  # in libRosa, pitch shifting factors are in semitones. In CLEESE, in cents.
            numSeg = 1
        else:
            sampleVec = np.rint(BPF[:,0]*sr)   # in samples
            rateVec = 2.0 ** (BPF[:,1] / float(100*bins_per_octave))

            numSeg = BPF.shape[0]


    winLen = pars['ana_pars']['anaWinLen']        # in seconds
    n_fft = int(2**np.ceil(np.log2(winLen*sr)))   # next pow 2
    overlapFactor = pars['ana_pars']['oversampling']
    synHop = n_fft//overlapFactor


    if numSeg==1:

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
            sampledBPF = np.interp(pos,sampleVec,rateVec)
            currHop = int(round(synHop/sampledBPF))
            anaHopVec = np.append(anaHopVec,currHop)
            allRatesVec = np.append(allRatesVec,sampledBPF)

    win = np.hamming(n_fft)

    stftMat = stft(waveIn,win,n_fft,anaHopVec)

    stftMat = np.squeeze(stftMat)
    stftMat = stftMat[0:n_fft//2+1,:]

    phase_locking = 1

    stft_stretch = phaseVocoder_varHop(stftMat, anaHopVec=anaHopVec, synHop=synHop, phase_locking=phase_locking)

    if doPitchShift==0:

        waveOut = istft(stft_stretch,win,n_fft,synHop)

    else:
        if numSeg==1:

            waveOut = istft(stft_stretch,win,n_fft,synHop)
            n_samples = int(np.ceil(len(waveOut) * rateVec))
            waveOut = sig.resample_poly(waveOut,n_samples,len(waveOut))

        else:

            waveOut = istft_resamp(stft_stretch,win,n_fft,synHop,allRatesVec,inSamples)

    return waveOut
