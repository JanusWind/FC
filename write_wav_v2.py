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

start = time.time( )

date1 = '2008-01-01-00-00-00'

io = raw_input( 'Enter i for Interactive and d for default? ==>  ' )

if ( io == 'i' ) :

	n_months = raw_input( 'Number of months to be downloaded ==>  ' )
else :

	n_months = 36

if ( io == 'i' ) :

	date1 = raw_input( 'Enter the starting date ( format: \
	                                          YYYY-MM-DD-HH-MM-SS) ==> ) ' )
	date2 = raw_input( 'Enter the end date ( format: \
	                                          YYYY-MM-DD-HH-MM-SS) ==> ) ' )

else :
	date1 = '2008-01-01-00-00-00'
	date2 = '2008-01-11-00-00-00'

i_date = datetime.strptime( date1, '%Y-%m-%d-%H-%M-%S')
f_date = i_date

#dur = ( f_date - i_date ).total_seconds( )

download = raw_input( 'Download the data ==>  ' )

for i in range( int( n_months ) ) :

	if( download == 'y' ) :

		i_date = f_date
		f_date = i_date + timedelta( days = 10 )

		dur = ( f_date - i_date ).total_seconds( )

		print 'Downloading data for days from ', i_date, 'to', f_date

		arcv = mfi_arcv_hres( )

		mfi_t   = arcv.load_rang( date1, dur )[0]
		mfi_b_x = arcv.load_rang( date1, dur )[1]
		mfi_b_y = arcv.load_rang( date1, dur )[2]
		mfi_b_z = arcv.load_rang( date1, dur )[3]

		print 'Data Downloaded, doing data rotations now'

		# Establish the number of data.

		n_mfi = len( mfi_t )

		# Compute and store derived paramters.

		mfi_s = [ ( t - mfi_t[0] ).total_seconds( )
		                                       for t in mfi_t ]

		# Compute the vector magnetic field.

		mfi_b_vec = [ [ mfi_b_x[j], mfi_b_y[j], mfi_b_z[j] ]
		                for j in range( len( mfi_s ) )      ]

		# Compute the magnetic field magnitude.

		mfi_b = [ sqrt( mfi_b_x[j]**2 +
		                     mfi_b_y[j]**2 +
		                     mfi_b_z[j]**2 )
		                     for j in range( len( mfi_b_x ) ) ]

		# Running average filter.

		N = 600

		cum_sum_x = [ 0. ]
		cum_sum_y = [ 0. ]
		cum_sum_z = [ 0. ]

		rng_avg_x = []
		rng_avg_y = []
		rng_avg_z = []

		for j, xx in enumerate( mfi_b_x, 1 ) :

			cum_sum_x.append( cum_sum_x[j-1] + xx )

			if j>=N:
				avg_x = ( cum_sum_x[j] -
				          cum_sum_x[j-N] )/N

				rng_avg_x.append( avg_x )

		for j, yy in enumerate( mfi_b_y, 1 ) :

			cum_sum_y.append( cum_sum_y[j-1] + yy )

			if j>=N:
				avg_y = ( cum_sum_y[j] -
				          cum_sum_y[j-N] )/N

				rng_avg_y.append( avg_y )

		for j, zz in enumerate( mfi_b_z, 1 ) :

			cum_sum_z.append( cum_sum_z[j-1] + zz )

			if j>=N:
				avg_z = ( cum_sum_z[j] -
				          cum_sum_z[j-N] )/N

				rng_avg_z.append( avg_z )

		rng_avg_vec = [ [ rng_avg_x[j], rng_avg_y[j],
		       rng_avg_z[j] ] for j in range( len( rng_avg_x ) ) ]


		rng_avg_mag = [ sqrt( sum(
		                 [ xx**2 for xx in( rng_avg_vec[j] ) ] ) )
			           for j in range( shape( rng_avg_vec)[1] ) ]

		rng_avg_nrm = [ xx/yy for xx,yy in zip( rng_avg_vec, rng_avg_mag ) ]
#		rng_avg_nrm = rng_avg_vec/rng_avg_mag

		z     = [ 0., 0., 1. ]
		e1 = rng_avg_nrm
		e2 = [ cross( z, xx )/ norm( cross( xx, z ) ) for xx in e1 ]
		e3 = [ cross( xx, yy ) for xx,yy in zip( e1, e2 ) ]

		mfi_x_rot = [ sum( xx*yy for xx,yy in zip(
		                 mfi_b_vec[j + int( N/2. ) ], e1[j] ) )
				                for j in range( len( e1 ) ) ]
		mfi_y_rot = [ sum( xx*yy for xx,yy in zip(
		                 mfi_b_vec[j + int( N/2. ) ], e2[j] ) )
				                for j in range( len( e1 ) ) ]
		mfi_z_rot = [ sum( xx*yy for xx,yy in zip(
		                 mfi_b_vec[j + int( N/2. ) ], e3[j] ) )
				                for j in range( len( e1 ) ) ]

		# Save the non-rotated data to 'wav' files

		os.chdir( '/home/ahmadr/Desktop/GIT/fm_development/data/wav_files' )

		files_raw = [ 'file_x_raw_', 'file_y_raw_', 'file_z_raw_' ]

		data_raw = [ mfi_b_x, mfi_b_y, mfi_b_z ]

		for j in range( 3 ) :

			file_n = files_raw[j] + '_' +\
		                 mfi_t[0 ].strftime( '%Y-%m-%d-%H-%M-%S' ) + '_'+\
		                 mfi_t[-1].strftime( '%Y-%m-%d-%H-%M-%S' ) + '.wav'

			data = int16( data_raw[j]/max(data_raw[j])*0.7*2**15 )

			write( file_n, 44100, data )

		# Save the rotated data to 'wav' files

		files_rot = [ 'file_x_rot_', 'file_y_rot_', 'file_z_rot_' ]

		data_rot = [ mfi_x_rot, mfi_y_rot, mfi_z_rot ]

		for j in range( 3 ) :

			file_n = files_rot[j] + '_' +\
		                 mfi_t[0 ].strftime( '%Y-%m-%d-%H-%M-%S' ) + '_'+\
		                 mfi_t[-1].strftime( '%Y-%m-%d-%H-%M-%S' ) + '.wav'

			data = int16( data_rot[j]/max(data_rot[j])*2**15 )

			write( file_n, 44100, data )

		os.chdir( '/home/ahmadr/Desktop/GIT/fm_development' )

		print 'Data saved for ', i_date, 'to', f_date
'''
plt.figure()
plt.plot( mfi_s[0], mfi_b_x[0], color='r', label='x' )
plt.legend()

plt.figure()
plt.plot( mfi_s[0][int( N/2. ):-int( N/2.-1 )], mfi_x_rot[0], color='r', ls=':', label='x_rot' )
plt.legend()

plt.figure()
plt.plot( mfi_s[0], mfi_b_y[0], color='g', label='y' )
plt.legend()

plt.figure()
plt.plot( mfi_s[0][int( N/2. ):-int( N/2.-1 )], mfi_y_rot[0], color='g', ls=':', label='y_rot' )
plt.legend()

plt.figure()
plt.plot( mfi_s[0], mfi_b_z[0], color='b', label='z' )
plt.legend()

plt.figure()
plt.plot( mfi_s[0][int( N/2. ):-int( N/2.-1 )], mfi_z_rot[0], color='b', ls=':', label='z_rot' )
plt.legend()

#plt.plot( mfi_s[0][300:-299], avg_mag[0], color='m', ls=':')

plt.show()

'''

print 'It took','%.6f'% (time.time()-start), 'seconds.'
