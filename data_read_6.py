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

#n_data = raw_input('Which file numbers do you want to run the code for ==>  ')
#n_data = [ int( n_data[j] ) for j in range( len( n_data ) ) ]

# Change the directory in which the saved file exists.

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/data/edited")

# Define the names of files to be analysed.

fname1 = 'janus_raw_mag_med_flt_21_fv_pcb_2008-11-04-12-01_2008-11-04-13-01.jns'

dat1 = [0]*len( fname1 )
dat1 = pickle.load( open( fname1, 'rb' ) )
nd1  = len( dat1['b0'] )

# Change back the directory to the working directory.

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

# Define all the parameters to be used during analysis.

dat1_time         = []

dat1_db_x_rng_avg = []
dat1_db_y_rng_avg = []
dat1_db_z_rng_avg = []
dat1_db_rng_avg   = []

dat1_b_avg        = []

dat1_fv_p_c       = []
dat1_fv_p_b       = []
dat1_sig_fv_p_c   = []
dat1_sig_fv_p_b   = []

dat1_alfvel       = []

dat1_s_fv_p_c     = []
dat1_s_fv_p_b     = []
dat1_s_sig_fv_p_c = []
dat1_s_sig_fv_p_b = []

dat1_s_db         = []

# Exaract the data from '.jns' file.

for j in range( nd1 ) :

	dat1_time.append( dat1['time'][j].time().strftime("%H-%M") )

	dat1_db_x_rng_avg.append( dat1['b0_fields_db'][j]['mfi_set_rng_avg'][0] )
	dat1_db_y_rng_avg.append( dat1['b0_fields_db'][j]['mfi_set_rng_avg'][1] )
	dat1_db_z_rng_avg.append( dat1['b0_fields_db'][j]['mfi_set_rng_avg'][2] )


	dat1_db_rng_avg.append( sqrt( 2 * ( std( dat1_db_x_rng_avg )**2 +
	                                    std( dat1_db_x_rng_avg )**2 +
	                                    std( dat1_db_x_rng_avg )**2 ) ) )

	dat1_b_avg.append( sqrt(
	           mean( dat1['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
	           mean( dat1['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
	           mean( dat1['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 ) )

	dat1_fv_p_c.append( dat1['fv_p_c'][j] )
	dat1_fv_p_b.append( dat1['fv_p_c'][j] )
	dat1_sig_fv_p_c.append( dat1['sig_fv_p_c'][j] )
	dat1_sig_fv_p_c.append( dat1['sig_fv_p_c'][j] )

	dat1_alfvel.append( dat1['alfvel_p'][j] )


	dat1_s_fv_p_c.append( dat1_fv_p_c[j]/dat1_alfvel[j] )
	dat1_s_fv_p_b.append( dat1_fv_p_b[j]/dat1_alfvel[j] )
	dat1_s_sig_fv_p_c.append( dat1_sig_fv_p_c[j]/dat1_alfvel[j] )
	dat1_s_sig_fv_p_b.append( dat1_sig_fv_p_b[j]/dat1_alfvel[j] )

	dat1_s_db.append( dat1_db_rng_avg[j]/dat1_b_avg[j] )

plt.figure( )

plt.scatter( range( len( dat1 ) ), dat1_fv_p_c )

plt,show()

print ('It took','%.6f'% (time.time()-start), 'seconds.')
