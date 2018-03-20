# Load the modules necessary for signaling the graphical interface.

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
                    cross, angle, argmax, max, zeros_like, argmin

from numpy.linalg import lstsq, norm
from numpy.fft import rfftfreq, fftfreq, fft, irfft, rfft
from operator import add

from scipy.special     import erf
from scipy.interpolate import interp1d
from scipy.optimize    import curve_fit
from scipy.stats       import pearsonr, spearmanr
from scipy.signal      import medfilt

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

arcv = mfi_arcv_hres( )

( mfi_t, mfi_b_x, mfi_b_y,
  mfi_b_z ) = arcv.load_rang('2008-11-04-12-00-00', 100 )

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

bx = [ sum( [ mfi_b_vec[i][j]*e1[j] for j in range(3)] )
                        for i in range( len( mfi_s ) ) ]
by = [ sum( [ mfi_b_vec[i][j]*e2[j] for j in range(3)] )
                        for i in range( len( mfi_s ) ) ]
bz = [ sum( [ mfi_b_vec[i][j]*e3[j] for j in range(3)] )
                        for i in range( len( mfi_s ) ) ]

b_vec = [ [ bx[i], by[i], bz[i] ] for i in range( len( mfi_s ) ) ]

# Define the time interval between measurements

dt = mfi_s[1] - mfi_s[0]

# Compute all the frequencies.

fq1 = rfftfreq( len( mfi_s ), d = dt )

# Compute the Fourier Transform of each component of magnetic field.

fb1_x = rfft( bx )
fb1_y = rfft( by )
fb1_z = rfft( bz )

# Compute the absolute value of fourier transformed data.

afb1_x = abs( fb1_x**2 )
afb1_y = abs( fb1_y**2 )
afb1_z = abs( fb1_z**2 )

# Compute the index at which maximum frequency occurs.

max_ind1_x = argmin( abs( afb1_x - max( afb1_x ) ) )
max_ind1_y = argmin( abs( afb1_y - max( afb1_y ) ) )
max_ind1_z = argmin( abs( afb1_z - max( afb1_z ) ) )

# Compute the value of maximum frequency.

fq1_x = fq1[ max_ind1_x ]
fq1_y = fq1[ max_ind1_y ]
fq1_z = fq1[ max_ind1_z ]

ffb1_x = zeros_like( fb1_x ) 
ffb1_y = zeros_like( fb1_y ) 
ffb1_z = zeros_like( fb1_z ) 

ffb1_x[ max_ind1_x ] = fb1_x[ max_ind1_x ]
ffb1_y[ max_ind1_y ] = fb1_y[ max_ind1_y ]
ffb1_z[ max_ind1_z ] = fb1_z[ max_ind1_z ]

bb1_x = irfft( ffb1_x )
bb1_y = irfft( ffb1_y )
bb1_z = irfft( ffb1_z )

# Calculate the residue and its rms value from fft.

res1_fft_x = [ ( bx[i] - bb1_x[i] ) for i in range( len( mfi_s ) ) ]
res1_fft_y = [ ( by[i] - bb1_y[i] ) for i in range( len( mfi_s ) ) ]
res1_fft_z = [ ( bz[i] - bb1_z[i] ) for i in range( len( mfi_s ) ) ]

rms_res1_x = std( res1_fft_x )
rms_res1_y = std( res1_fft_y )
rms_res1_z = std( res1_fft_z )

# Compute the Fourier Transform of residue of each component of magnetic field.

fb2_x = rfft( res1_fft_x )
fb2_y = rfft( res1_fft_y )
fb2_z = rfft( res1_fft_z )

# Compute the absolute value of fourier residual transformed data.

afb2_x = abs( fb2_x**2 )
afb2_y = abs( fb2_y**2 )
afb2_z = abs( fb2_z**2 )

# Compute the index at which maximum frequency occurs.

max_ind2_x = argmin( abs( afb2_x - max( afb2_x ) ) )
max_ind2_y = argmin( abs( afb2_y - max( afb2_y ) ) )
max_ind2_z = argmin( abs( afb2_z - max( afb2_z ) ) )

# Compute the value of maximum frequency.

fq2_x = fq1[ max_ind2_x ]
fq2_y = fq1[ max_ind2_y ]
fq2_z = fq1[ max_ind2_z ]

ffb2_x = zeros_like( fb2_x ) 
ffb2_y = zeros_like( fb2_y ) 
ffb2_z = zeros_like( fb2_z ) 

ffb2_x[ max_ind2_x ] = fb2_x[ max_ind2_x ]
ffb2_y[ max_ind2_y ] = fb2_y[ max_ind2_y ]
ffb2_z[ max_ind2_z ] = fb2_z[ max_ind2_z ]

bb2_x = irfft( ffb2_x )
bb2_y = irfft( ffb2_y )
bb2_z = irfft( ffb2_z )

# Calculate the residue and its rms value from fft.

res2_fft_x = [ ( res1_fft_x[i] - bb2_x[i] ) for i in range( len( mfi_s ) ) ]
res2_fft_y = [ ( res1_fft_y[i] - bb2_y[i] ) for i in range( len( mfi_s ) ) ]
res2_fft_z = [ ( res1_fft_z[i] - bb2_z[i] ) for i in range( len( mfi_s ) ) ]

rms_res2_x = std( res2_fft_x )
rms_res2_y = std( res2_fft_y )
rms_res2_z = std( res2_fft_z )

# Calculate the final fft value from summing for all modes.

bbf_x = bb1_x + bb2_x
bbf_y = bb1_y + bb2_y
bbf_z = bb1_z + bb2_z

# Calculate the residue and its rms value from fft.

resf_fft_x = [ ( bx[i] - bbf_x[i] ) for i in range( len( mfi_s ) ) ]
resf_fft_y = [ ( by[i] - bbf_y[i] ) for i in range( len( mfi_s ) ) ]
resf_fft_z = [ ( bz[i] - bbf_z[i] ) for i in range( len( mfi_s ) ) ]

rms_resf_x = std( resf_fft_x )
rms_resf_y = std( resf_fft_y )
rms_resf_z = std( resf_fft_z )

#print rms_res1_y, rms_res2_y, rms_resf_y
#print rms_res1_z, rms_res2_z, rms_resf_z


# Model the curve-fit sine function.
def fit_sin( t, b ) :

	f = fftfreq( len( t ), ( t[1] - t[0] ) )
	fb = abs( fft( b ) )
	gss_f = abs( f[ argmax( fb[1:] ) + 1 ] )
	gss_a = std( b ) * 2.**0.5
	gss_i = mean( b )
	gss = [ gss_a, 2.*pi*gss_f, 0., gss_i ]

	def sinfunc( t, A, w, p, c ):  return A * sin( w*t + p ) + c

	popt, pcov = curve_fit(sinfunc, t, b, p0=gss)
	A, w, p, c = popt
	af = w/(2.*pi)
	fitfunc = lambda t: A * sin(w*t + p) + c

	return { "amp"     : A,
	         "omega"   : w,  "phase": p,
	         "offset"  : c,  "freq" : f,
	         "period"  : [ ( 0 if f[i] == 0 else 1./f[i] ) for i in range( len ( f ) ) ],
	         "fitfunc" : fitfunc,
	         "maxcov"  : max( pcov ),
	         "rawres"  : ( gss,popt,pcov ) }

# Fit the given data to a sine function.

fit1_x = fit_sin( mfi_s, bx )
fit1_y = fit_sin( mfi_s, by )
fit1_z = fit_sin( mfi_s, bz )

ts = linspace(0, max( mfi_s ), len( mfi_s ) )

# Calculate residue from fit-function.

res1_fit_x = [ ( bx[i] - fit1_x['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
res1_fit_y = [ ( by[i] - fit1_y['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
res1_fit_z = [ ( bz[i] - fit1_z['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]

# Fit the residue with a sin function.

fit2_x = fit_sin( mfi_s, res1_fit_x )
fit2_y = fit_sin( mfi_s, res1_fit_y )
fit2_z = fit_sin( mfi_s, res1_fit_z )

# Calculate residue from fit-function.

res2_fit_x = [ ( res1_fit_x[i] - fit2_x['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
res2_fit_y = [ ( res1_fit_y[i] - fit2_y['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
res2_fit_z = [ ( res1_fit_z[i] - fit2_z['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]

# Fit the residue with a sin function.

fit2_x = fit_sin( mfi_s, res1_fit_x )
fit2_y = fit_sin( mfi_s, res1_fit_y )
fit2_z = fit_sin( mfi_s, res1_fit_z )

# Compute the final curve-fit value.

fitf_x = fit1_x['fitfunc'](ts) + fit2_x['fitfunc'](ts)
fitf_y = fit1_y['fitfunc'](ts) + fit2_y['fitfunc'](ts)
fitf_z = fit1_z['fitfunc'](ts) + fit2_z['fitfunc'](ts)

# Calculate residue from fit-function.

resf_fit_x = [ ( bx[i] - fitf_x[i] ) for i in range( len( mfi_s ) ) ]
resf_fit_y = [ ( by[i] - fitf_y[i] ) for i in range( len( mfi_s ) ) ]
resf_fit_z = [ ( bz[i] - fitf_z[i] ) for i in range( len( mfi_s ) ) ]

#print std(res1_fit_y), std(res2_fit_y)
#print std(res1_fit_z), std(res2_fit_z)

#print fit1_x['phase']
#print fit1_y['phase']
#print fit1_z['phase']

# Define the dictionary for all the residual values.

res = { 'res1_fft_x' : res1_fft_x, 'res1_fft_y' : res1_fft_y, 'res1_fft_z' : res1_fft_z,
        'res2_fft_x' : res2_fft_x, 'res2_fft_y' : res2_fft_y, 'res2_fft_z' : res2_fft_z,
        'resf_fft_x' : resf_fft_x, 'resf_fft_y' : resf_fft_y, 'resf_fft_z' : resf_fft_z,
        'res1_fit_x' : res1_fit_x, 'res1_fit_y' : res1_fit_y, 'res1_fit_z' : res1_fit_z,
        'res2_fit_x' : res2_fit_x, 'res2_fit_y' : res2_fit_y, 'res2_fit_z' : res2_fit_z,
        'resf_fit_x' : resf_fit_x, 'resf_fit_y' : resf_fit_y, 'resf_fit_z' : resf_fit_z }

std_res = { 'std1_fft_x' : std( res1_fft_x ), 'std1_fft_y' : std( res1_fft_y ), 'std1_fft_z' : std( res1_fft_z ),
            'std2_fft_x' : std( res2_fft_x ), 'std2_fft_y' : std( res2_fft_y ), 'std2_fft_z' : std( res2_fft_z ),
            'stdf_fft_x' : std( resf_fft_x ), 'stdf_fft_y' : std( resf_fft_y ), 'stdf_fft_z' : std( resf_fft_z ),
            'std1_fit_x' : std( res1_fit_x ), 'std1_fit_y' : std( res1_fit_y ), 'std1_fit_z' : std( res1_fit_z ),
            'std2_fit_x' : std( res2_fit_x ), 'std2_fit_y' : std( res2_fit_y ), 'std2_fit_z' : std( res2_fit_z ),
            'stdf_fit_x' : std( resf_fit_x ), 'stdf_fit_y' : std( resf_fit_y ), 'stdf_fit_z' : std( resf_fit_z ) }

#print std_res

plt.close('all')

fig, axs = plt.subplots( 2, 1, sharex = True )
fig.subplots_adjust(hspace=0)

#plt.figure( )
#axs[0].plot(mfi_s, bx, "-b", label="Data_x", linewidth=0.5)
#axs[0].plot( mfi_s, fit1_x["fitfunc"](ts), "r-", label="curve_fit", linewidth=0.5)
#axs[0].plot( mfi_s, bb1_x)
#axs[0].plot( mfi_s, ffit_x, 'k-', linestyle =  '-', label = 'Residue', linewidth = 0.5)
#axs[0].legend(loc="upper right")

axs[0].plot(mfi_s, by, "#868886", label="Data_y", linewidth=0.3)
#axs[0].plot( mfi_s, fit1_y["fitfunc"](ts), "r-", label="curve_fit", linewidth=0.5)
axs[0].plot( mfi_s, bb1_y,  'b-', label = 'FFT 1', linewidth = 0.3)
axs[0].plot( mfi_s, bb2_y,  'g-', label = 'FFT 2', linewidth = 0.3)
axs[0].plot( mfi_s, bbf_y,  'r-', label = 'FFT F', linewidth = 0.5)
#axs[0].plot( mfi_s, res1_fft_y, 'g-', label = 'RES 1', linewidth = 0.5)
#axs[0].plot( mfi_s, res2_fft_y, 'm-', label = 'RES 2', linewidth = 0.5)
#axs[0].plot( mfi_s, ffit_y, 'k-', linestyle =  '-', label = 'Residue', linewidth = 0.5)
axs[0].legend(loc="upper right")
axs[0].title.set_text('Magnetic field in y and z-direction (FFT)')

axs[1].plot(mfi_s, bz, "#868886", label="Data_z", linewidth=0.5)
#axs[0].plot( mfi_s, fit1_y["fitfunc"](ts), "r-", label="curve_fit", linewidth=0.5)
axs[1].plot( mfi_s, bb1_z,  'b-', label = 'FFT 1', linewidth = 0.5)
axs[1].plot( mfi_s, bb2_z,  'g-', label = 'FFT 2', linewidth = 0.5)
axs[1].plot( mfi_s, bbf_z,  'r-', label = 'FFT F', linewidth = 0.5)
#axs[0].plot( mfi_s, res1_fft_y, 'g-', label = 'RES 1', linewidth = 0.5)
#axs[0].plot( mfi_s, res2_fft_y, 'm-', label = 'RES 2', linewidth = 0.5)
#axs[0].plot( mfi_s, ffit_y, 'k-', linestyle =  '-', label = 'Residue', linewidth = 0.5)
axs[1].legend(loc="upper right")

fig, raxs = plt.subplots( 2, 1, sharex = True )
fig.subplots_adjust(hspace=0)

#raxs[0].plot( mfi_s, res1_fit_x, "r-", label="Residue1", linewidth=0.5)
#raxs[0].plot( mfi_s, res1_fit_x, "r-", label="Residue1", linewidth=0.5)
#raxs[0].plot( mfi_s, res1_fit_x, "r-", label="Residue1", linewidth=0.5)
##raxs[0].plot( mfi_s, res2_x, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
#raxs[0].legend(loc="upper right")

raxs[0].plot( mfi_s, res1_fft_y, "r-", label="Residue1", linewidth=0.5)
raxs[0].plot( mfi_s, res2_fft_y, "b-", label="Residue2", linewidth=0.5)
raxs[0].plot( mfi_s, resf_fft_y, "g-", label="Residuef", linewidth=0.5)
#raxs[0].plot( mfi_s, res2_y, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
raxs[0].legend(loc="upper right")
raxs[0].title.set_text('Residual of Magnetic field in y and z-direction (FFT)')

raxs[1].plot( mfi_s, res1_fft_z, "r-", label="Residue1", linewidth=0.5)
raxs[1].plot( mfi_s, res2_fft_z, "b-", label="Residue2", linewidth=0.5)
raxs[1].plot( mfi_s, resf_fft_z, "g-", label="Residuef", linewidth=0.5)
#raxs[1].plot( mfi_s, res2_z, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
raxs[1].legend(loc="upper right")
raxs[1].set_xlabel('Linear Frequency (Hz) ')

fig, faxs = plt.subplots( 2, 1, sharex = True )
fig.subplots_adjust(hspace=0)

faxs[0].plot(mfi_s, by,                "#868886", label="Data_y", linewidth=0.5)
faxs[0].plot( mfi_s, fit1_y["fitfunc"](ts), "b-", label="FIT 1",  linewidth=0.5)
faxs[0].plot( mfi_s, fit2_y["fitfunc"](ts), "g-", label="FIT 2",  linewidth=0.5)
faxs[0].plot( mfi_s, fitf_y,                "r-", label="FIT F",  linewidth=0.5)
faxs[0].legend(loc="upper right")
faxs[0].title.set_text('Magnetic field in y and z-direction (Curve Fit)')

faxs[1].plot(mfi_s, bz,                "#868886", label="Data_z", linewidth=0.5)
faxs[1].plot( mfi_s, fit1_z["fitfunc"](ts), "b-", label="FIT 1",  linewidth=0.5)
faxs[1].plot( mfi_s, fit2_z["fitfunc"](ts), "g-", label="FIT 2",  linewidth=0.5)
faxs[1].plot( mfi_s, fitf_z,                "r-", label="FIT F",  linewidth=0.5)
faxs[1].legend(loc="upper right")

fig, rfaxs = plt.subplots( 2, 1, sharex = True )
fig.subplots_adjust(hspace=0)

rfaxs[0].plot( mfi_s, res1_fit_y, "r-", label="Residue1", linewidth=0.5)
rfaxs[0].plot( mfi_s, res2_fit_y, "b-", label="Residue2", linewidth=0.5)
rfaxs[0].plot( mfi_s, resf_fit_y, "g-", label="Residuef", linewidth=0.5)
#rfaxs[0].plot( mfi_s, res2_y, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
rfaxs[0].legend(loc="upper right")
rfaxs[0].title.set_text('Residual of Magnetic field in y and z-direction (Curve Fit)')


rfaxs[1].plot( mfi_s, res1_fit_z, "r-", label="Residue1", linewidth=0.5)
rfaxs[1].plot( mfi_s, res2_fit_z, "b-", label="Residue2", linewidth=0.5)
rfaxs[1].plot( mfi_s, resf_fit_z, "g-", label="Residuef", linewidth=0.5)
#rfaxs[1].plot( mfi_s, res2_y, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
rfaxs[1].legend(loc="upper right")

plt.show( )

print 'Computation time = ','%.6f'% (time.time()-start), 'seconds.'
