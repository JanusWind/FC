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
#	fname = 'janus_2008-11-04-12-00-41_2008-11-04-13-01-02_auto_rng_avg_21_600_fvpcb_n.jns'
#	fname = 'janus_2008-11-04-12-00-41_2008-11-04-16-00-32_auto_rng_avg_21_300_fvpc.jns'
	fname = 'janus_2008-11-04-10-17-51_2008-11-04-13-01-02_auto_rng_avg_21_300_fvpc.jns'

	print 'Currently reading file ==> {}  \n'.format( fname )

	if( len( fname) > 15 ) :
		print 'Whoaaaa! Thats a big file name!\n'

	dat = [0]*len( fname )
	dat = pickle.load( open( fname, 'rb' ) )
	nd1  = len( dat['b0'] )

	# Change back the directory to the working directory.

	os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

	# Define all the parameters to be used during analysis.

	dat_time         = []

	ii                = [] # Initial index
	fi                = [] # Final index

	dat_db_rng_avg   = []

	dat_b_avg        = []

	dat_n_p_c        = []
	dat_n_p_b        = []
	dat_n_p          = []

	dat_del_v_p_c    = []
	dat_del_v_p_b    = []
	dat_fv_p_c       = []
	dat_fv_p_b       = []
	dat_sig_fv_p_c   = []
	dat_sig_fv_p_b   = []

	dat_dv_p_b       = []
	dat_s_dv_p_b     = []

	dat_w_fv_p       = []

	dat_alfvel       = []

	dat_s_fv_p_c     = []
	dat_s_fv_p_b     = []
	dat_s_sig_fv_p_c = []
	dat_s_sig_fv_p_b = []

	dat_s_db         = []
	dat_s_db_rng_avg = []

	r_ind = [ 4, 7, 16, 25, 25, 26, 30 ]

	keys = [ dat_time, dat_db_rng_avg, dat_b_avg,
	         dat_n_p_c, dat_n_p_b, dat_n_p, dat_fv_p_c, dat_fv_p_b,
	         dat_sig_fv_p_c, dat_sig_fv_p_b, dat_w_fv_p, dat_alfvel,
	         dat_s_fv_p_c, dat_s_fv_p_b, dat_s_sig_fv_p_c,
	         dat_s_sig_fv_p_b, dat_s_db    ]

	# Exaract the data from '.jns' file.

	dat_time.append( [ x.time().strftime("%H-%M") 
	                                              for x in  dat['time'] ] )

	for j in range( nd1 ) :

		ii = where( [ dat['timemin'][j] < x for x in dat['mfitime'][j] ] )[0][0]
		fi = where( [ dat['timemax'][j] > x for x in dat['mfitime'][j] ] )[0][-1]

		db_x_rng_avg = dat['b0_fields_db'][j]['mfi_set_rng_avg'][0]
		db_y_rng_avg = dat['b0_fields_db'][j]['mfi_set_rng_avg'][1]
		db_z_rng_avg = dat['b0_fields_db'][j]['mfi_set_rng_avg'][2]

		dat_db_rng_avg.append( sqrt( 2 * (
		                   std( db_x_rng_avg )**2 +
		                   std( db_x_rng_avg )**2 +
		                   std( db_x_rng_avg )**2 ) ) )

		dat_b_avg.append( sqrt(
		mean( dat['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
		mean( dat['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 +
		mean( dat['b0_fields_avg'][j]['mfi_set_rng_avg'][0] )**2 ) )

		dat_s_db.append( dat_db_rng_avg[j]/dat_b_avg[j] )

#		try :

	dat_n_p.append(   [ x if x!=None else float('nan') for x in  dat['n_p']   ] )
	dat_n_p_c.append( [ x if x!=None else float('nan') for x in  dat['n_p_c'] ] )
	dat_n_p_b.append( [ x if x!=None else float('nan') for x in  dat['n_p_b'] ] )
	
	dat_fv_p_c.append( [ x if x!=None else float('nan') for x in dat['fv_p_c'] ] )
	dat_fv_p_b.append( [ x if x!=None else float('nan') for x in dat['fv_p_b'] ] )
	dat_sig_fv_p_c.append( [ x if x!=None else float('nan') for x in dat['sig_fv_p_c'] ] )
	dat_sig_fv_p_b.append( [ x if x!=None else float('nan') for x in dat['sig_fv_p_b'] ] )
	
	dat_dv_p_b.append( [ x if x!=None else float('nan') for x in  dat['dv_p_b'] ] )

	dat_alfvel.append( [ x if x!=None else float('nan') for x in dat['alfvel_p'] ] )
	
	dat_del_v_p_c.append( [ dat_fv_p_c[0][k] *
	                                        dat_db_rng_avg[k]/dat_b_avg[k]
	                             for k in range( len( dat_fv_p_c[0] ) ) ] )

	dat_del_v_p_b.append( [ dat_fv_p_b[0][k] *
	                                        dat_db_rng_avg[k]/dat_b_avg[k]
	                             for k in range( len( dat_fv_p_b[0] ) ) ] )

	dat_s_fv_p_c.append( [ dat_del_v_p_c[0][k]/dat_alfvel[0][k] 
	                         for k in range( len( dat_fv_p_c[0] ) ) ] )

	dat_s_fv_p_b.append( [ dat_del_v_p_b[0][k]/dat_alfvel[0][k] 
	                         for k in range( len( dat_fv_p_b[0] ) ) ] )

	dat_s_sig_fv_p_c.append( [ dat_sig_fv_p_c[0][k] * dat_db_rng_avg[k] /
	                                     ( dat_b_avg[k]*dat_alfvel[0][k] )
	                         for k in range( len( dat_sig_fv_p_c[0] ) ) ] )

	dat_s_sig_fv_p_b.append( [ dat_sig_fv_p_b[0][k] * dat_db_rng_avg[k] /
	                                     ( dat_b_avg[k]*dat_alfvel[0][k] )
	                         for k in range( len( dat_sig_fv_p_c[0] ) ) ] )

	dat_s_dv_p_b.append( [ dat_dv_p_b[0][k] / dat_alfvel[0][k]
	                         for k in range( len( dat_sig_fv_p_c[0] ) ) ] )

	dat_w_fv_p.append( [ ( dat_fv_p_c[0][k] * dat_n_p_c[0][k] + 
	                 dat_fv_p_b[0][k] * dat_n_p_b[0][k] )/dat_n_p[0][k]
	                             for k in range( len( dat_fv_p_c[0] ) ) ] )

	dat_s_db_rng_avg.append( [ dat_db_rng_avg[k]/dat_b_avg[k]
	                             for k in range( len( dat_fv_p_c[0] ) ) ] )

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

if( len( dat_s_db) == 37 ) :

	[ dat_s_db.pop( i            ) for i in r_ind ]
	[ dat_time[0].pop( i         ) for i in r_ind ]
	[ dat_fv_p_c[0].pop( i       ) for i in r_ind ]
	[ dat_sig_fv_p_c[0].pop( i   ) for i in r_ind ]
	[ dat_s_fv_p_c[0].pop( i     ) for i in r_ind ]
	[ dat_s_sig_fv_p_c[0].pop( i ) for i in r_ind ]
	[ dat_fv_p_b[0].pop( i       ) for i in r_ind ]
	[ dat_sig_fv_p_b[0].pop( i   ) for i in r_ind ]
	[ dat_s_fv_p_b[0].pop( i     ) for i in r_ind ]
	[ dat_s_sig_fv_p_b[0].pop( i ) for i in r_ind ]
	[ dat_alfvel[0].pop( i       ) for i in r_ind ]
	[ dat_dv_p_b[0].pop( i       ) for i in r_ind ]
	[ dat_s_dv_p_b[0].pop( i     ) for i in r_ind ]

dat_s_fv_pc = [ xx/yy for xx,yy in zip( dat_fv_p_c[0], dat_alfvel[0]) ]
dat_s_sig_fv_pc = [ xx/yy for xx,yy in zip( dat_sig_fv_p_c[0], dat_alfvel[0]) ]

fit = stats.linregress( dat_s_db, dat_s_fv_p_c[0])

m = fit.slope
c = fit.intercept
r = fit.rvalue
sigma = fit. stderr

# Define figure paramaters

dpi = 40 # DPI of the saved plots

s = 15 # Marker size

legend_transparency = 0.50 # Transparency of legend

ncol = 1 # Number of columns for legend

rcParams['figure.figsize'] = 10, 10

ind = [ 15*i for i in range( 1 +  len( dat_time[0] )/15 ) ]

labels = [ dat_time[0][j] for j in ind ]


################################################################################
# Time-Series Plot
################################################################################

f, ax = plt.subplots( 1 )

ax.axhline( 0, ls='--', lw=0.5, color='gray' )

ax.scatter( dat_time[0], dat_s_fv_p_c[0], marker='^', s= 60, color='r' )

ax.set_ylim( -0.025, 0.025 )
ax.set_xlabel( 'Time', fontsize=20 )
ax.set_ylabel( '$\delta V_f / V_A$', fontsize=20 )

#ax.set_xticks( )
#ax.set_yticks( )

plt.xticks( [ dat_time[0][j] for j in ind ], rotation=45, fontsize=20 )
plt.yticks( fontsize=20 )

################################################################################
# Best fit plot and all
################################################################################

#f = plt.figure()
#
#plt.scatter( dat_s_db, dat_s_fv_p_c[0], color='r', marker='^', s=90, label='Computed Data' )
#plt.xticks( rotation=45 )
##plt.grid( True, which='major', axis='x', color='gray', lw='0.1', ls='--' )
#plt.plot( dat_s_db, np.array( dat_s_db ) * m, color='g', marker='*', ls='--', label='Best Fit' )
#plt.plot( dat_s_db, dat_s_db, color='gray', marker='.', ls='--', label='Theoretical Prediction' )
#plt.xlim( 0.002, 0.025 )
#plt.ylim( 0.002, 0.025 )
#plt.xlabel( r'$\left< \delta B \right>/B_0$', fontsize=20 )
#plt.ylabel( r'$\delta V_f / V_A$', fontsize=20 )
#plt.xticks( fontsize=20 )
#plt.yticks( fontsize=20 )
#
#plt.text( 0.01, 0.01570, 'Theoretical Slope= 1.', color='gray', fontsize=18, rotation=45 )
#plt.text( 0.010, 0.0114, 'Best Fit Slope= ' '%s'r'$\, \pm \,$' '%s'
#%( round( m, 2 ), round( fit.stderr, 2 ) ), color='gray', fontsize=18, rotation=32 )
#
#plt.legend( ncol=1, framealpha=legend_transparency, loc=2, fontsize=18 )
#plt.tight_layout( )

################################################################################
# Error bar plot
################################################################################

#f, ax = plt.subplots( 1 )
#
#ax.axhline( 0, ls='--', lw=0.5, color='gray' )
#
#eb1 = ax.errorbar( dat_time[0], dat_s_fv_p_c[0], yerr=dat_s_sig_fv_p_c[0],
#marker='^', ms=s, color='r', fmt='o', ecolor='gray', capsize=5,  label=r'$V_{fpc}$' )
#
#eb1[-1][0].set_linestyle( '-.' )
#
#if( len( dat_sig_fv_p_b[0] ) != 0 ) :
#
#	eb2 = ax.errorbar( dat_time[0], dat_s_fv_p_b[0], yerr=dat_s_sig_fv_p_b[0],
#	marker='v', ms=s, color='b', fmt='o', ecolor='k', capsize=3, label=r'$V_{fpb}$' )
#	eb2[-1][0].set_linestyle( '-.' )
#
#else :
#
#	ax.scatter( dat_time[0], dat_s_fv_p_b[0],
#	                       marker='v', s=s, color='b', label=r'$V_{fpb}$' )
#
##ax.scatter( dat_time[0], dat_s_fv_p_c[0], color='b', marker='^', label=r'$V_{fpc}$' )
##ax.scatter( dat_time[0], dat_s_fv_p_b[0], color='m', marker='v', label=r'$V_{fpb}$' )
##plt.grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )
#ax.set_xticks( ind )
#ax.set_xticklabels( labels, rotation=45, fontsize=24 )
#ax.legend( ncol=1, loc=1, fontsize=20 )
##plt.xlim( 0.002, 0.025 )
#ax.set_ylim( -0.025, 0.025 )
#ax.set_xlabel( 'Time', fontsize=28 )
##ax.set_xlabel( r'$\left< \delta B \right>/B_0$', fontsize=18 )
#ax.set_ylabel( r'$\delta V_f / V_A$', fontsize=28 )
##ax.set_yticks(  )
##ax.set_yticklabels( rotation=0, fontsize=18 )
#plt.yticks( fontsize=24 )
plt.tight_layout()

plt.show()

#os.chdir("/home/ahmadr/Desktop/GIT/fm_development/figures")
#
#pdf = matplotlib.backends.backend_pdf.PdfPages( fname[0:-4] + "_ICS_AGU.pdf" )
#
#for fig in xrange(1, f.number+1 ): ## will open an empty extra figure :(
#	pdf.savefig( fig )
#pdf.close()

'''
###############################################################################
## First Figure
###############################################################################

#if( len( dat_sig_fv_p_b[0] ) != 0 ) :
#
#	f, axs1 = plt.subplots( 3, 1, squeeze=True, sharex=False )
#
#else :

###############################################################################
## Second Figure
###############################################################################

f, axs1 = plt.subplots( 2, 1, squeeze=True, sharex=False )

axs1[0].errorbar( range( len( dat_time[0] ) ), dat_fv_p_c[0],
yerr=dat_sig_fv_p_c[0], marker='*', color='r', fmt='o', ecolor='g',
                                                           label='Proton Core' )

if( len( dat_sig_fv_p_b[0] ) != 0 ) :

	axs1[0].errorbar( range( len( dat_time[0] ) ), dat_fv_p_b[0],
	yerr=dat_sig_fv_p_b[0], marker='v', color='b', fmt='o',
	                                       ecolor='g', label='Proton Beam' )

else :

	axs1[0].scatter( range( len( dat_time[0] ) ), dat_fv_p_b[0],
	                       marker='v', s=s, color='b', label='Proton Beam' )
#axs2 = axs1[0].twinx()
#
#axs2.scatter( range( len( dat_time[0] ) ), dat_dv_p_b[0],
#             marker='d', s=s, color='m', label='Proton beam Drift Velocity' )

axs1[0].axhline( 0, marker='None', ls='--', color='c', lw='0.5' )
axs1[0].set_xlabel( 'Spectra number', fontsize=18 )
axs1[0].set_ylabel( r'$f_v$', fontsize=18 )
axs1[0].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )
axs1[0].set_xlim( [ 0, max( range( len( dat_time[0] ) ) ) ] )
axs1[0].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )

axs1[1].errorbar( dat_s_db, dat_fv_p_c[0], xerr=None, yerr=dat_sig_fv_p_c[0],
marker='*', color='r', fmt='o', ecolor='g', label='Proton Core' )

# Plotting the drift velocity on twin axis.

#axs3 = axs1[1].twinx()
#
#axs3.scatter( dat_s_db, dat_dv_p_b[0],
#                  marker='d', color='m', label='Proton Beam Drift Velocity' )

axs1[1].legend( ncol=ncol, framealpha=legend_transparency, loc=1, fontsize=18 )

axs1[1].axhline( 0, marker='None', ls='--', color='c', lw='0.5' )

axs1[1].set_xlabel( r'$|\Delta B /B_0|$', fontsize=18 )
axs1[1].set_ylabel( r'$f_v$', fontsize=18 )
axs1[1].set_xlim( [ 0, 0.025 ] )
axs1[1].grid( True, which='major', axis='x', color='b', lw='0.1', ls='--' )

#if( len( dat_sig_fv_p_b[0] ) != 0 ) :
#
#	axs1[2].errorbar( dat_s_db, dat_fv_p_b[0], xerr=None,
#	yerr=dat_sig_fv_p_b[0], marker='v', color='r', fmt='v',
#	ecolor='m', label='Proton Beam' )
#	axs1[2].legend( )
#	axs1[2].axhline( 0, marker='None', ls='--', color='gray', lw='0.5' )

#	axs1[2].set_ylabel( 'Velocity(km/s)', fontsize=18 )
#	axs1[2].set_xlabel( r'$\Delta B / B$', fontsize=18 )

#axs1[0].set_title( 'MFI Type = ' + fname[-22:-16], color='r', fontsize=20 )

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
'''
'''
###############################################################################
## Second Figure
###############################################################################

f, axs2 = plt.subplots( 1, 1, squeeze=True, sharex=False )

axs2.scatter( dat_s_db, dat_w_fv_p[0], marker='*', color='m',
                                                           label='Weighted fv' )
axs2.scatter( dat_s_db, dat_fv_p_c[0], marker='d', color='r',
                                                               label='Core fv' )
axs2.scatter( dat_s_db, dat_fv_p_b[0], marker='v', color='b',
                                                               label='Beam fv' )
axs2.axhline( 0, marker='None', ls='--', color='c', lw='0.5' )
axs2.legend( )
axs2.set_ylabel( 'Velocity(km/s)', fontsize=18 )
axs2.set_xlabel( r'$\Delta B / B$', fontsize=18 )

axs2.set_title( 'MFI Type = ' + fname[-21:-11], color='r', fontsize=20 )

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

pdf = matplotlib.backends.backend_pdf.PdfPages( fname[0:-4] + "_old.pdf" )

for fig in xrange(1, f.number+1 ): ## will open an empty extra figure :(
	pdf.savefig( fig )
pdf.close()
'''

os.chdir("/home/ahmadr/Desktop/GIT/fm_development")

print 'It took','%.6f'% (time.time()-start), 'seconds.'
