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
#plt.close('all')
#plt.clf()

# Load the modules necessary for saving results to a data file.

import pickle

# Load the modules necessary for copying.

from copy import deepcopy

plt.close('all')

start = time.time( )

download = raw_input('Download the data ==>  ')

date = '2014-01-01-23-00-00'
dur  =  3600*4.0
dur  = dur

filter_length = 109

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

rcParams['figure.figsize'] = 50, 25

f, axs = plt.subplots( 4, 1, squeeze=True, sharex=True )

axs[0].plot( mfi_s, mfi_b_filt,   color='k', label='b', lw=0.2 )
axs[0].set_xlim( min( mfi_s ), max( mfi_s ) )
axs[0].legend( loc=4, fontsize=32 )

axs[1].plot( mfi_s, mfi_b_x_filt, color='r', label=r'$B_x$', lw=0.2 )
axs[1].axhline( 0, color='c', linewidth=1 )
axs[1].set_xlim( min( mfi_s ), max( mfi_s ) )
axs[1].legend( loc=1, fontsize=32 )

axs[2].plot( mfi_s, mfi_b_y_filt, color='g', label=r'$B_y$', lw=0.2 )
axs[2].axhline( 0, color='c', linewidth=1 )
axs[2].set_xlim( min( mfi_s ), max( mfi_s ) )
axs[2].legend( loc=4, fontsize=32 )

axs[3].plot( mfi_s, mfi_b_z_filt, color='b', label=r'$B_z$', lw=0.2 )
axs[3].axhline( 0, color='c', linewidth=1 )
axs[3].set_xlim( min( mfi_s ), max( mfi_s ) )
axs[3].set_xlabel( 'Time', fontsize=32 )
axs[3].legend( loc=1, fontsize=32 )

plt.tight_layout( )

plt.subplots_adjust( left=0.020, right=.99, bottom=0.040, top=0.99, wspace=0., hspace = 0. )

for a in axs :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 32 )

#	tick_labels = a.get_yticklabels()
#	tick_labels[0]  = ""
#	tick_labels[-1] = ""
#	a.set_yticklabels( tick_labels )

for tick in axs[3].xaxis.get_major_ticks() :
	tick.label.set_fontsize( 32 )

f, axs2 = plt.subplots( 1, 1, squeeze=True, sharex=True )

axs2.plot( mfi_s, mfi_b_filt,   color='k', label='B', lw=0.2 )
axs2.set_xlim( min( mfi_s ), max( mfi_s ) )

axs2.plot( mfi_s, mfi_b_x_filt, color='r', label=r'$B_x$', lw=0.2 )
axs2.axhline( 0, color='c', linewidth=1 )
axs2.set_xlim( min( mfi_s ), max( mfi_s ) )

axs2.plot( mfi_s, mfi_b_y_filt, color='g', label=r'$B_y$', lw=0.2 )
axs2.set_xlim( min( mfi_s ), max( mfi_s ) )

axs2.plot( mfi_s, mfi_b_z_filt, color='b', label=r'$B_z$', lw=0.2 )
axs2.set_xlim( min( mfi_s ), max( mfi_s ) )

axs2.plot( mfi_s, -mfi_b_filt,   color='k', lw=0.2 )
axs2.set_xlim( min( mfi_s ), max( mfi_s ) )

axs2.set_xlabel( 'Time', fontsize=32 )
axs2.set_ylabel( 'Magnetic Fields', fontsize=32 )
axs2.legend( loc=2, ncol=4, fontsize=32 )

plt.tight_layout( )

plt.subplots_adjust( left=0.035, right=.99, bottom=0.040, top=0.99, wspace=0., hspace = 0. )

# Managing tick marks and all

for tick in axs2.xaxis.get_major_ticks() :
	tick.label.set_fontsize( 32 )

for tick in axs2.yaxis.get_major_ticks() :
	tick.label.set_fontsize( 32 )

#plt.show( )

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/figures")

pdf = matplotlib.backends.backend_pdf.PdfPages( 'Magnetic_field' + date + str(dur) + ".pdf" )

for fig in xrange(1, f.number+1 ): ## will open an empty extra figure :(
	pdf.savefig( fig )
pdf.close()

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")


'''
###############################################################################
## Defining Butterworth bandpass filter.
###############################################################################

def butter_bandpass(lowcut, highcut, fs, order):

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter( order, [ low, high ], btype='band' )

    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order):

    b, a = butter_bandpass(lowcut, highcut, fs, order)
    y = lfilter(b, a, data)

    return y

orders= [ 1 ]


N = 1000

cum_sum_x, mvg_avg_x = [0], []

for i, x in enumerate( mfi_b_x, 1 ) :

	cum_sum_x.append( cum_sum_x[i-1] + x )

	if i>=N:
		avg_x = ( cum_sum_x[i] - cum_sum_x[i-N] )/N

		#can do stuff with moving_ave here

		mvg_avg_x.append( avg_x )

cum_sum_y, mvg_avg_y = [0], []

for i, x in enumerate( mfi_b_y, 1 ) :

	cum_sum_y.append( cum_sum_y[i-1] + x )

	if i>=N:
		avg_y = ( cum_sum_y[i] - cum_sum_y[i-N] )/N

		#can do stuff with moving_ave here

		mvg_avg_y.append( avg_y )

cum_sum_z, mvg_avg_z = [0], []

for i, x in enumerate( mfi_b_z, 1 ) :

	cum_sum_z.append( cum_sum_z[i-1] + x )

	if i>=N:
		avg_z = ( cum_sum_z[i] - cum_sum_z[i-N] )/N

		#can do stuff with moving_ave here

		mvg_avg_z.append( avg_z )

for i in range( len( orders ) ) :

	fs = 1 / ( mfi_s[1] - mfi_s[0] )
	lc = 0.0
	mc = 0.005
	mc1 = 0.005
	hc = 1.5
	order = orders[i]

	# Compute the bandpass filtered data for all the three components.

	filt_x = butter_bandpass_filter( mfi_b_x_filt_11, mc1, hc, fs, order )
	filt_y = butter_bandpass_filter( mfi_b_y_filt_11, mc1, hc, fs, order )
	filt_z = butter_bandpass_filter( mfi_b_z_filt_11, mc1, hc, fs, order )

	filt_x_low = butter_bandpass_filter( mfi_b_x_filt, lc, mc, fs, order )
	filt_y_low = butter_bandpass_filter( mfi_b_y_filt, lc, mc, fs, order )
	filt_z_low = butter_bandpass_filter( mfi_b_z_filt, lc, mc, fs, order )

	resd_x = filt_x_low + filt_x
	resd_y = filt_y_low + filt_y
	resd_z = filt_z_low + filt_z

	a1 = 3000
	b1 = -3000

	indx = int( fs*300 )
	siggg = [ std( filt_x[indx:-indx] ),
	          std( filt_y[indx:-indx] ),
	          std( filt_z[indx:-indx] ) ]
	lw = 0.75
	lbl = [ 'non-filtered', 'band-pass', 'low-pass', 'residue' ]


	f, ax2 = plt.subplots( 3, 1, sharex = True )

	rcParams['figure.figsize'] = 20, 10

	ax2[0].plot( mfi_s[indx:-indx], mfi_b_x_filt[indx:-indx], linewidth=lw, color='k', label = lbl[0])
	ax2[0].plot( mfi_s[indx:-indx], filt_x[indx:-indx],  linewidth=lw, color='r', label = lbl[1])
	ax2[0].plot( mfi_s[indx:-indx], filt_x_low[indx:-indx], linewidth=lw, color='b', label = lbl[2])
	ax2[0].plot( mfi_s[indx:-indx], resd_x[indx:-indx],  linewidth=lw, color='#1e5c10', label = lbl[3] )
	ax2[0].set_ylabel( 'x-component' )
	ax2[0].legend( )

	ax2[1].plot( mfi_s[indx:-indx], mfi_b_y_filt[indx:-indx], linewidth=lw, color='k', label = lbl[0] )
	ax2[1].plot( mfi_s[indx:-indx], filt_y[indx:-indx],  linewidth=lw, color='r', label = lbl[1] )
	ax2[1].plot( mfi_s[indx:-indx], filt_y_low[indx:-indx], linewidth=lw, color='b', label = lbl[2] )
	ax2[1].plot( mfi_s[indx:-indx], resd_y[indx:-indx],  linewidth=lw, color='#1e5c10', label = lbl[3] )
	ax2[1].set_ylabel( 'y-component' )
	ax2[1].legend( )

	ax2[2].plot( mfi_s[indx:-indx], mfi_b_z_filt[indx:-indx], linewidth=lw, color='k', label = lbl[0] )
	ax2[2].plot( mfi_s[indx:-indx], filt_z[indx:-indx],  linewidth=lw, color='r', label = lbl[1] )
	ax2[2].plot( mfi_s[indx:-indx], filt_z_low[indx:-indx], linewidth=lw, color='b', label = lbl[2] )
	ax2[2].plot( mfi_s[indx:-indx], resd_z[indx:-indx],  linewidth=lw, color='#1e5c10', label = lbl[3] )
	ax2[2].set_ylabel( 'z-component' )
	ax2[2].legend( )

	#ax2[1].plot( mfi_s[indx:-indx], mfi_b_y, linewidth=lw, color='#d7d1cf', label = lbl[] )
	#ax2[1].plot( mfi_s[indx:-indx], filt_y,  linewidth=lw, color='#4D2619', label = lbl[] )
	##ax2[1].plot( mfi_s[indx:-indx], resd_y,  linewidth=lw, color='#1e5c10', label = lbl[])
	#ax2[1].set_ylabel( 'y-component' )
	#ax2[1].legend( )
	#
	#ax2[2].plot( mfi_s[indx:-indx], mfi_b_z, linewidth=lw, color='#d7d1cf', label = lbl[] )
	#ax2[2].plot( mfi_s[indx:-indx], filt_z,  linewidth=lw, color='#4D2619', label = lbl[] )
	##ax2[2].plot( mfi_s[indx:-indx], resd_z,  linewidth=lw, color='#1e5c10', label = lbl[] )
	#ax2[2].set_ylabel( 'z-component' )
	ax2[2].set_xlabel( 'Time ( Date hr:mn )' )
	ax2[2].legend( )

	plt.suptitle( 'Plot of magnetic field with and without Butterworth Filter ( order= %0.0f)' % (order) )


	plt.figure( )

	b_a = sqrt( [ ( filt_x[i]**2+filt_y[i]**2+filt_z[i]**2 ) for i in range( len( filt_x ) ) ]  )

	plt.plot( mfi_s[indx:-indx], b_a[indx:-indx], color='r', label='' )
	plt.xlabel( 'Time', fontsize=24 )
	plt.ylabel( 'Magnitude of Magnetic Field', fontsize=24 )
	plt.title( 'Magnitude of MF against Time', fontsize=24 )

	plt.figure( )

	plt.plot( mfi_s[indx:-indx], filt_y[indx:-indx], color='g', label='y-component' )
	plt.plot( mfi_s[indx:-indx], filt_z[indx:-indx], color='r', label='z-component' )
	plt.xlabel( 'Time', fontsize=24 )
	plt.ylabel( 'Magnetic Field', fontsize=24 )
	plt.title( 'Different components of MF against Time', fontsize=24 )
	plt.legend( )


	f, ax3 = plt.subplots( 3, 1, sharex=True )

	plt.subplots_adjust( hspace = 0. )

	ax3[0].plot( mfi_s, mfi_b_x, color='b', label='raw x-component')
	ax3[0].plot( mfi_s[N/2:-(N/2-1) ], mvg_avg_x, color='r', label='Moving average x-component')
	ax3[0].set_ylabel( 'Magnitude' )
	ax3[0].legend( )

	ax3[1].plot( mfi_s, mfi_b_y, color='b', label='raw y-component')
	ax3[1].plot( mfi_s[N/2:-(N/2-1) ], mvg_avg_y, color='r', label='Moving average y-component')
	ax3[1].set_ylabel( 'Magnitude' )
	ax3[1].legend( )

	ax3[2].plot( mfi_s, mfi_b_z, color='b', label='raw z-component')
	ax3[2].plot( mfi_s[N/2:-(N/2-1) ], mvg_avg_z, color='r', label='Moving average z-component')
	ax3[2].set_ylabel( 'Magnitude' )
	ax3[2].set_xlim( 0, 700 )
	ax3[2].set_xlabel( 'Time' )
	ax3[2].legend( )
	ax3[0].set_title( 'Raw magnetic field and time moving average for window size = 10sec' )

	plt.tight_layout( )
	for a in axs1 :
		for tick in a.yaxis.get_major_ticks() :
			tick.label.set_fontsize( 16 )


#	plt.show( )
	'''


'''
f, ax = plt.subplots( 3, 1, sharex = True )

rcParams['figure.figsize'] = 60, 30

ax[0].plot( mfi_s[indx:-indx], bx_r, color='#d7d1cf' )
ax[0].plot( mfi_s[indx:-indx], bxf,  color='#4D2619' )

ax[1].plot( mfi_s[indx:-indx], by_r, color='#d7d1cf' )
ax[1].plot( mfi_s[indx:-indx], byf,  color='#4D2619' )

ax[2].plot( mfi_s[indx:-indx], bz_r, color='#d7d1cf' )
ax[2].plot( mfi_s[indx:-indx], bzf,  color='#4D2619' )

legend = [ 'X-data', 'Y-data', 'Z-data' ]

ax[0].legend( legend[0], loc = 1 )
ax[1].legend( legend[1], loc = 1 )
ax[2].legend( legend[2], loc = 1 )

#plt.show( )

'''
