import time
start = time.time()

import os
os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen

import glob
import pickle
import numpy as np
import math
from numpy import mean, sqrt, corrcoef, nanmedian
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.backends.backend_pdf
from pylab import rcParams
from scipy.optimize import curve_fit
from datetime import datetime, timedelta
from scipy.signal import medfilt

from numpy import linspace, pi, sqrt, exp

from janus_const import const

rcParams['figure.figsize'] = 20, 15

plt.clf()
plt.close( 'all' )

t0 = datetime( 2014, 02, 19, 0, 0, 0 )

#fname = [ 'file_4.jns', 'file_5.jns', 'file_6.jns' ]
#figname = '12_24'

Person = raw_input( ' Who are you? ( m or r ) ==> ' )

mark_run = raw_input( ' Read Mark data? ( y or n ) ==> ' )
ramiz_run = raw_input( ' Read Ramiz data? ( y or n ) ==> ' )

data_run = 'n'

if ( mark_run == 'y' or ramiz_run == 'y' ) : data_run = 'y'

if ( data_run == 'y' ) :

	dat = [[],[]]

	nd  = [[],[]]

	fname = [[],[]]

	if ( mark_run == 'y' ) :

		# read in Mark's data

		if( Person == 'm' ) :

			os.chdir("/home/pultrone/Desktop/FC/results/save/mark")

		else :

			os.chdir("/home/ahmadr/Desktop/GIT/Personal/Janus/results/save/mark")

		i = 0

		fname[0] = [ 'm_file_1.jns', 'm_file_2.jns', 'm_file_3.jns',
		             'm_file_4.jns', 'm_file_5.jns', 'm_file_6.jns',
		             'm_file_7.jns' ]

		dat[0] = [0]*len(fname[0])

		# Find the total number of data points in all the files being
		# analyzed.
	
		for i in range (len(fname[0])):
		        dat[0][i] = pickle.load(open(fname[0][i],'rb'))

	if ( ramiz_run == 'y' ) :

		# read in Ramiz's data

		if( Person == 'm' ) :

		        os.chdir("/home/pultrone/Desktop/FC/results/save/ramiz")

		else:

			os.chdir("/home/ahmadr/Desktop/GIT/Personal/Janus/results/save/ramiz")

		i = 0

		fname[1] = [ 'r_file_1.jns', 'r_file_2.jns', 'r_file_3.jns',
		             'r_file_4.jns', 'r_file_5.jns', 'r_file_6.jns' ]

		dat[1] = [0]*len(fname[1])
	
		# Find the total number of data points in all the files being
		# analyzed.
	
		for i in range (len(fname[1])):
		        dat[1][i] = pickle.load(open(fname[1][i],'rb'))
	
	# Change back to the working directory.
	
	if( Person == 'm' ) :

		os.chdir("/home/pultrone/Desktop/FC/results/save/mark")

	else :

		os.chdir("/home/ahmadr/Desktop/GIT/Personal/Janus")
'''
	nd[0] = sum( [ len(dat[0][i]['b0'] ) for i in range ( len( fname[0] ) ) ] )
	nd[1] = sum( [ len(dat[1][i]['b0'] ) for i in range ( len( fname[1] ) ) ] )


	# Define the global parameters.

	t_time_hr    = [[],[]] # Time for the spectra

	t_b_hat      = [[],[]] # Average magnetic field direction
	t_b_vec      = [[],[]] # Average magnetic field ( vector )
	t_b_mag      = [[],[]] # Average magnetic field ( magnitude )
	t_b_x        = [[],[]] # x-component of the magnetic field.
	t_b_y        = [[],[]] # y-component of the magnetic field.
	t_b_z        = [[],[]] # z-component of the magnetic field.
	t_v_vec      = [[],[]] # Bulk velocity ( vector )
	t_v_mag      = [[],[]] # Bulk velocity ( magnitude )
	t_v_sig      = [[],[]] # Error in bulk velocity
	t_v_sig_x    = [[],[]] # Error in bulk velocity
	t_v_sig_y    = [[],[]] # Error in bulk velocity
	t_v_sig_z    = [[],[]] # Error in bulk velocity

	# Define parameters related to proton.

	t_p_n        = [[],[]] # Proton number density
	t_p_n_c      = [[],[]] # Proton core number density
	t_p_n_b      = [[],[]] # Proton beam number density
	t_p_nf       = [[],[]] # Beam fraction of proton
	t_p_n_c_sig  = [[],[]] # Error in proton core number density
	t_p_n_b_sig  = [[],[]] # Error in proton beam number density


	t_p_dv_c     = [[],[]] # Drift velocity of proton core
	t_p_dv_b     = [[],[]] # Drift velocity of proton beam
	f_t_p_dv_c   = [[],[]] # Filtered Drift velocity of proton core
	f_t_p_dv_b   = [[],[]] # Filtered Drift velocity of proton beam
	t_p_dv_vec_c = [[],[]] # Vector drift velocity of proton core
	t_p_dv_vec_b = [[],[]] # Vector drift velocity of proton beam

	t_p_t        = [[],[]] # Proton temperature
	t_p_t_c      = [[],[]] # Proton core temperature
	t_p_t_per_c  = [[],[]] # Proton core perpendicular temperature
	t_p_t_par_c  = [[],[]] # Proton core parallel temperature
	t_p_t_b      = [[],[]] # Proton beam temperature
	t_p_t_per_b  = [[],[]] # Proton beam perpendicular temperature
	t_p_t_par_b  = [[],[]] # Proton beam parallel temperature

	t_p_r        = [[],[]] # Anisotropy in proton temperature
	t_p_r_b      = [[],[]] # Anisotropy in proton beam temperature
	t_p_r_c      = [[],[]] # Anisotropy in proton core temperature

	t_p_w        = [[],[]] # Total thermal speed of proton

	t_p_w_par_c  = [[],[]] # Parallel thermal velocity of proton core
	t_p_w_per_c  = [[],[]] # Perpendicular thermal speed of proton core
	t_p_w_par_b  = [[],[]] # Prallel thermal velocity of proton beam
	t_p_w_per_b  = [[],[]] # Perpendicular thermal speed of proton beam

	t_p_w_par_c_sig = [[],[]] # Parallel thermal speed uncertainty of proton core
	t_p_w_per_c_sig = [[],[]] # Perpendicular thermal speed uncertainty of proton core
	t_p_w_par_b_sig = [[],[]] # Parallel thermal speed uncertainty of proton beam
	t_p_w_per_b_sig = [[],[]] # Perpendicular thermal speed uncertainty of proton beam
	
	# Define parameters related to alpha particle.

	t_a_n        = [[],[]] # Alpha number density
	t_a_n_c      = [[],[]] # Alpha core number density
	t_a_n_b      = [[],[]] # Alpha beam number density
	t_a_nf       = [[],[]] # Beam fraction of Alpha
	t_a_n_c_sig  = [[],[]] # Error in Alpha core number density
	t_a_n_b_sig  = [[],[]] # Error in Alpha beam number density

	t_a_dv_c     = [[],[]] # Drift velocity of Alpha core
	t_a_dv_b     = [[],[]] # Drift velocity of Alpha beam
	f_t_a_dv_c   = [[],[]] # Filtered Drift velocity of Alpha core
	f_t_a_dv_b   = [[],[]] # Filtered Drift velocity of Alpha beam
	t_a_dv_vec_c = [[],[]] # Vector drift velocity of Alpha core
	t_a_dv_vec_b = [[],[]] # Vector drift velocity of Alpha beam

	t_a_t        = [[],[]] # Alpha temperature
	t_a_t_c      = [[],[]] # Alpha core temperature
	t_a_t_per_c  = [[],[]] # Alpha core perpendicular temperature
	t_a_t_par_c  = [[],[]] # Alpha core parallel temperature
	t_a_t_b      = [[],[]] # Alpha beam temperature
	t_a_t_per_b  = [[],[]] # Alpha beam perpendicular temperature
	t_a_t_par_b  = [[],[]] # Alpha beam parallel temperature

	t_a_r        = [[],[]] # Anisotropy in Alpha temperature
	t_a_r_b      = [[],[]] # Anisotropy in Alpha beam temperature
	t_a_r_c      = [[],[]] # Anisotropy in Alpha core temperature

	t_a_w        = [[],[]] # Total thermal speed of Alpha
	t_a_w_par_c  = [[],[]] # Parallel thermal velocity of Alpha core
	t_a_w_per_c  = [[],[]] # Perpendicular thermal speed of Alpha core
	t_a_w_par_b  = [[],[]] # Prallel thermal speed of Alpha beam
	t_a_w_per_b  = [[],[]] # Perpendicular thermal speed of Alpha beam

	t_a_w_par_c_sig = [[],[]] # Parallel thermal velocity uncertainty of Alpha core
	t_a_w_per_c_sig = [[],[]] # Perpendicular thermal velocity uncertainty of Alpha core
	t_a_w_par_b_sig = [[],[]] # Parallel thermal velocity uncertainty of Alpha beam
	t_a_w_per_b_sig = [[],[]] # Perpendicular thermal velocity uncertainty of Alpha beam

	# Define parameters related to Oxygen particle.

	t_o_n        = [[],[]] # Oxygen number density
	t_o_n_c      = [[],[]] # Oxygen core number density
	t_o_n_b      = [[],[]] # Oxygen beam number density
	t_o_nf       = [[],[]] # Beam fraction of Oxygen
	t_o_n_c_sig  = [[],[]] # Error in Oxygen core number density

	t_o_dv_c     = [[],[]] # Drift velocity of Oxygen core
	t_o_dv_b     = [[],[]] # Drift velocity of Oxygen beam
	f_t_o_dv_c   = [[],[]] # Filtered Drift velocity of Oxygen core
	f_t_o_dv_b   = [[],[]] # Filtered Drift velocity of Oxygen beam
	t_o_dv_vec_c = [[],[]] # Vector drift velocity of Oxygen core
	t_o_dv_vec_b = [[],[]] # Vector drift velocity of Oxygen beam

	t_o_t        = [[],[]] # Oxygen temperature
	t_o_t_c      = [[],[]] # Oxygen core temperature
	t_o_t_b      = [[],[]] # Oxygen beam temperature
	t_o_r        = [[],[]] # Anisotropy in Oxygen temperature
	t_o_r_b      = [[],[]] # Anisotropy in Oxygen beam temperature
	t_o_r_c      = [[],[]] # Anisotropy in Oxygen core temperature

	t_o_w        = [[],[]] # Total thermal speed of Oxygen
	t_o_w_par_c  = [[],[]] # Parallel thermal velocity of Oxygen core
	t_o_w_per_c  = [[],[]] # Perpendicular thermal speed of Oxygen core
	t_o_w_par_b  = [[],[]] # Prallel thermal velocity of Oxygen beam
	t_o_w_per_b  = [[],[]] # Perpendicular thermal speed of Oxygen beam

	# Some other random required paramters.

	theta_b_v    = [[],[]] # Angle between average magnetic field and velocity

	r_tpb_tpc    = [[],[]] # Ratio of proton beam and core temperature 
	r_tab_tac    = [[],[]] # Ratio of alpha beam and core temperature
	r_tab_tpb    = [[],[]] # Ratio of alpha and proton beams temperature
	r_tac_tpc    = [[],[]] # Ratio of alpha and proton cores temperature

	mu_pcb       = [[],[]] # Reduced mass of proton core and beam
	mu_acb       = [[],[]] # Reduced mass of alpha core and beam

	dv2_p_b      = [[],[]] # Square of proton beam drift speed
	dv2_a_b      = [[],[]] # Square of alpha beam drift speed

	P_p_par_c    = [[],[]] # Parallel pressure exerted by the proton core
	P_p_per_c    = [[],[]] # Perpendicular pressure exerted by the proton core

	P_p_par_b    = [[],[]] # Parallel pressure exerted by the proton beam
	P_p_per_b    = [[],[]] # Perpendicular pressure exerted by the proton beam
 
	P_a_par_c    = [[],[]] # Parallel pressure exerted by the alpha core
	P_a_per_c    = [[],[]] # Perpendicular pressure exerted by the alpha core

	P_a_par_b    = [[],[]] # Parallel pressure exerted by the alpha beam
	P_a_per_b    = [[],[]] # Perpendicular pressure exerted by the alpha beam

	E_dv_p_b     = [[],[]] # Drift energy fraction of proton beam
	E_dv_a_b     = [[],[]] # Drift energy fraction of proton beam

	C_A_p_c      = [[],[]] # Alfven velocity ( proton core )

	alf_p_b      = [[],[]] # Alfvenicity of proton beam
	alf_a_b      = [[],[]] # Alfvenicity of alpha beam
 
	R_total_p    = [[],[]] # Total anisotropy of proton population
	R_total_p    = [[],[]] # Total anisotropy of proton population

	colat        = [[],[]] # Colatitude of the magnetic field

	dv_pc_pb     = [[],[]] # Difference in drift velocity of proton beam wrt proton core velocity
	dv_pc_ac     = [[],[]] # Difference in drift velocity of alpha core wrt proton core velocity
	dv_pc_ab     = [[],[]] # Difference in drift velocity of alpha beam wrt proton core velocity
	dv_pb_ab     = [[],[]] # Difference in drift velocity of proton beam wrt proton beam velocity
	dv_ac_ab     = [[],[]] # Difference in drift velocity of alpha beam wrt alpha core velocity


	# Time

	dat_time_sec      = [[],[]]
	dat_time_hr       = [[],[]]

	# Magnetic Field

	dat_b_hat         = [[],[]]
	dat_b_vec         = [[],[]]
	dat_b_mag         = [[],[]]

	# Velocity

	dat_v_vec         = [[],[]]
	dat_v_mag         = [[],[]]
	dat_v_sig_x       = [[],[]]
	dat_v_sig_y       = [[],[]]
	dat_v_sig_z       = [[],[]]

	# Proton

	dat_p_n           = [[],[]]
	dat_p_n_c         = [[],[]]
	dat_p_n_b         = [[],[]]
	dat_p_nf          = [[],[]]
	dat_p_n_c_sig     = [[],[]]
	dat_p_n_b_sig     = [[],[]]

	dat_p_dv_c        = [[],[]]
	dat_p_dv_b        = [[],[]]
	dat_p_dv_vec_c    = [[],[]]
	dat_p_dv_vec_b    = [[],[]]

	dat_p_t           = [[],[]]
	dat_p_t_c         = [[],[]]
	dat_p_t_per_c     = [[],[]]
	dat_p_t_par_c     = [[],[]]
	dat_p_t_b         = [[],[]]
	dat_p_t_per_b     = [[],[]]
	dat_p_t_par_b     = [[],[]]

	dat_p_r           = [[],[]]
	dat_p_r_c         = [[],[]]
	dat_p_r_b         = [[],[]]

	dat_p_w           = [[],[]]
	dat_p_w_par_c     = [[],[]]
	dat_p_w_per_c     = [[],[]]	
	dat_p_w_par_b     = [[],[]]
	dat_p_w_per_b     = [[],[]]

	dat_p_w_par_c_sig = [[],[]]
	dat_p_w_per_c_sig = [[],[]]
	dat_p_w_par_b_sig = [[],[]]
	dat_p_w_per_b_sig = [[],[]]

	# Alpha

	dat_a_n           = [[],[]]
	dat_a_n_c         = [[],[]]
	dat_a_n_b         = [[],[]]
	dat_a_nf          = [[],[]]
	dat_a_n_c_sig     = [[],[]]
	dat_a_n_b_sig     = [[],[]]

	dat_a_dv_c        = [[],[]]
	dat_a_dv_b        = [[],[]]
	dat_a_dv_vec_c    = [[],[]]
	dat_a_dv_vec_b    = [[],[]]

	dat_a_t           = [[],[]]
	dat_a_t_c         = [[],[]]
	dat_a_t_per_c     = [[],[]]
	dat_a_t_par_c     = [[],[]]
	dat_a_t_b         = [[],[]]
	dat_a_t_per_b     = [[],[]]
	dat_a_t_par_b     = [[],[]]

	dat_a_r           = [[],[]]
	dat_a_r_c         = [[],[]]
	dat_a_r_b         = [[],[]]

	dat_a_w           = [[],[]]
	dat_a_w_par_c     = [[],[]]
	dat_a_w_per_c     = [[],[]]
	dat_a_w_par_b     = [[],[]]
	dat_a_w_per_b     = [[],[]]

	dat_a_w_par_c_sig = [[],[]]
	dat_a_w_per_c_sig = [[],[]]
	dat_a_w_par_b_sig = [[],[]]
	dat_a_w_per_b_sig = [[],[]]

	# Oxygen

	dat_o_n           = [[],[]]
	dat_o_n_c         = [[],[]]
	dat_o_n_b         = [[],[]]
	dat_o_nf          = [[],[]]
	dat_o_n_c_sig     = [[],[]]

	dat_o_dv_c        = [[],[]]
	dat_o_dv_b        = [[],[]]
	dat_o_dv_vec_c    = [[],[]]
	dat_o_dv_vec_b    = [[],[]]

	dat_o_t           = [[],[]]
	dat_o_t_c         = [[],[]]
	dat_o_t_b         = [[],[]]

	dat_o_r           = [[],[]]
	dat_o_r_c         = [[],[]]
	dat_o_r_b         = [[],[]]

	dat_o_w           = [[],[]]
	dat_o_w_par_c     = [[],[]]
	dat_o_w_per_c     = [[],[]]
	dat_o_w_par_b     = [[],[]]
	dat_o_w_per_b     = [[],[]]

	for n in range ( len( fname ) ) :

		count  = 0
	
		for i in range ( len( fname[n] ) ) :

			print 'Reading file {}'.format(fname[n][i])
	
			for j in range( nd[n] ) :
	
				dat_time_sec[n] = [ (
			        	       dat[n][i]['time'][j]-t0 ).total_seconds()
				               for j in range( len( dat[n][i]['time'] ) ) ]
				dat_time_hr[n] = np.array( [ dat_time_sec[n][j]/3600
				                 for j in range(len(dat_time_sec[n]) ) ] )

				# Extract/compute everything related to magnetic
				# field.

			        dat_b_hat[n]      = np.array( dat[n][i]['b0_hat']       )
			        dat_b_vec[n]      = np.array( dat[n][i]['b0_vec']       )
			        dat_b_mag[n]      = np.array( dat[n][i]['b0_mag']       )
		
				# Extract/compute everything related to
				# velocity.
	
				dat_v_vec[n]      = np.array( dat[n][i]['v0_vec']       )
				dat_v_mag[n]      = np.array( dat[n][i]['v0_mag']       )
				dat_v_sig_x[n]    = np.array( dat[n][i]['v0_sig_x']     )
				dat_v_sig_y[n]    = np.array( dat[n][i]['v0_sig_y']     )
				dat_v_sig_z[n]    = np.array( dat[n][i]['v0_sig_z']     )

				# Extract other parameters computed in
				# 'janus_pyon'.

				# For proton

				dat_p_n[n]        = np.array( dat[n][i]['n_p']          )
				dat_p_n_c[n]      = np.array( dat[n][i]['n_p_c']        )
				dat_p_n_b[n]      = np.array( dat[n][i]['n_p_b']        )
#				dat_p_nf[n]       = np.array( dat[n][i]['n_p']
#				) /\
#				                 np.array( dat[n][i]['n_p_b']
#				                 )
				dat_p_n_c_sig[n]  = np.array( dat[n][i]['n_p_c_sig']    )
				dat_p_n_b_sig[n]  = np.array( dat[n][i]['n_p_b_sig']    )

				dat_p_dv_c[n]     = np.array( dat[n][i]['dv_p_c']       )
				dat_p_dv_b[n]     = np.array( dat[n][i]['dv_p_b']       )
				dat_p_dv_vec_c[n] = np.array( dat[n][i]['dv_p_c_vec']   )
				dat_p_dv_vec_b[n] = np.array( dat[n][i]['dv_p_b_vec']   )

				dat_p_t[n]        = np.array( dat[n][i]['t_p']          )
				dat_p_t_c[n]      = np.array( dat[n][i]['t_p_c']        )
				dat_p_t_per_c[n]  = np.array( dat[n][i]['t_per_p_c']    )
				dat_p_t_par_c[n]  = np.array( dat[n][i]['t_par_p_c']    )
				dat_p_t_b[n]      = np.array( dat[n][i]['t_p_b']        )
				dat_p_t_per_b[n]  = np.array( dat[n][i]['t_per_p_b']    )
				dat_p_t_par_b[n]  = np.array( dat[n][i]['t_par_p_b']    )

				dat_p_r[n]        = np.array( dat[n][i]['r_p']          )
				dat_p_r_c[n]      = np.array( dat[n][i]['r_p_c']        )
				dat_p_r_b[n]      = np.array( dat[n][i]['r_p_b']        )

				dat_p_w[n]        = np.array( dat[n][i]['w_p']          )
				dat_p_w_par_c[n]  = np.array( dat[n][i]['w_par_p_c']    )
				dat_p_w_per_c[n]  = np.array( dat[n][i]['w_per_p_c']    )
				dat_p_w_par_b[n]  = np.array( dat[n][i]['w_par_p_b']    )
				dat_p_w_per_b[n]  = np.array( dat[n][i]['w_per_p_b']    )

				dat_p_w_par_c_sig[n]  = np.array( dat[n][i]['w_par_p_c_sig']    )
				dat_p_w_per_c_sig[n]  = np.array( dat[n][i]['w_per_p_c_sig']    )
				dat_p_w_par_b_sig[n]  = np.array( dat[n][i]['w_par_p_b_sig']    )
				dat_p_w_per_b_sig[n]  = np.array( dat[n][i]['w_per_p_b_sig']    )

				# For Alpha

				dat_a_n[n]        = np.array( dat[n][i]['n_a']          )
				dat_a_n_c[n]      = np.array( dat[n][i]['n_a_c']        )
				dat_a_n_b[n]      = np.array( dat[n][i]['n_a_b']        )
#				dat_a_nf[n]       = np.array( dat[n][i]['n_a']
#				) /\
#				                 np.array( dat[n][i]['n_a_b']
#				                 )
				dat_a_n_c_sig[n]  = np.array( dat[n][i]['n_a_c_sig']    )
				dat_a_n_b_sig[n]  = np.array( dat[n][i]['n_a_b_sig']    )

				dat_a_dv_c[n]     = np.array( dat[n][i]['dv_a_c']       )
				dat_a_dv_b[n]     = np.array( dat[n][i]['dv_a_b']       )
				dat_a_dv_vec_c[n] = np.array( dat[n][i]['dv_a_c_vec']   )
				dat_a_dv_vec_b[n] = np.array( dat[n][i]['dv_a_b_vec']   )

				dat_a_t[n]        = np.array( dat[n][i]['t_a']          )
				dat_a_t_c[n]      = np.array( dat[n][i]['t_a_c']        )
				dat_a_t_per_c[n]  = np.array( dat[n][i]['t_per_a_c']    )
				dat_a_t_par_c[n]  = np.array( dat[n][i]['t_par_a_c']    )
				dat_a_t_b[n]      = np.array( dat[n][i]['t_a_b']        )
				dat_a_t_per_b[n]  = np.array( dat[n][i]['t_per_a_b']    )
				dat_a_t_par_b[n]  = np.array( dat[n][i]['t_par_a_b']    )

				dat_a_r[n]        = np.array( dat[n][i]['r_a']          )
				dat_a_r_c[n]      = np.array( dat[n][i]['r_a_c']        )
				dat_a_r_b[n]      = np.array( dat[n][i]['r_a_b']        )

				dat_a_w[n]        = np.array( dat[n][i]['w_a']          )
				dat_a_w_par_c[n]  = np.array( dat[n][i]['w_par_a_c']    )
				dat_a_w_per_c[n]  = np.array( dat[n][i]['w_per_a_c']    )
				dat_a_w_par_b[n]  = np.array( dat[n][i]['w_par_a_b']    )
				dat_a_w_per_b[n]  = np.array( dat[n][i]['w_per_a_b']    )

				dat_a_w_par_c_sig[n]  = np.array( dat[n][i]['w_par_a_c_sig']    )
				dat_a_w_per_c_sig[n]  = np.array( dat[n][i]['w_per_a_c_sig']    )
				dat_a_w_par_b_sig[n]  = np.array( dat[n][i]['w_par_a_b_sig']    )
				dat_a_w_per_b_sig[n]  = np.array( dat[n][i]['w_per_a_b_sig']    )

				# For Oxygen

				dat_o_n[n]        = np.array( dat[n][i]['n_o']          )
				dat_o_n_c[n]      = np.array( dat[n][i]['n_o_c']        )
				dat_o_n_b[n]      = np.array( dat[n][i]['n_o_b']        )
#				dat_o_nf[n]       = np.array( dat[n][i]['n_o']
#				) /\
#				    o            np.array( dat[n][i]['n_o_b']
#				    )
				dat_o_n_c_sig[n]  = np.array( dat[n][i]['n_o_c_sig']    )
	
				dat_o_dv_c[n]     = np.array( dat[n][i]['dv_o_c']       )
				dat_o_dv_b[n]     = np.array( dat[n][i]['dv_o_b']       )
				dat_o_dv_vec_c[n] = np.array( dat[n][i]['dv_o_c_vec']   )
				dat_o_dv_vec_b[n] = np.array( dat[n][i]['dv_o_b_vec']   )

				dat_o_t[n]        = np.array( dat[n][i]['t_o']          )
				dat_o_t_c[n]      = np.array( dat[n][i]['t_o_c']        )
				dat_o_t_b[n]      = np.array( dat[n][i]['t_o_b']        )

				dat_o_r[n]        = np.array( dat[n][i]['r_o']          )
				dat_o_r_c[n]      = np.array( dat[n][i]['r_o_c']        )
				dat_o_r_b[n]      = np.array( dat[n][i]['r_o_b']        )

				dat_o_w[n]        = np.array( dat[n][i]['w_o']          )
				dat_o_w_par_c[n]  = np.array( dat[n][i]['w_par_o_c']    )
				dat_o_w_per_c[n]  = np.array( dat[n][i]['w_per_o_c']    )
				dat_o_w_par_b[n]  = np.array( dat[n][i]['w_par_o_b']    )
				dat_o_w_per_b[n]  = np.array( dat[n][i]['w_per_o_b']    )

			inc = [ ( ( dat_p_n_c[n][j] is not None and dat_p_n_c[n][j] > 0.                            ) and
			          ( dat_p_n_b[n][j] is not None and dat_p_n_b[n][j] > 0. or dat_p_n_b[n][j] is None ) and
			          ( dat_a_n_c[n][j] is not None and dat_a_n_c[n][j] > 0. or dat_a_n_c[n][j] is None ) and
			          ( dat_a_n_b[n][j] is not None and dat_a_n_b[n][j] > 0. or dat_a_n_b[n][j] is None ) and
			          ( dat_o_n_c[n][j] is not None and dat_o_n_c[n][j] > 0. or dat_o_n_c[n][j] is None ) and
			          ( dat_p_r_c[n][j] > 0.1 and dat_p_r_c[n][j] < 10. )                                     )

			                 for j in range( len( dat_p_n_c[n] ) ) ]

		        tk = np.where( inc )[0]
	
		        if ( len( tk ) <= 1 ) :
		                continue

			sel_time_hr    = dat_time_hr[n][tk]

			# Extract/compute everything related to magnetic field.

		        sel_b_hat      = dat_b_hat[n][tk]
		        sel_b_vec      = dat_b_vec[n][tk]
		        sel_b_mag      = dat_b_mag[n][tk]
		
			# Extract/compute everything related to velocity.
	
			sel_v_vec      = dat_v_vec[n][tk]
			sel_v_mag      = dat_v_mag[n][tk]
			sel_v_sig_x    = dat_v_sig_x[n][tk]
			sel_v_sig_y    = dat_v_sig_y[n][tk]
			sel_v_sig_z    = dat_v_sig_z[n][tk]
			sel_v_sig      = sqrt( dat_v_sig_x[n]**2 + dat_v_sig_y[n]**2 +
			                                        dat_v_sig_z[n]**2   ) #FIXME wrong equation

			# For protons

			sel_p_n        = dat_p_n[n][tk]
			sel_p_n_c      = dat_p_n_c[n][tk]
			sel_p_n_b      = dat_p_n_b[n][tk]
#			sel_p_nf       = dat_p_nf[n][tk]

			sel_p_n_c_sig  = dat_p_n_c_sig[n][tk]
			sel_p_n_b_sig  = dat_p_n_b_sig[n][tk]
	
			sel_p_dv_c     = dat_p_dv_c[n][tk]
			sel_p_dv_b     = dat_p_dv_b[n][tk]
			sel_p_dv_vec_c = dat_p_dv_vec_c[n][tk]
			sel_p_dv_vec_b = dat_p_dv_vec_b[n][tk]
	
			sel_p_t        = dat_p_t[n][tk]
			sel_p_t_c      = dat_p_t_c[n][tk]
			sel_p_t_per_c  = dat_p_t_per_c[n][tk]
			sel_p_t_par_c  = dat_p_t_par_c[n][tk]
			sel_p_t_b      = dat_p_t_b[n][tk]
			sel_p_t_per_b  = dat_p_t_per_b[n][tk]
			sel_p_t_par_b  = dat_p_t_par_b[n][tk]

			sel_p_r        = dat_p_r[n][tk]
			sel_p_r_c      = dat_p_r_c[n][tk]
			sel_p_r_b      = dat_p_r_b[n][tk]

			sel_p_w        = dat_p_w[n][tk]
			sel_p_w_par_c  = dat_p_w_par_c[n][tk]
			sel_p_w_per_c  = dat_p_w_per_c[n][tk]
			sel_p_w_par_b  = dat_p_w_par_b[n][tk]
			sel_p_w_per_b  = dat_p_w_per_b[n][tk]

			sel_p_w_par_c_sig  = dat_p_w_par_c_sig[n][tk]
			sel_p_w_per_c_sig  = dat_p_w_per_c_sig[n][tk]
			sel_p_w_par_b_sig  = dat_p_w_par_b_sig[n][tk]
			sel_p_w_per_b_sig  = dat_p_w_per_b_sig[n][tk]

			# For Alpha

			sel_a_n        = dat_a_n[n][tk]
			sel_a_n_c      = dat_a_n_c[n][tk]
			sel_a_n_b      = dat_a_n_b[n][tk]
#			sel_a_nf       = dat_a_nf[n][tk]

			sel_a_n_c_sig  = dat_a_n_c_sig[n][tk]
			sel_a_n_b_sig  = dat_a_n_b_sig[n][tk]

			sel_a_dv_c     = dat_a_dv_c[n][tk]
			sel_a_dv_b     = dat_a_dv_b[n][tk]
			sel_a_dv_vec_c = dat_a_dv_vec_c[n][tk]
			sel_a_dv_vec_b = dat_a_dv_vec_b[n][tk]

			sel_a_t        = dat_a_t[n][tk]
			sel_a_t_c      = dat_a_t_c[n][tk]
			sel_a_t_per_c  = dat_a_t_per_c[n][tk]
			sel_a_t_par_c  = dat_a_t_par_c[n][tk]
			sel_a_t_b      = dat_a_t_b[n][tk]
			sel_a_t_per_b  = dat_a_t_per_b[n][tk]
			sel_a_t_par_b  = dat_a_t_par_b[n][tk]

			sel_a_r        = dat_a_r[n][tk]
			sel_a_r_c      = dat_a_r_c[n][tk]
			sel_a_r_b      = dat_a_r_b[n][tk]

			sel_a_w        = dat_a_w[n][tk]
			sel_a_w_par_c  = dat_a_w_par_c[n][tk]
			sel_a_w_per_c  = dat_a_w_per_c[n][tk]
			sel_a_w_par_b  = dat_a_w_par_b[n][tk]
			sel_a_w_per_b  = dat_a_w_per_b[n][tk]

			sel_a_w_par_c_sig  = dat_a_w_par_c_sig[n][tk]
			sel_a_w_per_c_sig  = dat_a_w_per_c_sig[n][tk]
			sel_a_w_par_b_sig  = dat_a_w_par_b_sig[n][tk]
			sel_a_w_per_b_sig  = dat_a_w_per_b_sig[n][tk]

			# For Oxygen

			sel_o_n        = dat_o_n[n][tk]
			sel_o_n_c      = dat_o_n_c[n][tk]
			sel_o_n_b      = dat_o_n_b[n][tk]
#			sel_o_nf       = dat_o_nf[n][tk]

			sel_o_n_c_sig  = dat_o_n_c_sig[n][tk]

			sel_o_dv_c     = dat_o_dv_c[n][tk]
			sel_o_dv_b     = dat_o_dv_b[n][tk]
			sel_o_dv_vec_c = dat_o_dv_vec_c[n][tk]
			sel_o_dv_vec_b = dat_o_dv_vec_b[n][tk]

			sel_o_t        = dat_o_t[n][tk]
			sel_o_t_c      = dat_o_t_c[n][tk]
			sel_o_t_b      = dat_o_t_b[n][tk]
			sel_o_r        = dat_o_r[n][tk]
			sel_o_r_c      = dat_o_r_c[n][tk]
			sel_o_r_b      = dat_o_r_b[n][tk]

			sel_o_w        = dat_o_w[n][tk]
			sel_o_w_par_c  = dat_o_w_par_c[n][tk]
			sel_o_w_per_c  = dat_o_w_per_c[n][tk]
			sel_o_w_par_b  = dat_o_w_par_b[n][tk]
			sel_o_w_per_b  = dat_o_w_per_b[n][tk]
	
	 		for k in range(len(sel_p_n)):

				t_time_hr[n]       += [ sel_time_hr[k]      ]
			        t_b_hat[n]         += [ sel_b_hat[k]        ]
			        t_b_vec[n]         += [ sel_b_vec[k]        ]
			        t_b_mag[n]         += [ sel_b_mag[k]        ]
				t_b_x[n]           += [ sel_b_vec[k][0]     ]
				t_b_y[n]           += [ sel_b_vec[k][1]     ]
				t_b_z[n]           += [ sel_b_vec[k][2]     ]

				# Extract/compute everything related to
				# velocity.
	
				t_v_vec[n]         += [ sel_v_vec[k]         ]
				t_v_mag[n]         += [ sel_v_mag[k]         ]
				t_v_sig[n]         += [ sel_v_sig[k]         ]
				t_v_sig_x[n]       += [ sel_v_sig_x[k]       ]
				t_v_sig_y[n]       += [ sel_v_sig_y[k]       ]
				t_v_sig_z[n]       += [ sel_v_sig_z[k]       ]

				# For protons

				t_p_n[n]           += [ sel_p_n[k]           ]
				t_p_n_c[n]         += [ sel_p_n_c[k]         ]
				t_p_n_b[n]         += [ sel_p_n_b[k]         ]
				if( sel_p_n_b[k] is not None ) :
					t_p_nf[n]  += [ sel_p_n_b[k] /
					                sel_p_n[k]           ]

				t_p_n_c_sig[n]     += [ sel_p_n_c_sig[k]     ]
				t_p_n_b_sig[n]     += [ sel_p_n_b_sig[k]     ]

				t_p_dv_c[n]        += [ sel_p_dv_c[k]        ]
				t_p_dv_b[n]        += [ sel_p_dv_b[k]        ]
				t_p_dv_vec_c[n]    += [ sel_p_dv_vec_c[k]    ]
				t_p_dv_vec_b[n]    += [ sel_p_dv_vec_b[k]    ]

				t_p_t[n]           += [ sel_p_t[k]           ]
				t_p_t_c[n]         += [ sel_p_t_c[k]         ]
				t_p_t_per_c[n]     += [ sel_p_t_per_c[k]     ]
				t_p_t_par_c[n]     += [ sel_p_t_par_c[k]     ]
				t_p_t_b[n]         += [ sel_p_t_b[k]         ]
				t_p_t_per_b[n]     += [ sel_p_t_per_b[k]     ]
				t_p_t_par_b[n]     += [ sel_p_t_par_b[k]     ]

				t_p_r[n]           += [ sel_p_r[k]           ]
				t_p_r_c[n]         += [ sel_p_r_c[k]         ]
				t_p_r_b[n]         += [ sel_p_r_b[k]         ]

				t_p_w[n]           += [ sel_p_w[k]           ]
				t_p_w_par_c[n]     += [ sel_p_w_par_c[k]     ]
				t_p_w_per_c[n]     += [ sel_p_w_per_c[k]     ]
				t_p_w_par_b[n]     += [ sel_p_w_par_b[k]     ]
				t_p_w_per_b[n]     += [ sel_p_w_per_b[k]     ]

				t_p_w_par_c_sig[n] += [ sel_p_w_par_c_sig[k] ]
				t_p_w_per_c_sig[n] += [ sel_p_w_per_c_sig[k] ]
				t_p_w_par_b_sig[n] += [ sel_p_w_par_b_sig[k] ]
				t_p_w_per_b_sig[n] += [ sel_p_w_per_b_sig[k] ]

				# For Alpha

				t_a_n[n]           += [ sel_a_n[k]           ]
				t_a_n_c[n]         += [ sel_a_n_c[k]         ]
				t_a_n_b[n]         += [ sel_a_n_b[k]         ]
				if( sel_a_n_b[k] is not None ) :
					t_a_nf[n]  += [ sel_a_n_b[k] /
					                sel_a_n[k]           ]

				t_a_n_c_sig[n]     += [ sel_a_n_c_sig[k]     ]
				t_a_n_b_sig[n]     += [ sel_a_n_b_sig[k]     ]

				t_a_dv_c[n]        += [ sel_a_dv_c[k]        ]
				t_a_dv_b[n]        += [ sel_a_dv_b[k]        ]
				t_a_dv_vec_c[n]    += [ sel_a_dv_vec_c[k]    ]
				t_a_dv_vec_b[n]    += [ sel_a_dv_vec_b[k]    ]
	
				t_a_t[n]           += [ sel_a_t[k]           ]
				t_a_t_c[n]         += [ sel_a_t_c[k]         ]
				t_a_t_per_c[n]     += [ sel_a_t_per_c[k]     ]
				t_a_t_par_c[n]     += [ sel_a_t_par_c[k]     ]
				t_a_t_b[n]         += [ sel_a_t_b[k]         ]
				t_a_t_per_b[n]     += [ sel_a_t_per_b[k]     ]
				t_a_t_par_b[n]     += [ sel_a_t_par_b[k]     ]

				t_a_r[n]           += [ sel_a_r[k]           ]
				t_a_r_c[n]         += [ sel_a_r_c[k]         ]
				t_a_r_b[n]         += [ sel_a_r_b[k]         ]

				t_a_w[n]           += [ sel_a_w[k]           ]
				t_a_w_par_c[n]     += [ sel_a_w_par_c[k]     ]
				t_a_w_per_c[n]     += [ sel_a_w_per_c[k]     ]
				t_a_w_par_b[n]     += [ sel_a_w_par_b[k]     ]
				t_a_w_per_b[n]     += [ sel_a_w_per_b[k]     ]

				t_a_w_par_c_sig[n] += [ sel_a_w_par_c_sig[k] ]
				t_a_w_per_c_sig[n] += [ sel_a_w_per_c_sig[k] ]
				t_a_w_par_b_sig[n] += [ sel_a_w_par_b_sig[k] ]
				t_a_w_per_b_sig[n] += [ sel_a_w_per_b_sig[k] ]

				# For Oxygen

				t_o_n[n]           += [ sel_o_n[k]           ]
				t_o_n_c[n]         += [ sel_o_n_c[k]         ]
				t_o_n_b[n]         += [ sel_o_n_b[k]         ]
				if( sel_o_n_b[k] is not None ) :
					t_o_nf[n]  += [ sel_o_n_b[k] /
					                sel_o_n[k]           ]

				t_o_n_c_sig[n]     += [ sel_o_n_c_sig[k]     ]

				t_o_dv_c[n]        += [ sel_o_dv_c[k]        ]
				t_o_dv_b[n]        += [ sel_o_dv_b[k]        ]
				t_o_dv_vec_c[n]    += [ sel_o_dv_vec_c[k]    ]
				t_o_dv_vec_b[n]    += [ sel_o_dv_vec_b[k]    ]

				t_o_t[n]           += [ sel_o_t[k]           ]
				t_o_t_c[n]         += [ sel_o_t_c[k]         ]
				t_o_t_b[n]         += [ sel_o_t_b[k]         ]
				t_o_r[n]           += [ sel_o_r[k]           ]
				t_o_r_c[n]         += [ sel_o_r_c[k]         ]
				t_o_r_b[n]         += [ sel_o_r_b[k]         ]

				t_o_w[n]           += [ sel_o_w[k]           ]
				t_o_w_par_c[n]     += [ sel_o_w_par_c[k]     ]
				t_o_w_par_b[n]     += [ sel_o_w_par_b[k]     ]
				t_o_w_per_c[n]     += [ sel_o_w_per_c[k]     ]
				t_o_w_per_b[n]     += [ sel_o_w_per_b[k]     ]

else :
	print 'Data not read, just running the plotting algorithm'
'''
'''
from scipy.stats import pearsonr
a = range(-40, 40)
new_data_1 = []
new_data_2 = []
corr_data_1 = []
corr_data_2 = []
corr_n_p_1 = []
corr_n_p_2 = []
for i in range(700):
	for j in a:
		if i >= j :
			if(t_hr[0][i+j] == t_hr[1][i]):
				if ( ( t_p_r_c[0][i+j] > 0.1 and t_p_r_c[0][i+j] < 10 ) and
				     ( t_p_r_c[1][i] > 0.1 and t_p_r_c[1][i] < 10 ) ) :
					new_data_1.append( t_hr[0][i+j] )
					new_data_2.append( t_hr[1][i] )
					corr_data_1.append( t_p_r_c[0][i+j] )
					corr_data_2.append( t_p_r_c[1][i] )
					corr_n_p_1.append( t_p_n[0][i+j] )
					corr_n_p_2.append( t_p_n[1][i] )
print pearsonr(corr_n_p_1, corr_n_p_2)
'''
'''
if ( data_run == 'y' ) :

	fz = 21 # Median filter size ( should be an odd number )

	f_t_p_dv_c = [[],[]]
	f_t_p_dv_b = [[],[]]
	f_t_a_dv_c = [[],[]]
	f_t_a_dv_b = [[],[]]
	f_t_o_dv_c = [[],[]]
	f_t_o_dv_b = [[],[]]

	for n in range( len( fname ) ):

		if ( len( fname[n] ) > 0 ) :

			f_t_p_dv_c[n] = medfilt( t_p_dv_c[n], fz )
			f_t_p_dv_b[n] = medfilt( t_p_dv_b[n], fz )
			f_t_a_dv_c[n] = medfilt( t_a_dv_c[n], fz )
			f_t_a_dv_b[n] = medfilt( t_a_dv_b[n], fz )
			f_t_o_dv_c[n] = medfilt( t_o_dv_c[n], fz )
			f_t_o_dv_b[n] = medfilt( t_o_dv_b[n], fz )

for n in range( len( fname ) ) :

	t_b_hat[n]         = [ float('nan') if i is None else i for i in t_b_hat[n] ]

	t_p_n[n]           = [ float('nan') if i is None else i for i in t_p_n[n]   ]
	t_p_n_c[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_n_c[n] ]
	t_p_n_b[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_n_b[n] ]

	t_p_n_c_sig[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_n_c_sig[n] ]
	t_p_n_b_sig[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_n_b_sig[n] ]

	t_p_dv_c[n]        = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_dv_c[n] ]
	t_p_dv_b[n]        = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_dv_b[n] ]

	t_a_n[n]           = [ float('nan') if i is None else i for i in t_a_n[n]   ]
	t_a_n_c[n]         = [ float('nan') if i is None else i for i in t_a_n_c[n] ]
	t_a_n_b[n]         = [ float('nan') if i is None else i for i in t_a_n_b[n] ]

	t_a_n_c_sig[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_n_c_sig[n] ]
	t_a_n_b_sig[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_n_b_sig[n] ]

	t_o_n[n]           = [ float('nan') if i is None else i for i in t_o_n[n]   ]

	t_a_dv_c[n]        = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_dv_c[n] ]
	t_a_dv_b[n]        = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_dv_b[n] ]

	t_v_vec[n]         = [ float('nan') if i is None else i for i in t_v_vec[n] ]

	t_p_r_c[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_r_c[n] ]
	t_p_r_b[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_r_b[n] ]
	t_a_r_c[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_r_c[n] ]
	t_a_r_b[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_r_b[n] ]

	t_p_t[n]           = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t[n]   ]
	t_p_t_c[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t_c[n] ]
	t_p_t_b[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t_b[n] ]
	t_p_t_par_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t_par_c[n] ]
	t_p_t_par_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t_par_b[n] ]
	t_p_t_per_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t_per_c[n] ]
	t_p_t_per_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_t_per_b[n] ]

	t_a_t[n]           = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t[n]   ]
	t_a_t_c[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t_c[n] ]
	t_a_t_b[n]         = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t_b[n] ]
	t_a_t_par_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t_par_c[n] ]
	t_a_t_par_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t_par_b[n] ]
	t_a_t_per_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t_per_c[n] ]
	t_a_t_per_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_t_per_b[n] ]
                         
	t_p_dv_b[n]        = [ float('nan') if i is None else i for i in t_p_dv_b[n]   ]

	t_p_w_par_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_w_par_c[n] ]
	t_p_w_per_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_w_per_c[n] ]
	t_p_w_par_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_w_par_b[n] ]
	t_p_w_per_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_p_w_per_b[n] ]

	t_a_w_par_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_w_par_c[n] ]
	t_a_w_per_c[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_w_per_c[n] ]
	t_a_w_par_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_w_par_b[n] ]
	t_a_w_per_b[n]     = [ float('nan') if ( i is 0 or i is None ) else i for i in t_a_w_per_b[n] ]

	t_p_w_par_c_sig[n] = [ float('nan') if i is None else i for i in t_p_w_par_c_sig[n]   ]
	t_p_w_per_c_sig[n] = [ float('nan') if i is None else i for i in t_p_w_per_c_sig[n]   ]
	t_p_w_par_b_sig[n] = [ float('nan') if i is None else i for i in t_p_w_par_b_sig[n]   ]
	t_p_w_per_b_sig[n] = [ float('nan') if i is None else i for i in t_p_w_per_b_sig[n]   ]

	t_a_w_par_c_sig[n] = [ float('nan') if i is None else i for i in t_a_w_par_c_sig[n]   ]
	t_a_w_per_c_sig[n] = [ float('nan') if i is None else i for i in t_a_w_per_c_sig[n]   ]
	t_a_w_par_b_sig[n] = [ float('nan') if i is None else i for i in t_a_w_par_b_sig[n]   ]
	t_a_w_per_b_sig[n] = [ float('nan') if i is None else i for i in t_a_w_per_b_sig[n]   ]

# Align Mark and Ramiz data

t_hr = [[],[]]
t_hr[0] = [ round( t_time_hr[0][j], 2 ) for j in range( len( t_time_hr[0] ) ) ]
t_hr[1] = [ round( t_time_hr[1][j], 2 ) for j in range( len( t_time_hr[1] ) ) ]


a = range(-40, 40)
new_data_1 = []
new_data_2 = []
corr_data_1 = []
corr_data_2 = []

M_hr = []
R_hr = []

M_p_n_c     = []
R_p_n_c     = []
M_p_n_c_sig = []
R_p_n_c_sig = []
M_p_n_b     = []
R_p_n_b     = []
M_p_n_b_sig = []
R_p_n_b_sig = []

M_a_n_c     = []
R_a_n_c     = []
M_a_n_c_sig = []
R_a_n_c_sig = []
M_a_n_b     = []
R_a_n_b     = []
M_a_n_b_sig = []
R_a_n_b_sig = []

for i in range(690):
	for j in a:
		if i >= j :
			if(t_hr[0][i+j] == t_hr[1][i]):
					if ( t_p_n_c[0][i+j] != float('inf') and
					     t_p_n_c[1][i]   != float('inf')     ) :

						M_hr.append( t_hr[0][i+j] )
						R_hr.append( t_hr[1][i] )

						M_p_n_c.append( t_p_n_c[0][i+j] )
						R_p_n_c.append( t_p_n_c[1][i] )
						M_p_n_c_sig.append( t_p_n_c_sig[0][i+j] )
						R_p_n_c_sig.append( t_p_n_c_sig[1][i] )
						M_p_n_b.append( t_p_n_b[0][i+j] )
						R_p_n_b.append( t_p_n_b[1][i] )
						M_p_n_b_sig.append( t_p_n_b_sig[0][i+j] )
						R_p_n_b_sig.append( t_p_n_b_sig[1][i] )

						M_a_n_c.append( t_a_n_c[0][i+j] )
						R_a_n_c.append( t_a_n_c[1][i] )
						M_a_n_c_sig.append( t_a_n_c_sig[0][i+j] )
						R_a_n_c_sig.append( t_a_n_c_sig[1][i] )
						M_a_n_b.append( t_a_n_b[0][i+j] )
						R_a_n_b.append( t_a_n_b[1][i] )
						M_a_n_b_sig.append( t_a_n_b_sig[0][i+j] )
						R_a_n_b_sig.append( t_a_n_b_sig[1][i] )

M_p_n_c     = np.array( M_p_n_c )
R_p_n_c     = np.array( R_p_n_c )
M_p_n_c_sig = np.array( M_p_n_c_sig )
R_p_n_c_sig = np.array( R_p_n_c_sig )
M_p_n_b     = np.array( M_p_n_b )
R_p_n_b     = np.array( R_p_n_b )
M_p_n_b_sig = np.array( M_p_n_b_sig )
R_p_n_b_sig = np.array( R_p_n_b_sig )

M_a_n_c     = np.array( M_a_n_c )
R_a_n_c     = np.array( R_a_n_c )
M_a_n_c_sig = np.array( M_a_n_c_sig )
R_a_n_c_sig = np.array( R_a_n_c_sig )
M_a_n_b     = np.array( M_a_n_b )
R_a_n_b     = np.array( R_a_n_b )
M_a_n_b_sig = np.array( M_a_n_b_sig )
R_a_n_b_sig = np.array( R_a_n_b_sig )

#ind = [ 30*i for i in range( len( M_hr )/30 ) ]
#labels = [ M_hr[j] for j in ind ]


count_pn  = 0
count_pnc = 0
count_pnb = 0

count_an  = 0
count_anc = 0
count_anb = 0

d_p_n = [ abs( M_p_n_c[i] + M_p_n_b[i] - R_p_n_c[i] - R_p_n_b[i]  )/
sqrt( M_p_n_c_sig[i]**2 + R_p_n_c_sig[i]**2 + M_p_n_b_sig[i]**2 + R_p_n_b_sig[i]**2 )
                                           for i in range( len( M_p_n_b ) ) ]

d_p_n_c = [ abs( M_p_n_c[i] - R_p_n_c[i]  )/
sqrt( M_p_n_c_sig[i]**2 + R_p_n_c_sig[i]**2  )
                                           for i in range( len( M_p_n_c ) ) ]

d_p_n_b = [ abs( M_p_n_b[i] - R_p_n_b[i]  )/
sqrt( R_p_n_b_sig[i]**2 + R_p_n_b_sig[i]**2 )
                                           for i in range( len( M_p_n_b ) ) ]

d_a_n = [ abs( M_a_n_c[i] + M_a_n_b[i] - R_a_n_c[i] - R_a_n_b[i]  )/
sqrt( M_a_n_c_sig[i]**2 + R_a_n_c_sig[i]**2 + M_a_n_c_sig[i]**2 + R_a_n_c_sig[i]**2 )
                                           for i in range( len( M_a_n_b ) ) ]

d_a_n_c = [ abs( M_a_n_c[i] - R_a_n_c[i]  )/
sqrt( M_a_n_c_sig[i]**2 + R_a_n_c_sig[i]**2  )
                                           for i in range( len( M_a_n_c ) ) ]

d_a_n_b = [ abs( M_a_n_b[i] - R_a_n_b[i]  )/
sqrt( R_a_n_b_sig[i]**2 + R_a_n_b_sig[i]**2 )
                                           for i in range( len( M_a_n_b ) ) ]

for i in range( len( d_n_p_b ) ) :

	if ( d_p_n[i] < 1.) :

		count_pn += 1

	if ( d_p_n_c[i] < 1.) :

		count_pnc += 1

	if ( d_p_n_b[i] < 1.) :

		count_pnb += 1

	if ( d_a_n[i] < 1. ) :

		count_an += 1

	if ( d_a_n_c[i] < 1.) :

		count_anc += 1

	if ( d_a_n_b[i] < 1.) :

		count_anb += 1

ll = float( len( M_a_n_c ) )

p_p_n   = 100.*float( count_pn  )/( ll - len([0 for x in d_p_n   if math.isnan( x ) ] ) )
p_p_n_c = 100.*float( count_pnc )/( ll - len([0 for x in d_p_n_c if math.isnan( x ) ] ) )
p_p_n_b = 100.*float( count_pnb )/( ll - len([0 for x in d_p_n_b if math.isnan( x ) ] ) )
p_a_n   = 100.*float( count_an  )/( ll - len([0 for x in d_a_n   if math.isnan( x ) ] ) )
p_a_n_c = 100.*float( count_anc )/( ll - len([0 for x in d_a_n_c if math.isnan( x ) ] ) )
p_a_n_b = 100.*float( count_anb )/( ll - len([0 for x in d_a_n_b if math.isnan( x ) ] ) )

m_p_n   = nanmedian( d_p_n   )
m_p_n_c = nanmedian( d_p_n_c )
m_p_n_b = nanmedian( d_p_n_b )
m_a_n   = nanmedian( d_a_n   )
m_a_n_c = nanmedian( d_a_n_c )
m_a_n_b = nanmedian( d_a_n_b )

#-----------------------------#
# WHOSE DATA ARE WE PLOTTING? #
#-----------------------------#

n = 1
	

# Co-latitude

colat[n] = [ 90. + 180. / pi * np.arctan( t_b_z[n][i] / sqrt( t_b_x[n][i]**2 + t_b_y[n][i]**2 ) )
                                                             for i in range( len( t_b_z[n] ) ) ]

# Anisotropy

t_b_hat[n]         = np.array( t_b_hat[n]         )
                               
t_p_n[n]           = np.array( t_p_n[n]           )
t_p_n_c[n]         = np.array( t_p_n_c[n]         )
t_p_n_b[n]         = np.array( t_p_n_b[n]         )
                               
t_p_n_c_sig[n]     = np.array( t_p_n_c_sig[n]     )
t_p_n_b_sig[n]     = np.array( t_p_n_b_sig[n]     )
                               
t_p_dv_c[n]        = np.array( t_p_dv_c[n]        )
t_p_dv_b[n]        = np.array( t_p_dv_b[n]        )
                               
t_a_n[n]           = np.array( t_a_n[n]           )
t_a_n_c[n]         = np.array( t_a_n_c[n]         )
t_a_n_b[n]         = np.array( t_a_n_b[n]         )
                               
t_a_n_c_sig[n]     = np.array( t_a_n_c_sig[n]     )
t_a_n_b_sig[n]     = np.array( t_a_n_b_sig[n]     )
                               
t_o_n[n]           = np.array( t_o_n[n]           )
                               
t_a_dv_c[n]        = np.array( t_a_dv_c[n]        )
t_a_dv_b[n]        = np.array( t_a_dv_b[n]        )
                               
t_v_vec[n]         = np.array( t_v_vec[n]         )
                               
t_p_r_c[n]         = np.array( t_p_r_c[n]         )
t_p_r_b[n]         = np.array( t_p_r_b[n]         )
t_a_r_c[n]         = np.array( t_a_r_c[n]         )
t_a_r_b[n]         = np.array( t_a_r_b[n]         )
                               
t_p_t[n]           = np.array( t_p_t[n]           )
t_p_t_c[n]         = np.array( t_p_t_c[n]         )
t_p_t_b[n]         = np.array( t_p_t_b[n]         )
t_p_t_par_c[n]     = np.array( t_p_t_par_c[n]     )
t_p_t_par_b[n]     = np.array( t_p_t_par_b[n]     )
t_p_t_per_c[n]     = np.array( t_p_t_per_c[n]     )
t_p_t_per_b[n]     = np.array( t_p_t_per_b[n]     )
                               
t_a_t[n]           = np.array( t_a_t[n]           )
t_a_t_c[n]         = np.array( t_a_t_c[n]         )
t_a_t_b[n]         = np.array( t_a_t_b[n]         )
t_a_t_par_c[n]     = np.array( t_a_t_par_c[n]     )
t_a_t_par_b[n]     = np.array( t_a_t_par_b[n]     )
t_a_t_per_c[n]     = np.array( t_a_t_per_c[n]     )
t_a_t_per_b[n]     = np.array( t_a_t_per_b[n]     )
                               
t_p_dv_b[n]        = np.array( t_p_dv_b[n]        )

t_p_w_par_c[n]     = np.array( t_p_w_par_c[n]     )
t_p_w_per_c[n]     = np.array( t_p_w_per_c[n]     )
t_p_w_par_b[n]     = np.array( t_p_w_par_b[n]     )
t_p_w_per_b[n]     = np.array( t_p_w_per_b[n]     )

t_a_w_par_c[n]     = np.array( t_a_w_par_c[n]     )
t_a_w_per_c[n]     = np.array( t_a_w_per_c[n]     )
t_a_w_par_b[n]     = np.array( t_a_w_par_b[n]     )
t_a_w_per_b[n]     = np.array( t_a_w_per_b[n]     )

t_p_w_par_c_sig[n] = np.array( t_p_w_par_c_sig[n] )
t_p_w_per_c_sig[n] = np.array( t_p_w_per_c_sig[n] )
t_p_w_par_b_sig[n] = np.array( t_p_w_par_b_sig[n] )
t_p_w_per_b_sig[n] = np.array( t_p_w_per_b_sig[n] )

t_a_w_par_c_sig[n] = np.array( t_a_w_par_c_sig[n] )
t_a_w_per_c_sig[n] = np.array( t_a_w_per_c_sig[n] )
t_a_w_par_b_sig[n] = np.array( t_a_w_par_b_sig[n] )
t_a_w_per_b_sig[n] = np.array( t_a_w_per_b_sig[n] )

aniso_err_p_c = sqrt( 4*t_p_w_par_c_sig[n]**2/t_p_w_par_c[n]**2 +
                      4*t_p_w_per_c_sig[n]**2/t_p_w_per_c[n]**2   ) * t_p_r_c[n]

aniso_err_p_b = sqrt( 4*t_p_w_par_b_sig[n]**2/t_p_w_par_b[n]**2 +
                      4*t_p_w_per_b_sig[n]**2/t_p_w_per_b[n]**2   ) * t_p_r_b[n]

aniso_err_a_c = sqrt( 4*t_a_w_par_c_sig[n]**2/t_a_w_par_c[n]**2 +
                      4*t_a_w_per_c_sig[n]**2/t_a_w_per_c[n]**2   ) * t_a_r_c[n]

aniso_err_a_b = sqrt( 4*t_a_w_par_b_sig[n]**2/t_a_w_par_b[n]**2 +
                      4*t_a_w_per_b_sig[n]**2/t_a_w_per_b[n]**2   ) * t_a_r_b[n]


# Ratio of temperatures

r_tpb_tpc[n] = t_p_t_b[n]/t_p_t_c[n]

r_tab_tac[n] = t_a_t_b[n]/t_a_t_c[n]

r_tab_tpb[n] = t_a_t_b[n]/t_p_t_b[n]

r_tac_tpc[n] = t_a_t_c[n]/t_p_t_c[n]

# Angle between velocity and the average magnetic field

theta_b_v[n] = [ np.degrees( np.arccos( np.dot(t_b_hat[n][i], t_v_vec[n][i] )/(
              np.linalg.norm( t_b_hat[n][i] ) * np.linalg.norm( t_v_vec[n][i] ) ) ) )
              for i in range( len( t_time_hr[n] ) )                        ]

# Energy in drift ( for proton beam )

mu_pcb[n] = [ const['m_p'] * t_p_n_c[n][i] * t_p_n_b[n][i] / ( t_p_n_c[n][i] + t_p_n_b[n][i] )
                                                    for i in range( len( t_p_n_c[n] ) ) ]

dv2_p_b[n] = [ 1.e6 * t_p_dv_b[n][i]**2 for i in range( len( t_p_dv_b[n] ) ) ]

# Calculate parallel pressure exerted by the proton core

for i in range( len( t_p_t_par_c[n] ) ) :

	if( t_p_t_par_c[n][i] is not None ) :

		P_p_par_c[n].append( t_p_n_c[n][i] * const['k_b'] * 1.e3 * t_p_t_par_c[n][i] )

	else :

		P_p_par_c[n].append( t_p_n_c[n][i] * const['k_b'] * 1.e3 * t_p_t_c[n][i] / sqrt(3.) )

# Calculate perpendicular pressure exerted by the proton core

for i in range( len( t_p_t_per_c[n] ) ) :

	if( t_p_t_per_c[n][i] is not None ) :

		P_p_per_c[n].append( t_p_n_c[n][i] * const['k_b'] * 1.e3 * t_p_t_per_c[n][i] )

	else :

		P_p_per_c[n].append( t_p_n_c[n][i] * const['k_b'] * 1.e3 * t_p_t_c[n][i] / sqrt(3.) )

# Calculate parallel pressure exerted by the proton beam

for i in range( len( t_p_t_par_b[n] ) ) :

	if( t_p_t_par_b[n][i] is not None ) :

		P_p_par_b[n].append( t_p_n_b[n][i] * const['k_b'] * 1.e3 * t_p_t_par_b[n][i] )

	else :

		P_p_par_b[n].append( t_p_n_b[n][i] * const['k_b'] * 1.e3 * t_p_t_b[n][i] / sqrt(3.) )

# Calculate perpendicular pressure exerted by the proton beam

for i in range( len( t_p_t_per_b[n] ) ) :

	if( t_p_t_per_b[n][i] is not None ) :

		P_p_per_b[n].append( t_p_n_b[n][i] * const['k_b'] * 1.e3 * t_p_t_per_b[n][i] )

	else :

		P_p_per_b[n].append( t_p_n_b[n][i] * const['k_b'] * 1.e3 * t_p_t_b[n][i] / sqrt(3.) )

E_dv_p_b[n] = [ mu_pcb[n][i] * dv2_p_b[n][i] / sqrt( P_p_par_c[n][i]**2 + P_p_par_b[n][i]**2 )
                                                for i in range( len( mu_pcb[n] ) ) ]

# Alfvenicity

C_A_p_c[n] = [ 22. * t_b_mag[n][i] / sqrt( t_p_n_c[n][i] + t_p_n_b[n][i] )
                                           for i in range( len( t_b_mag[n] ) ) ]

alf_p_b[n] = [ abs( t_p_dv_b[n][i] ) / C_A_p_c[n][i] for i in range( len( t_p_dv_b[n] ) ) ]

# Calculate the total anisotropy of the species

R_total_p[n] = [ ( P_p_par_c[n][i] + P_p_par_b[n][i] + mu_pcb[n][i] * dv2_p_b[n][i] )/
                 ( P_p_per_c[n][i] + P_p_per_b[n][i] ) for i in range( len( mu_pcb[n] ) ) ]

# Velocity differences among several species

dv_pc_pb[n] = ( t_p_dv_b[n] - t_p_dv_c[n] ) / C_A_p_c[n]
dv_pc_ac[n] = ( t_a_dv_c[n] - t_p_dv_c[n] ) / C_A_p_c[n]
dv_pc_ab[n] = ( t_a_dv_b[n] - t_p_dv_c[n] ) / C_A_p_c[n]
dv_pb_ab[n] = ( t_a_dv_b[n] - t_p_dv_b[n] ) / C_A_p_c[n]
dv_ac_ab[n] = ( t_a_dv_b[n] - t_a_dv_c[n] ) / C_A_p_c[n]

# Calculate the error in different data-sets

#nf = [ abs( t_p_n_c[n])
###############################################################################
## Figure Parameters
###############################################################################

#if len( t_hr[0] ) > 0 :
#	ind = [ 30*i for i in range( len( t_hr[0] )/30 ) ]
#else :

ind = [ 30*i for i in range( 1 +  len( t_hr[n] )/30 ) ]

labels = [ t_hr[n][j] for j in ind ]

dpi = 40 # DPI of the saved plots

s = 10 # Marker size

legend_transparency = 0.50 # Transparency of legend

ncol = 1 # Number of columns for legend

xmax = len( t_hr[n] )# - 26 # Maximum value of x-axis
'''
'''
###############################################################################
## First Figure
###############################################################################

f, axs1 = plt.subplots( 4, 1, sharex=True, squeeze=True )

axs1[0].axhline( 0, color='k', linewidth=2 )
axs1[0].scatter( range( len( t_hr[n] ) ), t_b_x[n], s=s, color='r', marker='^',
label=r'$B_x$' )                                  
axs1[0].scatter( range( len( t_hr[n] ) ), t_b_y[n], s=s, color='c', marker='<',
label=r'$B_y$' )                                  
axs1[0].scatter( range( len( t_hr[n] ) ), t_b_z[n], s=s, color='b', marker='>',
label=r'$B_z$' )
axs1[0].scatter( range( len( t_hr[n] ) ), t_b_mag[n], s=s, color='k', marker='.',
label=r'$|\vec{B}|$' )
axs1[0].scatter( range( len( t_hr[n] ) ), [ -b for b in( t_b_mag[n] ) ], s=s,
color='k', marker='.' )
axs1[0].set_ylabel( 'Magnetic Field (nT)', fontsize=18 )
axs1[0].set_xlim( 0, xmax )
axs1[0].set_ylim( -20, 20 )
axs1[0].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs1[0].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs1[1].scatter( range( len( t_hr[n] ) ), t_p_n[n], s=s, color='r', marker='^',
label=r'$n_p$' )                                  
axs1[1].scatter( range( len( t_hr[n] ) ), t_a_n[n], s=s, color='b', marker='D',
label=r'$n_a$' )                                  
axs1[1].scatter( range( len( t_hr[n] ) ), t_o_n[n], s=s, color='g', marker='s',
label=r'$n_o$' )
axs1[1].set_ylabel( r'$Number \ density \ (n/cm^{-3})$', fontsize=18 )
axs1[1].set_yscale( 'log' )
axs1[1].set_xlim( 0, xmax )
axs1[1].set_ylim( 0.001, 30 )
axs1[1].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs1[1].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs1[2].axhline( 0, color='k', linewidth=2 )
axs1[2].scatter( range( len( t_hr[n] ) ), t_p_dv_b[n], s=s, color='r', marker='d',
label=r'$\Delta V_{pb \parallel}$' )                 
axs1[2].scatter( range( len( t_hr[n] ) ), t_a_dv_c[n], s=s, color='g', marker='^',
label=r'$\Delta V_{ac \parallel}$' )                 
axs1[2].scatter( range( len( t_hr[n] ) ), t_a_dv_b[n], s=s, color='b', marker='v',
label=r'$\Delta V_{ab \parallel}$' )
axs1[2].scatter( range( len( t_hr[n] ) ), t_o_dv_c[n], s=s, color='c', marker='s',
label=r'$\Delta V_{oc \parallel}$' )
axs1[2].set_ylabel( 'Drift velocity (km/s)', fontsize=18 )
axs1[2].set_xlim( 0, xmax )
axs1[2].set_ylim( -60, 60 )
axs1[2].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs1[2].legend( ncol=3, framealpha=legend_transparency, loc=2, fontsize=18 )

axs1[3].scatter( range( len( t_hr[n] ) ), t_p_r_c[n], s=s, color='r',
marker='8', label=r'$R_{pc}$' )                     
axs1[3].scatter( range( len( t_hr[n] ) ), t_p_r_b[n], s=s, color='b',
marker='P', label=r'$R_{pb}$' )                     
axs1[3].scatter( range( len( t_hr[n] ) ), t_a_r_c[n], s=s, color='g',
marker='H', label=r'$R_{ac}$' )
axs1[3].set_ylabel( 'Anisotropy', fontsize=18 )
axs1[3].set_yscale( 'log' )
axs1[3].set_xlim( 0, xmax )
axs1[3].set_ylim( 0.1, 10 )
axs1[3].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs1[3].legend( ncol=3, framealpha=legend_transparency, loc=3, fontsize=18 )
axs1[3].set_xlabel( 'Time since T0 (Hr)', fontsize=18 )

axs1[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

#plt.yticks( fontsize=16 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs1 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Second Figure
###############################################################################

f, axs2 = plt.subplots( 4, 1, squeeze=True, sharex=True)

for a in axs2 :
	plt.setp(a.get_yticklabels()[ 0], visible=False)
	plt.setp(a.get_yticklabels()[-1], visible=False)

axs2[0].scatter( range( len( t_hr[n] ) ), t_p_n_b[n], s=s, marker='*', color='r',
label = r'$n_{pb}$' )
axs2[0].scatter( range( len( t_hr[n] ) ), t_p_n_c[n], s=s, marker='d', color='b',
label = r'$n_{pc}$' )
axs2[0].scatter( range( len( t_hr[n] ) ), t_p_n[n],   s=s, marker='.', color='g',
label = r'$n_p$' )
axs2[0].set_ylim( 0.1, 30  )
axs2[0].set_yscale( 'log' )
axs2[0].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs2[0].legend( ncol=ncol, framealpha=legend_transparency, loc=2, fontsize=18 )

axs2[1].scatter( range( len( t_hr[n] ) ), t_p_t_b[n], s=s, marker='*', color='r',
label = r'$T_{pb}$' )
axs2[1].scatter( range( len( t_hr[n] ) ), t_p_t_c[n], s=s, marker='d', color='b',
label = r'$T_{pc}$' )
axs2[1].scatter( range( len( t_hr[n] ) ), t_p_t[n],   s=s, marker='.', color='g',
label = r'$T_p$' )
axs2[1].set_ylim( 1, 1000 )
axs2[1].set_yscale( 'log' )
axs2[1].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs2[1].legend( ncol=ncol, framealpha=legend_transparency, loc=3, fontsize=18 )

axs2[2].scatter( range( len( t_hr[n] ) ), t_a_n_b[n], s=s, marker='*', color='r',
label = r'$n_{ab}$' )
axs2[2].scatter( range( len( t_hr[n] ) ), t_a_n_c[n], s=s, marker='d', color='c',
label = r'$n_{ac}$' )
axs2[2].scatter( range( len( t_hr[n] ) ), t_a_n[n],   s=s, marker='.', color='g',
label = r'$n_a$' )
axs2[2].set_ylim( 0.001, 3 )
axs2[2].set_yscale( 'log' )
axs2[2].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs2[2].legend( ncol=ncol, framealpha=legend_transparency, loc=3, fontsize=18 )

axs2[3].scatter( range( len( t_hr[n] ) ), t_a_t_b[n], s=s, marker='*', color='r',
label = r'$T_{ab}$' )
axs2[3].scatter( range( len( t_hr[n] ) ), t_a_t_c[n], s=s, marker='d', color='b',
label = r'$T_{ac}$' )
axs2[3].scatter( range( len( t_hr[n] ) ), t_a_t[n],   s=s, marker='.', color='g',
label = r'$T_a$' )
axs2[3].set_ylim( 10, 3000 )
axs2[3].set_xlim( 0, xmax )
axs2[3].set_yscale( 'log' )
axs2[3].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs2[3].legend( ncol=ncol, framealpha=legend_transparency, loc=3, fontsize=18 )
axs2[3].set_xlabel( 'Time since T0 (Hr)', fontsize=18 )

axs2[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs2 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[1] = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Third Figure
###############################################################################

f, axs3 = plt.subplots( 4, 1, squeeze=True, sharex=True)

axs3[0].scatter( range( len( t_hr[n] ) ), theta_b_v[n], s=s, marker='.', color='g',
label = r'$\theta_{\vec{B}\vec{V}}$' )
axs3[0].set_ylabel( 'Angle(degrees)', fontsize=22 )
axs3[0].set_ylim( 0., 150 )
axs3[0].set_xlim( 0, xmax )
axs3[0].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs3[0].legend( ncol=1, framealpha=legend_transparency, loc=1, fontsize=18 )

axs3[1].axhline( 0, color='gray', linewidth=2 )
axs3[1].scatter( range( len( t_hr[n] ) ), t_p_dv_b[n]/ C_A_p_c[n], s=s, marker='*', color='r',
label = r'$\Delta V_{pb}/C_A$' )
axs3[1].scatter( range( len( t_hr[n] ) ), t_a_dv_b[n]/ C_A_p_c[n], s=s, marker='*', color='b',
label = r'$\Delta V_{ab}/C_A$' )
axs3[1].set_ylabel( 'Drift Velocity(km/s) ', fontsize=22 )
axs3[1].set_ylim( -1.5, 1.5  )
axs3[1].set_xlim( 0, xmax )
axs3[1].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs3[1].legend( ncol=2, framealpha=legend_transparency, loc=2, fontsize=18 )

axs3[2].axhline( 0, color='gray', linewidth=2 )
axs3[2].scatter( range( len( t_hr[n] ) ), t_a_dv_c[n]/ C_A_p_c[n], s=s, marker='*', color='r',
label = r'$\Delta V_{ac}/C_A$' )
axs3[2].scatter( range( len( t_hr[n] ) ), t_a_dv_b[n]/ C_A_p_c[n], s=s, marker='*', color='b',
label = r'$\Delta V_{ab}/C_A$' )
axs3[2].set_ylabel( 'Drift Velocity(km/s) ', fontsize=22 )
axs3[2].set_ylim( -1.5, 1.5 )
axs3[2].set_xlim( 0, xmax )
axs3[2].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs3[2].legend( ncol=2, framealpha=legend_transparency, loc=2, fontsize=18 )

axs3[3].axhline( 0, color='gray', linewidth=2 )
axs3[3].scatter( range( len( t_hr[n] ) ), dv_pc_pb[n], s=s, color='g', marker='^', label=r'$( \Delta V_{pb} - \Delta V_{pc} ) / C_A $' )
axs3[3].scatter( range( len( t_hr[n] ) ), dv_ac_ab[n], s=s, color='m', marker='v', label=r'$( \Delta V_{ab} - \Delta V_{ac} ) / C_A $' )
axs3[3].set_ylim( -1.5, 1.5 )
axs3[3].set_xlim( 0, xmax )
axs3[3].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs3[3].legend( ncol=2, framealpha=legend_transparency, loc=2, fontsize=18 )


axs3[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )
axs3[3].set_xlabel( 'Hour of the day', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs3 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

#if( save_fig == 'y' ) :
#
#	os.chdir("/home/ahmadr/Desktop/GIT/Personal/Janus/figures")
#
#	plt.savefig( 'Stack_plot_drift_vel' +'.pdf', bbox_inches='tight', dpi=dpi )
#
#	os.chdir("/home/ahmadr/Desktop/GIT/Personal/Janus")

###############################################################################
## Fourth Figure
###############################################################################

f, axs4= plt.subplots( 5, 1, sharex=True, squeeze=True )

axs4[0].axhline( 0, color='c', linewidth=0.1 )
axs4[0].scatter( range( len( t_hr[n] ) ), dv_pc_pb[n], s=s, color='b', marker='^' )
axs4[0].set_ylabel( r'$( \Delta V_{pb} - \Delta V_{pc} ) / C_A $', fontsize=18 )
#axs4[0].set_yscale('log')
axs4[0].set_xlim( 0, xmax )
axs4[0].set_ylim( -1.5, 1.5 )
axs4[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs4[1].axhline( 0, color='c', linewidth=0.1 )
axs4[1].scatter( range( len( t_hr[n] ) ), dv_pc_ac[n], s=s, color='r', marker='^', label=r'$( \Delta V_{ac} - \Delta V_{pc} ) / C_A $' )
axs4[1].scatter( range( len( t_hr[n] ) ), dv_pb_ab[n], s=s, color='b', marker='v', label=r'$( \Delta V_{ab} - \Delta V_{pb} ) / C_A $' )
axs4[1].scatter( range( len( t_hr[n] ) ), dv_pc_ab[n], s=s, color='g', marker='*', label=r'$( \Delta V_{ab} - \Delta V_{pc} ) / C_A $' )
#axs4[1].set_ylabel( r'$( \Delta V_{ac} - \Delta V_{pc} ) / C_A $', fontsize=18 )
#axs4[1].set_yscale('log')
axs4[1].set_xlim( 0, xmax )
axs4[1].set_ylim( -1.5, 1.5 )
axs4[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs4[1].legend( ncol=3, framealpha=legend_transparency, loc=1, fontsize=18 )

axs4[2].axhline( 0, color='c', linewidth=0.1 )
axs4[2].scatter( range( len( t_hr[n] ) ), dv_pc_ab[n], s=s, color='g', marker='^' )
axs4[2].set_ylabel( r'$( \Delta V_{ab} - \Delta V_{pc} ) / C_A $', fontsize=18 )
#axs4[2].set_yscale('log')
axs4[2].set_xlim( 0, xmax )
axs4[2].set_ylim( -1.5, 1.5 )
axs4[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs4[3].axhline( 0, color='c', linewidth=0.1 )
axs4[3].scatter( range( len( t_hr[n] ) ), dv_pb_ab[n], s=s, color='m', marker='^' )
axs4[3].set_ylabel( r'$( \Delta V_{ab} - \Delta V_{pb} ) / C_A $', fontsize=18 )
#axs4[3].set_yscale('log')
axs4[3].set_xlim( 0, xmax )
axs4[3].set_ylim( -1.5, 1.5 )
axs4[3].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs4[4].axhline( 0, color='c', linewidth=0.1 )
axs4[4].scatter( range( len( t_hr[n] ) ), dv_ac_ab[n], s=s, color='k', marker='^' )
axs4[4].set_ylabel( r'$( \Delta V_{ab} - \Delta V_{ac} ) / C_A $', fontsize=18 )
#axs4[4].set_yscale('log')
axs4[4].set_xlim( 0, xmax )
axs4[4].set_ylim( -1.5, 1.5 )
axs4[4].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )


axs4[4].set_xlabel( r'Time since $T_0$ (Hr)', fontsize=18 )
axs4[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs4 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Fifth Figure
###############################################################################

f, axs5 = plt.subplots( 5, 1, squeeze=True, sharex=True)

axs5[0].scatter( range( len( t_hr[n] ) ), r_tpb_tpc[n], s=s, marker='*', color='r', label = r'$T_{pb}/T_{pc}$' )
axs5[0].set_yscale( 'log' )
axs5[0].set_ylim( 0.1, 100 )
axs5[0].set_xlim( 0, xmax )
axs5[0].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs5[0].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs5[1].scatter( range( len( t_hr[n] ) ), r_tab_tac[n], s=s, marker='*', color='b', label = r'$T_{ab}/T_{ac}$' )
axs5[1].set_yscale( 'log' )
axs5[1].set_ylim( 0.1, 100 )
axs5[1].set_xlim( 0, xmax )
axs5[1].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs5[1].legend( ncol=ncol, framealpha=legend_transparency, loc=4, fontsize=18 )

axs5[2].scatter( range( len( t_hr[n] ) ), r_tab_tpb[n], s=s, marker='*', color='g', label = r'$T_{ab}/T_{pb}$' )
axs5[2].set_yscale( 'log' )
axs5[2].set_ylim( 0.1, 100 )
axs5[2].set_xlim( 0, xmax )
axs5[2].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs5[2].legend( ncol=ncol, framealpha=legend_transparency, loc=4, fontsize=18 )

axs5[3].scatter( range( len( t_hr[n] ) ), r_tac_tpc[n], s=s, marker='*', color='m', label = r'$T_{ac}/T_{pc}$' )
axs5[3].set_yscale( 'log' )
axs5[3].set_ylim( 0.1, 100 )
axs5[3].set_xlim( 0, xmax )
axs5[3].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs5[3].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs5[4].scatter( range( len( t_hr[n] ) ), theta_b_v[n], s=s, marker='.', color='r', label = r'$\theta_{\vec{B}\vec{V}}$' )
axs5[4].set_ylabel( 'Angle(degrees)', fontsize=22 )
axs5[4].set_ylim( 0., 150 )
axs5[4].set_xlim( 0, xmax )
axs5[4].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
axs5[4].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )


axs5[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )
axs5[4].set_xlabel( 'Hour of the day', fontsize=18 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs5 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[1]  = ""
	tick_labels[-1] = ""
#	tick_labels[-2] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Sixth Figure
###############################################################################

f, axs6 = plt.subplots( 4, 1, sharex=True, squeeze=True )

axs6[0].scatter( range( len( t_hr[n] ) ), R_total_p[n], s=s, color='b', marker='^' )
axs6[0].set_ylabel( 'Total anisotropy', fontsize=18 )
axs6[0].set_yscale('log')
axs6[0].set_xlim( 0, xmax )
axs6[0].set_ylim( 0.1, 10 )
axs6[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs6[0].text( 300, 0.2, r'$R_{total} = \frac{ p_{\parallel pc} + p_{\parallel pb}+ \mu_{pcb} \times \Delta{V_{pb}}^2}{p_{\perp pc} + p_{\perp pb}}$ ', color='k', fontsize=22 )

axs6[1].scatter( range( len( t_hr[n] ) ), t_p_t_par_b[n]/t_p_t_par_c[n], s=s, color='r', marker='^', label= r'$T_{\parallel pb}/T_{\parallel pc } $')
axs6[1].scatter( range( len( t_hr[n] ) ), t_a_t_par_b[n]/t_a_t_par_c[n], s=s, color='g', marker='^', label= r'$T_{\parallel ab}/T_{\parallel ac } $')
#axs6[1].scatter( range( len( t_hr[n] ) ), t_p_t_par_b[n]/t_p_t_par_c[n], s=s, color='r', marker='^' )
#axs6[1].set_ylabel( r'$T_{\parallel pb}/T_{\parallel pc } $', fontsize=18 )
axs6[1].set_yscale('log')
axs6[1].set_xlim( 0, xmax )
axs6[1].set_ylim( 0.1, 100 )
axs6[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs6[1].legend( ncol=2, framealpha=legend_transparency, loc=3, fontsize=18 )

#axs6[2].scatter( range( len( t_hr[n] ) ), t_a_t_par_b[n]/t_a_t_par_c[n], s=s, color='g', marker='^' )
#axs6[2].set_ylabel( r'$T_{\parallel ab}/T_{\parallel ac } $', fontsize=18 )
#axs6[2].set_yscale('log')
#axs6[2].set_xlim( 0, xmax )
#axs6[2].set_ylim( 0.1, 100 )
#axs6[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs6[2].scatter( range( len( t_hr[n] ) ), t_a_t_par_c[n]/t_p_t_par_c[n], s=s, color='m', marker='^' )
axs6[2].set_ylabel( r'$T_{\parallel ac}/T_{\parallel pc } $', fontsize=18 )
axs6[2].set_yscale('log')
axs6[2].set_xlim( 0, xmax )
axs6[2].set_ylim( 0.1, 100 )
axs6[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs6[3].scatter( range( len( t_hr[n] ) ), t_a_t_par_b[n]/t_p_t_par_b[n], s=s, color='k', marker='^' )
axs6[3].set_ylabel( r'$T_{\parallel ab}/T_{\parallel pb } $', fontsize=18 )
axs6[3].set_yscale('log')
axs6[3].set_xlim( 0, xmax )
axs6[3].set_ylim( 0.1, 100 )
axs6[3].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs6[3].set_xlabel( r'Time since $T_0$ (Hr)', fontsize=18 )
axs6[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs6 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[1] = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Seventh Figure
###############################################################################

f, axs7 = plt.subplots( 4, 1, sharex=True, squeeze=True )

axs7[0].scatter( range( len( t_hr[n] ) ), R_total_p[n], s=s, color='b', marker='^' )
axs7[0].set_ylabel( 'Total anisotropy', fontsize=18 )
axs7[0].set_yscale('log')
axs7[0].set_xlim( 0, xmax )
axs7[0].set_ylim( 0.1, 10 )
axs7[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs7[0].text( 300, 0.2, r'$R_{total} = \frac{ p_{\parallel pc} + p_{\parallel pb}+ \mu_{pcb} \times \Delta{V_{pb}}^2}{p_{\perp pc} + p_{\perp pb}}$ ', color='k', fontsize=22 )

axs7[1].scatter( range( len( t_hr[n] ) ), t_p_t_per_b[n]/t_p_t_per_c[n], s=s, color='r', marker='^', label= r'$T_{\perp pb}/T_{\perp pc } $')
axs7[1].scatter( range( len( t_hr[n] ) ), t_a_t_per_b[n]/t_a_t_per_c[n], s=s, color='g', marker='^', label= r'$T_{\perp ab}/T_{\perp ac } $')
#axs7[1].set_ylabel( r'$T_{\perp pb}/T_{\perp pc } $', fontsize=18 )
axs7[1].set_yscale('log')
axs7[1].set_xlim( 0, xmax )
axs7[1].set_ylim( 0.1, 100 )
axs7[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs7[1].legend( ncol=2, framealpha=legend_transparency, loc=3, fontsize=18 )

#axs7[2].scatter( range( len( t_hr[n] ) ), t_a_t_per_b[n]/t_a_t_per_c[n], s=s, color='g', marker='^' )
#axs7[2].set_ylabel( r'$T_{\perp ab}/T_{\perp ac } $', fontsize=18 )
#axs7[2].set_yscale('log')
#axs7[2].set_xlim( 0, xmax )
#axs7[2].set_ylim( 0.1, 100 )
#axs7[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs7[2].scatter( range( len( t_hr[n] ) ), t_a_t_per_c[n]/t_p_t_per_c[n], s=s, color='m', marker='^' )
axs7[2].set_ylabel( r'$T_{\perp ac}/T_{\perp pc } $', fontsize=18 )
axs7[2].set_yscale('log')
axs7[2].set_xlim( 0, xmax )
axs7[2].set_ylim( 0.1, 100 )
axs7[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs7[3].scatter( range( len( t_hr[n] ) ), t_a_t_per_b[n]/t_p_t_per_b[n], s=s, color='k', marker='^' )
axs7[3].set_ylabel( r'$T_{\perp ab}/T_{\perp pb } $', fontsize=18 )
axs7[3].set_yscale('log')
axs7[3].set_xlim( 0, xmax )
axs7[3].set_ylim( 0.1, 100 )
axs7[3].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs7[3].set_xlabel( r'Time since $T_0$ (Hr)', fontsize=18 )
axs7[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs7 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[1] = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Eigth Figure
###############################################################################

f, axs8 = plt.subplots( 4, 1, sharex=True, squeeze=True )

axs8[0].axhline( 30,  color='gray', linewidth=1, ls='-')
axs8[0].axhline( 150, color='gray', linewidth=1, ls='-')
axs8[0].scatter( range( len( t_hr[n] ) ), colat[n],     s=s, color='b', marker='^', label=r'$\lambda$' )
axs8[0].scatter( range( len( t_hr[n] ) ), theta_b_v[n], s=s, color='r', marker='.', label = r'$\theta_{\vec{B}\vec{V}}$' )
#axs8[0].set_ylabel( 'Co-latitude', fontsize=18 )
axs8[0].set_xlim( 0, xmax )
axs8[0].set_ylim( 0, 180 )
axs8[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs8[0].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs8[1].scatter( range( len( t_hr[n] ) ), t_p_r_c[n], marker='<', color='b', label=r'$R_{pc}$' )
axs8[1].scatter( range( len( t_hr[n] ) ), t_a_r_c[1], marker='>', color='r', label=r'$R_{ac}$' )
#axs8[1].errorbar( range( len( t_hr[n] ) ), t_p_r_c[n], yerr=aniso_err_p_c, marker='<', color='b', fmt='o', ecolor='m', label=r'$R_{pc}$' )
#axs8[1].errorbar( range( len( t_hr[n] ) ), t_a_r_c[1], yerr=aniso_err_a_c, marker='>', color='r', fmt='o', ecolor='g', label=r'$R_{ac}$' )
axs8[1].set_ylabel( 'Anisotropy', fontsize=18 )
axs8[1].set_yscale( 'log' )
axs8[1].set_xlim( 0, xmax )
axs8[1].set_ylim( 0.1, 10 )
axs8[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs8[1].legend( ncol=2, framealpha=legend_transparency, loc=4, fontsize=18 )

axs8[2].scatter( range( len( t_hr[n] ) ), E_dv_p_b[n], s=s, color='b',marker='8' )
axs8[2].set_ylabel( r'$E_{{\Delta}v,pb}$', fontsize=18 )
axs8[2].set_xlim( 0.1, xmax )
axs8[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs8[3].scatter( range( len( t_hr[n] ) ), alf_p_b[n], s=s, color='b',marker='8' )
axs8[3].set_ylabel( 'Alfvenicity', fontsize=18 )
axs8[3].set_xlim( 0, xmax )
axs8[3].set_ylim( 0, 1.5 )
axs8[3].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs8[3].set_xlabel( r'Time since $T_0$ (Hr)', fontsize=18 )

axs8[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs8 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )
	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[n] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Ninth Figure
###############################################################################

f, axs9 = plt.subplots( 4, 1, sharex=True, squeeze=True )

axs9[0].errorbar( range( len( t_hr[n] ) ), t_p_r_c[n], yerr=aniso_err_p_c, marker='<', color='b', fmt='o', ecolor='m' )
axs9[0].set_ylabel( r'$R_{pc}$', fontsize=18 )
axs9[0].set_yscale( 'log' )
axs9[0].set_xlim( 0, xmax )
axs9[0].set_ylim( 0.1, 10 )
axs9[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs9[1].errorbar( range( len( t_hr[n] ) ), t_p_r_b[n], yerr=aniso_err_p_b, marker='<', color='r', fmt='o', ecolor='g' )
axs9[1].set_ylabel( r'$R_{pb}$', fontsize=18 )
axs9[1].set_yscale( 'log' )
axs9[1].set_xlim( 0, xmax )
axs9[1].set_ylim( 0.1, 10 )
axs9[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs9[2].errorbar( range( len( t_hr[n] ) ), t_a_r_c[n], yerr=aniso_err_a_c, marker='<', color='b', fmt='o', ecolor='m' )
axs9[2].set_ylabel( r'$R_{ac}$', fontsize=18 )
axs9[2].set_yscale( 'log' )
axs9[2].set_xlim( 0, xmax )
axs9[2].set_ylim( 0.1, 10 )
axs9[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )

axs9[3].errorbar( range( len( t_hr[n] ) ), t_a_r_b[n], yerr=aniso_err_a_b, marker='<', color='r', fmt='o', ecolor='g' )
axs9[3].set_ylabel( r'$R_{ab}$', fontsize=18 )
axs9[3].set_yscale( 'log' )
axs9[3].set_xlim( 0, xmax )
axs9[3].set_ylim( 0.1, 10 )
axs9[3].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )


axs9[3].set_xlabel( r'Time since $T_0$ (Hr)', fontsize=18 )
axs9[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs9 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	tick_labels[1]  = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( t_hr[1] ) )[j] for j in ind ], labels,
rotation=45, fontsize=16 )

###############################################################################
## Tenth Figure
###############################################################################

# Define new indexes and labels for the modified data

new_ind = [ 30*i for i in range( len( M_hr )/30 ) ]

new_labels = [ M_hr[j] for j in new_ind ]

f, axs10 = plt.subplots( 3, 1, sharex=True, squeeze=True )

axs10[0].axhline( 1, color='c', lw=0.1 )
axs10[0].scatter( range( len( M_hr ) ), d_p_n, s=s, color='b', marker='^' )
axs10[0].set_ylabel( r'$|\frac{n_{pM}-n_{pR}}{\sqrt{{\sigma_M}^2 + {\sigma_R}^2}}|$', fontsize=28 )
#axs10[0].set_yscale('log')
axs10[0].set_xlim( 0, xmax )
axs10[0].set_ylim( 0, 2 )
axs10[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs10[0].text( 550, 1.6, 'Percentage < 1 = %s\n Meadian = %s ' %( round( p_p_n, 4 ), round( m_p_n, 4 ) ) , color='r', fontsize=18 )

axs10[1].axhline( 1, color='c', lw=0.1 )
axs10[1].scatter( range( len( M_hr ) ), d_p_n_c, s=s, color='b', marker='^' )
axs10[1].set_ylabel( r'$|\frac{n_{pcM}-n_{pcR}}{\sqrt{{\sigma_M}^2 + {\sigma_R}^2}}|$', fontsize=28 )
#axs10[1].set_yscale('log')
axs10[1].set_xlim( 0, xmax )
axs10[1].set_ylim( 0, 2 )
axs10[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs10[1].text( 550, 1.6, 'Percentage < 1 = %s\n Meadian = %s ' %( round( p_p_n_c, 4 ), round( m_p_n_c, 4 ) ) , color='r', fontsize=18 )

axs10[2].axhline( 1, color='c', lw=0.1 )
axs10[2].scatter( range( len( M_hr ) ), d_p_n_b, s=s, color='b', marker='^' )
axs10[2].set_ylabel( r'$|\frac{n_{pbM}-n_{pbR}}{\sqrt{{\sigma_M}^2 + {\sigma_R}^2}}|$', fontsize=28 )
#axs10[2].set_yscale('log')
axs10[2].set_xlim( 0, xmax )
axs10[2].set_ylim( 0, 2 )
axs10[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs10[2].text( 550, 1.6, 'Percentage < 1 = %s\n Meadian = %s ' %( round( p_p_n_b, 4 ), round( m_p_n_b, 4 ) ) , color='r', fontsize=18 )

axs10[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs10 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( M_hr ) )[j] for j in new_ind ], new_labels,
rotation=45, fontsize=16 )

###############################################################################
## Eleventh Figure
###############################################################################

f, axs11 = plt.subplots( 3, 1, sharex=True, squeeze=True )

axs11[0].axhline( 1, color='c', lw=0.1 )
axs11[0].scatter( range( len( M_hr ) ), d_a_n, s=s, color='b', marker='^' )
axs11[0].set_ylabel( r'$|\frac{n_{aM}-n_{aR}}{\sqrt{{\sigma_M}^2 + {\sigma_R}^2}}|$', fontsize=28 )
#axs11[0].set_yscale('log')
axs11[0].set_xlim( 0, xmax )
axs11[0].set_ylim( 0, 2 )
axs11[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs11[0].text( 550, 1.6, 'Percentage < 1 = %s\n Meadian = %s ' %( round( p_a_n, 4 ), round( m_a_n, 4 ) ) , color='r', fontsize=18 )

axs11[1].axhline( 1, color='c', lw=0.1 )
axs11[1].scatter( range( len( M_hr ) ), d_a_n_c, s=s, color='b', marker='^' )
axs11[1].set_ylabel( r'$|\frac{n_{acM}-n_{acR}}{\sqrt{{\sigma_M}^2 + {\sigma_R}^2}}|$', fontsize=28 )
#axs11[1].set_yscale('log')
axs11[1].set_xlim( 0, xmax )
axs11[1].set_ylim( 0, 2 )
axs11[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs11[1].text( 550, 1.6, 'Percentage < 1 = %s\n Meadian = %s ' %( round( p_a_n_c, 4 ), round( m_a_n_c, 4 ) ) , color='r', fontsize=18 )

axs11[2].axhline( 1, color='c', lw=0.1 )
axs11[2].scatter( range( len( M_hr ) ), d_a_n_b, s=s, color='b', marker='^' )
axs11[2].set_ylabel( r'$|\frac{n_{abM}-n_{pbR}}{\sqrt{{\sigma_M}^2 + {\sigma_R}^2}}|$', fontsize=28 )
#axs11[2].set_yscale('log')
axs11[2].set_xlim( 0, xmax )
axs11[2].set_ylim( 0, 2 )
axs11[2].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs11[2].text( 550, 1.6, 'Percentage < 1 = %s\n Meadian = %s ' %( round( p_a_n_b, 4 ), round( m_a_n_b, 4 ) ) , color='r', fontsize=18 )

axs10[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Managing tick marks and all

for a in axs11 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ range( len( M_hr ) )[j] for j in new_ind ], new_labels,
rotation=45, fontsize=16 )

###############################################################################
## Last Figure
###############################################################################

f, axs12 = plt.subplots( 2, 1, sharex=True, squeeze=True )

axs12[0].scatter( M_hr, M_p_n_c, s=s, color='b', marker='^', label='Mark' )
axs12[0].scatter( R_hr, R_p_n_c, s=s, color='r', marker='<', label='Ramiz' )
axs12[0].fill_between( M_hr, M_p_n_c - M_p_n_c_sig, M_p_n_c + M_p_n_c_sig,
                     alpha=0.5, edgecolor='b', facecolor='#73a2ef')
axs12[0].fill_between( R_hr, R_p_n_c - R_p_n_c_sig, R_p_n_c + R_p_n_c_sig,
                     alpha=0.5, edgecolor='r', facecolor='#e5625e')
axs12[0].set_ylabel( r'$n_{pc}$ $(cm^{-3})$', fontsize=18 )
axs12[0].set_yscale('log')
axs12[0].set_xlim( 0, 24 )
axs12[0].set_ylim( 0.1, 40 )
axs12[0].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs12[0].legend( loc=1, fontsize=18 )
axs12[1].scatter( M_hr, M_p_n_b, s=s, color='b', marker='^', label='Mark' )
axs12[1].scatter( R_hr, R_p_n_b, s=s, color='r', marker='<', label='Ramiz' )
axs12[1].fill_between( M_hr, M_p_n_b - M_p_n_b_sig, M_p_n_b + M_p_n_b_sig,
                     alpha=0.5, edgecolor='b', facecolor='#73a2ef')
axs12[1].fill_between( R_hr, R_p_n_b - R_p_n_b_sig, R_p_n_b + R_p_n_b_sig,
                     alpha=0.5, edgecolor='r', facecolor='#e5625e')
axs12[1].set_ylabel( r'$n_{pb}$ $(cm^{-3})$', fontsize=18 )
axs12[1].set_yscale('log')
axs12[1].set_xlim( 0, 24 )
axs12[1].set_ylim( 0.1, 40 )
axs12[1].grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
axs12[1].legend( loc=1, fontsize=18 )
axs12[1].set_xlabel( r'Time since $T_0$ (Hr)', fontsize=18 )
axs12[0].set_title( r'$T_0 = 2014-02-19/00:00:00$', fontsize=22 )

plt.yticks( fontsize=16 )
plt.subplots_adjust(wspace=0, hspace=0)
plt.tight_layout()

# Managing tick marks and all

for a in axs12 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	tick_labels[0]  = ""
	tick_labels[-1] = ""
	a.set_yticklabels( tick_labels )

plt.xticks( [ M_hr[j] for j in new_ind ], new_labels, rotation=45, fontsize=16 )

pdf = matplotlib.backends.backend_pdf.PdfPages("Stack_Plots_all.pdf")

for fig in xrange(1, f.number+1 ): ## will open an empty extra figure :(
	pdf.savefig( fig )
pdf.close()
'''
print 'It took','%.6f'% (time.time()-start), 'seconds.'
