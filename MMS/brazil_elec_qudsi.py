import time as tm

start = tm.time()

#-------------------------------------------------------------------------------
# MODULES
#-------------------------------------------------------------------------------

# Load the necessary modules.

from spacepy      import pycdf
from numpy        import *
from datetime     import *
from matplotlib   import pyplot
from scipy.signal import medfilt
from glob         import glob
from janus_const  import const

import pickle

import sys
sys.path.insert( 0, '/data/Research/Active_Research/mms/mms_fest' )

import matplotlib.pyplot as plt

import matplotlib as mpl

#from bam_plot import *

#-------------------------------------------------------------------------------
# FUNCTION: get_ion
#-------------------------------------------------------------------------------

# Define the function for retrieving the FPI ion data from a specified day.

def get_ion( date, num ) :

	sc = 'mms' + str( num )

	fls = glob( '/data/Research/Active_Research/mms/mms_fest/SDC/'
	            + date + '/' + sc + '_fpi_brst_l2_dis*' )


	n_fls = len( fls )

	print 'Loading', n_fls, 'FPI ion files'
	print ''

	n_ion = 0


	for i in range( n_fls ) :

		dat = pycdf.CDF( fls[i] )

		if ( n_ion == 0 ) :

			time_strt = array( dat['Epoch']                       )
			dens      = array( dat[sc+'_dis_numberdensity_brst']  )
			vel_vec   = array( dat[sc+'_dis_bulkv_gse_brst']      )
			temp_tens = array( dat[sc+'_dis_temptensor_gse_brst'] )
			temp_per  = array( dat[sc+'_dis_tempperp_brst']       )
			temp_par  = array( dat[sc+'_dis_temppara_brst']       )

		else :

			time_strt = concatenate( ( time_strt, array( dat['Epoch']                       ) ) )
			dens      = concatenate( ( dens     , array( dat[sc+'_dis_numberdensity_brst']  ) ) )
			vel_vec   = concatenate( ( vel_vec  , array( dat[sc+'_dis_bulkv_gse_brst']      ) ) )
			temp_tens = concatenate( ( temp_tens, array( dat[sc+'_dis_temptensor_gse_brst'] ) ) )
			temp_per  = concatenate( ( temp_per , array( dat[sc+'_dis_tempperp_brst']       ) ) )
			temp_par  = concatenate( ( temp_par , array( dat[sc+'_dis_temppara_brst']       ) ) )

		n_ion = len( time_strt )

		print '     File', ( i + 1 ), 'done'

	time_stop = time_strt + timedelta( milliseconds=150. )

	temp_tot = ( temp_par + ( 2. * temp_per ) ) / 3.

	[ eigen_val, eigen_vec ] = linalg.eig( temp_tens )

	print ''
	print '     Number of data:', n_ion
	print ''

	return { 'n'         : n_ion    ,
	         'time_strt' : time_strt,
	         'time_stop' : time_stop,
	         'dens'      : dens     ,
	         'vel_vec'   : vel_vec  ,
	         'temp_tens' : temp_tens,
	         'temp_per'  : temp_per ,
	         'temp_par'  : temp_par ,
	         'temp_tot'  : temp_tot ,
	         'eigen_val' : eigen_val,
	         'eigen_vec' : eigen_vec  }


#-------------------------------------------------------------------------------
# FUNCTION: get_elec
#-------------------------------------------------------------------------------

# Define the function for retrieving the FPI electron data from a specified day.

def get_elec( date, num ) :

	sc = 'mms' + str( num )

	fls = glob( '/data/Research/Active_Research/mms/mms_fest/SDC/'
	            + date + '/' + sc + '_fpi_brst_l2_des*' )

	n_fls = len( fls )

	print 'Loading', n_fls, 'FPI electron files'
	print ''

	n_elec = 0

	for i in range( n_fls ) :

		dat = pycdf.CDF( fls[i] )

		if ( n_elec == 0 ) :

			time_strt = array( dat['Epoch']                       )
			dens      = array( dat[sc+'_des_numberdensity_brst']  )
			vel_vec   = array( dat[sc+'_des_bulkv_gse_brst']      )
			temp_tens = array( dat[sc+'_des_temptensor_gse_brst'] )
			temp_per  = array( dat[sc+'_des_tempperp_brst']       )
			temp_par  = array( dat[sc+'_des_temppara_brst']       )

		else :

			time_strt = concatenate( ( time_strt, array( dat['Epoch']                       ) ) )
			dens      = concatenate( ( dens     , array( dat[sc+'_des_numberdensity_brst']  ) ) )
			vel_vec   = concatenate( ( vel_vec  , array( dat[sc+'_des_bulkv_gse_brst']      ) ) )
			temp_tens = concatenate( ( temp_tens, array( dat[sc+'_des_temptensor_gse_brst'] ) ) )
			temp_per  = concatenate( ( temp_per , array( dat[sc+'_des_tempperp_brst']       ) ) )
			temp_par  = concatenate( ( temp_par , array( dat[sc+'_des_temppara_brst']       ) ) )

		n_elec = len( time_strt )

		print '     File', ( i + 1 ), 'done'

	time_stop = time_strt + timedelta( milliseconds=30. )

	temp_tot = ( temp_par + ( 2. * temp_per ) ) / 3.

	[ eigen_val, eigen_vec ] = linalg.eig( temp_tens )

	print ''
	print '     Number of data:', n_elec
	print ''

	return { 'n'         : n_elec   ,
	         'time_strt' : time_strt,
	         'time_stop' : time_stop,
	         'dens'      : dens     ,
	         'vel_vec'   : vel_vec  ,
	         'temp_tens' : temp_tens,
	         'temp_per'  : temp_per ,
	         'temp_par'  : temp_par ,
	         'temp_tot'  : temp_tot ,
	         'eigen_val' : eigen_val,
	         'eigen_vec' : eigen_vec  }


#-------------------------------------------------------------------------------
# FUNCTION: get_mag
#-------------------------------------------------------------------------------

# Define the function for retrieving the FGM magnetic-field data from a
# specified day.

def get_mag( date, num ) :

	sc = 'mms' + str( num )

	fls = glob( '/data/Research/Active_Research/mms/mms_fest/SDC/' + date + '/' + sc + '_fgm*' )

	n_fls = len( fls )

	print 'Loading', n_fls, 'FGM files'
	print ''

	n_mag = 0

	for i in range( n_fls ) :

		dat = pycdf.CDF( fls[i] )

		if ( n_mag == 0 ) :

			time = array( dat['Epoch']                 )
			mag  = array( dat[sc+'_fgm_b_gse_brst_l2'] )[:,0:3]

		else :

			time = concatenate( ( time, array( dat['Epoch']                 )        ) )
			mag  = concatenate( ( mag , array( dat[sc+'_fgm_b_gse_brst_l2'] )[:,0:3] ) )

		n_mag = len( time )

		print '     File', ( i + 1 ), 'done'

	print ''
	print 'Number of data:', n_mag
	print ''

	return { 'n'    : n_mag,
	         'time' : time ,
	         'mag'  : mag    }


#-------------------------------------------------------------------------------
# FUNCTION: get_sync
#-------------------------------------------------------------------------------

# Define the function for retrieving and syncronizing the electron and magnetic-field
# data from a specified day.

def get_sync( date, num ) :

	fname = '/data/Research/Active_Research/mms/mms_fest/sync_e/sync_' + date + '_' + str( num ) + '.e'

	try :
		sync = pickle.load( open( fname, 'rb' ) )
		return sync
	except :
		pass

#	ion  = get_ion(  date, num )
	elec = get_elec( date, num )
	mag  = get_mag(  date, num )

	print 'Syncronizing data'
	print ''

	avg_mag = tile( 0., ( elec['n'], 3 ) )

	avg_elec_dens    = tile( 0.,   elec['n']      )
	avg_elec_vel_vec = tile( 0., ( elec['n'], 3 ) )

	for i in range( elec['n'] ) :

		tk_mag = where( ( mag['time'] >= elec['time_strt'][i] ) &
		                ( mag['time'] <  elec['time_stop'][i] )   )

		if ( len( tk_mag[0] ) > 0 ) :

			avg_mag[i,0] = mean( (mag['mag'][tk_mag])[:,0] )
			avg_mag[i,1] = mean( (mag['mag'][tk_mag])[:,1] )
			avg_mag[i,2] = mean( (mag['mag'][tk_mag])[:,2] )

		tk_elec = where( ( elec['time_strt'] >= elec['time_strt'][i] ) &
		                 ( elec['time_strt'] <  elec['time_stop'][i] )   )

		if ( len( tk_elec[0] ) > 0 ) :

			avg_elec_dens[i] = mean( elec['dens'][tk_elec] )

			avg_elec_vel_vec[i,0] = mean( (elec['vel_vec'][tk_elec])[:,0] )
			avg_elec_vel_vec[i,1] = mean( (elec['vel_vec'][tk_elec])[:,1] )
			avg_elec_vel_vec[i,2] = mean( (elec['vel_vec'][tk_elec])[:,2] )

	tk_sync = where( ( sum( avg_mag, axis=1 ) != 0. ) &
	                 ( avg_elec_dens          != 0. )   )

	n_sync = len( tk_sync[0] )

	sync = { 'n'            : n_sync                   ,
	         'mag_vec'      : avg_mag[tk_sync]         ,
	         'elec_dens'    : avg_elec_dens[tk_sync]   ,
	         'elec_vel_vec' : avg_elec_vel_vec[tk_sync]  }

	for key in elec.keys( ) :
		if ( key == 'n' ) :
			continue
		sync['elec_'+key] = elec[key][tk_sync]

	sync['mag_dir'] = array( [ b / linalg.norm( b ) for b in sync['mag_vec'] ] )

	sync['mag_mag'] = sqrt( sync['mag_vec'][:,0]**2 + sync['mag_vec'][:,1]**2
	                                                + sync['mag_vec'][:,2]**2 )

	sync['elec_beta_par'] = (   ( 2 * const['mu_0'] ) * ( 1.E6 * sync['elec_dens'] )
                                  * ( const['q_p'] * sync['elec_temp_par'] ) / ( 1E-9 * sync['mag_mag'] )**2 )

#	sync['var_ion_beta_par'] = (   ( 2 * const['mu_0'] ) * ( 1.E6 * sync['elec_dens'] )
#                                     * ( const['q_p'] * sync['ion_temp_par'] ) / ( 1E-9 * sync['mag_mag'] )**2 )

	sync['elec_temp_aniso'] = sync['elec_temp_per'] / sync['elec_temp_par']

#	sync['elec_phi']        = tile( 0.,   sync['n']      )
#	sync['elec_temp_asym']  = tile( 0.,   sync['n']      )
#	sync['curr_vec']        = tile( 0., ( sync['n'], 3 ) )
#	sync['curr_mag']        = tile( 0.,   sync['n']      )
#	sync['var_curr_vec']    = tile( 0., ( sync['n'], 3 ) )
#	sync['var_curr_mag']    = tile( 0.,   sync['n']      )

#	for i in range( sync['n'] ) :
#
#		ang = array( [ rad2deg( arccos( abs( dot(
#		                            sync['mag_dir'      ][i],
#			                    sync['ion_eigen_vec'][i,:,j] ) ) ) )
#			       for j in range( 3 )                           ] )
#
#		sync['ion_phi'][i] = amin( ang )
#
#		val = sorted( sync['ion_eigen_val'][i] )
#
#		sync['ion_temp_asym' ][i] = min( [ val[1]/val[0], val[2]/val[1] ] )
#
#		curr_vec = ( 1.E9 * const['q_p'] ) * (     # [A/m^2]
#		                ( sync['ion_dens' ][i] * sync[ 'ion_vel_vec'][i] )
#		              - ( sync['elec_dens'][i] * sync['elec_vel_vec'][i] ) )
#
#		var_curr_vec = ( 1.E9 * const['q_p'] ) * sync['elec_dens'][i] * (
#		                       sync[ 'ion_vel_vec'][i] - sync['elec_vel_vec'][i] )
#
#		sync['curr_vec'][i] = curr_vec
#		sync['curr_mag'][i] = linalg.norm( curr_vec )
#
#		sync['var_curr_vec'][i] = var_curr_vec
#		sync['var_curr_mag'][i] = linalg.norm( var_curr_vec )

	print '     Number of data:', sync['n']
	print ''

	pickle.dump( sync, open( fname, 'wb' ) )

	return sync

#-------------------------------------------------------------------------------
# ANALYSIS
#-------------------------------------------------------------------------------

print ''

#date = [ '20160111' ]
date = [ '20160111', '20160124', '20161025', '20170118', '20170127',
         '20171123'                                                  ]

"""
arr = [ get_sync( d, 1 ) for d in date ]
for a in arr :
	t_min = min( a['ion_time_strt'] )
	t_max = max( a['ion_time_stop'] )
	print t_min, t_max
"""

arr = [ get_sync( d, i ) for i in range( 1, 5 )
                         for d in date          ]

sync = { }

for key in arr[0].keys( ) :
	if ( key == 'n' ) :
		sync[key] = sum( [ a[key] for a in arr ] )
	else :
		sync[key] = concatenate( [ a[key] for a in arr ] )

print 'Number of data for plots:', sync['n']
print ''

print 'It took','%.6f'% (tm.time()-start), 'seconds.'


y = sync['elec_temp_aniso']
x = log10( sync['elec_beta_par'] )

labels = [ 10**-1, 10**0, 10**1, 10**2 ]

ind = range( len( labels ) )

plt.clf( )
h=plt.hist2d( x, y,range=[[ -1.1, 2.],[0.4, 1.6]],bins=[ 50, 50 ],
              norm=mpl.colors.LogNorm(), cmap=plt.cm.jet )

plt.axhline( 1, color='k', lw=0.8 )

plt.xticks( arange(-1, 3), labels )

plt.colorbar( )
plt.xlabel( r'$\beta_{\parallel {\rm e}} \equiv 2\,\mu_0\,n_{\rm e}\,k_{\rm B}\,T_{\parallel {\rm e}}\,/\,B^2$' )

plt.ylabel( r'$R_{\rm e} \equiv T_{\perp {\rm e}}\,/\,T_{\parallel {\rm e}}$' )

plt.tight_layout()

plt.savefig( 'beta_aniso_e.pdf' )
plt.show()
