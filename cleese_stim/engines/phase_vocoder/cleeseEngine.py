#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Spectral processing engine: STFT with time-varying hops, phase-locking phase vocoder and ISTFT with window-by-window resampling.
'''

import numpy as np
import scipy.fftpack as fft
import scipy
import scipy.signal as sig
import scipy.interpolate


def stft(waveForm,win,winSize,hopVec):

    numSamples = waveForm.shape[0]
    numFrames = len(hopVec)

    # security padding
    numExtraSamples = np.sum(hopVec) - numSamples + winSize*2
    waveForm = np.concatenate((waveForm,np.zeros(numExtraSamples)))

    atoms = np.zeros((winSize,numFrames))

    pos = 0
    for i in range(0,numFrames):
        atoms[:,i] = waveForm[pos:pos+winSize]*win
        pos += hopVec[i]

    stft = np.fft.fft(atoms,axis=0)

    return stft

def istft(stft,win,winSize,hopSize):

    numFrames = stft.shape[1]
    numSamples = numFrames*hopSize + winSize

    outWaveform = np.zeros(numSamples) # TODO: stereo

    winSum = np.zeros(numSamples)
    winSq = win * win

    pos = 0
    for i in range(0,numFrames):

        currSpec = stft[:, i].flatten()
        currSpec = np.concatenate((currSpec, currSpec[-2:0:-1].conj()), 0)

        outWaveform[pos:(pos+winSize)] += fft.ifft(currSpec).real * win
        winSum[pos:(pos+winSize)]      += winSq

        pos += hopSize

    # amplitude normalization
    nonZero = winSum > np.finfo(winSum.dtype).tiny
    outWaveform[nonZero] /= winSum[nonZero]

    return outWaveform

def istft_resamp(stft,win,winSize,hopSize,ratesVec,oriLength):

    numFrames = stft.shape[1]
    numSamples = oriLength + 4*winSize

    outWaveform = np.zeros(numSamples)

    winSum = np.zeros(numSamples)
    winSq = win * win

    pos = 0
    for i in range(0,numFrames):

        currSpec = stft[:, i].flatten()
        currSpec = np.concatenate((currSpec, currSpec[-2:0:-1].conj()), 0)
        currAtom = fft.ifft(currSpec).real * win

        n_currLen = int(round(winSize/ratesVec[i]))

        if (pos+n_currLen) > numSamples:
            break

        outWaveform[pos:(pos+n_currLen)] += sig.resample(currAtom,n_currLen)
        winSum[pos:(pos+n_currLen)]      += sig.resample(winSq,n_currLen)

        pos += int(round(hopSize/ratesVec[i]))

    # amplitude normalization
    nonZero = winSum > np.finfo(winSum.dtype).tiny
    outWaveform[nonZero] /= winSum[nonZero]

    return outWaveform


def phaseVocoder_varHop(specIn, anaHopVec, synHop=256, phase_locking=True):

    specOut = np.zeros(specIn.shape,dtype=complex)
    specOut[:,0] = specIn[:,0]

    n_frames = specIn.shape[1]
    halfLen = specIn.shape[0]
    fftLen = (halfLen-1)*2
    omega = 2 * np.pi * np.arange(0,halfLen) / fftLen

    for i in range(1,n_frames):

        currPhase = np.angle(specIn[:,i])
        lastPhase = np.angle(specIn[:,i-1])

        expAdv = omega * anaHopVec[i-1]  # expected phase advance

        deltaPhase = currPhase - lastPhase - expAdv
        deltaPhase = deltaPhase - 2 * np.pi * np.round(deltaPhase/(2*np.pi))  # princarg function

        hopAdv = (omega + deltaPhase/float(anaHopVec[i])) * synHop  # phase advance during synth hop

        lastOutPhase = np.angle(specOut[:,i-1])

        if phase_locking:

            peakIndVec, regStart, regEnd = findPeaks(np.abs(specIn[:,i]))

            theta = np.zeros(len(specOut[:,i]))
            for pk, st, en in zip(peakIndVec, regStart, regEnd):
                theta[st:en+1] = lastOutPhase[pk] + hopAdv[pk] - currPhase[pk]

        else:

            theta = lastOutPhase + hopAdv - currPhase


        specOut[:,i] = np.exp(1j * theta) * specIn[:,i]


    return specOut


def findPeaks(inVec):

    nn = 4 # number of neighbors. must be even

    flagMat = np.zeros((nn,len(inVec)))

    # zero pad
    oriVec = inVec
    inVec = np.append(inVec,np.zeros(nn//2))
    inVec = np.insert(inVec,0,np.zeros(nn//2))

    # find peaks
    startInd = np.arange(0,nn+1)
    startInd = np.delete(startInd,nn//2)
    endInd = np.arange(-nn,1)
    endInd = np.delete(endInd,nn//2)
    endInd[-1] = len(inVec)
    for i,(st,en) in enumerate(zip(startInd,endInd)):
        flagMat[i,:] = inVec[st:en] < inVec[nn//2:-nn//2]
    peakIndVec = np.nonzero(np.prod(flagMat,axis=0))[0]

    if len(peakIndVec) == 0:
        return [],[],[]

    # define influence regions
    regStart = np.zeros(len(peakIndVec),dtype=int)
    regEnd   = np.zeros(len(peakIndVec),dtype=int)

    regStart[0] = 0
    regStart[1:] = np.ceil((peakIndVec[1:] + peakIndVec[0:-1])/2)
    regEnd[0:-1] = regStart[1:] - 1
    regEnd[-1] = len(oriVec)


    return peakIndVec, regStart, regEnd
