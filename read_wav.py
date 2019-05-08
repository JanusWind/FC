#  Load the modules necessary for signaling the graphical interface.

#from PyQt4.QtCore import QObject, SIGNAL, QThread
from matplotlib.backends.qt_compat import QtCore
#from QtCore import QObject, SIGNAL, QThread

# Load the modules necessary for file operations.

import os.path

from pathlib2 import Path

# Load the modules necessary for handling dates and times.

import time
start = time.time()

from time import sleep
from datetime import datetime, timedelta
from janus_time import calc_time_epc, calc_time_sec, calc_time_val

# Load the module necessary handling step functions.

from janus_step import step

# Load the dictionary of physical constants.

from janus_const import const

# Load the modules necessary for loading Wind/FC and Wind/MFI data.

#from janus_fc_arcv   import fc_arcv
#from janus_spin_arcv import spin_arcv
#from janus_mfi_arcv_lres  import mfi_arcv_lres
from janus_mfi_arcv_hres import mfi_arcv_hres

# Load the necessary array modules and mathematical functions.

from numpy import amax, amin, append, arccos, arctan2, arange, argsort, array, \
                int16, average, cos, deg2rad, diag, dot, exp, indices, interp, \
                    mean, pi, polyfit, rad2deg, reshape, sign, sin, sum, sqrt, \
                    std, tile, transpose, where, zeros, shape, abs, linspace,\
                    cross, angle, argmax, max, zeros_like, argmin, corrcoef

from numpy.linalg import lstsq, norm
from numpy.fft import rfftfreq, fftfreq, fft, irfft, rfft
from operator import add

from scipy.special     import erf
from scipy.interpolate import interp1d
from scipy.optimize    import curve_fit
from scipy.stats       import pearsonr, spearmanr
from scipy.signal      import medfilt, butter, lfilter
from scipy.io.wavfile import write
from pylab import rcParams
import matplotlib.backends.backend_pdf

from janus_helper import round_sig

from janus_fc_spec import fc_spec

# Load the "pyon" module.

from janus_pyon import plas, series

import matplotlib.pyplot as plt
plt.close('all')
plt.clf()

# Load the modules necessary for saving results to a data file.

import pickle

# Load the modules necessary for copying.

from copy import deepcopy

plt.close('all')

strt_time = raw_input( 'Enter the start time of file ==> ' )[12:31]

occ_sec   = raw_input( 'Enter the event occurance time ==> ' )

i_time = datetime.strptime( strt_time, '%Y-%m-%d-%H-%M-%S' )

e_time = i_time + timedelta( seconds = float( occ_sec )*44100*0.092 )

print e_time
