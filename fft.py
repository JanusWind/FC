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
#
#f_x = rfft( bx )
#f_y = rfft( by )
#f_z = rfft( bz )
#
# Compute the standard deviation of magnetic field.

#davb = [ std( array( [ mfi_b_vec[i][j]
#         for i in range( len( mfi_b_vec ) ) ] ) )
#         for j in range( 3 )                         ]
#
#N = len( mfi_s )
# w = [ i / ( max( mfi_s ) ) for i in range( len( mfi_s ) ) ]
#w = rfftfreq( N, 1/11. )
#
#af_x = fft(bx)
#af_y = fft(by)
#af_z = fft(bz)
#
#pf_x = [ degrees( angle(af_x[i] ) ) for i in range( len( mfi_s ) ) ]
#pf_y = [ degrees( angle(af_y[i] ) ) for i in range( len( mfi_s ) ) ]
#pf_z = [ degrees( angle(af_z[i] ) ) for i in range( len( mfi_s ) ) ]
#
#saf_x = [af_x[i]**2 for i in range( len( f_x ) ) ]
#saf_y = [af_y[i]**2 for i in range( len( f_x ) ) ]
#saf_z = [af_z[i]**2 for i in range( len( f_x ) ) ]
#
#sf_x = [f_x[i]**2 for i in range( len( f_x ) ) ]
#sf_y = [f_y[i]**2 for i in range( len( f_x ) ) ]
#sf_z = [f_z[i]**2 for i in range( len( f_x ) ) ]
#
#gss_y = [ mean( mfi_b_y), 3*std( mfi_b_y )/sqrt( 2 ), 0.13, 0 ]
#
#def model( t, bt, db, omega, p ) :
##
#	return bt+db*cos( 2*pi*omega*t + p )
##
##( fitx, covarx ) = curve_fit( model, mfi_s, bx)
#( fity, covary ) = curve_fit( model, mfi_s, by, p0 = gss_y)
##( fitz, covarz ) = curve_fit( model, mfi_s, bz)
##
##bx_m = [ fitx[0]*mfi_s[i] + fitx[1]*cos( omega * mfi_s[i] + fitx[2] )
##                                     for i in range( len( mfi_s ) ) ]
#by_m = [ fity[0] + fity[1] * cos( 2*pi*fity[2] * mfi_s[i] + fity[3] )
#                                     for i in range( len( mfi_s ) ) ]
##bz_m = [ fity[0]*mfi_s[i] + 0.16*cos( omega * mfi_s[i] + fitz[2] )
##                                     for i in range( len( mfi_s ) ) ]
#
#byy = [ gss_y[0] + gss_y[1]*cos( 2*pi*gss_y[2]*mfi_s[i] + gss_y[3] )
#                                for i in range( len( mfi_s ) ) ]

# Define the time interval between measurements

dt = mfi_s[1] - mfi_s[0]

# Compute all the frequencies.

fq = rfftfreq( len( mfi_s ), d = dt )

# Compute the Fourier Transform of each component of magnetic field.

fbx = rfft( bx )
fby = rfft( by )
fbz = rfft( bz )

# Compute the absolute value of fourier transformed data.

afbx = abs( fbx**2 )
afby = abs( fby**2 )
afbz = abs( fbz**2 )

# Compute the index at which maximum frequency occurs.

max_ind_x = argmin( abs( afbx - max( afbx ) ) )
max_ind_y = argmin( abs( afby - max( afby ) ) )
max_ind_z = argmin( abs( afbz - max( afbz ) ) )

# Compute the value of maximum frequency.

fq_x = fq[ max_ind_x ]
fq_y = fq[ max_ind_y ]
fq_z = fq[ max_ind_z ]

ffbx = zeros_like( fbx ) 
ffby = zeros_like( fby ) 
ffbz = zeros_like( fbz ) 

ffbx[ max_ind_x ] = fby[ max_ind_x ]
ffby[ max_ind_y ] = fby[ max_ind_y ]
ffbz[ max_ind_z ] = fby[ max_ind_z ]

bbx = irfft( ffbx )
bby = irfft( ffby )
bbz = irfft( ffbz )

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

	return { "amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period":1./f,
	     "fitfunc": fitfunc, "maxcov": max(pcov), "rawres": (gss,popt,pcov)}

#	if( axes == 0 ) :
#		return res_x == {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period":1./f,
#		     "fitfunc": fitfunc, "maxcov": max(pcov), "rawres": (gss,popt,pcov)}
#
#	if( axes == 1 ) :
#		return res_y == {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period":1./f,
#		     "fitfunc": fitfunc, "maxcov": max(pcov), "rawres": (gss,popt,pcov)}
#
#	if( axes == 2 ) :
#		return res_z == {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period":1./f,
#		     "fitfunc": fitfunc, "maxcov": max(pcov), "rawres": (gss,popt,pcov)}

fit1_x = fit_sin( mfi_s, bx )
fit1_y = fit_sin( mfi_s, by )
fit1_z = fit_sin( mfi_s, bz )

ts = linspace(0, max( mfi_s ), len( mfi_s ) )

res1_x = [ ( bx[i] - fit1_x['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
res1_y = [ ( by[i] - fit1_y['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
res1_z = [ ( bz[i] - fit1_z['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]

fit2_x = fit_sin( mfi_s, res1_x )
fit2_y = fit_sin( mfi_s, res1_y )
fit2_z = fit_sin( mfi_s, res1_z )

#res2_x = [ ( bx[i] - ( fit1_x['fitfunc'](ts)[i] + fit2_x['fitfunc'](ts)[i] ) ) for i in range( len( mfi_s ) ) ]
#res2_y = [ ( by[i] - ( fit1_y['fitfunc'](ts)[i] + fit2_y['fitfunc'](ts)[i] ) ) for i in range( len( mfi_s ) ) ]
#res2_z = [ ( bz[i] - ( fit1_z['fitfunc'](ts)[i] + fit2_z['fitfunc'](ts)[i] ) ) for i in range( len( mfi_s ) ) ]

#ffit_x = [ ( fit1_x['fitfunc'](ts)[i] + fit2_x['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
#ffit_y = [ ( fit1_y['fitfunc'](ts)[i] + fit2_y['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]
#ffit_z = [ ( fit1_z['fitfunc'](ts)[i] + fit2_z['fitfunc'](ts)[i] ) for i in range( len( mfi_s ) ) ]

#ffit_x = [  ( fit1_x['fitfunc'](ts)[i] +
#              0.25*fit1_x['amp']*sin( 3*fit1_x['omega']*mfi_s[i] +
#              fit1_x['phase'] ) ) 
#                                                for i in range( len( mfi_s ) ) ]
#ffit_y = [  ( fit1_y['fitfunc'](ts)[i] +
#              0.5*fit1_y['amp']*sin( 3*fit1_y['omega']*mfi_s[i] +
#              fit1_y['phase'] ) + fit1_y['offset'] ) 
#                                                for i in range( len( mfi_s ) ) ]
#ffit_z = [  ( fit1_z['fitfunc'](ts)[i] +
#              0.5*fit1_z['amp']*sin( 3*fit1_z['omega']*mfi_s[i] +
#              fit1_z['phase'] ) + fit1_z['offset'] ) 
#                                                for i in range( len( mfi_s ) ) ]

#y2 = [ (0.5**1)*fit1_y['amp']*sin( 2*fit1_y['omega']*mfi_s[i] )
#              for i in range( len( mfi_s ) ) ]
#
#z2 = [ (0.5**1)*fit1_z['amp']*sin( 2*fit1_z['omega']*mfi_s[i] +
#              fit1_z['phase'] ) + fit1_z['offset']
#              for i in range( len( mfi_s ) ) ]
#
#y3 = [ (0.5**2)*fit1_y['amp']*sin( 3*fit1_y['omega']*mfi_s[i] )
#              for i in range( len( mfi_s ) ) ]
#
#z3 = [ (0.5**2)*fit1_z['amp']*sin( 3*fit1_z['omega']*mfi_s[i] +
#              fit1_z['phase'] ) + fit1_z['offset']
#              for i in range( len( mfi_s ) ) ]
#
#y4 = [ (0.5**3)*fit1_y['amp']*sin( 4*fit1_y['omega']*mfi_s[i] )
#              for i in range( len( mfi_s ) ) ]
#
#z4 = [ (0.5**3)*fit1_z['amp']*sin( 4*fit1_y['omega']*mfi_s[i] +
#              fit1_z['phase'] ) + fit1_y['offset']
#              for i in range( len( mfi_s ) ) ]
#
#ay_1 = map( add, fit1_y['fitfunc'](ts), y2 )
#az_1 = map( add, fit1_z['fitfunc'](ts), z2 )
#
#ay_2 = map( add, ay_1, y3 )
#az_2 = map( add, az_1, z3 )
#
#ffit_y = map( add, ay_2, y4 )
#ffit_z = map( add, az_2, z4 )

print fit1_x['phase']
print fit1_y['phase']
print fit1_z['phase']

plt.close('all')

fig, axs = plt.subplots( 3, 1, sharex = True )
fig.subplots_adjust(hspace=0)

#plt.figure( )
axs[0].plot(mfi_s, bx, "-b", label="Data_x", linewidth=0.5)
axs[0].plot( mfi_s, fit1_x["fitfunc"](ts), "r-", label="curve_fit", linewidth=0.5)
axs[0].plot( mfi_s, bbx)
#axs[0].plot( mfi_s, ffit_x, 'k-', linestyle =  '-', label = 'Residue', linewidth = 0.5)
axs[0].legend(loc="upper right")

axs[1].plot(mfi_s, by, "-b", label="Data_y", linewidth=0.5)
axs[1].plot( mfi_s, fit1_y["fitfunc"](ts), "r-", label="curve_fit", linewidth=0.5)
axs[1].plot( mfi_s, bby, 'k-', label = 'New Data', linewidth = 0.5)
#axs[1].plot( mfi_s, ffit_y, 'k-', linestyle =  '-', label = 'Residue', linewidth = 0.5)
axs[1].legend(loc="upper right")

axs[2].plot(mfi_s, bz, "-b", label="Data_z", linewidth=0.5)
axs[2].plot( mfi_s, fit1_z["fitfunc"](ts), "r-", label="curve_fit", linewidth=0.5)
axs[2].plot( mfi_s, bbz, 'k-', label = 'New Data', linewidth = 0.5)
#axs[2].plot( mfi_s, ffit_z, 'k-', linestyle =  '-', label = 'Residue', linewidth = 0.5)
axs[2].legend(loc="upper right")
axs[2].set_xlabel('Linear Frequency (Hz) ')
#plt.figure( )

fig, raxs = plt.subplots( 3, 1, sharex = True )
fig.subplots_adjust(hspace=0)

raxs[0].plot( mfi_s, res1_x, "r-", label="Residue1", linewidth=0.5)
#raxs[0].plot( mfi_s, res2_x, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
raxs[0].legend(loc="upper right")

raxs[1].plot( mfi_s, res1_y, "r-", label="Residue1", linewidth=0.5)
#raxs[1].plot( mfi_s, res2_y, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
raxs[1].legend(loc="upper right")

raxs[2].plot( mfi_s, res1_z, "r-", label="Residue1", linewidth=0.5)
#raxs[2].plot( mfi_s, res2_z, 'k-', linestyle =  '-', label = 'Residue2', linewidth = 0.5)
raxs[2].legend(loc="upper right")
raxs[2].set_xlabel('Linear Frequency (Hz) ')

#plt.plot( mfi_s, by, 'r' )
#plt.plot( mfi_s, by_m, 'b' )

#plt.figure( )
#plt.plot( mfi_s, mfi_b_y, 'r' )
#plt.plot( mfi_s, by_m, 'b' )
#plt.plot( mfi_s, byy, 'k')
#plt.show( )

#fig, axs = plt.subplots( 3, 2, sharex = 'col' )
#fig.subplots_adjust(hspace=0)
#
#axs[0,0].loglog( w[5:N//2], medfilt( abs( af_x[5:N//2] ), 5 ), 'r', label = 'f(x)' )
#axs[0,0].set_ylim( 10**(-1), 2*10**1 )
#axs[0,0].legend(loc="upper right")
#
#axs[1,0].loglog( w[5:N//2], medfilt( abs( af_y[5:N//2] ), 5 ), 'b', label = 'f(y)' )
##plt.loglog( w[5:N//2], saf_y[5:N//2], label = 'saf_y' )
#axs[1,0].set_ylim(10**(-1), 2*10**1)
#axs[1,0].legend(loc="upper right")
#
#axs[2,0].loglog( w[5:N//2], medfilt( abs( af_z[5:N//2] ), 5 ), 'k', label = 'f(z)' )
##plt.loglog( w[5:N//2], saf_z[5:N//2], label = 'saf_z' )
#axs[2,0].set_ylim(10**(-1), 2*10**1)
#axs[2,0].legend(loc="upper right")
#
#axs[0,1].semilogx( w[5:N//2], angle( af_x[5:N//2] ) )
#axs[1,1].semilogx( w[5:N//2], angle( af_y[5:N//2] ) )
#axs[2,1].semilogx( w[5:N//2], angle( af_z[5:N//2] ) )
#
#[ axs[j,0].axvline( 0.05, linestyle=':' ) for j in range( 3 ) ]
#[ axs[j,1].axvline( 0.05, linestyle=':' ) for j in range( 3 ) ]

#plt.figure( )
#plt.plot( mfi_s[0:20], mfi_b_y[0:20], label = 'mfi_b_y' )
#plt.plot( mfi_s[0:20], mfi_b_z[0:20], label = 'mfi_b_z' )


plt.show( )

print 'Computation time = ','%.6f'% (time.time()-start), 'seconds.'
