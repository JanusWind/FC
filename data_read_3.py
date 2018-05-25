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

#fname1 = 'fm_22.jns'
#fname2 = 'fm_14.jns'
#fname3 = 'ms_14.jns'

fname1 = 'dat_auto_run_11.jns'
fname2 = 'dat_non_auto_run_11.jns' 
fname3 = 'dat_auto_run_22.jns' 

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

################################################################################
## Auto-Run: Filter size = 11
################################################################################

for j in range( nd1 ) :

	dat1_b_x_rot = np.array( dat1['b0_fields'][j]['rot_smt'] )[0]

	dat1_b_y_sig_rot[j] = np.array(
	                           dat1['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat1_b_z_sig_rot[j] = np.array(
	                           dat1['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat1_sig_b_rot[j] = sqrt(
	                      dat1_b_y_sig_rot[j]**2 + dat1_b_z_sig_rot[j]**2 )

	dat1_sig_bb[j] = dat1_sig_b_rot[j] / mean( dat1_b_x_rot )

	dat1_fv_p[j] = dat1['fv_p'][j]

	dat1_sig_fv_p[j] = dat1['sig_fv_p'][j]

	dat1_alfvel[j] = dat1['alfvel_p'][j]

	dat1_s_fv[j] = ( dat1_fv_p[j]/dat1_alfvel[j] ) * (
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
	                + 2*dat1_bsig[j]/dat1_bmag[j] )

	dat1_rat[j]  = ( 1 - dat1_ocycl[j]/dat1_ogyro[j] )

# Define the linear model to fit the data.

def fitlin( b1, v1, sigma1 ) :

	def linfunc( b, m1, c1 ) :

		return m1 * b + c1

	sigma1 = np.ones(len(b1))
	sigma1[ -1]= 1.E-5
#	sigma[ -3]= 1.E1
	popt1, pcov1 = curve_fit( linfunc, b1, v1, sigma=sigma1 )
	m1, c1 = popt1

	fitfunc = lambda b1: m1 * b1 + c1

	return { "slope"   : m1,
	         "offset"  : c1,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt1,pcov1 ) }

################################################################################
## Non-Auto-Run: Filter size = 11
################################################################################


for j in range( nd2 ) :

	dat2_b_x_rot = np.array( dat2['b0_fields'][j]['rot_smt'] )[0]

	dat2_b_y_sig_rot[j] = np.array(
	                            dat2['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat2_b_z_sig_rot[j] = np.array(
	                            dat2['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat2_sig_b_rot[j] = sqrt(
	                       dat2_b_y_sig_rot[j]**2 + dat2_b_z_sig_rot[j]**2 )

	dat2_sig_bb[j] = dat2_sig_b_rot[j] / mean( dat2_b_x_rot )

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

	dat2_vsig[j] = sqrt( dat2['sig_v0_x'][j]**2 + dat2['sig_v0_y'][j]**2 +
	                     dat2['sig_v0_z'][j]**2                         )

	dat2_n[j]    = dat2['n_p'][j]

	dat2_nsig[j] = dat2['sig_n_p_c'][j] + dat2['sig_n_p_c'][j]

	dat2_bmag[j] = dat2['b0'][j]

	dat2_bsig[j] = dat2['sig_b0'][j]

	dat2_m[j]    = ( dat2_vsig[j]/dat2_vmag[j] + 0.5*dat2_nsig[j]/dat2_n[j] 
	                + 2*dat2_bsig[j]/dat2_bmag[j] )

# Define the linear model to fit the data.

def fitlin( b2, v2, sigma2 ) :

	def linfunc( b2, m2, c2 ) :

		return m2 * b2 + c2

	sigma2 = np.ones(len(b2))
	sigma2[ -1]= 1.E-5
#	sigma2[ -3]= 1.E1
	popt2, pcov2 = curve_fit( linfunc, b2, v2, sigma=sigma2 )
	m2, c2 = popt2

	fitfunc = lambda b2: m2 * b2 + c2

	return { "slope"   : m2,
	         "offset"  : c2,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt2,pcov2 ) }

################################################################################
## Auto-Run: Filter size = 22
################################################################################

for j in range( nd3 ) :

	dat3_b_x_rot = np.array( dat3['b0_fields'][j]['rot_smt'] )[0]

	dat3_b_y_sig_rot[j] = np.array(
	                            dat3['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat3_b_z_sig_rot[j] = np.array(
	                            dat3['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat3_sig_b_rot[j] = sqrt(
	                       dat3_b_y_sig_rot[j]**3 + dat3_b_z_sig_rot[j]**3 )

	dat3_sig_bb[j] = dat3_sig_b_rot[j] / mean( dat3_b_x_rot )

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

# Define the linear model to fit the data.

def fitlin( b3, v3, sigma3 ) :

	def linfunc( b3, m3, c3 ) :

		return m3 * b3 + c3

	sigma3 = np.ones(len(b3))
	sigma3[ -1]= 1.E-5
#	sigma3[ -3]= 1.E1
	popt3, pcov3 = curve_fit( linfunc, b3, v3, sigma=sigma3 )
	m3, c3 = popt3

	fitfunc = lambda b3: m3 * b3 + c3

	return { "slope"   : m3,
	         "offset"  : c3,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt3,pcov3 ) }

################################################################################
## Everything for first data set.
################################################################################

dat1_sig_bb.append(0)
dat1_s_fv.append(0)
dat1_s_sig_fv_p.append(0)

dat1_sig_bb.pop(-3)
dat1_s_fv.pop(-3)
dat1_s_sig_fv_p.pop(-3)

dat1_sig_bb.pop(-5)
dat1_s_fv.pop(-5)
dat1_s_sig_fv_p.pop(-5)

dat1_fit = fitlin( dat1_sig_bb, dat1_s_fv, dat1_s_sig_fv_p )

# Define list of index.

ind1 = linspace( 0., max( dat1_sig_bb ), len( dat1_sig_bb ) )

# Extract the slope and intercept.

m1 = dat1_fit['slope']
c1 = dat1_fit['offset']

dat1_m = mean( np.array( dat1_vsig )/dat1_vmag + 0.5*np.array( dat1_nsig )/dat1_n
          + 2*np.array( dat1_bsig )/dat1_bmag )

slope1 = r'$ m \pm del_m$'

y1_fit = [ ( m1*ind1[i] + c1 ) for i in range( len( dat1_sig_bb ) ) ]

fit1_x = dat1_fit['fitfunc'](ind1)

cv1 = corrcoef( dat1_sig_bb[0:-1], dat1_s_fv[0:-1] )[0,1]

#dat1_thr = [ dat1_sig_bb[i] * dat1_thr_slp[i]
#                                        for i in range( len( dat1_sig_bb )-1 ) ]

#plt.figure( )

plt.errorbar( range( len( dat1_s_fv ) ), dat1_s_fv, dat1_s_sig_fv_p,fmt='D',
                                                    ecolor = 'b', color = 'b'  )

#plt.errorbar( dat1_sig_bb[0:-1], dat1_s_fv[0:-1], yerr=dat1_s_sig_fv_p[0:-1],
#                                                           fmt='o', ecolor='g' )
#plt.plot( ind1, y1_fit )
#plt.plot( ind1, y3_fit, dashes=[6,2], color='m')
#plt.scatter(dat1_sig_bb[0:-1], dat1_thr, marker='*', color='r')

#plt.xticks([0, 0.02, 0.04, 0.05], fontsize=20)
#plt.yticks([0, 0.02, 0.04, 0.05], fontsize=20)
#
#plt.ylim( 0, 0.055 )
##plt.ylim( ( min( dat1_s_fv ) + 0.1*min( dat1_s_fv ),
##          ( max( dat1_s_fv ) + 0.1*max( dat1_s_fv ) ) ) )
#plt.xlim( 0, 0.055 )
##plt.xlim(( 0., ( max( dat1_sig_bb )+ 0.1*max( dat1_sig_bb ) ) ) )
#
#plt.text( 0.0, 0.03, 'Slope = %s+/- %s'
#%( round( m1, 2 ), round( mean( dat1_m ), 2 ) ), fontsize = 30 )

plt.xlabel( 'Observation number', fontsize = 32 )
plt.ylabel( 'f', fontsize = 32 )

#leg1 = [ 'Linear Fit ', 'Predicted' , 'Observations']
#plt.legend( leg1, loc = 2, fontsize = 30 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error bars', fontsize = 24 )
plt.tight_layout()
plt.show( )


################################################################################
## Everything for second data set.
################################################################################

dat2_sig_bb.append(0)
dat2_s_fv.append(0)
dat2_s_sig_fv_p.append(0)
dat2['time'].append(0)

dat2_sig_bb.pop(-3)
dat2_s_fv.pop(-3)
dat2_s_sig_fv_p.pop(-3)
dat2['time'].pop(-3)

dat2_fit = fitlin( dat2_sig_bb, dat2_s_fv, dat2_s_sig_fv_p )

# Define list of index.

ind2 = linspace( 0., max( dat2_sig_bb ), len( dat2_sig_bb ) )

# Extract the slope and intercept.

m2 = dat2_fit['slope']
c2 = dat2_fit['offset']

slope2 = r'$ m \pm del_m$'

y2_fit = [ ( m2*ind1[i] + c2 ) for i in range( len( dat2_sig_bb ) ) ]
y3_fit = [ ( mean(dat2_thr_slp)*ind1[i] ) for i in range( len( dat2_sig_bb ) ) ]

fit2_x = dat2_fit['fitfunc'](ind2)

cv2 = corrcoef( dat2_sig_bb[0:-1], dat2_s_fv[0:-1] )[0,1]

dat2_thr = [ dat2_sig_bb[i] * dat2_thr_slp[i]
                                        for i in range( len( dat2_sig_bb )-1 ) ]

#plt.figure( )

plt.errorbar( range( len( dat2_s_fv ) ), dat2_s_fv, dat2_s_sig_fv_p,fmt='.',
                                                    ecolor = 'r', color = 'r'  )
#plt.errorbar( dat2_sig_bb[0:-1], dat2_s_fv[0:-1], yerr=dat2_s_sig_fv_p[0:-1],
#                                                           fmt='o', ecolor='g' )
#plt.plot( ind1, y2_fit, color='r' )
#plt.plot( ind1, y3_fit, dashes=[6,2], color='m' )
#plt.scatter( dat2_sig_bb[0:-1], dat2_thr, marker='*', color='r')

#plt.xticks([0, 0.02, 0.04, 0.05], fontsize=20)
#plt.yticks([0, 0.02, 0.04, 0.05], fontsize=20)
#
#plt.ylim( 0, 0.055 )
##plt.ylim((min(s_fv)+0.1*min(s_fv), ( max(s_fv)+ 0.1*max(s_fv))))
#plt.xlim( 0.0, 0.055 )
##plt.xlim(( 0., ( max(sig_bb)+ 0.1*max(sig_bb))))
#
#plt.text( 0.0, 0.03, 'Slope = %s+/- %s'
#%( round( m2, 2 ), round( mean( dat2_m ), 2 ) ), fontsize = 30 )
#
#plt.xlabel( r'$\frac{\sigma_B}{| \vec B|}$'  , fontsize = 32 )
#plt.ylabel( r'$\frac{\delta v}{v_A}(km/sec)$', fontsize = 32 )

#leg2 = [ 'Linear Fit', 'Theoretical Data', 'Observations' ]
#plt.legend( leg2, loc = 2, fontsize = 30 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error bars', fontsize = 24 )
#plt.tight_layout()
#plt.show( )

################################################################################
## Everything for third data set.
################################################################################

dat3_sig_bb.append(0)
dat3_s_fv.append(0)
dat3_s_sig_fv_p.append(0)
dat3['time'].append(0)

dat3_sig_bb.pop(-3)
dat3_s_fv.pop(-3)
dat3_s_sig_fv_p.pop(-3)
dat3['time'].pop(-3)

dat3_fit = fitlin( dat3_sig_bb, dat3_s_fv, dat3_s_sig_fv_p )

# Define list of index.

ind3 = linspace( 0., max( dat3_sig_bb ), len( dat3_sig_bb ) )

# Extract the slope and intercept.

m3 = dat3_fit['slope']
c3 = dat3_fit['offset']

slope3 = r'$ m \pm del_m$'

y3_fit = [ ( m3*ind1[i] + c3 ) for i in range( len( dat3_sig_bb ) ) ]
y3_fit = [ ( mean(dat3_thr_slp)*ind1[i] ) for i in range( len( dat3_sig_bb ) ) ]

fit3_x = dat3_fit['fitfunc'](ind3)

cv3 = corrcoef( dat3_sig_bb[0:-1], dat3_s_fv[0:-1] )[0,1]

dat3_thr = [ dat3_sig_bb[i] * dat3_thr_slp[i]
                                        for i in range( len( dat3_sig_bb )-1 ) ]

#plt.figure( )

plt.errorbar( range( len( dat3_s_fv ) ), dat3_s_fv, dat3_s_sig_fv_p,fmt='d',
                                                    ecolor = 'g', color = 'g'  )
#plt.errorbar( dat3_sig_bb[0:-1], dat3_s_fv[0:-1], yerr=dat3_s_sig_fv_p[0:-1],
#                                                           fmt='o', ecolor='g' )
#plt.plot( ind1, y3_fit, color='r' )
#plt.plot( ind1, y3_fit, dashes=[6,2], color='m' )
#plt.scatter( dat3_sig_bb[0:-1], dat3_thr, marker='*', color='r')

#plt.xticks([0, 0.02, 0.04, 0.05], fontsize=20)
#plt.yticks([0, 0.02, 0.04, 0.05], fontsize=20)
#
#plt.ylim( 0, 0.055 )
##plt.ylim((min(s_fv)+0.1*min(s_fv), ( max(s_fv)+ 0.1*max(s_fv))))
#plt.xlim( 0.0, 0.055 )
##plt.xlim(( 0., ( max(sig_bb)+ 0.1*max(sig_bb))))
#
#plt.text( 0.0, 0.03, 'Slope = %s+/- %s'
#%( round( m3, 2 ), round( mean( dat3_m ), 2 ) ), fontsize = 30 )
#
#plt.xlabel( r'$\frac{\sigma_B}{| \vec B|}$'  , fontsize = 32 )
#plt.ylabel( r'$\frac{\delta v}{v_A}(km/sec)$', fontsize = 32 )

leg3 = [ 'Dat_1', 'Dat_2', 'Dat_3' ]
plt.legend( leg3, loc = 1, fontsize = 30 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error bars', fontsize = 24 )
plt.tight_layout()
plt.show( )

print ('It took','%.6f'% (time.time()-start), 'seconds.')#plt,show()
