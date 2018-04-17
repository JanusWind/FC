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

rcParams['figure.figsize'] = 20, 10

plt.clf()
plt.close()

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
for file in glob.glob("janus_2008-11-04-10-45-35_2008-11-04-12-33-18.jns"):
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
	        dat_b_sig      = np.array( dat[i]['b0_sig']       )
	
		dat_b_r        = dat_b_sig/np.array( dat[i]['b0'] )
	
		dat_sig_fvpc   = np.array( dat[i]['sig_fv_p_c']   )

		# Extract other parameters computed in 'janus_pyon'.
	
		dat_r_p        = np.array( dat[i]['r_p']          )
		dat_r_p_c      = np.array( dat[i]['r_p_c']        )
		dat_r_p_b      = np.array( dat[i]['r_p_b']        )
		dat_n_p        = np.array( dat[i]['n_p']          )
		dat_n_p_c      = np.array( dat[i]['n_p_c']        )
		dat_n_p_b      = np.array( dat[i]['n_p_b']        )
		dat_fv_p_c     = np.array( dat[i]['fv_p_c']       )
		dat_fv_p_b     = np.array( dat[i]['fv_p_b']       )
		dat_dv_p_c     = np.array( dat[i]['dv_p_c']       )
		dat_dv_p_b     = np.array( dat[i]['dv_p_b']       )
		dat_w_par_c    = np.array( dat[i]['w_par_p_c']    )
		dat_w_per_c    = np.array( dat[i]['w_per_p_c']    )
		dat_w_par_b    = np.array( dat[i]['w_par_p_b']    )
		dat_w_per_b    = np.array( dat[i]['w_per_p_b']    )
		dat_w_p        = np.array( dat[i]['w_p']          )
		dat_dv_vec_p_c = np.array( dat[i]['dv_p_c_vec']   )
		dat_dv_vec_p_b = np.array( dat[i]['dv_p_b_vec']   )
		dat_s_p        = np.array( dat[i]['p_s']          )
		dat_k_p        = np.array( dat[i]['p_k']          )
		dat_t_p_c      = np.array( dat[i]['t_par_p_c']    )
		dat_t_p_b      = np.array( dat[i]['t_par_p_b']    )
		dat_w_par_p    = np.array( dat[i]['w_par_p']      )
	
	        inc = [ ( ( dat_n_p_b[j]  is not None ) and ( dat_n_p_b[j] >  0 ) and
	                  ( dat_n_p[j]    is not None ) and ( dat_n_p[j]   >  0 ) and
	                  ( dat_s_p[j]    is not None ) and ( dat_s_p[j]   != 0 ) and
	                  ( dat_s_p[j]    is not None ) and
		          ( dat_dv_p_b[j] is not None ) and ( dat_r_p_c[j] > .1 ) and 
	                  ( dat_r_p_b[j] > .1 )         and ( dat_r_p_c[j] < 10 ) and 
	                  ( dat_r_p_b[j] < 10 )                                      )
	
	                for j in range( len( dat_n_p_b ) ) ]
	
	        tk = np.where( inc )[0]
	
	        if ( len( tk ) <= 1 ) :
	                continue
	
	        sel_b0      = dat_b_hat[tk]
	        sel_bs      = dat_b_sig[tk]
	        sel_br      = dat_b_r[tk]
	        sel_rp      = dat_r_p[tk]
	        sel_rc      = dat_r_p_c[tk]
	        sel_rb      = dat_r_p_b[tk]
	        sel_np      = dat_n_p[tk]
	        sel_nc      = dat_n_p_c[tk]
	        sel_nb      = dat_n_p_b[tk]
	        sel_fvpc    = dat_fv_p_c[tk]
	        sel_fvpb    = dat_fv_p_b[tk]
	        sel_dvpc    = dat_dv_p_c[tk]
	        sel_dvpb    = dat_dv_p_b[tk]
	        sel_wparc   = dat_w_par_c[tk]
	        sel_wparb   = dat_w_par_b[tk]
	        sel_wperc   = dat_w_per_c[tk]
	        sel_wperb   = dat_w_per_b[tk]
		sel_wp      = dat_w_p[tk]
	        sel_dvvecpc = dat_dv_vec_p_c[tk]
	        sel_dvvecpb = dat_dv_vec_p_b[tk]
	        sel_s       = dat_s_p[tk]
	        sel_k       = dat_k_p[tk]
	        sel_nf      = dat_n_p_b[tk] / dat_n_p[tk]
	        sel_tpc     = dat_t_p_c[tk]
	        sel_tpb     = dat_t_p_b[tk]
		sel_wparp   = dat_w_par_p[tk]
		sel_b_r     = dat_b_r[tk]
#		sel_sig_b   = dat_sig_b[tk]
	
	        for k in range(len(sel_np)):
	
	                t_b0[count]      = sel_b0[k]
	                t_bs[count]      = sel_bs[k]
	                t_br[count]      = sel_br[k]
	                t_rp[count]      = sel_rp[k]
	                t_rc[count]      = sel_rc[k]
	                t_rb[count]      = sel_rb[k]
	                t_np[count]      = sel_np[k]
	                t_nc[count]      = sel_nc[k]
	                t_nb[count]      = sel_nb[k]
	                t_fvpc[count]    = sel_fvpc[k]
	                t_fvpb[count]    = sel_fvpb[k]
	                t_dvpc[count]    = sel_dvpc[k]
	                t_dvpb[count]    = sel_dvpb[k]
	                t_wparc[count]   = sel_wparc[k]
	                t_wparb[count]   = sel_wparb[k]
	                t_wperc[count]   = sel_wperc[k]
	                t_wperb[count]   = sel_wperb[k]
			t_wp[count]      = sel_wp[k]
	                t_dvvecpc[count] = sel_dvvecpc[k]
	                t_dvvecpb[count] = sel_dvvecpb[k]
			t_wparp[count]   = sel_wparp[k]
	                t_s[count]       = sel_s[k]
	                t_k[count]       = sel_k[k]
	                t_nf[count]      = sel_nf[k]
	                t_tpc[count]     = sel_tpc[k]
	                t_tpb[count]     = sel_tpb[k]
			t_b_r[count]     = sel_b_r[k]
	
                count           += 1

if Place == 'w' :
        os.chdir("/home/ahmadr/Desktop/GIT/fm_development")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research")


def fitlin( b, v, sigma ) :

	def linfunc( b, m, c ) :

		return m * b + c

#	sigma = [1]*len(b)
#	sigma[0]= 0.01
	popt, pcov = curve_fit( linfunc, b, v, sigma=sigma )
	m, c = popt

	fitfunc = lambda b: m * b + c

	return { "slope"   : m,
	         "offset"  : c,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt,pcov ) }

ind = linspace( 0., max( sig_bb ), len( sig_bb ) )

dat_fit = fitlin( sig_bb, dat_fv_p_c , dat_sig_fvpc )

m = dat_fit['slope']
c = dat_fit['offset']

y_fit = [ ( m*ind[i] + c ) for i in range( len( sig_bb ) ) ]

cv = corrcoef(sig_bb, dat_fv_p_c )[0,1]

fit_x = dat_fit['fitfunc'](ind)
plt.errorbar( sig_bb, dat_fv_p_c, yerr=dat_sig_fvpc,
                                                fmt='o', ecolor='g' )
#plt.xlim[0,1]
plt.plot( ind, y_fit )

#plt.scatter( dat_fv_p_c, sig_bb )
#plt.scatter( t_fvpc, t_b_r )

plt.ylim((min(dat_fv_p_c)+0.1*min(dat_fv_p_c), ( max(dat_fv_p_c)+ 0.1*max(dat_fv_p_c))))
plt.xlim(( 0., ( max(sig_bb)+ 0.1*max(sig_bb))))

plt.text( 0.08, 2.5, 'Slope = %s\n Offset = %s\n Corr Coeff = %s\n'
       %( round( m, 2 ), round( c, 2 ), round( cv, 2 ) ), fontsize=22 )

plt.xlabel(r'$\frac{\sigma_B}{| \vec B|}$', fontsize = 28 )
plt.ylabel('Fluctuating Velocity (km/sec)', fontsize = 22 )

#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error bars', fontsize = 24 )
plt.show( )

'''
u1 = linspace(-125,175,201)
u2 = linspace(-150,150,201)

#Method = raw_input( 'Default or interactive (write d or i) ==>  ' )
Method='d'
if Method=='d' :
#        k = [84,126,150,169,217,549,197,261,482,332,335,366,172,96,53,121,570,565]
#             366,367,479,480,481,482,483,588,589,590,591,592,593,594,595,596]
        k = [1,0,3]
#        k = range(0,633)
else:
        k = int(raw_input( 'The value of k ==>  ' ))


f  = np.zeros((len(u1),len(u2),len(k)))
fl = np.zeros((len(u1),len(u2),len(k)))

for p in range(len(k)):
#for p in range(1):

        Ac      = t_nc[k[p]]/(((2*pi)**1.5)*t_wparc[k[p]]*t_wperc[k[p]]**2)
        Ab      = t_nb[k[p]]/(((2*pi)**1.5)*t_wparb[k[p]]*t_wperb[k[p]]**2)
        A_par_c = t_nc[k[p]]/(((2*pi)**0.5)*t_wparc[k[p]])
        A_par_b = t_nb[k[p]]/(((2*pi)**0.5)*t_wparb[k[p]])
        A_per_c = t_nc[k[p]]/(((2*pi)**1.0)*t_wperc[k[p]]**2)
        A_per_b = t_nb[k[p]]/(((2*pi)**1.0)*t_wperb[k[p]]**2)

        Bc      = [0]*len(u1)
        Bb      = [0]*len(u2)
        Cc      = [0]*len(u1)
        Cb      = [0]*len(u2)
        fc      = np.zeros((len(u1),len(u2)))
        fb      = np.zeros((len(u1),len(u2)))
        f_par   = np.zeros(len(u1))
        f_per   = np.zeros(len(u2))
        f_par_c = np.zeros(len(u1))
        f_par_b = np.zeros(len(u1))
        f_per_c = np.zeros(len(u2))
        f_per_b = np.zeros(len(u2))
#        f  = np.zeros((len(u1),len(u2),len(k)))

        for i in range(len(u1)):
                for j in range(len(u2)):
                        Bc[i]     = -(u1[i]/(sqrt(2)*t_wparc[k[p]]))**2
                        Bb[i]     = -((u1[i]-t_dvpb[k[p]])/(sqrt(2)*t_wparb[k[p]]))**2

                        Cc[j]     = -(u2[j]/(sqrt(2)*t_wperc[k[p]]))**2
                        Cb[j]     = -(u2[j]/(sqrt(2)*t_wperb[k[p]]))**2

                        fc[j,i]   = Ac*exp(Bc[i]+Cc[j])
                        fb[j,i]   = Ab*exp(Bb[i]+Cb[j])
                        f[j,i,p]  = fc[j,i]+fb[j,i]

                        if (f[j,i,p]>0):
                                fl[j,i,p] = np.log10(f[j,i,p])
        for i in range(len(u1)):
                f_par_c[i] = A_par_c*exp(Bc[i])
                f_par_b[i] = A_par_b*exp(Bb[i])
                f_per_c[i] = A_per_c*exp(Cc[i])
                f_per_b[i] = A_per_b*exp(Cb[i])

                f_par[i]   = f_par_c[i]+f_par_b[i]
                f_per[i]   = f_per_c[i]+f_per_b[i]
               
        textstr = '$\mathrm{n_{pb}/n_{p}}=%.2f$\n$T_pc=%.2f$\n$T_pb=%.2f$\n$\mathrm{T_{pb}/T_{pc}}=%.2f$\n$\mathrm{R_{pc}}=%.2f$\n$\mathrm{R_{pb}}=%.2f$'%(t_nb[k[p]]/t_np[k[p]],t_tpc[k[p]],t_tpb[k[p]],t_tpb[k[p]]/t_tpc[k[p]],t_rc[k[p]], t_rb[k[p]])

        textstr2 = '$S=%.2f$\n$K=%.2f$\n$\Delta V_{pb}=%.2f$\n$W_{\parallel pc}=%.2f$\n$W_{\parallel pb}=%.2f$\n$\mathrm{W_{\parallel pb}/W_{\parallel pc}}=%.2f$'%(t_s[k[p]],t_k[k[p]]-3,t_dvpb[k[p]],t_wparc[k[p]],t_wparb[k[p]],t_wparb[k[p]]/t_wparc[k[p]])

        

        fig,axarr = plt.subplots(4)
        axarr[0] = plt.subplot2grid((4, 4), (0, 0), colspan=3,rowspan=3)
        axarr[1] = plt.subplot2grid((4, 4), (3, 0), colspan=3,rowspan=1, sharex = axarr[0])
        axarr[2] = plt.subplot2grid((4, 4), (0, 3), colspan=1,rowspan=3, sharey = axarr[0])
#        axarr[3] = plt.subplot2grid((4, 4), (3, 3), colspan=1,rowspan=1, sharex = axarr[1])
        plt.subplots_adjust(wspace=0, hspace=0)

        m=max([max(fl[:,j,p])for j in range(len(fl[1,:,p]))])
        X,Y = np.meshgrid(u1,u2)
        cont = axarr[0].contour(X,Y,fl[:,:,p],levels= linspace(m-2.5,m,6),linewidths=1,
                                        cmap=plt.get_cmap('gist_rainbow'),origin='upper')
        plt.clabel(cont,inline=1, fontsize=12) 
        plt.setp(axarr[0].get_xticklabels(), visible=False)
        axarr[0].locator_params(axis='y', nbins=9)
        axarr[0].set_xlim([min(u1),max(u1)])
        axarr[0].set_ylim([min(u2),max(u2)])
#        axarr[0].set_title('Contour plot of distribution function')
        axarr[0].set_ylabel(r'$U_{\perp}$ (km/s)', fontsize=16)

        axarr[1].plot(u1,f_par/max(f_par),   color = 'blue',linewidth=0.6,    label= '$n_p$')
        axarr[1].plot(u1,f_par_c/max(f_par), color = 'red',linewidth=0.6,     label= '$n_{pc}$')
        axarr[1].plot(u1,f_par_b/max(f_par), color = 'magenta',linewidth=0.6, label= '$n_{pb}$')
#        axarr[1].legend(bbox_to_anchor=(1, 1), loc=1, fontsize=12)
        axarr[1].locator_params(axis='y', nbins=3)
        axarr[1].set_xlabel(r'$U_{\parallel}$ (km/s)', fontsize=16)
        axarr[1].set_ylabel(r'F$(u_{\parallel})$', fontsize=16)
        axarr[1].set_xlim([min(u1),max(u1)])

        axarr[2].plot(f_per/max(f_per),u2,   color = 'blue',linewidth=0.6,    label= '$n_p$')
        axarr[2].plot(f_per_c/max(f_per),u2, color = 'red',linewidth=0.6,     label= '$n_{pc}$')
        axarr[2].plot(f_per_b/max(f_per),u2, color = 'magenta',linewidth=0.6, label= '$n_{pb}$')
        axarr[2].legend(bbox_to_anchor=(1, 1), loc=1, fontsize=12)
#        axarr[2].xaxis.set_label_position('top')
        axarr[2].set_xlabel(r'F$(u_{\perp})$', fontsize=14)
#        axarr[2].xaxis.set_ticks_position('top')
        axarr[2].locator_params(axis='x', nbins=3)
#        plt.setp(axarr[2].get_xticklabels(), visible=True)
        plt.setp(axarr[2].get_yticklabels(), visible=False)
        plt.tick_params(axis = 'y', which = 'both', left = 'off')

        for n in range(3):
                labels = axarr[n].get_yticklabels()
                labels[0]=labels[-1]=''
                for tick in axarr[n].yaxis.get_major_ticks():
                        tick.label.set_fontsize(14)
                        tick.label.set_rotation('horizontal')
                for tick in axarr[n].xaxis.get_major_ticks():
                        tick.label.set_fontsize(14)
                        tick.label.set_rotation('horizontal')

        plt.setp(axarr[0].get_yticklabels()[0], visible=False) 
        plt.setp(axarr[2].get_xticklabels()[1], visible=False) 
#        axarr[3].text(-120,0.15, textstr, fontsize=13)
#        axarr[3].text(15,0.15, textstr2, fontsize=13)
#        axarr[3].axvline(x=14,linestyle='-', color='k')

#        plt.setp(axarr[3].get_xticklabels(), visible=False)
#        plt.setp(axarr[3].get_yticklabels(), visible=False)
#        plt.tick_params(axis = 'both', which = 'both', bottom = 'off', left = 'off')
        plt.show()
        plt.savefig('contour_gaussian_final_'+ str(k[p]) + '_.eps', bbox_inches='tight', dpi=60)
#        plt.close(p)
        print(p)


if Place == 'w' :
        os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research")
'''
print ('It took','%.6f'% (time.time()-start), 'seconds.')
