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

from glob import glob

plt.clf()
plt.close('all')

# Load the modules necessary for saving results to a data file.

import pickle

# Load the modules necessary for copying.

from copy import deepcopy

start = time.time( )

method = 'i'
#method = raw_input( 'Interative or default ( i or d )? == > ' )

#if( method == 'i' ) :
download = 'y'
#	download = raw_input( 'Download the data ==>  ' )

date = str( e_time )
#date = raw_input( 'Enter the date ==> ' )

dur  = int( raw_input( 'Enter the duration ==> ' ) )

dur = dur*3600

#else :
#
#	download = raw_input( 'Download the data ==>  ' )
#
#	date = '2008-11-04-00-00-00.0'
#
#	dur  =  3600

filter_length = 1

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

	mfi_b_filt   = medfilt( mfi_b,   filter_length )
	mfi_b_x_filt = medfilt( mfi_b_x, filter_length )
	mfi_b_y_filt = medfilt( mfi_b_y, filter_length )
	mfi_b_z_filt = medfilt( mfi_b_z, filter_length )

	mfi_b_x_filt_11 = medfilt( mfi_b_x, 11 )
	mfi_b_y_filt_11 = medfilt( mfi_b_y, 11 )
	mfi_b_z_filt_11 = medfilt( mfi_b_z, 11 )

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

	bxf = medfilt( bx_r, filter_length )
	byf = medfilt( by_r, filter_length )
	bzf = medfilt( bz_r, filter_length )

	omega_p = mfi_avg_mag*const['q_p']/const['m_p']

mfi_hr = [ xx/ 3600. for xx in mfi_s ]

rcParams['figure.figsize'] = 15, 10

lims = linspace( 0, dur/3600, int( dur/180 ) )

os.chdir( '/home/ahmadr/Desktop/GIT/fm_development/test_figs' )

for f in glob( "*.pdf" ) :

	os.remove( f )

os.chdir( '/home/ahmadr/Desktop/GIT/fm_development' )

# Stop printing the 'Too many figure' warning

plt.rcParams.update({'figure.max_open_warning': 0})

for i in range( len( lims ) - 1 ) :


	f, axs = plt.subplots( 2, 1, squeeze=True, sharex=True )
	
	#axs[0].plot( mfi_hr, mfi_b_filt,   color='k', label='b', lw=0.2 )
	##axs[0].set_ylim( 3., 3.5 )
	#axs[0].set_xlim( min( mfi_hr ), max( mfi_hr ) )
	#axs[0].legend( loc=4, fontsize=32 )
	#
	#axs[1].plot( mfi_hr, mfi_b_x_filt, color='r', label=r'$B_x$', lw=0.2 )
	##axs[1].axhline( 0, color='c', linewidth=1 )
	##axs[1].set_ylim( 3., 3.5 )
	#axs[1].set_xlim( min( mfi_hr ), max( mfi_hr ) )
	#axs[1].legend( loc=1, fontsize=32 )
	
	axs[0].plot( mfi_hr, mfi_b_y_filt, color='g', label=r'$B_y$', lw=0.8 )
	#axs[2].axhline( 0, color='c', linewidth=1 )
	#axs[2].set_ylim( -0.8, 0.2 )
	axs[0].set_xlim( min( mfi_hr ), max( mfi_hr ) )
	axs[0].grid( True, which='both', axis='x', color='m', lw='0.5', ls='--' )
	axs[0].legend( loc=4, fontsize=22 )
	
	axs[1].plot( mfi_hr, mfi_b_z_filt, color='b', label=r'$B_z$', lw=0.8 )
	#axs[3].axhline( 0, color='c', linewidth=1 )
	#axs[3].set_xlim( 300, 400 )
	#axs[3].set_ylim( -0.6, 1 )
	axs[1].set_xlim( min( mfi_hr ), max( mfi_hr ) )
	axs[1].set_xlabel( 'Time (hr)', fontsize=22 )
	axs[1].grid( True, which='both', axis='x', color='m', lw='0.5', ls='--' )
	axs[1].legend( loc=1, fontsize=22 )

	axs[1].set_xlim( lims[i], lims[i+1] )
	axs[0].set_title( 'Figure ' + str( i + 1 ) + ' of ' + str( len( lims ) -1 ) + "  for date " + date )

	plt.tight_layout( )
	
	plt.subplots_adjust( left=0.035, right=.995, bottom=0.070, top=0.97, wspace=0., hspace = 0. )
	
	for a in axs :
		for tick in a.yaxis.get_major_ticks() :
			tick.label.set_fontsize( 18 )
	
	#	tick_labels = a.get_yticklabels()
	#	tick_labels[0]  = ""
	#	tick_labels[-1] = ""
	#	a.set_yticklabels( tick_labels )
	
	for tick in axs[1].xaxis.get_major_ticks() :
		tick.label.set_fontsize( 18 )

os.chdir( '/home/ahmadr/Desktop/GIT/fm_development/test_figs' )

pdf = matplotlib.backends.backend_pdf.PdfPages( "MFI_Data_time_series.pdf" )

for fig in xrange(1, f.number+1 ): ## will open an empty extra figure :(
	pdf.savefig( fig )
pdf.close()

os.chdir( '/home/ahmadr/Desktop/GIT/fm_development' )

#plt.show( )
