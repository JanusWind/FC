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

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/data/edited/error_analysis")

#fname1 = 'fm_22.jns'
#fname2 = 'fm_14.jns'
#fname3 = 'ms_14.jns'

#fname1 = 'dat_auto_run_11.jns'
#fname2 = 'dat_non_auto_run_11.jns' 
#fname3 = 'dat_auto_run_22.jns' 
#fname4 = 'dat_auto_run_03.jns'
#fname4 = 'dat_auto_run_03_b.jns'
fname4 = 'janus_fit_smt_med_flt_21_2008-11-04-12-00-41_2008-11-04-12-56-08.jns'
#fname4 = 'dat_auto_run_11_d.jns'
#fname4  = 'test_1_fm.jns'

i = 0

dat4   = [0]*len( fname4 )

dat4 = pickle.load( open( fname4, 'rb' ) )

# Find the total number of data points in all the files being analyzed.
os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

nd4 = len( dat4['b0'] )

dat4_b_x_raw     = [None]*nd4
dat4_b_y_raw     = [None]*nd4
dat4_b_z_raw     = [None]*nd4
dat4_db_x_raw    = [None]*nd4
dat4_db_y_raw    = [None]*nd4
dat4_db_z_raw    = [None]*nd4
dat4_db_raw      = [None]*nd4
dat4_b_x_rot     = [None]*nd4
dat4_b_y_rot     = [None]*nd4
dat4_b_z_rot     = [None]*nd4
dat4_b_y_sig_rot = [None]*nd4
dat4_b_z_sig_rot = [None]*nd4
dat4_sig_b_rot   = [None]*nd4
dat4_sig_bb      = [None]*nd4
dat4_fv_p        = [None]*nd4
dat4_sig_fv_p    = [None]*nd4
dat4_s_sig_fv_p  = [None]*nd4
dat4_alfvel      = [None]*nd4
dat4_s_fv        = [None]*nd4
dat4_ogyro       = [None]*nd4
dat4_ocycl       = [None]*nd4
dat4_thr_slp     = [None]*nd4
dat4_vmag        = [None]*nd4
dat4_vsig        = [None]*nd4
dat4_n           = [None]*nd4
dat4_nsig        = [None]*nd4
dat4_bmag        = [None]*nd4
dat4_bsig        = [None]*nd4
dat4_m           = [None]*nd4
dat4_rat         = [None]*nd4
time4            = [None]*nd4

################################################################################
## Auto-Run: Filter size = 03
################################################################################

for j in range( nd4 ) :

	time4[j] = dat4['time'][j].time().strftime("%H-%M")

	dat4_b_x_raw[j] = mean( np.array( dat4['b0_fields'][j]['raw_smt'] )[0] )

	dat4_b_y_raw[j] = mean( np.array( dat4['b0_fields'][j]['raw_smt'] )[1] )

	dat4_b_z_raw[j] = mean( np.array( dat4['b0_fields'][j]['raw_smt'] )[2] )

	dat4_b_x_rot[j] = mean( np.array( dat4['b0_fields'][j]['rot_smt'] )[0] )

	dat4_b_y_rot[j] = mean( np.array( dat4['b0_fields'][j]['rot_smt'] )[1] )

	dat4_b_z_rot[j] = mean( np.array( dat4['b0_fields'][j]['rot_smt'] )[2] )

	dat4_db_x_raw[j] = mean( [ abs( ( dat4['b0_fields'][j]['raw_smt'][0][k] -
	                                dat4_b_x_raw[j] ) / dat4_b_x_rot[j] )
	                            for k in range( len( time4 ) ) ] )

	dat4_db_y_raw[j] = mean( [ abs( ( dat4['b0_fields'][j]['raw_smt'][1][k] -
	                                dat4_b_y_raw[j] ) / dat4_b_x_rot[j] )
	                            for k in range( len( time4 ) ) ] )

	dat4_db_z_raw[j] = mean( [ abs( ( dat4['b0_fields'][j]['raw_smt'][2][k] -
	                                dat4_b_z_raw[j] )  / dat4_b_x_rot[j] )
	                            for k in range( len( time4 ) ) ] )

	dat4_b_y_sig_rot[j] = np.array(
	                            dat4['sig_b0_fields'][j]['sig_rot_smt'][1] )
	dat4_b_z_sig_rot[j] = np.array(
	                            dat4['sig_b0_fields'][j]['sig_rot_smt'][2] )

	dat4_sig_b_rot[j] = sqrt(
	                       dat4_b_y_sig_rot[j]**2 + dat4_b_z_sig_rot[j]**2 )

	dat4_sig_bb[j] = dat4_sig_b_rot[j] / dat4_b_x_rot[j]

	dat4_fv_p[j] = dat4['fv_p'][j]

	dat4_sig_fv_p[j] = dat4['sig_fv_p'][j]

	dat4_alfvel[j] = dat4['alfvel_p'][j]

	dat4_s_fv[j] = dat4_fv_p[j]/dat4_alfvel[j] * (
	                             1 - dat4['ocycl_p'][j]/dat4['ogyro_p'][j] )


	dat4_s_sig_fv_p[j] = dat4_sig_fv_p[j]/dat4_alfvel[j] * (
	                             1 - dat4['ocycl_p'][j]/dat4['ogyro_p'][j] )

	dat4_ogyro[j] = dat4['ogyro_p'][j]

	dat4_ocycl[j] = dat4['ocycl_p'][j]

	dat4_thr_slp[j] = 1/( 1 - dat4_ocycl[j]/dat4_ogyro[j] )

	dat4_vmag[j] = dat4['v0'][j]

	dat4_vsig[j] = sqrt( dat4['sig_v0_x'][j]**3 + dat4['sig_v0_y'][j]**3 +
	                     dat4['sig_v0_z'][j]**3                         )

	dat4_n[j]    = dat4['n_p'][j]

	dat4_nsig[j] = dat4['sig_n_p_c'][j] + dat4['sig_n_p_c'][j]

	dat4_bmag[j] = dat4['b0'][j]

	dat4_bsig[j] = dat4['sig_b0'][j]

	dat4_m[j]    = ( dat4_vsig[j]/dat4_vmag[j] + 0.5*dat4_nsig[j]/dat4_n[j] 
	                + 3*dat4_bsig[j]/dat4_bmag[j] )

dat4_db_raw = [ sqrt( dat4_db_x_raw[i]**2 + dat4_db_y_raw[i]**2 + 
                      dat4_db_z_raw[i]**2 ) for i in range( len( time4 ) ) ]

# Define the linear model to fit the data.

#def fitlin( b4, v4, sigma4 ) :
#
#	def linfunc( b4, m4, c4 ) :
#
#		return m4 * b4 + c4
#
#	sigma4 = np.ones(len(b4))
#	sigma4[ -1]= 1.E-5
##	sigma4[ -3]= 1.E1
#	popt4, pcov4 = curve_fit( linfunc, b4, v4, sigma=sigma4 )
#	m4, c4 = popt4
#
#	fitfunc = lambda b4: m4 * b4 + c4
#
#	return { "slope"   : m4,
#	         "offset"  : c4,
#	         "fitfunc" : fitfunc,
#	         "rawres"  : ( popt4,pcov4 ) }
#
#################################################################################
### Everything for fourth data set.
#################################################################################
#
#k = 0
#
#for i in range( len( time4 ) ) :
#
#	if( ( dat4_s_fv[i] < -1.5 ) or ( dat4_db_raw[i] >= 0.1 ) ) :
#
#		dat4_sig_bb.pop(i)
#		dat4_sig_bb.append(0)
#
#		dat4_db_raw.pop(i)
#		dat4_db_raw.append(0)
#
#		dat4_s_fv.pop(i)
#		dat4_s_fv.append(0)
#
#		dat4_s_sig_fv_p.pop(i)
#		dat4_s_sig_fv_p.append(0)
#
#		time4.pop(i)
#		time4.append(0)
#
#		k += 1
#print k
#f, ax4 = plt.subplots( 3, 1, sharex=True )
#
#if (k > 0 ) :
#
#	ax4[0].scatter( range( len( time4 ) - k ), dat4_sig_bb[0:-k], color='r',
#	                                                            marker='D' )
#	ax4[1].errorbar( range( len( time4 ) - k ), dat4_s_fv[0:-k],
#	            yerr=dat4_s_sig_fv_p[0:-k], fmt='o', ecolor='b', color='b' )
#
#	ax4[2].scatter( range( len( time4 ) - k ), dat4_db_raw[0:-k], color='m',
#	                                                            marker='D' )
#else:
#
#	ax4[0].scatter( range( len( time4 ) ), dat4_sig_bb, color='r',
#	                                                            marker='D' )
#	ax4[1].errorbar( range( len( time4 ) ), dat4_s_fv,
#	            yerr=dat4_s_sig_fv_p, fmt='o', ecolor='b', color='b' )
#
#	ax4[2].scatter( range( len( time4 ) ), dat4_db_raw, color='m',
#	                                                            marker='D' )
#
#ax4[0].set_ylabel( r'$\frac{\sigma_B}{| \vec B|}$', fontsize = 32, color='r' )
#ax4[0].set_ylim( 0., 0.125 )
#
#ax4[1].set_ylabel( 'f', fontsize = 32, color='b' )
#ax4[2].set_ylabel( r'$\sigma_b$', fontsize = 32, color='m' )
#ax4[2].set_xlabel( 'Data Number', fontsize = 32, color='k')
#ax4[1].tick_params( 'y', colors='b' )
##ax4[1].set_ylim( -1.5, 1.5 )
##ax4[1].set_xlim( 0., 75 )
#'''
#ind = [0, 10, 20, 30, 40 ,50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150,
#160, 170, 180, 190]
#
#label = [ time4[j] for j in ind ]
#
#plt.xticks( ind, label, rotation = 'vertical', fontsize = 16 )
#
#f1, ax41 = plt.subplots( )
#
#ax41.set_ylabel( r'$h$' , fontsize = 32, color='m' )
#ax41.set_ylim( -1.2, 1.2 )
#ax42 = ax41.twinx()
#
##ax42.scatter( range( len( time4 ) - k ), dat4_sig_bb[0:-k], color='r',
##                                                                    marker='D' )
#if ( k > 0 ) :
#
#	ax41.plot( range( len( time4 ) - k ), dat4_s_fv[0:-k], color='m',
#	                                                            marker='^' )
#	ax42.plot( range( len( time4 ) - k ), dat4_db_raw[0:-k], color='g',
#	                                                            marker='d' )
#else :
#
#	ax41.plot( range( len( time4 ) ), dat4_s_fv, color='m', marker='^'   )
#	ax42.plot( range( len( time4 ) ), dat4_db_raw, color='g', marker='d' )
#
#ax42.tick_params( 'y', colors='g' )
#ax42.set_ylabel( r'$\left< \frac{\Delta{\vec{B}}}{| \vec B|} \right >$',
#fontsize = 32, color='g' )
#ax42.set_ylim( 0., 0.1 )
##plt.plot(range(nd4), dat4_b_y_rot, color='r')
##plt.plot(range(nd4), dat4_b_z_rot, color='b')
#plt.xticks( ind, label, rotation = 'vertical', fontsize = 16 )
#
##ind=[0, 10, 20, 30, 40, 50, 60, 70]
##label = [ time4[j] for j in ind ]
##plt.xticks( ind, label )
##ax42.set_xticks( [0,10,20,30,40,50,60,70],
##[time4[0],time4[10],time4[20],time4[30],time4[40],time4[50],time4[60],time4[70]])
#
#plt.xlabel('Time', fontsize = 26 )
#plt.suptitle( 'Autorun: Yes, Filter Size: 11', fontsize = 24 )
#
#plt.tight_layout()
#plt.show( )
#
#'''
print ('It took','%.6f'% (time.time()-start), 'seconds.')
