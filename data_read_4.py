import time
start = time.time()

import os
os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen

import glob
import pickle
import numpy as np
from numpy import mean, sqrt, corrcoef
import matplotlib.pyplot as plt
from matplotlib import gridspec
from pylab import rcParams
from scipy.optimize import curve_fit

from numpy import linspace, pi, sqrt, exp

from janus_const import const

rcParams['figure.figsize'] = 20, 10

#plt.clf()
plt.close('all')

fname1 = 'data_final_filter_01.jns'
fname2 = 'data_final_filter_11.jns'
fname3 = 'data_final_filter_21.jns'

i = 0

dat1   = [0]*len( fname1 )
dat2   = [0]*len( fname2 )
dat3   = [0]*len( fname3 )

dat1 = pickle.load( open( fname1, 'rb' ) )
dat2 = pickle.load( open( fname2, 'rb' ) )
dat3 = pickle.load( open( fname3, 'rb' ) )

# Find the total number of data points in all the files being analyzed.

nd1 = len( dat1['b0'] )
nd2 = len( dat2['b0'] )
nd3 = len( dat3['b0'] )

dat1_b_x_raw     = [None]*nd1
dat1_b_y_raw     = [None]*nd1
dat1_b_z_raw     = [None]*nd1
dat1_db          = [None]*nd1
dat1_db_x_raw    = [None]*nd1
dat1_db_y_raw    = [None]*nd1
dat1_db_z_raw    = [None]*nd1
dat1_db_raw      = [None]*nd1
dat1_b_x_rot     = [None]*nd1
dat1_b_y_rot     = [None]*nd1
dat1_b_z_rot     = [None]*nd1
dat1_b_y_sig_rot = [None]*nd1
dat1_b_z_sig_rot = [None]*nd1
dat1_sig_b_rot   = [None]*nd1
dat1_sig_bb      = [None]*nd1
dat1_fv_p        = [None]*nd1
dat1_sig_fv_p    = [None]*nd1
dat1_s_sig_fv_p  = [None]*nd1
dat1_alfvel      = [None]*nd1
dat1_s_fv        = [None]*nd1
dat1_ogyro       = [None]*nd1
dat1_ocycl       = [None]*nd1
dat1_thr_slp     = [None]*nd1
dat1_vmag        = [None]*nd1
dat1_vsig        = [None]*nd1
dat1_n           = [None]*nd1
dat1_nsig        = [None]*nd1
dat1_bmag        = [None]*nd1
dat1_bsig        = [None]*nd1
dat1_m           = [None]*nd1
dat1_rat         = [None]*nd1
time1            = [None]*nd1

dat2_b_x_raw     = [None]*nd2
dat2_b_y_raw     = [None]*nd2
dat2_b_z_raw     = [None]*nd2
dat2_db          = [None]*nd2
dat2_db_x_raw    = [None]*nd2
dat2_db_y_raw    = [None]*nd2
dat2_db_z_raw    = [None]*nd2
dat2_db_raw      = [None]*nd2
dat2_b_x_rot     = [None]*nd2
dat2_b_y_rot     = [None]*nd2
dat2_b_z_rot     = [None]*nd2
dat2_b_y_sig_rot = [None]*nd2
dat2_b_z_sig_rot = [None]*nd2
dat2_sig_b_rot   = [None]*nd2
dat2_sig_bb      = [None]*nd2
dat2_fv_p        = [None]*nd2
dat2_sig_fv_p    = [None]*nd2
dat2_s_sig_fv_p  = [None]*nd2
dat2_alfvel      = [None]*nd2
dat2_s_fv        = [None]*nd2
dat2_ogyro       = [None]*nd2
dat2_ocycl       = [None]*nd2
dat2_thr_slp     = [None]*nd2
dat2_vmag        = [None]*nd2
dat2_vsig        = [None]*nd2
dat2_n           = [None]*nd2
dat2_nsig        = [None]*nd2
dat2_bmag        = [None]*nd2
dat2_bsig        = [None]*nd2
dat2_m           = [None]*nd2
dat2_rat         = [None]*nd2
time2            = [None]*nd2

dat3_b_x_raw     = [None]*nd3
dat3_b_y_raw     = [None]*nd3
dat3_b_z_raw     = [None]*nd3
dat3_db          = [None]*nd3
dat3_db_x_raw    = [None]*nd3
dat3_db_y_raw    = [None]*nd3
dat3_db_z_raw    = [None]*nd3
dat3_db_raw      = [None]*nd3
dat3_b_x_rot     = [None]*nd3
dat3_b_y_rot     = [None]*nd3
dat3_b_z_rot     = [None]*nd3
dat3_b_y_sig_rot = [None]*nd3
dat3_b_z_sig_rot = [None]*nd3
dat3_sig_b_rot   = [None]*nd3
dat3_sig_bb      = [None]*nd3
dat3_fv_p        = [None]*nd3
dat3_sig_fv_p    = [None]*nd3
dat3_s_sig_fv_p  = [None]*nd3
dat3_alfvel      = [None]*nd3
dat3_s_fv        = [None]*nd3
dat3_ogyro       = [None]*nd3
dat3_ocycl       = [None]*nd3
dat3_thr_slp     = [None]*nd3
dat3_vmag        = [None]*nd3
dat3_vsig        = [None]*nd3
dat3_n           = [None]*nd3
dat3_nsig        = [None]*nd3
dat3_bmag        = [None]*nd3
dat3_bsig        = [None]*nd3
dat3_m           = [None]*nd3
dat3_rat         = [None]*nd3
time3            = [None]*nd3


################################################################################
## For data set 1 of filter size 01.
################################################################################

for j in range( nd1 ) :

	time1[j] = dat1['time'][j].time().strftime("%H-%M")

	dat1_b_x_raw[j] = mean( np.array( dat1['b0_fields'][j]['raw_smt'] )[0] )

	dat1_b_y_raw[j] = mean( np.array( dat1['b0_fields'][j]['raw_smt'] )[1] )

	dat1_b_z_raw[j] = mean( np.array( dat1['b0_fields'][j]['raw_smt'] )[2] )

	dat1_b_x_rot[j] = mean( np.array( dat1['b0_fields'][j]['rot_smt'] )[0] )

	dat1_b_y_rot[j] = mean( np.array( dat1['b0_fields'][j]['rot_smt'] )[1] )

	dat1_b_z_rot[j] = mean( np.array( dat1['b0_fields'][j]['rot_smt'] )[2] )

	dat1_db_x_raw = [ dat1['b0_fields'][j]['raw_smt'][0][k] - dat1_b_x_raw[j]
	                            for k in range( len(
	                                dat1['b0_fields'][j]['raw_smt'][0] ) ) ]

	dat1_db_y_raw = [ dat1['b0_fields'][j]['raw_smt'][1][k] - dat1_b_y_raw[j]
	                            for k in range( len( 
	                                 dat1['b0_fields'][j]['raw_smt'][0]) ) ]

	dat1_db_z_raw = [ dat1['b0_fields'][j]['raw_smt'][2][k] - dat1_b_z_raw[j]
	                            for k in range( len( 
	                                dat1['b0_fields'][j]['raw_smt'][0] ) ) ]

	dat1_db[j]    = sum( [ sqrt( dat1_db_x_raw[k]**2 + dat1_db_y_raw[k]**2 +
	                             dat1_db_z_raw[k]**2  )
	                            for k in range( len( dat1_db_x_raw ) ) ] )/(
	                len( dat1_db_x_raw )*( sqrt( dat1_b_x_raw[j]**2 +
	                           dat1_b_y_raw[j]**2 + dat1_b_z_raw[j]**2 ) ) )

	dat1_b_y_sig_rot[j] = np.array(
	                            dat1['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat1_b_z_sig_rot[j] = np.array(
	                            dat1['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat1_sig_b_rot[j] = sqrt(
	                       dat1_b_y_sig_rot[j]**2 + dat1_b_z_sig_rot[j]**2 )

	dat1_sig_bb[j] = dat1_sig_b_rot[j] / dat1_b_x_rot[j]

	dat1_fv_p[j] = dat1['fv_p'][j]

	dat1_sig_fv_p[j] = dat1['sig_fv_p'][j]

	dat1_alfvel[j] = dat1['alfvel_p'][j]

	dat1_s_fv[j] = dat1_fv_p[j]/dat1_alfvel[j] * (
	                             1 - dat1['ocycl_p'][j]/dat1['ogyro_p'][j] )

	dat1_s_sig_fv_p[j] = dat1_sig_fv_p[j]/dat1_alfvel[j] * (
	                             1 - dat1['ocycl_p'][j]/dat1['ogyro_p'][j] )

	dat1_ogyro[j] = dat1['ogyro_p'][j]

	dat1_ocycl[j] = dat1['ocycl_p'][j]

	dat1_thr_slp[j] = 1/( 1 - dat1_ocycl[j]/dat1_ogyro[j] )

	dat1_vmag[j] = dat1['v0'][j]

	dat1_vsig[j] = sqrt( dat1['sig_v0_x'][j]**2 + dat1['sig_v0_y'][j]**2 +
	                     dat1['sig_v0_z'][j]**2                         )

	dat1_n[j]    = dat1['n_p'][j]

	dat1_nsig[j] = dat1['sig_n_p_c'][j] + dat1['sig_n_p_c'][j]

	dat1_bmag[j] = dat1['b0'][j]

	dat1_bsig[j] = dat1['sig_b0'][j]

	dat1_m[j]    = ( dat1_vsig[j]/dat1_vmag[j] + 0.5*dat1_nsig[j]/dat1_n[j] 
	                + 3*dat1_bsig[j]/dat1_bmag[j] )

	dat1_vmag[j] = dat1['v0'][j]

	dat1_vsig[j] = sqrt( dat1['sig_v0_x'][j]**2 + dat1['sig_v0_y'][j]**2 +
	                     dat1['sig_v0_z'][j]**2                         )

	dat1_n[j]    = dat1['n_p'][j]

	dat1_nsig[j] = dat1['sig_n_p_c'][j] + dat1['sig_n_p_c'][j]

	dat1_bmag[j] = dat1['b0'][j]

	dat1_bsig[j] = dat1['sig_b0'][j]

# Define the linear model to fit the data.

def fitlin( b1, v1, sigma1 ) :

	def linfunc( b1, m1, c1 ) :

		return m1 * b1 + c1

	sigma1 = np.ones(len(b1))
	sigma1[ -1]= 1.E-5
	popt1, pcov1 = curve_fit( linfunc, b1, v1, sigma=sigma1 )
	m1, c1 = popt1

	fitfunc = lambda b1: m1 * b1 + c1

	return { "slope"   : m1,
	         "offset"  : c1,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt1,pcov1 ) }

dat1_db.pop( -7 )
dat1_s_fv.pop( -7 )
dat1_s_sig_fv_p.pop( -7 )

dat1_db.append( 0 )
dat1_s_fv.append( 0 )
dat1_s_sig_fv_p.append( 0 )

dat1_fit = fitlin( dat1_db, dat1_s_fv, dat1_s_sig_fv_p )

# Define list of index.

ind1 = linspace( 0., max( dat1_db ), len( dat1_db ) )

# Extract the slope and intercept.

m1 = dat1_fit['slope']
c1 = dat1_fit['offset']

slope1 = r'$ m \pm del_m$'

y1_fit_dat = [ ( m1*ind1[i] + c1 ) for i in range( len( dat1_db ) ) ]

y1_fit_thr = [ ( mean(dat1_thr_slp)*ind1[i] ) for i in range( len( dat1_db ) ) ]

fit1_x = dat1_fit['fitfunc'](ind1)

cv1 = corrcoef( dat1_db[0:-1], dat1_s_fv[0:-1] )[0,1]

dat1_thr = [ dat1_db[i] * dat1_thr_slp[i] for i in range( len( dat1_db )-1 ) ]

################################################################################
## For data set 2 of filter size 11.
################################################################################

for j in range( nd2 ) :

	time2[j] = dat2['time'][j].time().strftime("%H-%M")

	dat2_b_x_raw[j] = mean( np.array( dat2['b0_fields'][j]['raw_smt'] )[0] )

	dat2_b_y_raw[j] = mean( np.array( dat2['b0_fields'][j]['raw_smt'] )[1] )

	dat2_b_z_raw[j] = mean( np.array( dat2['b0_fields'][j]['raw_smt'] )[2] )

	dat2_b_x_rot[j] = mean( np.array( dat2['b0_fields'][j]['rot_smt'] )[0] )

	dat2_b_y_rot[j] = mean( np.array( dat2['b0_fields'][j]['rot_smt'] )[1] )

	dat2_b_z_rot[j] = mean( np.array( dat2['b0_fields'][j]['rot_smt'] )[2] )

	dat2_db_x_raw = [ dat2['b0_fields'][j]['raw_smt'][0][k] - dat2_b_x_raw[j]
	                            for k in range( len(
	                                dat2['b0_fields'][j]['raw_smt'][0] ) ) ]

	dat2_db_y_raw = [ dat2['b0_fields'][j]['raw_smt'][1][k] - dat2_b_y_raw[j]
	                            for k in range( len( 
	                                 dat2['b0_fields'][j]['raw_smt'][0]) ) ]

	dat2_db_z_raw = [ dat2['b0_fields'][j]['raw_smt'][2][k] - dat2_b_z_raw[j]
	                            for k in range( len( 
	                                dat2['b0_fields'][j]['raw_smt'][0] ) ) ]

	dat2_db[j]    = sum( [ sqrt( dat2_db_x_raw[k]**2 + dat2_db_y_raw[k]**2 +
	                             dat2_db_z_raw[k]**2  )
	                            for k in range( len( dat2_db_x_raw ) ) ] )/(
	                len( dat2_db_x_raw )*( sqrt( dat2_b_x_raw[j]**2 +
	                           dat2_b_y_raw[j]**2 + dat2_b_z_raw[j]**2 ) ) )

	dat2_b_y_sig_rot[j] = np.array(
	                            dat2['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat2_b_z_sig_rot[j] = np.array(
	                            dat2['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat2_sig_b_rot[j] = sqrt(
	                       dat2_b_y_sig_rot[j]**2 + dat2_b_z_sig_rot[j]**2 )

	dat2_sig_bb[j] = dat2_sig_b_rot[j] / dat2_b_x_rot[j]

	dat2_fv_p[j] = dat2['fv_p'][j]

	dat2_sig_fv_p[j] = dat2['sig_fv_p'][j]

	dat2_alfvel[j] = dat2['alfvel_p'][j]

	dat2_s_fv[j] = dat2_fv_p[j]/dat2_alfvel[j] * (
	                             1 - dat2['ocycl_p'][j]/dat2['ogyro_p'][j] )

	dat2_s_sig_fv_p[j] = dat2_sig_fv_p[j]/dat2_alfvel[j] * (
	                             1 - dat2['ocycl_p'][j]/dat2['ogyro_p'][j] )

	dat2_ogyro[j] = dat2['ogyro_p'][j]

	dat2_ocycl[j] = dat2['ocycl_p'][j]

	dat2_thr_slp[j] = 1/( 1 - dat2_ocycl[j]/dat2_ogyro[j] )

	dat2_vmag[j] = dat2['v0'][j]

	dat2_vsig[j] = sqrt( dat2['sig_v0_x'][j]**3 + dat2['sig_v0_y'][j]**3 +
	                     dat2['sig_v0_z'][j]**3                         )

	dat2_n[j]    = dat2['n_p'][j]

	dat2_nsig[j] = dat2['sig_n_p_c'][j] + dat2['sig_n_p_c'][j]

	dat2_bmag[j] = dat2['b0'][j]

	dat2_bsig[j] = dat2['sig_b0'][j]

	dat2_m[j]    = ( dat2_vsig[j]/dat2_vmag[j] + 0.5*dat2_nsig[j]/dat2_n[j] 
	                + 3*dat2_bsig[j]/dat2_bmag[j] )

	dat2_vmag[j] = dat2['v0'][j]

	dat2_vsig[j] = sqrt( dat2['sig_v0_x'][j]**2 + dat2['sig_v0_y'][j]**2 +
	                     dat2['sig_v0_z'][j]**2                         )

	dat2_n[j]    = dat2['n_p'][j]

	dat2_nsig[j] = dat2['sig_n_p_c'][j] + dat2['sig_n_p_c'][j]

	dat2_bmag[j] = dat2['b0'][j]

	dat2_bsig[j] = dat2['sig_b0'][j]

# Define the linear model to fit the data.

def fitlin( b2, v2, sigma2 ) :

	def linfunc( b2, m2, c2 ) :

		return m2 * b2 + c2

	sigma2 = np.ones(len(b2))
	sigma2[ -1]= 1.E-5
#	sigma4[ -3]= 1.E1
	popt2, pcov2 = curve_fit( linfunc, b2, v2, sigma=sigma2 )
	m2, c2 = popt2

	fitfunc = lambda b2: m2 * b2 + c2

	return { "slope"   : m2,
	         "offset"  : c2,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt2,pcov2 ) }

dat2_db.pop( -7 )
dat2_s_fv.pop( -7 )
dat2_s_sig_fv_p.pop( -7 )

dat2_db.append( 0 )
dat2_s_fv.append( 0 )
dat2_s_sig_fv_p.append( 0 )

dat2_fit = fitlin( dat2_db, dat2_s_fv, dat2_s_sig_fv_p )

# Define list of index.

ind2 = linspace( 0., max( dat2_db ), len( dat2_db ) )

# Extract the slope and intercept.

m2 = dat2_fit['slope']
c2 = dat2_fit['offset']

slope2 = r'$ m \pm del_m$'

y2_fit_dat = [ ( m2*ind2[i] + c2 ) for i in range( len( dat2_db ) ) ]

y2_fit_thr = [ ( mean(dat2_thr_slp)*ind2[i] ) for i in range( len( dat2_db ) ) ]

fit2_x = dat2_fit['fitfunc'](ind2)

cv2 = corrcoef( dat2_db[0:-1], dat2_s_fv[0:-1] )[0,1]

dat2_thr = [ dat2_db[i] * dat2_thr_slp[i] for i in range( len( dat2_db )-1 ) ]

################################################################################
## For data set 3 of filter size 21.
################################################################################

for j in range( nd3 ) :

	time3[j] = dat3['time'][j].time().strftime("%H-%M")

	dat3_b_x_raw[j] = mean( np.array( dat3['b0_fields'][j]['raw_smt'] )[0] )

	dat3_b_y_raw[j] = mean( np.array( dat3['b0_fields'][j]['raw_smt'] )[1] )

	dat3_b_z_raw[j] = mean( np.array( dat3['b0_fields'][j]['raw_smt'] )[2] )

	dat3_b_x_rot[j] = mean( np.array( dat3['b0_fields'][j]['rot_smt'] )[0] )

	dat3_b_y_rot[j] = mean( np.array( dat3['b0_fields'][j]['rot_smt'] )[1] )

	dat3_b_z_rot[j] = mean( np.array( dat3['b0_fields'][j]['rot_smt'] )[2] )

	dat3_db_x_raw = [ dat3['b0_fields'][j]['raw_smt'][0][k] - dat3_b_x_raw[j]
	                            for k in range( len(
	                                dat3['b0_fields'][j]['raw_smt'][0] ) ) ]

	dat3_db_y_raw = [ dat3['b0_fields'][j]['raw_smt'][1][k] - dat3_b_y_raw[j]
	                            for k in range( len( 
	                                 dat3['b0_fields'][j]['raw_smt'][0]) ) ]

	dat3_db_z_raw = [ dat3['b0_fields'][j]['raw_smt'][2][k] - dat3_b_z_raw[j]
	                            for k in range( len( 
	                                dat3['b0_fields'][j]['raw_smt'][0] ) ) ]

	dat3_db[j]    = sum( [ sqrt( dat3_db_x_raw[k]**2 + dat3_db_y_raw[k]**2 +
	                             dat3_db_z_raw[k]**2  )
	                            for k in range( len( dat3_db_x_raw ) ) ] )/(
	                len( dat3_db_x_raw )*( sqrt( dat3_b_x_raw[j]**2 +
	                           dat3_b_y_raw[j]**2 + dat3_b_z_raw[j]**2 ) ) )

	dat3_b_y_sig_rot[j] = np.array(
	                            dat3['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat3_b_z_sig_rot[j] = np.array(
	                            dat3['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat3_sig_b_rot[j] = sqrt(
	                       dat3_b_y_sig_rot[j]**2 + dat3_b_z_sig_rot[j]**2 )

	dat3_sig_bb[j] = dat3_sig_b_rot[j] / dat3_b_x_rot[j]

	dat3_fv_p[j] = dat3['fv_p'][j]

	dat3_sig_fv_p[j] = dat3['sig_fv_p'][j]

	dat3_alfvel[j] = dat3['alfvel_p'][j]

	dat3_s_fv[j] = dat3_fv_p[j]/dat3_alfvel[j] * (
	                             1 - dat3['ocycl_p'][j]/dat3['ogyro_p'][j] )

	dat3_s_sig_fv_p[j] = dat3_sig_fv_p[j]/dat3_alfvel[j] * (
	                             1 - dat3['ocycl_p'][j]/dat3['ogyro_p'][j] )

	dat3_ogyro[j] = dat3['ogyro_p'][j]

	dat3_ocycl[j] = dat3['ocycl_p'][j]

	dat3_thr_slp[j] = 1/( 1 - dat3_ocycl[j]/dat3_ogyro[j] )

	dat3_vmag[j] = dat3['v0'][j]

	dat3_vsig[j] = sqrt( dat3['sig_v0_x'][j]**3 + dat3['sig_v0_y'][j]**3 +
	                     dat3['sig_v0_z'][j]**3                         )

	dat3_n[j]    = dat3['n_p'][j]

	dat3_nsig[j] = dat3['sig_n_p_c'][j] + dat3['sig_n_p_c'][j]

	dat3_bmag[j] = dat3['b0'][j]

	dat3_bsig[j] = dat3['sig_b0'][j]

	dat3_m[j]    = ( dat3_vsig[j]/dat3_vmag[j] + 0.5*dat3_nsig[j]/dat3_n[j] 
	                + 3*dat3_bsig[j]/dat3_bmag[j] )

	dat3_vmag[j] = dat3['v0'][j]

	dat3_vsig[j] = sqrt( dat3['sig_v0_x'][j]**2 + dat3['sig_v0_y'][j]**2 +
	                     dat3['sig_v0_z'][j]**2                         )

	dat3_n[j]    = dat3['n_p'][j]

	dat3_nsig[j] = dat3['sig_n_p_c'][j] + dat3['sig_n_p_c'][j]

	dat3_bmag[j] = dat3['b0'][j]

	dat3_bsig[j] = dat3['sig_b0'][j]

# Define the linear model to fit the data.

def fitlin( b3, v3, sigma3 ) :

	def linfunc( b3, m3, c3 ) :

		return m3 * b3 + c3

	sigma3 = np.ones(len(b3))
	sigma3[ -1]= 1.E-5
#	sigma4[ -3]= 1.E1
	popt3, pcov3 = curve_fit( linfunc, b3, v3, sigma=sigma3 )
	m3, c3 = popt3

	fitfunc = lambda b3: m3 * b3 + c3

	return { "slope"   : m3,
	         "offset"  : c3,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt3,pcov3 ) }

dat3_db.pop( -7 )
dat3_s_fv.pop( -7 )
dat3_s_sig_fv_p.pop( -7 )

dat3_db.append( 0 )
dat3_s_fv.append( 0 )
dat3_s_sig_fv_p.append( 0 )

dat3_fit = fitlin( dat3_db, dat3_s_fv, dat3_s_sig_fv_p )

# Define list of index.

ind3 = linspace( 0., max( dat3_db ), len( dat3_db ) )

# Extract the slope and intercept.

m3 = dat3_fit['slope']
c3 = dat3_fit['offset']

slope3 = r'$ m \pm del_m$'

y3_fit_dat = [ ( m3*ind3[i] + c3 ) for i in range( len( dat3_db ) ) ]

y3_fit_thr = [ ( mean(dat3_thr_slp)*ind3[i] ) for i in range( len( dat3_db ) ) ]

fit3_x = dat3_fit['fitfunc'](ind3)

cv3 = corrcoef( dat3_db[0:-1], dat3_s_fv[0:-1] )[0,1]

dat3_thr = [ dat3_db[i] * dat3_thr_slp[i] for i in range( len( dat3_db )-1 ) ]

################################################################################
## Plotting figures: Data Set 1
################################################################################

plt.figure( )

plt.errorbar( dat1_db[0:-1], dat1_s_fv[0:-1], yerr=dat1_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind1, y1_fit_dat, color='r' )
plt.plot( ind1, y1_fit_thr, dashes=[1,1], color='m' )
plt.scatter( dat1_db[0:-1], dat1_thr, marker='*', color='r')

plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)
plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)

plt.text( 0.0, -0.003, 'Slope =' '%s' r'$\pm$' '%s'
%( round( m1, 2 ), round( mean( dat1_m ), 2 ) ), fontsize = 24 )

plt.xlabel( r'$\left< \Delta \vec {B}/|\vec B|\right >$', fontsize = 24 )
plt.ylabel( r'$\delta v/v_A$', fontsize = 24 )

#leg1 = [ 'Linear Fit', 'Theoretical Data', 'Observations' ]
#plt.legend( leg1, loc = 2, fontsize = 30 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error
#bars', fontsize = 24 )
plt.tight_layout()

plt.savefig('fv_delb_fz01', format='eps', dpi=44000)

#plt.show( )

################################################################################
## Plotting figures: Data Set 2
################################################################################

plt.figure( )

plt.errorbar( dat2_db[0:-1], dat2_s_fv[0:-1], yerr=dat2_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind2, y2_fit_dat, color='r' )
plt.plot( ind2, y2_fit_thr, dashes=[6,2], color='m' )
plt.scatter( dat2_db[0:-1], dat2_thr, marker='*', color='r')

plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)
plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)

plt.text( 0.0, -0.003, 'Slope =' '%s' r'$\pm$' '%s'
%( round( m2, 2 ), round( mean( dat2_m ), 2 ) ), fontsize = 24 )

plt.xlabel( r'$\left< \Delta \vec {B}/|\vec B|\right >$', fontsize = 24 )
plt.ylabel( r'$\delta v/v_A$', fontsize = 24 )

#leg2 = [ 'Linear Fit', 'Theoretical Data', 'Observations' ]
#plt.legend( leg2, loc = 2, fontsize = 24 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error
#bars', fontsize = 24 )
plt.tight_layout()

plt.savefig('fv_delb_fz11', format='eps', dpi=4000)

#plt.show( )

################################################################################
## Plotting figures: Data Set 3
################################################################################

plt.figure( )

plt.errorbar( dat3_db[0:-1], dat3_s_fv[0:-1], yerr=dat3_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind3, y3_fit_dat, color='r' )
plt.plot( ind3, y3_fit_thr, dashes=[4,2], color='m' )
plt.scatter( dat3_db[0:-1], dat3_thr, marker='*', color='r')

plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)
plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)

plt.text( 0.0, -0.003, 'Slope =' '%s' r'$\pm$' '%s'
%( round( m3, 2 ), round( mean( dat3_m ), 2 ) ), fontsize = 24 )

plt.xlabel( r'$\left< \Delta \vec {B}/|\vec B|\right >$', fontsize = 24 )
plt.ylabel( r'$\delta v/v_A$', fontsize = 24 )

#leg3 = [ 'Linear Fit', 'Theoretical Data', 'Observations' ]
#plt.legend( leg3, loc = 2, fontsize = 24 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error
#bars', fontsize = 24 )
plt.tight_layout()

plt.savefig('fv_delb_fz21', format='eps', dpi=4000)

#plt.show( )

print ('It took','%.6f'% (time.time()-start), 'seconds.')#plt,show()
