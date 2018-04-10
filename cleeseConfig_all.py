#!/usr/bin/env python
'''
CLEESE toolbox v1.0
mar 2018, J.J. Burred <jjburred@jjburred.com> for IRCAM/CNRS

Example configuration script.
'''

# main parameters
main_pars = {
    'outPath': './CLEESE_output_data/',   # output root folder
    'numFiles': 10,     # number of output files to generate (for random modifications)
    'chain': True,
    'transf': ['stretch','pitch','eq','gain']   # modifications to apply
    # 'transf': ['pitch']
}

# global analysis parameters
ana_pars = {
    'anaWinLen':   0.04,    # analysis window length in s (not to be confused with the BPF processing window lengths)
    'oversampling':   8,    # number of hops per analysis window
}

# parameters for random pitch countours
pitch_pars = {
    'winLen': 0.11,    # pitch transposition window in seconds. If 0 : static transformation
    'numWin': 6,       # number of pitch transposition windows. If 0 : static transformation
    'winUnit': 'n',    # 's': force winlength in seconds,'n': force number of windows (equal length)
    'std': 300,        # standard deviation (cents) for random transposisiton (Gaussian distrib for now)
    'trunc': 1,        # truncate distribution values (factor of std)
    'BPFtype': 'ramp', # type of breakpoint function:
                       #      'ramp': linear interpolation between breakpoints
                       #      'square': square BPF, with specified transition times at edges
    'trTime': 0.02  # in s: transition time for square BPF
}

# parameters for random time stretching
stretch_pars = {
    'winLen': 0.1,
    'numWin': 5,
    'winUnit': 'n',
    'std': 1.5,        # stretching factor. >1: expansion, <1: compression
    'trunc': 1,
    'BPFtype': 'ramp',
    'trTime': 0.05
}

# parameters for random EQ
eq_pars = {
    'winLen': 0.1,
    'numWin': 5,
    'winUnit': 'n',
    'std': 5,
    'trunc': 1,
    'BPFtype': 'ramp',
    'trTime': 0.05,
    'scale': 'mel',   # mel, linear
    'numBands': 10
}

# parameters for random gain
gain_pars = {
    'winLen': 0.1,
    'numWin': 5,
    'winUnit': 'n',
    'std': 8,
    'trunc': 1,
    'BPFtype': 'ramp',
    'trTime': 0.05
}

pars = {
    'main_pars': main_pars,
    'ana_pars': ana_pars,
    'pitch_pars': pitch_pars,
    'stretch_pars': stretch_pars,
    'eq_pars': eq_pars,
    'gain_pars': gain_pars
}
