import time
start = time.time()
 
import os
os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen

import glob
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch as cp
from pylab import rcParams

rcParams['figure.figsize'] = 25, 15

plt.clf()
plt.close()

#Place= raw_input('Are you using work or home computer? (w for work, h for home) ==> ')
Place='w'
if Place=='w' :
        os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research/results/save")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research/results/save")

#os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research/results/save")

fname=[]
i = 0

for file in glob.glob("test.jns"):
        fname.append( file )

dat    = [0]*len(fname)

t_b0      = [0]*633
t_rp      = [0]*633
t_rb      = [0]*633
t_rc      = [0]*633
t_np      = [0]*633
t_nc      = [0]*633
t_nb      = [0]*633
t_dvpc    = [0]*633
t_dvpb    = [0]*633
t_wparc   = [0]*633
t_wparb   = [0]*633
t_wperc   = [0]*633
t_wperb   = [0]*633
t_dvvecpc = [0]*633
t_dvvecpb = [0]*633
t_s       = [0]*633
t_k       = [0]*633
t_tpc     = [0]*633
t_tpb     = [0]*633
t_nf      = [0]*633

count  = 0

for i in range (len(fname)):
        dat[i] = pickle.load(open(fname[i],'rb'))

        dat_b_hat      = np.array(dat[i]['b0_hat'])
        dat_r_p        = np.array(dat[i]['r_p'])
        dat_r_p_c      = np.array(dat[i]['r_p_c'])
        dat_r_p_b      = np.array(dat[i]['r_p_b'])
        dat_n_p        = np.array(dat[i]['n_p'])
        dat_n_p_c      = np.array(dat[i]['n_p_c'])
        dat_n_p_b      = np.array(dat[i]['n_p_b'])
        dat_dv_p_c     = np.array(dat[i]['dv_p_c'])
        dat_dv_p_b     = np.array(dat[i]['dv_p_b'])
        dat_w_par_c    = np.array(dat[i]['w_par_p_c'])
        dat_w_per_c    = np.array(dat[i]['w_per_p_c'])
        dat_w_par_b    = np.array(dat[i]['w_par_p_b'])
        dat_w_per_b    = np.array(dat[i]['w_per_p_b'])
        dat_dv_vec_p_c = np.array(dat[i]['dv_p_c_vec'])
        dat_dv_vec_p_b = np.array(dat[i]['dv_p_b_vec'])
        dat_s_p        = np.array(dat[i]['p_s'])
        dat_k_p        = np.array(dat[i]['p_k'])
        dat_t_p_c      = np.array(dat[i]['t_par_p_c'])
        dat_t_p_b      = np.array(dat[i]['t_par_p_b'])

        inc = [ ( ( dat_n_p_b[j] is not None ) and ( dat_n_p_b[j] >  0 ) and
                  ( dat_n_p[j]   is not None ) and ( dat_n_p[j]   >  0 ) and
                  ( dat_s_p[j]   is not None ) and ( dat_s_p[j]   != 0 ) and
                  ( dat_s_p[j]   is not None ) and ( dat_dv_p_b[j] is not None) and
                  ( dat_r_p_c[j] > .1        ) and ( dat_r_p_b[j] > .1 ) and
                  ( dat_r_p_c[j] < 10        ) and ( dat_r_p_b[j] < 10 )       )
                for j in range( len( dat_n_p_b ) ) ]

        tk = np.where( inc )[0]

        if ( len( tk ) <= 1 ) :
                continue

        sel_b0      = dat_b_hat[tk]
        sel_rp      = dat_r_p[tk]
        sel_rc      = dat_r_p_c[tk]
        sel_rb      = dat_r_p_b[tk]
        sel_np      = dat_n_p[tk]
        sel_nc      = dat_n_p_c[tk]
        sel_nb      = dat_n_p_b[tk]
        sel_dvpc    = dat_dv_p_c[tk]
        sel_dvpb    = dat_dv_p_b[tk]
        sel_wparc   = dat_w_par_c[tk]
        sel_wparb   = dat_w_par_b[tk]
        sel_wperc   = dat_w_per_c[tk]
        sel_wperb   = dat_w_per_b[tk]
        sel_dvvecpc = dat_dv_vec_p_c[tk]
        sel_dvvecpb = dat_dv_vec_p_b[tk]
        sel_s       = dat_s_p[tk]
        sel_k       = dat_k_p[tk]
        sel_nf      = dat_n_p_b[tk] / dat_n_p[tk]
        sel_tpc     = dat_t_p_c[tk]
        sel_tpb     = dat_t_p_b[tk]

        for k in range(len(sel_np)):
                t_b0[count]      = sel_b0[k]
                t_rp[count]      = sel_rp[k]
                t_rc[count]      = sel_rc[k]
                t_rb[count]      = sel_rb[k]
                t_np[count]      = sel_np[k]
                t_nc[count]      = sel_nc[k]
                t_nb[count]      = sel_nb[k]
                t_dvpc[count]    = sel_dvpc[k]
                t_dvpb[count]    = sel_dvpb[k]
                t_wparc[count]   = sel_wparc[k]
                t_wparb[count]   = sel_wparb[k]
                t_wperc[count]   = sel_wperc[k]
                t_wperb[count]   = sel_wperb[k]
                t_dvvecpc[count] = sel_dvvecpc[k]
                t_dvvecpb[count] = sel_dvvecpb[k]
                t_s[count]       = sel_s[k]
                t_k[count]       = sel_k[k]
                t_nf[count]      = sel_nf[k]
                t_tpc[count]     = sel_tpc[k]
                t_tpb[count]     = sel_tpb[k]

                count           += 1

if Place == 'w' :
        os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research")

u1 = linspace(-200,200,200)
u2 = linspace(-200,200,200)

if Place == 'w' :
	os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research/Graphs/Contours")
else:
	os.chdir('/home/ramiz/Dropbox/Studies/Research/Janus_Research/Graphs/Contours')

Method = raw_input( 'Default or interactive (write d or i) ==>  ' )

if Method=='d' :
        k = [31,50,84,93,96,121,138,169,170,172,284,285,286,287,290,297,338,339,
             366,367,479,480,481,482,483,588,589,590,591,592,593,594,595,596]
#        k = range(172,173)
else:
        k = int(raw_input( 'The value of k ==>  ' ))


f  = np.zeros((len(u1),len(u2),len(k)))

for p in range(len(k)):

        Ac = t_nc[k[p]]/(((2*pi)**1.5)*t_wparc[k[p]]*t_wperc[k[p]]**2)
        Ab = t_nb[k[p]]/(((2*pi)**1.5)*t_wparb[k[p]]*t_wperb[k[p]]**2)

        Bc = [0]*len(u1)
        Bb = [0]*len(u2)
        Cc = [0]*len(u1)
        Cb = [0]*len(u2)
        fc = np.zeros((len(u1),len(u2)))
        fb = np.zeros((len(u1),len(u2)))
#        f  = np.zeros((len(u1),len(u2),len(k)))

        for i in range(len(u1)):
                for j in range(len(u2)):
                        Bc[i] = -(u1[i]/(sqrt(2)*t_wparc[k[p]]))**2
                        Bb[i] = -((u1[i]-t_dvpb[k[p]])/(sqrt(2)*t_wparb[k[p]]))**2

                        Cc[j] = -(u2[j]/(sqrt(2)*t_wperc[k[p]]))**2
                        Cb[j] = -(u2[j]/(sqrt(2)*t_wperb[k[p]]))**2

                        fc[j,i] = exp(Bc[i]+Cc[j])
                        fb[j,i] = exp(Bb[i]+Cb[j])
                        if (Ac*fc[j,i]+Ab*fb[j,i]>0):
                                f[j,i,p] = np.log10(Ac*fc[j,i]+Ab*fb[j,i])

af = np.zeros((len(u1),len(u2)))

for i in range(len(u1)):
        for j in range(len(u2)):
                af[i,j] = np.mean(f[i,j,:])
'''
        textstr = '$\Delta V_{pb}=%.2f$\n$\mathrm{R_{pc}}=%.2f$\n$\mathrm{R_{pb}}=%.2f$\n$\mathrm{n_{pb}/n_{p}}=%0.2f$\n$S=%0.2f$\n$K=%0.2f$'%(t_dvpb[k[p]], t_rc[k[p]], t_rb[k[p]],t_nb[k[p]]/t_np[k[p]],t_s[k[p]],t_k[k[p]]-3)
'''
X,Y = np.meshgrid(u1,u2)
plt.figure(p)
cont = plt.contour(X,Y,af,30,cmap=plt.cm.RdYlBu_r,origin='upper')
#CS2=plt.contourf(X,Y,f,cmap=plt.cm.RdYlBu_r)
plt.xlim([min(u1),max(u1)])
plt.ylim([min(u2),max(u2)])
plt.colorbar()
plt.title('Contour plot of distribution function')
plt.xlabel(r'$U_{\parallel}$')
plt.ylabel(r'$U_{\perp}$')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#        plt.text(600,600, textstr)
plt.show()
#        savefig('contour_'+ str(k[p]) + '.png', bbox_inches='tight', dpi=150)
#        plt.close(p)

if Place == 'w' :
        os.chdir("/home/ahmadr/Dropbox/Studies/Research/Janus_Research")
else:
        os.chdir("/home/ramiz/Dropbox/Studies/Research/Janus_Research")
