#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Breakpoint function (BPF) creation and utility functions.
'''

import numpy as np


def createBPF(tr, config, BPFtime, numPoints, endOnTrans, eqFreqVec=None):

    # for pitch, stretch and gain, BPFval is a vector
    if tr in ["pitch", "stretch", "gain"]:

        BPFval = createBPFamplVec(config[tr], numPoints, endOnTrans)

        if tr == "stretch":
            BPFval += 1
            BPFval[BPFval <= 0] = 1
        elif tr == "gain":
            BPFval = 10**(BPFval/10.0)

        BPF = np.column_stack((BPFtime, BPFval))

    # for EQ, BPFval is a matrix
    elif tr == "eq":

        numBands = config["eq"]["band"]["count"] + 1

        BPFval = np.zeros((numBands, len(BPFtime)))
        for i in range(0, numBands):
            BPFval[i, :] = createBPFamplVec(config["eq"], numPoints, 0)

        # line format of an EQ BPF: time numBands freq1 ampl1 freq2 ampl2 ...
        BPF = np.zeros((len(BPFtime), (config["eq"]["band"]["count"]+1)*2 + 2))
        for i in range(0, len(BPFtime)):
            BPF[i, 0] = BPFtime[i]
            BPF[i, 1] = config["eq"]["band"]["count"]
            BPF[i, 2::2] = eqFreqVec
            BPF[i, 3::2] = BPFval[:, i]

    return BPF


def createBPFtimeVec(duration, local_pars, timeVec=None):

    BPFtime = np.array([0])
    numPoints = 1
    endOnTrans = 0

    if timeVec is not None:
        numWin = len(timeVec)
    elif local_pars["window"]["unit"] == 'n':
        if local_pars["window"]["count"] == 0:
            return BPFtime, numPoints, endOnTrans
        numWin = local_pars["window"]["count"]
    elif local_pars["window"]["unit"] == 's':
        if local_pars["window"]["len"] == 0:
            return BPFtime, numPoints, endOnTrans
        numWin = np.floor(duration/local_pars["window"]["len"]) + 1

    if numWin == 1:
        return BPFtime, numPoints, endOnTrans

    if timeVec is not None:
        BPFtime = timeVec
        if timeVec[0] != 0:
            BPFtime = np.insert(BPFtime, 0, 0.)
            numWin += 1
        BPFtime = np.append(BPFtime, duration)
    elif local_pars["window"]["unit"] == 'n':
        BPFtime = np.linspace(0, duration, numWin+1)
    elif local_pars["window"]["unit"] == 's':
        BPFtime = local_pars["window"]["len"]*np.arange(0, numWin)
        BPFtime = np.append(BPFtime, duration)

    if local_pars['BPFtype'] == 'ramp':
        numPoints = numWin + 1
    elif local_pars['BPFtype'] == 'square':
        BPFtime = np.sort(np.concatenate((
            BPFtime[1:-1]-local_pars['trTime']/2,
            BPFtime[1:-1]+local_pars['trTime']/2)))
        if BPFtime[-1] > duration:
            BPFtime = np.delete(temp, -1)
            endOnTrans = 1
        BPFtime = np.append(BPFtime, duration)
        BPFtime = np.insert(BPFtime, 0, 0.)
        numPoints = numWin

    return BPFtime, numPoints, endOnTrans


def createBPFamplVec(local_pars, numPoints, endOnTrans):

    # random BPF values
    BPFval = np.random.normal(0, local_pars['std'], int(numPoints))

    # eliminate far samples (trunc factor)
    # and replace them by new random values
    for i in range(0, len(BPFval)):
        while np.abs(BPFval[i]) > (local_pars['std'] * local_pars['trunc']):
            BPFval[i] = np.random.normal(0, local_pars['std'], 1)

    if numPoints == 1:
        return BPFval

    if local_pars['BPFtype'] == 'square':
        temp = np.array([])
        for i in range(0, len(BPFval)):
            temp = np.append(temp, [BPFval[i], BPFval[i]])
        if endOnTrans:
            temp = np.delete(temp, -1)
        BPFval = temp

    return(BPFval)


def createBPFfreqs(config):

    sr = config["main"]["sr"]
    band_count = config["eq"]["band"]["count"]

    if config["eq"]["scale"] == "linear":
        eqFreqVec = np.linspace(0., sr/float(2), band_count+1)
    elif config["eq"]["scale"] == "mel":
        minMel = 0
        maxMel = freq2mel(sr/float(2))
        melPerBin = (maxMel-minMel)/(band_count)
        eqFreqVec = melPerBin*np.ones(band_count)
        eqFreqVec = np.insert(eqFreqVec, 0, minMel)
        Vmel2freq = np.vectorize(mel2freq)
        eqFreqVec = Vmel2freq(np.cumsum(eqFreqVec))

    return eqFreqVec


def freq2mel(freq):
    return 1127.01048*np.log(1.+freq/700.)


def mel2freq(mel):
    return 700.0*(np.exp(mel/1127.01048)-1.0)
