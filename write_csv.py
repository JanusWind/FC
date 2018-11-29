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

n_months = raw_input( 'Number of months to be downloaded ==>  ' )

date = '2008-11-04-12-00-00.0'

if( download == 'y' ) :

	mfi_t       = [ [] for x in range( int( n_months ) ) ]
	mfi_b_x     = [ [] for x in range( int( n_months ) ) ]
	mfi_b_y     = [ [] for x in range( int( n_months ) ) ]
	mfi_b_z     = [ [] for x in range( int( n_months ) ) ]
	
	mfi_x_rot   = [ [] for x in range( int( n_months ) ) ]
	mfi_y_rot   = [ [] for x in range( int( n_months ) ) ]
	mfi_z_rot   = [ [] for x in range( int( n_months ) ) ]
	
	n_mfi       = [ [] for x in range( int( n_months ) ) ]
	mfi_s       = [ [] for x in range( int( n_months ) ) ]
	mfi_b_vec   = [ [] for x in range( int( n_months ) ) ]
	mfi_b       = [ [] for x in range( int( n_months ) ) ]
	rng_avg_vec = [ [] for x in range( int( n_months ) ) ]
	rng_avg_x   = [ [] for x in range( int( n_months ) ) ]
	rng_avg_y   = [ [] for x in range( int( n_months ) ) ]
	rng_avg_z   = [ [] for x in range( int( n_months ) ) ]
	cum_sum_x   = [ [0.] for x in range( int( n_months ) ) ]
	cum_sum_y   = [ [0.] for x in range( int( n_months ) ) ]
	cum_sum_z   = [ [0.] for x in range( int( n_months ) ) ]
	rng_avg_mag = [ [] for x in range( int( n_months ) ) ]
	rng_avg_nrm = [ [] for x in range( int( n_months ) ) ]

e1 = [ [] for x in range( int( n_months ) ) ]
e2 = [ [] for x in range( int( n_months ) ) ]
e3 = [ [] for x in range( int( n_months ) ) ]

for i in range( int( n_months ) ) :

	download = raw_input( 'Download the data ==>  ' )

	dur  = 24.*3600.
#	dur = 90

	if( download == 'y' ) :

		arcv = mfi_arcv_hres( )

		mfi_t[i]   = arcv.load_rang( date, dur )[0]
		mfi_b_x[i] = arcv.load_rang( date, dur )[1]
		mfi_b_y[i] = arcv.load_rang( date, dur )[2]
		mfi_b_z[i] = arcv.load_rang( date, dur )[3]

		# Establish the number of data.

		n_mfi[i] = len( mfi_t[i] )

		# Compute and store derived paramters.

		mfi_s[i] = [ ( t - mfi_t[i][0] ).total_seconds( )
		                                       for t in mfi_t[i] ]

		# Compute the vector magnetic field.

		mfi_b_vec[i] = [ [ mfi_b_x[i][j], mfi_b_y[i][j], mfi_b_z[i][j] ]
		                for j in range( len( mfi_s[i] ) )      ]

		# Compute the magnetic field magnitude.

		mfi_b[i] = [ sqrt( mfi_b_x[i][j]**2 +
		                     mfi_b_y[i][j]**2 +
		                     mfi_b_z[i][j]**2 )
		                     for j in range( len( mfi_b_x[i] ) ) ]

		# Running average filter.

		N = 600

		
		for j, xx in enumerate( mfi_b_x[i], 1 ) :
		
			cum_sum_x[i].append( cum_sum_x[i][j-1] + xx )
		
			if j>=N:
				avg_x = ( cum_sum_x[i][j] -
				          cum_sum_x[i][j-N] )/N

				rng_avg_x[i].append( avg_x )

		for j, yy in enumerate( mfi_b_y[i], 1 ) :
		
			cum_sum_y[i].append( cum_sum_y[i][j-1] + yy )
		
			if j>=N:
				avg_y = ( cum_sum_y[i][j] -
				          cum_sum_y[i][j-N] )/N

				rng_avg_y[i].append( avg_y )

		for j, zz in enumerate( mfi_b_z[i], 1 ) :
		
			cum_sum_z[i].append( cum_sum_z[i][j-1] + zz )
		
			if j>=N:
				avg_z = ( cum_sum_z[i][j] -
				          cum_sum_z[i][j-N] )/N

				rng_avg_z[i].append( avg_z )

		rng_avg_vec[i] = [ [ rng_avg_x[i][j], rng_avg_y[i][j],
		       rng_avg_z[i][j] ] for j in range( len( rng_avg_x[i] ) ) ]


		rng_avg_mag[i] = [ sqrt( sum(
		                 [ xx**2 for xx in( rng_avg_vec[i][j] ) ] ) )
			        for j in range( numpy.shape( rng_avg_vec)[1] ) ]

		rng_avg_nrm[i] = [ xx/yy for xx,yy in zip( rng_avg_vec[0], rng_avg_mag[0]) ]
#		rng_avg_nrm[i] = rng_avg_vec[i]/rng_avg_mag[i]

		z     = [ 0., 0., 1. ]
		e1[i] = rng_avg_nrm[i]
		e2[i] = [ cross( z, xx )/ norm( cross( xx, z ) ) for xx in e1[i] ]
		e3[i] = [ cross( xx, yy ) for xx,yy in zip( e1[i], e2[i] ) ]

		mfi_x_rot[i] = [ sum( xx*yy for xx,yy in zip(
		                 mfi_b_vec[i][j + int( N/2. ) ], e1[i][j] ) )
				                for j in range( len( e1[i] ) ) ]
		mfi_y_rot[i] = [ sum( xx*yy for xx,yy in zip(
		                 mfi_b_vec[i][j + int( N/2. ) ], e2[i][j] ) )
				                for j in range( len( e1[i] ) ) ]
		mfi_z_rot[i] = [ sum( xx*yy for xx,yy in zip(
		                 mfi_b_vec[i][j + int( N/2. ) ], e3[i][j] ) )
				                for j in range( len( e1[i] ) ) ]

#		mfi_x_rot[i] = [ sum( xx*yy for xx,yy in zip( mfi_b_vec[i][j], e1[i][j] ) ) for j in range( numpy.shape( rng_avg_vec)[1] ) ]
		
#		mfi_x_rot[i] = [ sum( [ mfi_b_vec[i][j][k]*e1[i][k]
#		for k in range( 3 ) ] )
#		for j in range( numpy.shape( mfi_b_vec )[1] ) ]
plt.figure()

plt.figure()
plt.plot( mfi_s[0], mfi_b_x[0], color='r', label='x' )
plt.plot( mfi_s[0][int( N/2. ):-int( N/2./-1 )], mfi_x_rot[0], color='r', ls=':')

plt.figure()

plt.plot( mfi_s[0], mfi_b_y[0], color='g', label='y' )
plt.figure()
plt.plot( mfi_s[0][int( N/2. ):-int( N/2./-1 )], mfi_y_rot[0], color='g', ls=':')

plt.figure()
plt.plot( mfi_s[0], mfi_b_z[0], color='b', label='z' )
plt.figure()
plt.plot( mfi_s[0][int( N/2. ):-int( N/2./-1 )], mfi_z_rot[0], color='b', ls=':')

#plt.plot( mfi_s[0][300:-299], avg_mag[0], color='m', ls=':')

'''
scaled = np.int16( mfi_b_z/max(mfi_b_y) * 32767 )

write( 'test_y.wav', 44100, scaled )

with open("b_x.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_b_x )

with open("b_y.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_b_y )

with open("b_z.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_b_z )

with open("b_t.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_t )
'''
