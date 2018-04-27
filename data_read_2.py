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

plt.clf()

fname1 = 'fm_22.jns'
fname2 = 'fm_14.jns'
fname3 = 'ms_14.jns'

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
#dat1_ogyro       = [None]*nd1
#dat1_ocycl       = [None]*nd1
#dat1_thr_slp     = [None]*nd1
dat1_vmag        = [None]*nd1
dat1_vsig        = [None]*nd1
dat1_n           = [None]*nd1
dat1_nsig        = [None]*nd1
dat1_bmag        = [None]*nd1
dat1_bsig        = [None]*nd1

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

	dat1_s_fv[j] = dat1_fv_p[j]/dat1_alfvel[j]

	dat1_s_sig_fv_p[j] = dat1_sig_fv_p[j]/dat1_alfvel[j]

#	dat1_ogyro[j] = dat1['ogyro_p'][j]
#
#	dat1_ocycl[j] = dat1['ocycl_p'][j]
#
#	dat1_thr_slp[j] = 1/( 1 - dat1_ogyro[j]/dat1_ocycl[j] )

	dat1_vmag[j] = dat1['v0'][j]

	dat1_vsig[j] = sqrt( dat1['sig_v0_x'][j]**2 + dat1['sig_v0_y'][j]**2 +
	                     dat1['sig_v0_z'][j]**2                         )

	dat1_n[j]    = dat1['n_p'][j]

	dat1_nsig[j] = dat1['sig_n_p_c'][j] + dat1['sig_n_p_c'][j]

	dat1_bmag[j] = dat1['b0'][j]

	dat1_bsig[j] = dat1['sig_b0'][j]

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

	dat2_s_fv[j] = dat2_fv_p[j]/dat2_alfvel[j]

	dat2_s_sig_fv_p[j] = dat2_sig_fv_p[j]/dat2_alfvel[j]

	dat2_ogyro[j] = dat2['ogyro_p'][j]

	dat2_ocycl[j] = dat2['ocycl_p'][j]

	dat2_thr_slp[j] = 1/( 1 - dat2_ocycl[j]/dat2_ogyro[j])

	dat2_vmag[j] = dat2['v0'][j]

	dat2_vsig[j] = sqrt( dat2['sig_v0_x'][j]**2 + dat2['sig_v0_y'][j]**2 +
	                     dat2['sig_v0_z'][j]**2                         )

	dat2_n[j]    = dat2['n_p'][j]

	dat2_nsig[j] = dat2['sig_n_p_c'][j] + dat2['sig_n_p_c'][j]

	dat2_bmag[j]    = dat2['b0'][j]

	dat2_bsig[j] = dat2['sig_b0'][j]

	dat2_m[j]    = ( dat2_vsig[j]/dat2_vmag[j] + 0.5*dat2_nsig[j]/dat2_n[j] 
	                + 2*dat2_bsig[j]/dat2_bmag[j] )

dat3_b = np.array( dat3['b0'] )

# Define the linear model to fit the data.

def fitlin( b, v, sigma ) :

	def linfunc( b, m, c ) :

		return m * b + c

	sigma = np.ones(len(b))
	sigma[ -1]= 1.E-5
#	sigma[ -3]= 1.E1
	popt, pcov = curve_fit( linfunc, b, v, sigma=sigma )
	m, c = popt

	fitfunc = lambda b: m * b + c

	return { "slope"   : m,
	         "offset"  : c,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt,pcov ) }

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

plt.errorbar( dat1_sig_bb[0:-1], dat1_s_fv[0:-1], yerr=dat1_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind1, y1_fit )
#plt.scatter(dat1_sig_bb[0:-1], dat1_thr, marker='*', color='r')

plt.xticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], fontsize=20)
plt.yticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], fontsize=20)

plt.ylim( 0, 0.1 )
#plt.ylim( ( min( dat1_s_fv ) + 0.1*min( dat1_s_fv ),
#          ( max( dat1_s_fv ) + 0.1*max( dat1_s_fv ) ) ) )
plt.xlim( 0, 0.1 )
#plt.xlim(( 0., ( max( dat1_sig_bb )+ 0.1*max( dat1_sig_bb ) ) ) )

plt.text( 0.0, 0.03, 'Slope = %s+/- %s\nOffset = %s\nCorr Coeff = %s\n'
%( round( m1, 2 ), round( mean( dat1_m ), 2 ),  round( c1, 4 ), round( cv1, 2 )
                                                               ), fontsize=22 )

plt.xlabel(r'$\frac{\sigma_B}{| \vec B|}$', fontsize = 28 )
plt.ylabel(r'$\frac{\delta v}{v_A}(km/sec)$', fontsize = 22 )

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

print c2
slope2 = r'$ m \pm del_m$'

y2_fit = [ ( m2*ind2[i] + c2 ) for i in range( len( dat2_sig_bb ) ) ]

fit2_x = dat2_fit['fitfunc'](ind2)

cv2 = corrcoef( dat2_sig_bb[0:-1], dat2_s_fv[0:-1] )[0,1]

dat2_thr = [ dat2_sig_bb[i] * dat2_thr_slp[i]
                                        for i in range( len( dat2_sig_bb )-1 ) ]

plt.figure( )

plt.errorbar( dat2_sig_bb[0:-1], dat2_s_fv[0:-1], yerr=dat2_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind2, y2_fit )
plt.scatter(dat2_sig_bb[0:-1], dat2_thr, marker='*', color='r')

#plt.xticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], fontsize=20)
#plt.yticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], fontsize=20)

plt.ylim( 0, 0.055 )
#plt.ylim((min(s_fv)+0.1*min(s_fv), ( max(s_fv)+ 0.1*max(s_fv))))
plt.xlim( 0.0, 0.055 )
#plt.xlim(( 0., ( max(sig_bb)+ 0.1*max(sig_bb))))

plt.text( 0.0, 0.03, 'Slope = %s+/- %s\nOffset = %s\nCorr Coeff = %s\n'
%( round( m2, 2 ), round( mean( dat2_m ), 2 ),  round( c2, 4 ), round( cv2, 2 )
                                                               ), fontsize=22 )

plt.xlabel(r'$\frac{\sigma_B}{| \vec B|}$', fontsize = 28 )
plt.ylabel(r'$\frac{\delta v}{v_A}(km/sec)$', fontsize = 22 )

#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error bars', fontsize = 24 )
plt.tight_layout()
plt.show( )

print ('It took','%.6f'% (time.time()-start), 'seconds.')#plt,show()
