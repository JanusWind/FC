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

plt.clf()
plt.close('all')

#n_data = raw_input('Which file numbers do you want to run the code for ==>  ')
#n_data = [ int( n_data[j] ) for j in range( len( n_data ) ) ]

data_run = raw_input( 'Run the data? ==>  ' )
print '\n'

if( data_run=='y' ):

	print 'Please wait. The computer is running the data! We appreciate your patience \n'
	# Change the directory in which the saved file exists.

	os.chdir("/home/ahmadr/Desktop/GIT/fm_development/data/edited")

	# Define the names of files to be analysed.

	fname1 = 'janus_raw_mag_med_flt_21_fv_pc_2008-11-04-12-01_2008-11-04-13-01.jns'

	print 'Currently reading file ==> {}  '.format( fname1 )
	print '\n'

	if( len( fname1) > 15 ) :
		print 'Whoaaaa! Thats a big file name!'

	dat1 = [0]*len( fname1 )
	dat1 = pickle.load( open( fname1, 'rb' ) )
	nd1  = len( dat1['b0'] )

	# Change back the directory to the working directory.

	os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

	# Define all the parameters to be used during analysis.

	dat1_time         = []

#	dat1_db_x_rng_avg = []
#	dat1_db_y_rng_avg = []
#	dat1_db_z_rng_avg = []
	dat1_db_rng_avg   = []

	dat1_b_avg        = []

	dat1_n_p_c        = []
	dat1_n_p_b        = []
	dat1_n_p          = []

	dat1_fv_p_c       = []
	dat1_fv_p_b       = []
	dat1_sig_fv_p_c   = []
	dat1_sig_fv_p_b   = []

	dat1_w_fv_p       = []

	dat1_alfvel       = []

	dat1_s_fv_p_c     = []
	dat1_s_fv_p_b     = []
	dat1_s_sig_fv_p_c = []
	dat1_s_sig_fv_p_b = []

	dat1_s_db         = []

	r_ind = [ 4, 7, 16, 25 ]

	keys = [ dat1_time, dat1_db_rng_avg, dat1_b_avg,
	         dat1_n_p_c, dat1_n_p_b, dat1_n_p, dat1_fv_p_c, dat1_fv_p_b,
	         dat1_sig_fv_p_c, dat1_sig_fv_p_b, dat1_w_fv_p, dat1_alfvel,
	         dat1_s_fv_p_c, dat1_s_fv_p_b, dat1_s_sig_fv_p_c,
	         dat1_s_sig_fv_p_b, dat1_s_db    ]

	# Exaract the data from '.jns' file.

	for j in range( nd1 ) :


		dat1_time.append( dat1['time'][j].time().strftime("%H-%M") )

		db_x_rng_avg = dat1['b0_fields_db'][j]['mfi_set_rng_avg'][0]
		db_y_rng_avg = dat1['b0_fields_db'][j]['mfi_set_rng_avg'][1]
		db_z_rng_avg = dat1['b0_fields_db'][j]['mfi_set_rng_avg'][2]

		dat1_db_rng_avg.append( sqrt( 2 * ( std( db_x_rng_avg )**2 +
		                                    std( db_x_rng_avg )**2 +
		                                    std( db_x_rng_avg )**2 ) ) )

		dat1_b_avg.append( sqrt(
		 mean( dat1['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
		 mean( dat1['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
		 mean( dat1['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 ) )

		try :

			dat1_n_p_c.append( dat1['n_p_c'][j] )
			dat1_n_p_b.append( dat1['n_p_b'][j] )
			dat1_n_p.append( dat1['n_p'][j] )
	
			dat1_fv_p_c.append( dat1['fv_p_c'][j] )
			dat1_fv_p_b.append( dat1['fv_p_b'][j] )
			dat1_sig_fv_p_c.append( dat1['sig_fv_p_c'][j] )
			dat1_sig_fv_p_b.append( dat1['sig_fv_p_b'][j] )
	
			dat1_alfvel.append( dat1['alfvel_p'][j] )	
	
			dat1_s_fv_p_c.append( dat1_fv_p_c[j]/dat1_alfvel[j] )
			dat1_s_fv_p_b.append( dat1_fv_p_b[j]/dat1_alfvel[j] )
			dat1_s_sig_fv_p_c.append( dat1_sig_fv_p_c[j]/dat1_alfvel[j] )
			dat1_s_sig_fv_p_b.append( dat1_sig_fv_p_b[j]/dat1_alfvel[j] )
	
			dat1_w_fv_p.append( ( dat1_fv_p_c[j] * dat1_n_p_c[j] + 
			           dat1_fv_p_c[j] * dat1_n_p_c[j] )/dat1_n_p[j] )

		except:

			pass
	
		dat1_s_db.append( dat1_db_rng_avg[j]/dat1_b_avg[j] )

	try :
		for key in keys :

			[ key.pop( i ) for i in r_ind ]
	except :

		pass

else:
	print 'Data not read, running plotting algorithm.'


rcParams['figure.figsize'] = 20, 10

f1, axs1 = plt.subplots( 3, 1, squeeze=True, sharex=False )

axs1[0].errorbar( range( len( dat1_time ) ), dat1_fv_p_c, yerr=dat1_sig_fv_p_c,
marker='*', color='b', fmt='o', ecolor='g', label='Proton Core' )

#if( fname1[20] == 'b' ) :

axs1[0].errorbar( range( len( dat1_time ) ), dat1_fv_p_b, yerr=dat1_sig_fv_p_b,
marker='v', color='r', fmt='o', ecolor='m', label='Proton Beam' )

axs1[0].axhline( 0, marker='None', ls='--', color='gray', lw='0.5' )

axs1[0].set_ylabel( 'Velocity(km/s)', fontsize=18 )

axs1[0].legend( )

axs1[1].errorbar( dat1_s_db, dat1_fv_p_c, xerr=None, yerr=dat1_sig_fv_p_c,
marker='*', color='b', fmt='o', ecolor='g', label='Proton Core' )

axs1[1].legend( )

axs1[1].axhline( 0, marker='None', ls='--', color='gray', lw='0.5' )

axs1[1].set_ylabel( 'Velocity(km/s)', fontsize=18 )

#if( fname1[20] == 'b' ) :

axs1[2].errorbar( dat1_s_db, dat1_fv_p_b, xerr=None, yerr=dat1_sig_fv_p_b,
marker='v', color='r', fmt='v', ecolor='m', label='Proton Beam' )

axs1[2].legend( )

axs1[2].axhline( 0, marker='None', ls='--', color='gray', lw='0.5' )

axs1[2].set_ylabel( 'Velocity(km/s)', fontsize=18 )

axs1[2].set_xlabel( r'$\Delta B / B$', fontsize=18 )

plt.suptitle( 'MFI Type = ' + fname1[6:13], color='r', fontsize=20 )

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/figures")

if( 'aniso' in fname1 ) :

	plt.savefig( fname1[6:38] + '.pdf', bbox_inches='tight', dpi=500 )

else:

	plt.savefig( fname1[6:32] + '.pdf', bbox_inches='tight', dpi=500 )

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

rcParams['figure.figsize'] = 10, 10

f2, axs2 = plt.subplots( 1, 1, squeeze=True, sharex=False )

axs2.scatter( dat1_s_db, dat1_w_fv_p, marker='*', color='r', label='Weighted fv' )

axs2.scatter( dat1_s_db, dat1_fv_p_c, marker='d', color='b', label='Core fv' )

axs2.scatter( dat1_s_db, dat1_fv_p_b, marker='v', color='m', label='Beam fv' )

axs2.axhline( 0, marker='None', ls='--', color='gray', lw='0.5' )

axs2.legend( )

axs2.set_ylabel( 'Velocity(km/s)', fontsize=18 )

axs2.set_xlabel( r'$\Delta B / B$', fontsize=18 )

plt.suptitle( 'MFI Type = ' + fname1[6:13], color='r', fontsize=20 )

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/figures")

if( 'aniso' in fname1 ) :

	plt.savefig( 'C_' + fname1[6:38] + '.pdf', bbox_inches='tight', dpi=500 )

else:

	plt.savefig( 'C_' + fname1[6:32] + '.pdf', bbox_inches='tight', dpi=500 )

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

#plt.show()

print ('It took','%.6f'% (time.time()-start), 'seconds.')
