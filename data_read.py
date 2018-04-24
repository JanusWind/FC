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
#plt.close()

#Place= raw_input('Are you using work or home computer? (w for work, h for home) ==> ')
Place='w'
if Place=='w' :
        os.chdir("/home/ahmadr/Desktop/GIT/fm_development/results/save")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research/results/save")

#os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research/results/save")

fname=[]
i = 0

#for file in glob.glob("janus_2008-11-04-12-00-41_2008-11-04-12-52-53.jns"):
#for file in glob.glob("janus_2008-11-04-10-45-35_2008-11-04-12-33-18.jns"):
for file in glob.glob("janus_2008-11-04-10-45-35_2008-11-04-12-23-31_fm.jns"):
	fname.append( file )

dat    = [0]*len(fname)

# Find the total number of data points in all the files being analyzed.

for i in range (len(fname)):
        dat[i] = pickle.load(open(fname[i],'rb'))

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
sig_b     = [0]*nd
sig_bb    = [0]*nd
error_sigbb = [0]*nd
t_av      = [0]*nd

dat_b_x_sig_raw = [0]*nd
dat_b_y_sig_raw = [0]*nd
dat_b_z_sig_raw = [0]*nd
               
dat_b_x_sig_rot = [0]*nd
dat_b_y_sig_rot = [0]*nd
dat_b_z_sig_rot = [0]*nd
               
dat_b_x_sig_fit = [0]*nd
dat_b_y_sig_fit = [0]*nd
dat_b_z_sig_fit = [0]*nd

count  = 0

for i in range ( len( fname ) ) :

	for j in range( nd ) :

	# Extract/compute everything related to magnetic field.

		dat_b_fields_raw = np.array( dat[i]['b0_fields'][j]['raw_smt'] )
		dat_b_fields_rot = np.array( dat[i]['b0_fields'][j]['rot_smt'] )
		dat_b_fields_fit = np.array( dat[i]['b0_fields'][j]['fit_smt'] )
	
		dat_b_fields_sig_raw = np.array( dat[i]['sig_b0_fields'][j]['sig_raw_smt'] )
		dat_b_fields_sig_rot = np.array( dat[i]['sig_b0_fields'][j]['sig_rot_smt'] )
		dat_b_fields_sig_fit = np.array( dat[i]['sig_b0_fields'][j]['sig_fit_smt'] )
	
		dat_b_x_raw = dat_b_fields_raw[0]
	
		dat_b_y_raw = dat_b_fields_raw[1]
	
		dat_b_z_raw = dat_b_fields_raw[2]
	
		dat_b_x_rot = dat_b_fields_rot[0]
	
		dat_b_y_rot = dat_b_fields_rot[1]
	
		dat_b_z_rot = dat_b_fields_rot[2]
	
		dat_b_x_fit = dat_b_fields_fit[0]
	
		dat_b_y_fit = dat_b_fields_fit[1]
	
		dat_b_z_fit = dat_b_fields_fit[2]
	
		dat_b_x_sig_raw[j] = dat_b_fields_sig_raw[0]
		dat_b_y_sig_raw[j] = dat_b_fields_sig_raw[1]
		dat_b_z_sig_raw[j] = dat_b_fields_sig_raw[2]
	
		dat_b_x_sig_rot[j] = dat_b_fields_sig_rot[0]
		dat_b_y_sig_rot[j] = dat_b_fields_sig_rot[1]
		dat_b_z_sig_rot[j] = dat_b_fields_sig_rot[2]
	
		dat_b_x_sig_fit[j] = dat_b_fields_sig_fit[0]
		dat_b_y_sig_fit[j] = dat_b_fields_sig_fit[1]
		dat_b_z_sig_fit[j] = dat_b_fields_sig_fit[2]
	
		sig_b[j] = sqrt ( dat_b_y_sig_rot[j]**2 + dat_b_z_sig_rot[j]**2 )

#		sig_b2[j]      = sqrt( sum( dat_b_y_rot**2 + dat_b_z_rot**2 ) /
#		                                       ( len( dat_b_x_rot    ) ) )

		error_sigbb[j] = abs( sig_b[j] - dat_b_x_sig_rot[j] )

		sig_bb[j] = sig_b[j] / mean( dat_b_x_rot )
	
	        dat_b_hat      = np.array( dat[i]['b0_hat']       )
	        dat_b_mag      = np.array( dat[i]['b0_mag']       )
	        dat_b_sig      = np.array( dat[i]['b0_sig']       )
	
		dat_b_r        = dat_b_sig/np.array( dat[i]['b0'] )
	
		dat_sig_fvpc   = np.array( dat[i]['sig_fv_p_c']   )

		# Extract other parameters computed in 'janus_pyon'.
	
		dat_r_p        = np.array( dat[i]['r_p']          )
		dat_n_p        = np.array( dat[i]['n_p']          )
		dat_n_p_c_sig  = np.array( dat[i]['n_p_c_sig']    )
		dat_n_p_b_sig  = np.array( dat[i]['n_p_b_sig']    )
		dat_n_p_c      = np.array( dat[i]['n_p_c']        )
		dat_n_p_b      = np.array( dat[i]['n_p_b']        )
		dat_fv_p_c     = np.array( dat[i]['fv_p_c']       )
		dat_dv_p_b     = np.array( dat[i]['dv_p_b']       )
		dat_w_par_c    = np.array( dat[i]['w_par_p_c']    )
		dat_w_per_c    = np.array( dat[i]['w_per_p_c']    )
		dat_w_par_b    = np.array( dat[i]['w_par_p_b']    )
		dat_w_per_b    = np.array( dat[i]['w_per_p_b']    )
		dat_w_p        = np.array( dat[i]['w_p']          )
		dat_t_p_c      = np.array( dat[i]['t_par_p_c']    )
		dat_t_p_b      = np.array( dat[i]['t_par_p_b']    )
		dat_w_par_p    = np.array( dat[i]['w_par_p']      )
		dat_alf_vel    = np.array( dat[i]['alfv_vel']     )
		dat_v0_mag     = np.array( dat[i]['v0_mag']       )
		dat_v0_sig_x   = np.array( dat[i]['v0_sig_x']     )
		dat_v0_sig_y   = np.array( dat[i]['v0_sig_y']     )
		dat_v0_sig_z   = np.array( dat[i]['v0_sig_z']     )

	        inc = [ ( ( dat_n_p_b[j]  is not None ) and ( dat_n_p_b[j] >  0 ) and
	                ( dat_n_p[j] is not None ) and ( dat_n_p[j]   >  0 ) and
	                ( dat_s_p[j] is not None ) and ( dat_s_p[j]   != 0 ) and
	                ( dat_s_p[j] is not None ) and
		        ( dat_dv_p_b[j] is not None ) and  
	                ( dat_r_p_b[j] > .1 )      and ( dat_r_p_c[j] < 10 ) and 
	                ( dat_r_p_c[j] > .1 )      and ( dat_r_p_b[j] < 10 )   )
	
	                for j in range( len( dat_n_p_b ) ) ]
	
	        tk = np.where( inc )[0]
	
	        if ( len( tk ) <= 1 ) :
	                continue
	
	        sel_b0      = dat_b_hat[tk]
	        sel_bs      = dat_b_sig[tk]
	        sel_rp      = dat_r_p[tk]
	        sel_np      = dat_n_p[tk]
	        sel_nc      = dat_n_p_c[tk]
	        sel_nb      = dat_n_p_b[tk]
		sel_nsig    = dat_n_p_b_sig[tk]+dat_n_p_c_sig[tk]
	        sel_fvpc    = dat_fv_p_c[tk]
	        sel_dvpb    = dat_dv_p_b[tk]
	        sel_wparc   = dat_w_par_c[tk]
	        sel_wparb   = dat_w_par_b[tk]
	        sel_wperc   = dat_w_per_c[tk]
	        sel_wperb   = dat_w_per_b[tk]
		sel_wp      = dat_w_p[tk]
	        sel_nf      = dat_n_p_b[tk] / dat_n_p[tk]
	        sel_tpc     = dat_t_p_c[tk]
	        sel_tpb     = dat_t_p_b[tk]
		sel_wparp   = dat_w_par_p[tk]
		sel_b_r     = dat_b_r[tk]
#		sel_sig_b   = dat_sig_b[tk]
#		sel_av      = dat_alf_vel[tk]
		sel_bsig    = dat_b_sig[tk]
		sel_bmag    = dat_b_mag[tk]
		sel_vmag    = dat_v0_mag[tk]
		sel_vsig    = sqrt( dat_v0_sig_x**2 + dat_v0_sig_y**2 +
		                                      dat_v0_sig_z**2   )
		sel_av      = [ ( dat[0]['b0'][l]*10**(-9) )/\
		                  sqrt( const['mu_0']*dat[0]['n_p'][l]*\
		                  10**6*const['m_p'] )
		                                     for l in (tk) ]
#	        for k in range(len(sel_np)):
#	
#	                t_b0[count]      = sel_b0[k]
#	                t_bs[count]      = sel_bs[k]
#	                t_br[count]      = sel_br[k]
#	                t_rp[count]      = sel_rp[k]
#	                t_rc[count]      = sel_rc[k]
#	                t_rb[count]      = sel_rb[k]
#	                t_np[count]      = sel_np[k]
#	                t_nc[count]      = sel_nc[k]
#	                t_nb[count]      = sel_nb[k]
#	                t_fvpc[count]    = sel_fvpc[k]
#	                t_fvpb[count]    = sel_fvpb[k]
#	                t_dvpc[count]    = sel_dvpc[k]
#	                t_dvpb[count]    = sel_dvpb[k]
#	                t_wparc[count]   = sel_wparc[k]
#	                t_wparb[count]   = sel_wparb[k]
#	                t_wperc[count]   = sel_wperc[k]
#	                t_wperb[count]   = sel_wperb[k]
#			t_wp[count]      = sel_wp[k]
#	                t_dvvecpc[count] = sel_dvvecpc[k]
#	                t_dvvecpb[count] = sel_dvvecpb[k]
#			t_wparp[count]   = sel_wparp[k]
#	                t_s[count]       = sel_s[k]
#	                t_k[count]       = sel_k[k]
#	                t_nf[count]      = sel_nf[k]
#	                t_tpc[count]     = sel_tpc[k]
#	                t_tpb[count]     = sel_tpb[k]
#			t_b_r[count]     = sel_b_r[k]
#			t_av[count]      = sel_av[k]
##			print sel_av[k]
#	
#			print count
#	                count           += 1

# Change back to the working directory.

if Place == 'w' :
        os.chdir("/home/ahmadr/Desktop/GIT/fm_development")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research")

# Define the linear model to fit the data.

def fitlin( b, v, sigma ) :

	def linfunc( b, m, c ) :

		return m * b + c

	sigma = np.ones(len(b))
	sigma[ -1]= 1.E-5
	popt, pcov = curve_fit( linfunc, b, v, sigma=sigma )
	m, c = popt

	fitfunc = lambda b: m * b + c

	return { "slope"   : m,
	         "offset"  : c,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt,pcov ) }

# Scale the fluctuating velocity with Alfven speed.

s_fv = 1.E3*dat_fv_p_c/sel_av 

# Calculate the  amplitude of wave using standard deviation of the magnetic
# field.

amp_b = [ sqrt(2)*sig_bb[i] for i in range( len( sig_bb ) ) ]

# Scale the error in the fluctuating velocity,

s_sig_fv = 1.E3*dat_sig_fvpc/sel_av

# Linearly fit the data using the model defined earlier.

sig_bb       = np.append( sig_bb, 0 )
s_fv         = np.append( s_fv, 0)
dat_sig_fvpc = np.append( dat_sig_fvpc, 0 )

dat_fit = fitlin( sig_bb, s_fv, dat_sig_fvpc )

# Define list of index.

ind = linspace( 0., max( sig_bb ), len( sig_bb ) )

# Extract the slope and intercept.

m = dat_fit['slope']
c = dat_fit['offset']

del_m = mean( sel_vsig/sel_vmag + 0.5*sel_nsig/sel_np + 2*sel_bs/sel_bmag )

slope = r'$ m \pm del_m$'

# 
y_fit = [ ( m*ind[i] + c ) for i in range( len( sig_bb ) ) ]

# Find the Pearson correlation coefficient.

#amp_b = np.append( amp_b, 0 )
cv = corrcoef( amp_b, s_fv[0:-1] )[0,1]

# Extract the x-value from the fit.

fit_x = dat_fit['fitfunc'](ind)
#plt.scatter( sig_bb, s_fv )
plt.errorbar( sig_bb[0:-1], s_fv[0:-1], yerr=s_sig_fv, fmt='o', ecolor='g' )
#plt.xlim[0,1]
plt.plot( ind, y_fit )

plt.xticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], fontsize=20)
plt.yticks([0, 0.02, 0.04, 0.06, 0.08, 0.1], fontsize=20)

#plt.scatter( dat_fv_p_c, sig_bb )
#plt.scatter( t_fvpc, t_b_r )

plt.ylim( 0, 0.045 )
#plt.ylim((min(s_fv)+0.1*min(s_fv), ( max(s_fv)+ 0.1*max(s_fv))))
plt.xlim( 0.0, 0.045 )
#plt.xlim(( 0., ( max(sig_bb)+ 0.1*max(sig_bb))))

plt.text( 0.0, 0.03, 'Slope = %s+/- %s\nOffset = %s\nCorr Coeff = %s\n'
%( round( m, 2 ), round( del_m, 2 ),  round( c, 4 ), round( cv, 2 ) ), fontsize=22 )

plt.xlabel(r'$\frac{\sigma_B}{| \vec B|}$', fontsize = 28 )
plt.ylabel(r'$\frac{\delta v}{v_A}(km/sec)$', fontsize = 22 )

#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error bars', fontsize = 24 )
plt.tight_layout()
plt.show( )

print ('It took','%.6f'% (time.time()-start), 'seconds.')
