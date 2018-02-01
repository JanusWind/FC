################################################################################
##
## Janus -- GUI Software for Processing Thermal-Ion Measurements from the
##          Wind Spacecraft's Faraday Cups
##
## Copyright (C) 2016 Bennett A. Maruca (bmaruca@udel.edu)
##
## This program is free software: you can redistribute it and/or modify it under
## the terms of the GNU General Public License as published by the Free Software
## Foundation, either version 3 of the License, or (at your option) any later
## version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
## FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
## details.
##
## You should have received a copy of the GNU General Public License along with
## this program.  If not, see http://www.gnu.org/licenses/.
##
################################################################################


################################################################################
## LOAD THE NECESSARY MODULES.
################################################################################

from math import sqrt, acos, pi
from numpy import interp, sin, cos, deg2rad, exp, array
from scipy.special import erf

from janus_const import const
from janus_helper import calc_arr_norm, calc_arr_dot


################################################################################
## DEFINE THE CLASS FOR DATUM
################################################################################

class fc_dat( ) :

	def __init__( self,
                      spec=None, azim=None,
                      elev=None, volt_cen=None, time=None,
                      volt_del=None, curr=None, valid=False ) :

		self._spec      = spec
		self._azim      = azim
		self._elev      = elev
		self._volt_cen  = volt_cen
		self._volt_del  = volt_del
                self._valid     = valid
                self._time      = time

		self._volt_strt = (self._volt_cen - ( self._volt_del / 2. ) )
		self._volt_stop = (self._volt_cen + ( self._volt_del / 2. ) )

		self._vel_strt  = 1E-3*( sqrt(2.0*const['q_p']*
		                         self['volt_strt']/const['m_p'] )   )
		self._vel_stop  = 1E-3*( sqrt((2.0*const['q_p']*
		                         self['volt_stop']/const['m_p'] ) ) )
                self._vel_cen   = 1E-3*( sqrt(2.0*const['q_p']*
		                         self['volt_cen']/const['m_p']  )   )
		self._vel_del   = ( self['vel_stop']-self['vel_strt']       )
		self._curr      = curr

                # TODO: Confirm these two formulae

		self._the       = ( 90 + self._elev ) * pi/180
		self._phi       = (    - self._azim ) * pi/180

		self._dir_x     = sin( self._the ) * cos( self._phi )
		self._dir_y     = sin( self._the ) * sin( self._phi )
		self._dir_z     = cos( self._the )

		self._norm_b_x  = None
		self._norm_b_y  = None
		self._norm_b_z  = None

		self._maglook   = None

		if ( ( self._azim     is None ) or ( self._elev     is None ) or
		     ( self._volt_cen is None ) or ( self._volt_del is None ) or
                     ( self._curr     is None )                              ) :
			self._valid = False
		else :
			self._valid = True

	def __getitem__( self, key ) :

#               return self.__dict__['_'+key]

		if ( key == 'spec' ) :
			return self._spec
		elif ( key == 'valid' ) :
			return self._valid
		elif ( key == 'azim' ) :
			return self._azim
		elif ( key == 'elev' ) :
			return self._elev
                elif ( key == 'time' ) :
                        return self._time
		elif ( key == 'volt_cen' ) :
			return self._volt_cen
		elif ( key == 'volt_del' ) :
			return self._volt_del
		elif ( key == 'volt_strt' ) :
			return self._volt_strt
		elif ( key == 'volt_stop' ) :
			return self._volt_stop
		elif ( key == 'vel_strt' ) :
			return self._vel_strt
		elif ( key == 'vel_stop' ) :
			return self._vel_stop
		elif ( key == 'vel_cen' ) :
			return self._vel_cen
		elif ( key == 'vel_del' ) :
			return self._vel_del
		elif ( key == 'curr' ) :
			return self._curr
		elif ( key == 'curr_valid' ) :
			if ( self['valid'] ) :
				return self['curr']
			else :
				return 0.
		elif ( key == 'the' ) :
			return self._the
		elif ( key == 'phi' ) :
			return self._phi
		elif ( key == 'dir_x' ) :
			return self._dir_x
		elif ( key == 'dir_y' ) :
			return self._dir_y
		elif ( key == 'dir_z' ) :
			return self._dir_z
		elif ( key == 'dir' ) :
			return ( self._dir_x, self._dir_y, self._dir_z )
		elif ( key == 'norm_b_x' ) :
			return self._norm_b_x
		elif ( key == 'norm_b_y' ) :
			return self._norm_b_y
		elif ( key == 'norm_b_z' ) :
			return self._norm_b_z
		elif ( key == 'norm_b' ) :
			return ( self._norm_b_x,self._norm_b_y,self._norm_b_z )
		elif ( key == 'maglook' ) :
			return ( self._maglook )
		else :
			raise KeyError( 'Invalid key for "fc_dat".' )

	def __setitem__( self, key, val ) :

		raise KeyError('Reassignment not allowed after initialization.')


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SETIING THE MAGNETIC FIELD DIRECTION.
	#-----------------------------------------------------------------------

	def set_mag( self, b_vec ) :

		# Normalize the magnetic-field vector.

		norm_b = calc_arr_norm( b_vec )

		# Store the components of the normalized magnetic-field vector.

		self._norm_b_x = norm_b[0]
		self._norm_b_y = norm_b[1]
		self._norm_b_z = norm_b[2]

		self._maglook = calc_arr_dot( self['norm_b'], self['dir'] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING THE EFFECTIVE AREA OF THE CUP.
	#-----------------------------------------------------------------------
	
	def calc_eff_area( self, v ) :

		# Note. #nvn is a vector similar to inflow particle bulk 
		# velocity and ndir is the look direction. 


		# Normalize the particle velocity.

		vn  = calc_arr_norm( v )
		nvn = tuple( [ -c for c in vn ] )

		# Calculate the particle inflow angle (in degrees) relative to
		# the cup normal (i.e., the cup pointing direction).

		psi = acos( calc_arr_dot( self['dir'], nvn ) )*pi/180.
		if ( psi > 90. ) :
			return 0. 
 		
		# Return the effective collecting area corresponding to "psi".

		return interp( psi, self._spec._eff_deg, self._spec._eff_area )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION TO CALCULATE EXPECTED MAXWELLIAN CURRENT.
	#-----------------------------------------------------------------------

	def calc_curr( self, m, q, v0, n, dv, w ) :

		# Note.  This function is based on Equation 2.34 from Maruca
		#        (PhD thesis, 2012), but differs by a factor of $2$
		#        (i.e., the factor of $2$ from Equation 2.13, which is
		#        automatically calibrated out of the Wind/FC data).

		# Check whether thermal velocity is a 2-D list, which implies
		# anisotropy. If it is calculate the effective thermal velocity,
		# else continue.

		if ( hasattr( w, '__len__' ) and ( w is not None ) ) :

			if ( w is not None ) :
				ml2 = ( self['maglook'] )**2

				w_eff = sqrt( ( ( 1. - ml2 ) * w[0]**2 ) +
			                    (          ml2   * w[1]**2 )   )
		else :
			w_eff = w

		# Calculate the total velocity using drift

		if ( dv is None ) :
			v_vec = [ v0[i] for i in range( len( v0 ) ) ]
		else :
			v_vec = [ v0[i] + dv * self['norm_b'][i]
			                           for i in range( len( v0 ) ) ]

		# Calculate the component of the magnetic field unit vector
		# along that lies along the look direction.

		dlk_v   = -calc_arr_dot( self['dir'], v_vec )

		# Scale the velocities with charge to mass ratio.

		vel_strt = self['vel_strt'] * sqrt( q/m )
		vel_stop = self['vel_stop'] * sqrt( q/m )

		# Calculate the exponential terms of the current.

		ret_exp_1 = 1.e3 * w_eff * sqrt( 2. / pi ) * exp(
		                   - ( ( vel_strt - dlk_v  ) / w_eff )**2 / 2. )

		ret_exp_2 = 1.e3 * w_eff * sqrt( 2. / pi ) * exp(
		                   - ( ( vel_stop - dlk_v  ) / w_eff )**2 / 2. )

		# Calculate the "erf" terms.

		ret_erf_1 = 1.e3 * dlk_v * erf( ( vel_strt - dlk_v ) /
		                                ( sqrt(2.) * w_eff ) )
		ret_erf_2 = 1.e3 * dlk_v * erf( ( vel_stop - dlk_v ) /
		                                ( sqrt(2.) * w_eff ) )

		# Calculate the parenthetical expression.

		ret_prn = ( ( ret_exp_2 + ret_erf_2 ) -
		            ( ret_exp_1 + ret_erf_1 )   )

		# Calculate the expected current.

		return (   ( 1.e12 ) * ( 1. / 2. )
		         * ( q * const['q_p'] ) * ( 1.e6 * n )
		         * ( 1.e-4 * self.calc_eff_area( v_vec ) )
		         * ( ret_prn )                             )
