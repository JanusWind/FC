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

for j in range( nd1 ) :

	dat1_b_x_rot = np.array( dat1['b0_fields'][j]['rot_smt'] )[0]

	dat1_b_y_sig_rot[j] = dat1['sig_b0_fields'][j]['sig_rot_smt'][1] 
	dat1_b_z_sig_rot[j] = dat1['sig_b0_fields'][j]['sig_rot_smt'][2]

for j in range( nd2 ) :

	dat2_b_x_rot = np.array( dat2['b0_fields'][j]['rot_smt'] )[0]

	dat2_b_y_sig_rot[j] = dat2['sig_b0_fields'][j]['sig_rot_smt'][1] 
	dat2_b_z_sig_rot[j] = dat2['sig_b0_fields'][j]['sig_rot_smt'][2]

	dat3_b_x_rot = np.array( dat3['b0_fields'][j]['rot_smt'] )[0]

	dat3_b_y_sig_rot[j] = dat3['sig_b0_fields'][j]['sig_rot_smt'][1] 
	dat3_b_z_sig_rot[j] = dat3['sig_b0_fields'][j]['sig_rot_smt'][2]

dat2_b_x_rot = np.array( dat2['b0_fields'][0]['rot_smt'] )
dat3_b_x_rot = np.array( dat3['b0_fields'][0]['rot_smt'] )


dat2_b_y_sig_rot = np.array( dat2['sig_b0_fields'][1]['sig_rot_smt'] )
dat2_b_z_sig_rot = np.array( dat2['sig_b0_fields'][1]['sig_rot_smt'] ) 

dat3_b_y_sig_rot = np.array( dat3['sig_b0_fields'][1]['sig_rot_smt'] )
dat3_b_z_sig_rot = np.array( dat3['sig_b0_fields'][1]['sig_rot_smt'] ) 

