#  Load the modules necessary for signaling the graphical interface.

#from PyQt4.QtCore import QObject, SIGNAL, QThread
from matplotlib.backends.qt_compat import QtCore
#from QtCore import QObject, SIGNAL, QThread

# Load the modules necessary for file operations.

import os.path

# Load the modules necessary for handling dates and times.

import time
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
                    average, cos, deg2rad, diag, dot, exp, indices, interp, \
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
from pylab import rcParams

from janus_helper import round_sig

from janus_fc_spec import fc_spec

# Load the "pyon" module.

from janus_pyon import plas, series

import matplotlib.pyplot as plt
plt.close('all')

# Load the modules necessary for saving results to a data file.

import pickle

# Load the modules necessary for copying.

from copy import deepcopy

start = time.time( )

download = raw_input('Download the data ==>  ')

#date = '2008-12-26-18-00-00'
#dur  =  3600

if( download == 'y' ) :

	arcv = mfi_arcv_hres( )

	( mfi_t, mfi_b_x, mfi_b_y,
	  mfi_b_z ) = arcv.load_rang( date, dur )

	# Establish the number of data.
	
	n_mfi = len( mfi_t )
	
	# Compute and store derived paramters.
	
	mfi_s = [ ( t - mfi_t[0] ).total_seconds( )
	                                       for t in mfi_t ]
	
	# Compute the vector magnetic field.
	
	mfi_b_vec = [ [ mfi_b_x[i], mfi_b_y[i], mfi_b_z[i]  ]
	                for i in range( len( mfi_s ) )      ]
	
	# Compute the magnetic field magnitude.
	
	mfi_b = [ sqrt( mfi_b_x[i]**2 +
	                     mfi_b_y[i]**2 +
	                     mfi_b_z[i]**2 )
	                     for i in range( len( mfi_b_x ) ) ]
	
	mfi_b_std = std( mfi_b )
	
	sig_b_x = std( mfi_b_x )
	sig_b_y = std( mfi_b_y )
	sig_b_z = std( mfi_b_z )
	
	sig_b = sqrt( sig_b_x**2 +  sig_b_y**2 + sig_b_z**2 )
	
	# Compute the average magetic field and its norm.
	
	mfi_avg_vec = array( [ mean( mfi_b_x ),
	                       mean( mfi_b_y ),
	                       mean( mfi_b_z ) ] )
	
	mfi_avg_mag = sqrt( mfi_avg_vec[0]**2 +
	                    mfi_avg_vec[1]**2 +
	                    mfi_avg_vec[2]**2   )
	
	mfi_avg_nrm = mfi_avg_vec / mfi_avg_mag
	
	mfi_nrm     = [ ( mfi_b_x[i], mfi_b_y[i],
	                  mfi_b_z[i] ) /mfi_b[i]
	                  for i in range( len( mfi_b ) ) ]
	
	z  = [0., 0., 1.]
	e1 = mfi_avg_nrm
	e2 = cross( z, e1 )/ norm( cross( e1, z ) )
	e3 = cross( e1, e2 )
	
	bx_r = [ sum( [ mfi_b_vec[i][j]*e1[j] for j in range(3)] )
	                            for i in range( len( mfi_s ) ) ]
	by_r = [ sum( [ mfi_b_vec[i][j]*e2[j] for j in range(3)] )
	                            for i in range( len( mfi_s ) ) ]
	bz_r = [ sum( [ mfi_b_vec[i][j]*e3[j] for j in range(3)] )
	                            for i in range( len( mfi_s ) ) ]
	
	b_vec = [ [ bx_r[i], by_r[i], bz_r[i] ] for i in range( len( mfi_s ) ) ]
	
	bxf = medfilt( bx_r, 11 )
	byf = medfilt( by_r, 11 )
	bzf = medfilt( bz_r, 11 )
	
	omega_p = mfi_avg_mag*const['q_p']/const['m_p']

###############################################################################
## Defining Butterworth bandpass filter.
###############################################################################

def butter_bandpass(lowcut, highcut, fs, order=5):

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter( order, [ low, high ], btype='band' )

    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):

    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)

    return y

fs = 1 / ( mfi_s[1] - mfi_s[0] )
lc = 0.0001
hc = 0.5

# Compute the bandpass filtered data for all the three components.

filt_x = butter_bandpass_filter( mfi_b_x, lc, hc, fs, order=8 )
filt_y = butter_bandpass_filter( mfi_b_y, lc, hc, fs, order=8 )
filt_z = butter_bandpass_filter( mfi_b_z, lc, hc, fs, order=8 )

resd_x = mfi_b_x - filt_x
resd_y = mfi_b_y - filt_y
resd_z = mfi_b_z - filt_z

f, ax2 = plt.subplots( 3, 1, sharex = True )

rcParams['figure.figsize'] = 20, 10

ax2[0].plot( mfi_t, mfi_b_x, linewidth=0.75, color='#d7d1cf', label = 'non-filtered' )
ax2[0].plot( mfi_t, filt_x,  linewidth=0.75, color='#4D2619', label = 'filtered'     )
#ax2[0].plot( mfi_t, resd_x,  linewidth=0.75, color='#1e5c10', label = 'residue' )
ax2[0].set_ylabel( 'x-component' )
ax2[0].legend( )

ax2[1].plot( mfi_t, mfi_b_y, linewidth=0.75, color='#d7d1cf', label = 'non-filtered' )
ax2[1].plot( mfi_t, filt_y,  linewidth=0.75, color='#4D2619', label = 'filtered'     )
#ax2[1].plot( mfi_t, resd_y,  linewidth=0.75, color='#1e5c10', label = 'residue' )
ax2[1].set_ylabel( 'y-component' )
ax2[1].legend( )

ax2[2].plot( mfi_t, mfi_b_z, linewidth=0.75, color='#d7d1cf', label = 'non-filtered' )
ax2[2].plot( mfi_t, filt_z,  linewidth=0.75, color='#4D2619', label = 'filtered'     )
#ax2[2].plot( mfi_t, resd_z,  linewidth=0.75, color='#1e5c10', label = 'residue' )
ax2[2].set_ylabel( 'z-component' )
ax2[2].set_xlabel( 'Time ( Date hr:mn )' )
ax2[2].legend( )

plt.suptitle( 'Plot of magnetic field with and without Butterworth Filter ( order=5 )' )

plt.show( )
plt.tight_layout( )

'''
f, ax = plt.subplots( 3, 1, sharex = True )

rcParams['figure.figsize'] = 60, 30

ax[0].plot( mfi_t, bx_r, color='#d7d1cf' )
ax[0].plot( mfi_t, bxf,  color='#4D2619' )

ax[1].plot( mfi_t, by_r, color='#d7d1cf' )
ax[1].plot( mfi_t, byf,  color='#4D2619' )

ax[2].plot( mfi_t, bz_r, color='#d7d1cf' )
ax[2].plot( mfi_t, bzf,  color='#4D2619' )

legend = [ 'X-data', 'Y-data', 'Z-data' ]

ax[0].legend( legend[0], loc = 1 )
ax[1].legend( legend[1], loc = 1 )
ax[2].legend( legend[2], loc = 1 )

plt.show( )

'''
