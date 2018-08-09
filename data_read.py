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
plt.close()

#Place= raw_input('Are you using work or home computer? (w for work, h for home) ==> ')
Place='w'
if Place=='w' :
        os.chdir("/home/ahmadr/Desktop/GIT/master/results/save")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research/results/save")

#os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research/results/save")

fname=[]
i = 0

#for file in glob.glob("janus_2008-11-04-12-00-41_2008-11-04-12-52-53.jns"):
#for file in glob.glob("janus_2008-11-04-10-45-35_2008-11-04-12-33-18.jns"):
for file in glob.glob("00-0307.jns"):
	fname.append( file )

dat    = [0]*len(fname)

# Find the total number of data points in all the files being analyzed.

for i in range (len(fname)):
        dat[i] = pickle.load(open(fname[i],'rb'))

# Change back to the working directory.

if Place == 'w' :
        os.chdir("/home/ahmadr/Desktop/GIT/master")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research")

nd = sum( [ len(dat[i]['b0'] ) for i in range ( len( fname ) ) ] )

t_b0      = [0]*nd # Magnetic field
t_bs      = [0]*nd # Error in Magnetic field
t_br      = [0]*nd # Ratio of standard deviation and magnitude of Magnetic field
t_rp      = [0]*nd # Anisotropy in proton temperature
t_rb      = [0]*nd # Anisotropy in proton beam temperature
t_rc      = [0]*nd # Anisotropy in proton core temperature
t_np      = [0]*nd # Proton number density
t_nc      = [0]*nd # Proton core number density
t_nb      = [0]*nd # Proton beam number density
t_fvpc    = [0]*nd # Fluctuating velocity of proton core
t_fvpb    = [0]*nd # Fluctuating velocity of proton beam
t_dvpc    = [0]*nd # Drift velocity of proton core
t_dvpb    = [0]*nd # Drift velocity of proton beam
t_wparc   = [0]*nd # Parallel thermal velocity of proton core
t_wparb   = [0]*nd # Prallel thermal velocity of proton beam
t_wperc   = [0]*nd # Perpendicular thermal speed of proton core
t_wperb   = [0]*nd # Perpendicular thermal speed of proton beam
t_wp      = [0]*nd # Total thermal speed of proton
t_dvvecpc = [0]*nd # Vector drift velocity of proton core
t_dvvecpb = [0]*nd # Vector drift velocity of proton beam
t_s       = [0]*nd # Skewness
t_k       = [0]*nd # Kurtosis
t_tpc     = [0]*nd # Proton core temperature
t_tpb     = [0]*nd # Proton beam temperature
t_nf      = [0]*nd # Total number density
t_wparp   = [0]*nd # Total thermal speed of proton
t_b_r     = [0]*nd
t_nsig    = [0]*nd
t_bmag    = [0]*nd
t_vmag    = [0]*nd
t_vsig    = [0]*nd


t_b0 = [0]*nd
t_bmag = [0]*nd
t_vmag = [0]*nd
t_vsig = [0]*nd


t_p_n = [0]*nd
t_p_nc = [0]*nd
t_p_nb = [0]*nd
t_p_nsig = [0]*nd
t_p_dvpb = [0]*nd
t_p_wparc = [0]*nd
t_p_wparb = [0]*nd
t_p_wperc = [0]*nd
t_p_wperb = [0]*nd
t_p_wp = [0]*nd
t_p_nf = [0]*nd
t_p_tpc = [0]*nd
t_p_tpb = [0]*nd
t_p_wparp = [0]*nd

t_a_n = [0]*nd
t_a_nc = [0]*nd
t_a_nb = [0]*nd
t_a_nsig = [0]*nd
t_a_dvpb = [0]*nd
t_a_wparc = [0]*nd
t_a_wparb = [0]*nd
t_a_wperc = [0]*nd
t_a_wperb = [0]*nd
t_a_wp = [0]*nd
t_a_nf = [0]*nd
t_a_tpc = [0]*nd
t_a_tpb = [0]*nd
t_a_wparp = [0]*nd



count  = 0

for i in range ( len( fname ) ) :

	for j in range( nd ) :

		# Extract/compute everything related to magnetic field.

	        dat_b_hat      = np.array( dat[i]['b0_hat']       )
	        dat_b_mag      = np.array( dat[i]['b0_mag']       )
	
		# Extract/compute everything related to velocity.

		dat_v0_sig_x   = np.array( dat[i]['v0_sig_x']     )
		dat_v0_sig_y   = np.array( dat[i]['v0_sig_y']     )
		dat_v0_sig_z   = np.array( dat[i]['v0_sig_z']     )
		dat_v0_mag     = np.array( dat[i]['v0_mag']       )

		# Extract other parameters computed in 'janus_pyon'.

		# For proton

		dat_r_p        = np.array( dat[i]['r_p']          )
		dat_r_p_c      = np.array( dat[i]['r_p_c']        )
		dat_r_p_b      = np.array( dat[i]['r_p_b']        )
		dat_n_p        = np.array( dat[i]['n_p']          )
		dat_n_p_c_sig  = np.array( dat[i]['n_p_c_sig']    )
		dat_n_p_b_sig  = np.array( dat[i]['n_p_b_sig']    )
		dat_n_p_c      = np.array( dat[i]['n_p_c']        )
		dat_n_p_b      = np.array( dat[i]['n_p_b']        )
		dat_dv_p_b     = np.array( dat[i]['dv_p_b']       )
		dat_w_par_p_c  = np.array( dat[i]['w_par_p_c']    )
		dat_w_per_p_c  = np.array( dat[i]['w_per_p_c']    )
		dat_w_par_p_b  = np.array( dat[i]['w_par_p_b']    )
		dat_w_per_p_b  = np.array( dat[i]['w_per_p_b']    )
		dat_w_p        = np.array( dat[i]['w_p']          )
		dat_t_p_c      = np.array( dat[i]['t_par_p_c']    )
		dat_t_p_b      = np.array( dat[i]['t_par_p_b']    )
		dat_w_par_p    = np.array( dat[i]['w_par_p']      )
		dat_v0_mag     = np.array( dat[i]['v0_mag']       )

		# For alpha

		dat_r_a        = np.array( dat[i]['r_a']          )
		dat_r_a_c      = np.array( dat[i]['r_a_c']        )
		dat_r_a_b      = np.array( dat[i]['r_a_b']        )
		dat_n_a        = np.array( dat[i]['n_a']          )
		dat_n_a_c_sig  = np.array( dat[i]['n_a_c_sig']    )
		dat_n_a_b_sig  = np.array( dat[i]['n_a_b_sig']    )
		dat_n_a_c      = np.array( dat[i]['n_a_c']        )
		dat_n_a_b      = np.array( dat[i]['n_a_b']        )
		dat_dv_a_b     = np.array( dat[i]['dv_a_b']       )
		dat_w_par_a_c  = np.array( dat[i]['w_par_a_c']    )
		dat_w_per_a_c  = np.array( dat[i]['w_per_a_c']    )
		dat_w_par_a_b  = np.array( dat[i]['w_par_a_b']    )
		dat_w_per_a_b  = np.array( dat[i]['w_per_a_b']    )
		dat_w_a        = np.array( dat[i]['w_a']          )
		dat_t_a_c      = np.array( dat[i]['t_par_a_c']    )
		dat_t_a_b      = np.array( dat[i]['t_par_a_b']    )
		dat_w_par_a    = np.array( dat[i]['w_par_a']      )

#	        inc = [ ( ( dat_n_p_b[j]  is not None ) and ( dat_n_p_b[j] >  0 ) and
#	                ( dat_n_p[j] is not None ) and ( dat_n_p[j]   >  0 ) and
#	                ( dat_s_p[j] is not None ) and ( dat_s_p[j]   != 0 ) and
#	                ( dat_s_p[j] is not None ) and
#		        ( dat_dv_p_b[j] is not None ) and  
#	                ( dat_r_p_b[j] > .1 )      and ( dat_r_p_c[j] < 10 ) and 
#	                ( dat_r_p_c[j] > .1 )      and ( dat_r_p_b[j] < 10 )   )
#	
#	                for j in range( len( dat_n_p_b ) ) ]
	
        inc = [ ( ( dat_n_p_b[j]  is not None ) and ( dat_n_p_b[j] >  0 ) )
	                            for j in range( len( dat_n_p_b ) ) ]

        tk = np.where( inc )[0]

        if ( len( tk ) <= 1 ) :
                continue

        sel_b0        = dat_b_hat[tk]
	sel_p_bmag    = dat_b_mag[tk]
	sel_p_vmag    = dat_v0_mag[tk]
	sel_p_vsig    = sqrt( dat_v0_sig_x**2 + dat_v0_sig_y**2 +
	                                      dat_v0_sig_z**2   )

	# For protons

        sel_p_np      = dat_n_p[tk]
        sel_p_nc      = dat_n_p_c[tk]
        sel_p_nb      = dat_n_p_b[tk]
	sel_p_nsig    = dat_n_p_b_sig[tk]+dat_n_p_c_sig[tk]
        sel_p_dvpb    = dat_dv_p_b[tk]
        sel_p_wparc   = dat_w_par_p_c[tk]
        sel_p_wparb   = dat_w_par_p_b[tk]
        sel_p_wperc   = dat_w_per_p_c[tk]
        sel_p_wperb   = dat_w_per_p_b[tk]
	sel_p_wp      = dat_w_p[tk]
        sel_p_nf      = dat_n_p_b[tk] / dat_n_p[tk]
        sel_p_tpc     = dat_t_p_c[tk]
        sel_p_tpb     = dat_t_p_b[tk]
	sel_p_wparp   = dat_w_par_p[tk]

	# For alpha

        sel_a_np      = dat_n_a[tk]
        sel_a_nc      = dat_n_a_c[tk]
        sel_a_nb      = dat_n_a_b[tk]
	#sel_a_nsig    = dat_n_a_b_sig[tk]+dat_n_a_c_sig[tk]
        sel_a_dvpb    = dat_dv_a_b[tk]
        sel_a_wparc   = dat_w_par_a_c[tk]
        sel_a_wparb   = dat_w_par_a_b[tk]
        sel_a_wperc   = dat_w_per_a_c[tk]
        sel_a_wperb   = dat_w_per_a_b[tk]
	sel_a_wp      = dat_w_a[tk]
#        sel_a_nf      = dat_n_a_b[tk] / dat_n_a[tk]
        sel_a_tpc     = dat_t_a_c[tk]
        sel_a_tpb     = dat_t_a_b[tk]
	sel_a_wparp   = dat_w_par_a[tk]

        for k in range(len(sel_np)):

		t_b0[count]     = sel_b0[k] 
		t_bmag[count]   = sel_bmag[k] 
		t_vmag[count]   = sel_vmag[k] 
		t_vsig[count]   = sel_vsig[k] 

		# For protons

		t_p_n[count]      = sel_np[k] 
		t_p_nc[count]     = sel_nc[k] 
		t_p_nb[count]     = sel_nb[k] 
		t_p_nsig[count]   = sel_nsig[k] 
		t_p_dvpb[count]   = sel_dvpb[k] 
		t_p_wparc[count]  = sel_wparc[k]
		t_p_wparb[count]  = sel_wparb[k]
		t_p_wperc[count]  = sel_wperc[k]
		t_p_wperb[count]  = sel_wperb[k]
		t_p_wp[count]     = sel_wp[k] 
		t_p_nf[count]     = sel_nf[k] 
		t_p_tpc[count]    = sel_tpc[k] 
		t_p_tpb[count]    = sel_tpb[k] 
		t_p_wparp[count]  = sel_wparp[k]

		# For protons

		t_a_n[count]     = sel_np[k] 
		t_a_nc[count]     = sel_nc[k] 
		t_a_nb[count]     = sel_nb[k] 
#		t_a_nsig[count]   = sel_nsig[k] 
		t_a_dvpb[count]   = sel_dvpb[k] 
		t_a_wparc[count]  = sel_wparc[k]
		t_a_wparb[count]  = sel_wparb[k]
		t_a_wperc[count]  = sel_wperc[k]
		t_a_wperb[count]  = sel_wperb[k]
		t_a_wp[count]     = sel_wp[k] 
#		t_a_nf[count]     = sel_nf[k] 
		t_a_tpc[count]    = sel_tpc[k] 
		t_a_tpb[count]    = sel_tpb[k] 
		t_a_wparp[count]  = sel_wparp[k]

                count           += 1

plt.subplot( 4, 1, 1 )

plt.scatter( range( len( t_np ) ), t_p_nc, color='r', marker='^', label='proton core density' )
plt.scatter( range( len( t_np ) ), t_p_nb, color='b', marker='^', label='proton beam density' )
#plt.scatter( range( len( t_np ) ), t_a_nc, color='g', marker='>', label='alpha core density' )
#plt.scatter( range( len( t_np ) ), t_a_nb, color='m', marker='<', label='alpha beam density' )
plt.legend()

plt.subplot( 4, 1, 2 )

plt.scatter( range( len( t_np ) ), t_p_tpc, color='r', marker='>', label='proton core temperature' )
plt.scatter( range( len( t_np ) ), t_p_tpb, color='b', marker='<', label='proton beam temperatur ' )
plt.legend()


plt.show()
plt.tight_layout()

print ('It took','%.6f'% (time.time()-start), 'seconds.')
