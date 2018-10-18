import time
start = time.time()


import os
import sys
os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen

import glob
import pickle
import numpy as np
from numpy import mean, sqrt, corrcoef, where
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib import gridspec, rc
from pylab import rcParams
from scipy.optimize import curve_fit
from scipy import stats

from numpy import linspace, pi, sqrt, exp, std

from janus_const import const

plt.clf()
plt.close('all')

#n_data = raw_input('Which file numbers do you want to run the code for ==>  ')
#n_data = [ int( n_data[j] ) for j in range( len( n_data ) ) ]

data_run = raw_input( 'Run the data? ==>  ' )
print '\n'

if( data_run=='y' ):

	print 'Please wait. The computer is running the code! We appreciate your patience \n'
	# Change the directory in which the saved file exists.

	os.chdir("/home/ahmadr/Desktop/GIT/fm_development/data/edited")

	# Define the names of files to be analysed.
#	fname1 = 'janus_2014-01-01-22-59-37_2014-01-02-03-32-12_man_rngavg_21_600_fvpc.jns'

#	fname1 = 'janus_raw_mag_2008-11-04-11-55-41_2008-11-04-12-57-46.jns'
#	fname1 = 'janus_2008-11-04-12-00-41_2008-11-04-12-59-24_man_rng_avg_21_600_fvpc.jns'
#	fname1 = 'janus_2008-11-04-12-00-41_2008-11-04-12-57-46_man_rngavg_21_600_fvpcb.jns'
#	fname1 = 'janus_2014-01-01-23-16-02_2014-01-02-01-37-15_man_rng_avg_21_600_fvpc.jns'

#	fname1 = 'janus_2008-11-04-12-00-41_2008-11-04-12-57-46_man_rngavg_21_600_fvpcb.jns'
	fname1 = 'janus_2008-11-04-12-00-41_2008-11-04-13-01-02_auto_rng_avg_21_600_fvpcb_n.jns'

	print 'Currently reading file ==> {}  '.format( fname1 )
	print '\n'

	if( len( fname1) > 15 ) :
		print 'Whoaaaa! Thats a big file name!'
		print '\n'

	dat3 = [0]*len( fname1 )
	dat3 = pickle.load( open( fname1, 'rb' ) )
	nd1  = len( dat3['b0'] )

	# Change back the directory to the working directory.

	os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

	# Define all the parameters to be used during analysis.

	dat3_time         = []

	ii                = [] # Initial index
	fi                = [] # Final index

	dat3_db_rng_avg   = []

	dat3_b_avg        = []

	dat3_n_p_c        = []
	dat3_n_p_b        = []
	dat3_n_p          = []

	dat3_del_v_p_c    = []
	dat3_del_v_p_b    = []
	dat3_fv_p_c       = []
	dat3_fv_p_b       = []
	dat3_sig_fv_p_c   = []
	dat3_sig_fv_p_b   = []

	dat3_w_fv_p       = []

	dat3_alfvel       = []

	dat3_s_fv_p_c     = []
	dat3_s_fv_p_b     = []
	dat3_s_sig_fv_p_c = []
	dat3_s_sig_fv_p_b = []

	dat3_s_db         = []
	dat3_s_db_rng_avg = []

	r_ind = [ 4, 7, 16, 25 ]

	keys = [ dat3_time, dat3_db_rng_avg, dat3_b_avg,
	         dat3_n_p_c, dat3_n_p_b, dat3_n_p, dat3_fv_p_c, dat3_fv_p_b,
	         dat3_sig_fv_p_c, dat3_sig_fv_p_b, dat3_w_fv_p, dat3_alfvel,
	         dat3_s_fv_p_c, dat3_s_fv_p_b, dat3_s_sig_fv_p_c,
	         dat3_s_sig_fv_p_b, dat3_s_db    ]

	# Exaract the data from '.jns' file.

	dat3_time.append( [ x.time().strftime("%H-%M") 
	                                              for x in  dat3['time'] ] )

	for j in range( nd1 ) :

		ii = where( [ dat3['timemin'][j] < x for x in dat3['mfitime'][j] ] )[0][0]
		fi = where( [ dat3['timemax'][j] > x for x in dat3['mfitime'][j] ] )[0][-1]

		db_x_rng_avg = dat3['b0_fields_db'][j]['mfi_set_rng_avg'][0]
		db_y_rng_avg = dat3['b0_fields_db'][j]['mfi_set_rng_avg'][1]
		db_z_rng_avg = dat3['b0_fields_db'][j]['mfi_set_rng_avg'][2]

		dat3_db_rng_avg.append( sqrt( 2 * (
		                   std( db_x_rng_avg )**2 +
		                   std( db_x_rng_avg )**2 +
		                   std( db_x_rng_avg )**2 ) ) )

		dat3_b_avg.append( sqrt(
		mean( dat3['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
		mean( dat3['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
		mean( dat3['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 ) )

		dat3_s_db.append( dat3_db_rng_avg[j]/dat3_b_avg[j] )

#		try :

	dat3_n_p.append(   [ x if x!=None else 0. for x in  dat3['n_p']   ] )
	dat3_n_p_c.append( [ x if x!=None else 0. for x in  dat3['n_p_c'] ] )
	dat3_n_p_b.append( [ x if x!=None else 0. for x in  dat3['n_p_b'] ] )
	
	dat3_fv_p_c.append( [ x if x!=None else 0. for x in dat3['fv_p_c'] ] )
	dat3_fv_p_b.append( [ x if x!=None else 0. for x in dat3['fv_p_b'] ] )
	dat3_sig_fv_p_c.append( [ x if x!=None else 0. for x in dat3['sig_fv_p_c'] ] )
	dat3_sig_fv_p_b.append( [ x if x!=None else 0. for x in dat3['sig_fv_p_b'] ] )
	
	dat3_alfvel.append( dat3['alfvel_p'] )
	
	dat3_del_v_p_c.append( [ dat3_fv_p_c[0][k] *
	                                        dat3_db_rng_avg[k]/dat3_b_avg[k]
	                             for k in range( len( dat3_fv_p_c[0] ) ) ] )

	dat3_del_v_p_b.append( [ dat3_fv_p_b[0][k] *
	                                        dat3_db_rng_avg[k]/dat3_b_avg[k]
	                             for k in range( len( dat3_fv_p_b[0] ) ) ] )

	dat3_s_fv_p_c.append( [ dat3_del_v_p_c[0][k]/dat3_alfvel[0][k] 
	                         for k in range( len( dat3_fv_p_c[0] ) ) ] )

	dat3_s_fv_p_b.append( [ dat3_del_v_p_b[0][k]/dat3_alfvel[0][k] 
	                         for k in range( len( dat3_fv_p_b[0] ) ) ] )

	dat3_s_sig_fv_p_c.append( [ dat3_sig_fv_p_c[0][k] * dat3_db_rng_avg[k] /
	                                     ( dat3_b_avg[k]*dat3_alfvel[0][k] )
	                         for k in range( len( dat3_sig_fv_p_c[0] ) ) ] )

	dat3_s_sig_fv_p_b.append( [ dat3_sig_fv_p_b[0][k] * dat3_db_rng_avg[k] /
	                                     ( dat3_b_avg[k]*dat3_alfvel[0][k] )
	                         for k in range( len( dat3_sig_fv_p_c[0] ) ) ] )

	dat3_w_fv_p.append( [ ( dat3_fv_p_c[0][k] * dat3_n_p_c[0][k] + 
	                 dat3_fv_p_b[0][k] * dat3_n_p_b[0][k] )/dat3_n_p[0][k]
	                             for k in range( len( dat3_fv_p_c[0] ) ) ] )

	dat3_s_db_rng_avg.append( [ dat3_db_rng_avg[k]/dat3_b_avg[k]
	                             for k in range( len( dat3_fv_p_c[0] ) ) ] )

#		except:

#			pass
	
#	try :
#		for key in keys :
#
#			[ key.pop( i ) for i in r_ind ]
#	except :
#
#		pass

else:
	print 'Data not read, running plotting algorithm.'

dat3_s_fv_pc = [ xx/yy for xx,yy in zip( dat3_fv_p_c[0], dat3_alfvel[0]) ]
dat3_s_sig_fv_pc = [ xx/yy for xx,yy in zip( dat3_sig_fv_p_c[0], dat3_alfvel[0]) ]

fit = stats.linregress( dat3_s_db, dat3_s_fv_p_c[0])

m = fit.slope
c = fit.intercept
r = fit.rvalue
sigma = fit. stderr

# Define figure paramaters

dpi = 40 # DPI of the saved plots

s = 10 # Marker size

legend_transparency = 0.50 # Transparency of legend

ncol = 1 # Number of columns for legend

rcParams['figure.figsize'] = 10, 10

ind = [ 5*i for i in range( 1 +  len( dat3_time[0] )/5 ) ]

labels = [ dat3_time[0][j] for j in ind ]

plt.figure()

#plt.scatter(dat3_s_db, dat3_s_fv_p_c[0], marker='^', color='b')

plt.errorbar( dat3_s_db, dat3_s_fv_p_c[0], dat3_s_sig_fv_p_c[0], fmt='o', ecolor='g', color='b', label='Proton Core')

plt.xlabel( r'$\Delta{B}/|\vec B|$' )
plt.ylabel( r'$V_f/V_A$' )

plt.show()
###############################################################################
## First Figure
###############################################################################

#if( len( dat3_sig_fv_p_b[0] ) != 0 ) :
#
#	f, axs1 = plt.subplots( 3, 1, squeeze=True, sharex=False )
#
#else :

f, axs1 = plt.subplots( 2, 1, squeeze=True, sharex=False )

axs1[0].errorbar( range( len( dat3_time[0] ) ), dat3_fv_p_c[0],
yerr=dat3_sig_fv_p_c[0], marker='*', color='r', fmt='o', ecolor='g',
                                                           label='Proton Core' )

if( len( dat3_sig_fv_p_b[0] ) != 0 ) :

	axs1[0].errorbar( range( len( dat3_time[0] ) ), dat3_fv_p_b[0],
	yerr=dat3_sig_fv_p_b[0], marker='v', color='b', fmt='o',
	                                       ecolor='g', label='Proton Beam' )

else :

	axs1[0].scatter( range( len( dat3_time[0] ) ), dat3_fv_p_b[0],
	                       marker='v', s=s, color='b', label='Proton Beam' )


axs1[0].axhline( 0, marker='None', ls='--', color='c', lw='0.5' )
axs1[0].set_xlabel( 'Spectra number', fontsize=18 )
axs1[0].set_ylabel( r'$f_v$', fontsize=18 )
axs1[0].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )
axs1[0].set_xlim( [ 0, max( range( len( dat3_time[0] ) ) ) ] )

axs1[1].errorbar( dat3_s_db, dat3_fv_p_c[0], xerr=None, yerr=dat3_sig_fv_p_c[0],
marker='*', color='r', fmt='o', ecolor='g', label='Proton Core' )

axs1[1].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs1[1].axhline( 0, marker='None', ls='--', color='c', lw='0.5' )

axs1[1].set_xlabel( r'$|\Delta B /B_0|$', fontsize=18 )
axs1[1].set_ylabel( r'$f_v$', fontsize=18 )
axs1[1].set_xlim( [ 0, 0.35 ] )
#if( len( dat3_sig_fv_p_b[0] ) != 0 ) :
#
#	axs1[2].errorbar( dat3_s_db, dat3_fv_p_b[0], xerr=None,
#	yerr=dat3_sig_fv_p_b[0], marker='v', color='r', fmt='v',
#	ecolor='m', label='Proton Beam' )
#	axs1[2].legend( )
#	axs1[2].axhline( 0, marker='None', ls='--', color='gray', lw='0.5' )

#	axs1[2].set_ylabel( 'Velocity(km/s)', fontsize=18 )
#	axs1[2].set_xlabel( r'$\Delta B / B$', fontsize=18 )

axs1[0].set_title( 'MFI Type = ' + fname1[-22:-16], color='r', fontsize=20 )

plt.tight_layout()
plt.subplots_adjust(left=0.1, right=.97, bottom=0.1, top=0.95, wspace=0, hspace=0.2)

# Managing tick marks and all

for a in axs1 :
	for tick in a.xaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_xticklabels()
	a.set_xticklabels( tick_labels )

for a in axs1 :
	for tick in a.yaxis.get_major_ticks() :
		tick.label.set_fontsize( 16 )

	tick_labels = a.get_yticklabels()
	a.set_yticklabels( tick_labels )

rcParams['figure.figsize'] = 10, 10

###############################################################################
## Second Figure
###############################################################################

f, axs2 = plt.subplots( 1, 1, squeeze=True, sharex=False )

axs2.scatter( dat3_s_db, dat3_w_fv_p[0], marker='*', color='m',
                                                           label='Weighted fv' )
axs2.scatter( dat3_s_db, dat3_fv_p_c[0], marker='d', color='r',
                                                               label='Core fv' )
axs2.scatter( dat3_s_db, dat3_fv_p_b[0], marker='v', color='b',
                                                               label='Beam fv' )
axs2.axhline( 0, marker='None', ls='--', color='c', lw='0.5' )
axs2.legend( )
axs2.set_ylabel( 'Velocity(km/s)', fontsize=18 )
axs2.set_xlabel( r'$\Delta B / B$', fontsize=18 )

axs2.set_title( 'MFI Type = ' + fname1[-21:-11], color='r', fontsize=20 )

plt.tight_layout()
plt.subplots_adjust(left=0.1, right=.99, bottom=0.1, top=0.95, wspace=0, hspace=0.2)

# Managing tick marks and all

for tick in axs2.xaxis.get_major_ticks() :
	tick.label.set_fontsize( 16 )

tick_labels = axs2.get_xticklabels()
axs2.set_xticklabels( tick_labels )

for tick in axs2.yaxis.get_major_ticks() :
	tick.label.set_fontsize( 16 )

tick_labels = axs2.get_yticklabels()
axs2.set_yticklabels( tick_labels )

# Save all the figures in one single file

os.chdir("/home/ahmadr/Desktop/GIT/fm_development/figures")

pdf = matplotlib.backends.backend_pdf.PdfPages( fname1[0:-4] + "_old.pdf" )

for fig in xrange(1, f.number+1 ): ## will open an empty extra figure :(
	pdf.savefig( fig )
pdf.close()

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

print 'It took','%.6f'% (time.time()-start), 'seconds.'
