import time
start = time.time()


import os
import sys
os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen

import glob
import pickle
import numpy as np
from numpy import mean, sqrt, corrcoef
import matplotlib.pyplot as plt
from matplotlib import gridspec, rc
from pylab import rcParams
from scipy.optimize import curve_fit

from numpy import linspace, pi, sqrt, exp, std

from janus_const import const

#plt.clf()
#plt.close('all')

n_data = raw_input('Which file numbers do you want to run the code for ==>  ')
n_data = [ int( n_data[j] ) for j in range( len( n_data ) ) ]

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/data/edited")

fname1 = 'janus_rng_avg_600_med_flt_21_2008-11-04-12-00-41_2008-11-04-12-56-08.jns'

if ( 1 in n_data ) :

	try :
		dat1 = [0]*len( fname1 )
		dat1 = pickle.load( open( fname1, 'rb' ) )
		nd1  = len( dat1['b0'] )
	except :
		print "Requested file not found. Exiting the code now."
		os.chdir("/home/ahmadr/Desktop/GIT/fm_development")
		sys.exit(1)

	dat1_b_x_raw     = [None]*nd1
	dat1_b_y_raw     = [None]*nd1
	dat1_b_z_raw     = [None]*nd1
	dat1_b           = [None]*nd1
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

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

if ( 1 in n_data ) :

	########################################################################
	## For data set 1 of filter size 01.
	########################################################################

	for j in range( nd1 ) :

		time1[j] = dat1['time'][j].time().strftime("%H-%M")

		dat1_b_x_raw[j] = mean(
		dat1['b0_fields'][j]['but_low'][0][2930:int(2930+10.869*50)] )

		dat1_b_y_raw[j] = mean(
		dat1['b0_fields'][j]['but_low'][1][2930:int(2930+10.869*50)] )

		dat1_b_z_raw[j] = mean(
		dat1['b0_fields'][j]['but_low'][2][2930:int(2930+10.869*50)] )

		dat1_b_x_rot[j] = mean(
		                np.array( dat1['b0_fields'][j]['rot_smt'] )[0] )

		dat1_b_y_rot[j] = mean(
		                np.array( dat1['b0_fields'][j]['rot_smt'] )[1] )

		dat1_b_z_rot[j] = mean(
		                np.array( dat1['b0_fields'][j]['rot_smt'] )[2] )

		dat1_db_x_raw = dat1['b0_fields'][j]['but_bnd'][0]

		dat1_db_y_raw = dat1['b0_fields'][j]['but_bnd'][1]

		dat1_db_z_raw = dat1['b0_fields'][j]['but_bnd'][2]

		dat1_db[j]    = sum( [ sqrt( dat1_db_x_raw[k]**2 +
		                             dat1_db_y_raw[k]**2 +
		                             dat1_db_z_raw[k]**2  )
		                    for k in range( len( dat1_db_x_raw ) ) ] )/(
		            len( dat1_db_x_raw )*( sqrt( dat1_b_x_raw[j]**2 +
		                 dat1_b_y_raw[j]**2 + dat1_b_z_raw[j]**2   ) ) )

#		if( j == 1 ) :
#
#			f, ax = plt.subplots( 3, 1, sharex=True )
#	
#			ax[0].plot( range( len(
#			  dat1_db_x_raw[2930:int( 2930+10.986*50) ] ) ),
#			  dat1_db_x_raw[2930:int( 2930+10.986*50) ] )
#	
#			ax[1].plot( range( len(
#			  dat1_db_y_raw[2930:int( 2930+10.986*50) ] ) ),
#			  dat1_db_y_raw[2930:int( 2930+10.986*50) ] )
#	
#			ax[2].plot( range( len(
#			  dat1_db_z_raw[2930:int( 2930+10.986*50) ] ) ),
#			  dat1_db_z_raw[2930:int( 2930+10.986*50) ] )


#		dat1_db_x_raw = [
#		         dat1['b0_fields'][j]['raw_smt'][0][k] - dat1_b_x_raw[j]
#		                        for k in range( len(
#		                        dat1['b0_fields'][j]['raw_smt'][0] ) ) ]
#
#		dat1_db_y_raw = [
#		         dat1['b0_fields'][j]['raw_smt'][1][k] - dat1_b_y_raw[j]
#		                        for k in range( len( 
#		                         dat1['b0_fields'][j]['raw_smt'][0]) ) ]
#
#		dat1_db_z_raw = [
#		         dat1['b0_fields'][j]['raw_smt'][2][k] - dat1_b_z_raw[j]
#		                        for k in range( len( 
#		                        dat1['b0_fields'][j]['raw_smt'][0] ) ) ]
#
#		dat1_db[j]    = sum( [ sqrt( dat1_db_x_raw[k]**2 +
#		                             dat1_db_y_raw[k]**2 +
#		                             dat1_db_z_raw[k]**2  )
#		                    for k in range( len( dat1_db_x_raw ) ) ] )/(
#		            len( dat1_db_x_raw )*( sqrt( dat1_b_x_raw[j]**2 +
#		                 dat1_b_y_raw[j]**2 + dat1_b_z_raw[j]**2   ) ) )

		dat1_b_y_sig_rot[j] = np.array(
		                    dat1['sig_b0_fields'][j]['sig_rot_smt'][1] )
		dat1_b_z_sig_rot[j] = np.array(
		                    dat1['sig_b0_fields'][j]['sig_rot_smt'][2] )

		dat1_sig_b_rot[j] = sqrt( 2 ) * sqrt(
		                           std( dat1_db_y_raw[3260:-3260] )**2 +
		                           std( dat1_db_z_raw[3260:-3260] )**2 )
#		dat1_sig_b_rot[j] = sqrt(
#		               dat1_b_y_sig_rot[j]**2 + dat1_b_z_sig_rot[j]**2 )

#		dat1_sig_bb[j] = dat1_sig_b_rot[j] / dat1_b_x_rot[j]

		dat1_b[j] = sqrt( dat1_b_x_raw[j]**2 + dat1_b_y_raw[j]**2 +
		                  dat1_b_z_raw[j]**2 )
		dat1_sig_bb[j] = sqrt(
		 std( dat1_db_x_raw[2930:int(2930+10.869*50)] )**2 +
		 std( dat1_db_y_raw[2930:int(2930+10.869*50)] )**2 +
		 std( dat1_db_z_raw[2930:int(2930+10.869*50)] )**2 )


		dat1_fv_p[j] = dat1['fv_p_c'][j]

		dat1_sig_fv_p[j] = dat1['sig_fv_p'][j]

		dat1_alfvel[j] = dat1['alfvel_p'][j]

		try :
			dat1_s_fv[j] = dat1_fv_p[j]/dat1_alfvel[j] * (
			             1 - dat1['ocycl_p'][j]/dat1['ogyro_p'][j] )

			dat1_s_sig_fv_p[j] = dat1_sig_fv_p[j]/dat1_alfvel[j] * (
			             1 - dat1['ocycl_p'][j]/dat1['ogyro_p'][j] )

			dat1_ogyro[j] = dat1['ogyro_p'][j]
	
			dat1_ocycl[j] = dat1['ocycl_p'][j]
	
			dat1_thr_slp[j] = 1/( 1 - dat1_ocycl[j]/dat1_ogyro[j] )
	
			dat1_vmag[j] = dat1['v0'][j]
	
			dat1_vsig[j] = sqrt( dat1['sig_v0_x'][j]**2 +
			                     dat1['sig_v0_y'][j]**2 +
			                     dat1['sig_v0_z'][j]**2   )
	
			dat1_n[j]    = dat1['n_p'][j]
	
			dat1_nsig[j] = dat1['sig_n_p_c'][j] + dat1['sig_n_p_c'][j]
	
			dat1_bmag[j] = dat1['b0'][j]
	
			dat1_bsig[j] = dat1['sig_b0'][j]
	
			dat1_m[j]    = ( dat1_vsig[j]/dat1_vmag[j] +
			             0.5*dat1_nsig[j]/dat1_n[j] 
			             + 3*dat1_bsig[j]/dat1_bmag[j] )
	
			dat1_vmag[j] = dat1['v0'][j]
	
			dat1_vsig[j] = sqrt( dat1['sig_v0_x'][j]**2 +
			                     dat1['sig_v0_y'][j]**2 +
			                     dat1['sig_v0_z'][j]**2   )
	
			dat1_n[j]    = dat1['n_p'][j]
	
			dat1_nsig[j] = dat1['sig_n_p_c'][j] + dat1['sig_n_p_c'][j]
	
			dat1_bmag[j] = dat1['b0'][j]
	
			dat1_bsig[j] = dat1['sig_b0'][j]

		except :

			dat1_s_fv[j]       = None

			dat1_s_sig_fv_p[j] = None

			dat1_ogyro[j]      = None 

			dat1_ocycl[j]      = None 

			dat1_thr_slp[j]    = None 

			dat1_vmag[j]       = None 

			dat1_vsig[j]       = None

			dat1_n[j]          = None 

			dat1_nsig[j]       = None 

			dat1_bmag[j]       = None 

			dat1_bsig[j]       = None 

			dat1_m[j]          = None 

			dat1_vmag[j]       = None 

			dat1_vsig[j]       = None 

			dat1_n[j]          = None 

			dat1_nsig[j]       = None 

			dat1_bmag[j]       = None 

			dat1_bsig[j]       = None 


#	# Define the linear model to fit the data.
#
#	def fitlin( b1, v1, sigma1 ) :
#
#		def linfunc( b1, m1, c1 ) :
#
#			return m1 * b1 + c1
#
#		sigma1 = np.ones(len(b1))
#		sigma1[ -1]= 1.E-5
#		popt1, pcov1 = curve_fit( linfunc, b1, v1, sigma=sigma1 )
#		m1, c1 = popt1
#
#		fitfunc = lambda b1: m1 * b1 + c1
#
#		return { "slope"   : m1,
#		         "offset"  : c1,
#		         "fitfunc" : fitfunc,
#		         "rawres"  : ( popt1,pcov1 ) }

#	dat1_db.pop( 13 )
#	dat1_s_fv.pop( 13 )
#	dat1_fv_p.pop( 13 )
#	dat1_s_sig_fv_p.pop( 13 )
#
#	dat1_db.pop( 13 )
#	dat1_s_fv.pop( 13 )
#	dat1_fv_p.pop( 13 )
#	dat1_s_sig_fv_p.pop( 13 )
#
#	dat1_db.pop( 16 )
#	dat1_s_fv.pop( 16 )
#	dat1_fv_p.pop( 16 )
#	dat1_s_sig_fv_p.pop( 16 )
#
#	dat1_db.pop( 16 )
#	dat1_s_fv.pop( 16 )
#	dat1_fv_p.pop( 16 )
#	dat1_s_sig_fv_p.pop( 16 )
#
#	dat1_db.pop( 16 )
#	dat1_s_fv.pop( 16 )
#	dat1_fv_p.pop( 16 )
#	dat1_s_sig_fv_p.pop( 16 )
#
#	dat1_db.pop( 17 )
#	dat1_s_fv.pop( 17 )
#	dat1_fv_p.pop( 17 )
#	dat1_s_sig_fv_p.pop( 17 )
#
#	dat1_db.pop( 18 )
#	dat1_s_fv.pop( 18 )
#	dat1_fv_p.pop( 18 )
#	dat1_s_sig_fv_p.pop( 18 )
#
#	dat1_db.pop( 18 )
#	dat1_s_fv.pop( 18 )
#	dat1_fv_p.pop( 18 )
#	dat1_s_sig_fv_p.pop( 18 )
#
#	dat1_db.pop( 18 )
#	dat1_s_fv.pop( 18 )
#	dat1_fv_p.pop( 18 )
#	dat1_s_sig_fv_p.pop( 18 )
#
#	dat1_db.pop( 18 )
#	dat1_s_fv.pop( 18 )
#	dat1_fv_p.pop( 18 )
#	dat1_s_sig_fv_p.pop( 18 )
#
#	dat1_db.pop( -1 )
#	dat1_s_fv.pop( -1 )
#	dat1_fv_p.pop( -1 )
#	dat1_s_sig_fv_p.pop( -1 )

#	dat1_db.append( 0 )
#	dat1_sig_bb.append( 0 )
#	dat1_s_fv.append( 0 )
#	dat1_fv_p.append( 0 )
#	dat1_s_sig_fv_p.append( 0 )
#
#	dat1_fit = fitlin( dat1_sig_bb, dat1_s_fv, dat1_s_sig_fv_p )

	# Define list of index.

	ind1 = linspace( 0., max( dat1_sig_bb ), len( dat1_sig_bb ) )

	# Extract the slope and intercept.

#	m1 = dat1_fit['slope']
#	c1 = dat1_fit['offset']
#
#	slope1 = r'$ m \pm del_m$'
#
#	y1_fit_dat = [ ( m1*ind1[i] + c1 ) for i in range( len( dat1_sig_bb ) ) ]
#
#	y1_fit_thr = [ ( mean(dat1_thr_slp)*ind1[i] )
#	                                  for i in range( len( dat1_sig_bb ) ) ]
#
#	fit1_x = dat1_fit['fitfunc'](ind1)
#
#	cv1 = corrcoef( dat1_sig_bb[0:-1], dat1_s_fv[0:-1] )[0,1]
#
#	dat1_thr = [ dat1_sig_bb[i] * dat1_thr_slp[i]
#	                                    for i in range( len( dat1_db )-1 ) ]

	########################################################################
	## Plotting figures: Data Set 1
	########################################################################

#	plt.figure( )
#
#	rcParams['figure.figsize'] = 10, 10
#
#	plt.errorbar( dat1_sig_bb[0:-1], dat1_s_fv[0:-1],
#	                       yerr=dat1_s_sig_fv_p[0:-1], fmt='o', ecolor='g' )
#
#	plt.plot( ind1, y1_fit_dat, color='r' )
#	plt.plot( ind1, y1_fit_thr, dashes=[1,1], color='m' )
#	plt.scatter( dat1_db[0:-1], dat1_thr, marker='*', color='r')
#	plt.axhline( 0, color='gray' )
#	plt.axvline( 0, color='gray' )

#	plt.ylim( [ -0.005, 0.08 ] )
#	plt.xlim( [ -0.005, 0.08 ] )

#	plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=24 )
	#plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=24 )

#	plt.text( 0.0, 0.01, 'Fit Slope = ' '%s' r'$\, \pm \,$' '%s'
#	%( round( m1, 2 ), round( mean( dat1_m ), 2 ) ), fontsize = 20,
#	                                                           rotation=33 )

	#plt.text( 0.052, 0.069, 'Expected Slope = 1', fontsize = 20,
	#                                                          rotation=45 )

#	rc( 'text', usetex=True )

#	plt.xlabel( r'$\left< \delta B\right >/ B_0$', fontsize = 24 )
#	plt.ylabel( r'$\delta V/v_A$', fontsize = 24 )

#	plt.tight_layout()

	'''
	#os.chdir("/home/ahmadr/Desktop/GIT/fm_development/figures")

	#plt.savefig('fv_delb_fz01'+'.eps', bbox_inches='tight', dpi=200)

	#os.chdir("/home/ahmadr/Desktop/GIT/fm_development
	'''

	plt.figure( )

	plt.scatter( range( len( dat1_fv_p ) ), dat1_fv_p, marker='*', color='r', label='scaled fluctuating velocity' )
#	plt.ylim( -0.025, 0.025 )
	plt.axhline( 0 )
	plt.axvline( 0 )
	plt.xlabel( 'Spectra number', fontsize=22 )
	plt.ylabel( r'$f_v/v_A$', fontsize=22 )
	plt.title( 'Scaled fluctuating velocity against time', fontsize=22 )

	plt.show( )

print ('It took','%.6f'% (time.time()-start), 'seconds.')#plt,show()
