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

from janus_const import const
from math import sqrt, acos, pi
from janus_helper import calc_arr_norm, calc_arr_dot
from numpy import interp, sin, cos, deg2rad


################################################################################
## DEFINE THE CLASS FOR DATUM
################################################################################

class fc_dat( ) :

	def __init__( self,
                      spec=None, azim=None,
                      elev=None, volt_cen=None,
                      volt_del=None, curr=None, valid = False                ) :

		self._spec      = spec
		self._azim      = azim
		self._elev      = elev
		self._volt_cen  = volt_cen
		self._volt_del  = volt_del
                self._valid     = valid

		self._volt_strt = (self._volt_cen - ( self._volt_del / 2. ) )
		self._volt_stop = (self._volt_cen + ( self._volt_del / 2. ) )

		self._vel_strt  = 1E-3*( sqrt(2.0*const['q_p']*
                                         self['volt_strt']/const['m_p'])    )
		self._vel_stop  = 1E-3*( sqrt((2.0*const['q_p']*
                                         self['volt_stop']/const['m_p']))   )
		self._vel_cen   = ( (self['vel_strt']+self['vel_stop'])/2.  )
		self._vel_del   = (  self['vel_stop']-self['vel_strt']      )
		self._curr      = curr


                # TODO: Confirm these two formulae

		self._the       = 90 - self._elev
		self._phi       =    - self._azim

		self._dir_x     = (sin( deg2rad( self._the ) ) *
                                   cos( deg2rad( self._phi ) )              )
		self._dir_y     = (sin( deg2rad( self._the ) ) *
                                   sin( deg2rad( self._phi ) )              )
		self._dir_z     = (cos( deg2rad( self._the ) )              )

		self._norm_b_x  = None
		self._norm_b_y  = None
		self._norm_b_z  = None

		if ( ( self._azim     is None ) or ( self._elev     is None ) or
		     ( self._volt_cen is None ) or ( self._volt_del is None ) or
                     ( self._curr     is None )                              ) :
			self.valid = False
		else :
			self.valid = True

	def __getitem__( self, key ) :
#
#               return self.__dict__['_'+key]
#

		if ( key == 'spec' ) :
			return self._spec
		elif ( key == 'valid' ) :
			return self._valid
		elif ( key == 'azim' ) :
			return self._azim
		elif ( key == 'elev' ) :
			return self._elev
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
			return ( self._norm_b_x, self._norm_b_y, self._norm_b_z )

		else :
			raise KeyError( 'Invalid key for "fc_dat ".' )


	def __setitem__( self, key, val ) :

		raise KeyError('Reassignment not allowed after initialization')


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


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING THE EFFECTIVE AREA OF THE CUP.
	#-----------------------------------------------------------------------
	
	def calc_eff_area( self, v ) :

		# Note.#nvn is a vector similar to inflow particle bulk 
		# velocity and ndir is the look direction. 


		# Normalize the look direction and particle velocity.

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
	# DEFINE THE FUNCTION FOR CALCULATING EXPECTED CURRENT (MAXWELLIAN).
	#-----------------------------------------------------------------------

	#TODO Make this not a stupid hack of the bi-Maxwellian version.

#        def calc_cur_max( self,
#                           vel_cen, vel_wid,
#                           dir_alt, dir_azm,
#                           prm_n, prm_v_x, prm_v_y, prm_v_z, prm_w ) :
 
 
                 # Return the equivalent bi-Maxwellian response for equal
                 # perpendicular and parallel thermal speeds and a dummy
                 # magnetic field.
 
#                return self.calc_cur_bmx( vel_cen, vel_wid,
#                                          dir_alt, dir_azm, 1., 0., 0.,
#                                          prm_n, prm_v_x, prm_v_y, prm_v_z,
#                                          prm_w, prm_w                      )
 

        # TODO: Even if we have defined the parameters, doesn't a function
        #       still need inputs? Or can we just skip that part and remove
        #       all the inputs and put them in the function as self.* ???

	def calc_curr_max( self,
	                    vel_cen, vel_wid,
	                    dir_alt, dir_azm,
	                    n, v_x, v_y, v_z, w ) :

		# Return the equivalent bi-Maxwellian response for equal
		# perpendicular and parallel thermal speeds and a dummy
		# magnetic field.

		# Calcualte the vector bulk velocity.

                x = array([v_x, v_y, v_z])

                if (v.ndim > 1 ) :
                        v = transpose( v )

                # Calculate the look direction as a cartesian unit vector.

                mag = array( [ mag_x, mag_y, mag_z ] ) 

                if ( mag.ndim > 1 ) :
                        mag = transpose( mag )

                dmg = self.calc_arr_nrm( mag )


                # Calculate the component of the magnetic field unit vector
                # along that lies along the look direction.

                dmg_dlk = self.calc_arr_dot( dmg, dlk )


		# Calculate the exponential terms of the current.

		ret_exp_1 = 1.e3 * w * sqrt( 2. / pi ) * exp(
		            - ( ( self['vel_strt']
		            - self.calc_arr_dot( dlk, -v ) )
		            / w )**2 / 2. )
		ret_exp_2 = 1.e3 * w * sqrt( 2. / pi ) * exp(
		            - ( ( self['vel_stop']
		            - self.calc_arr_dot( dlk, -v ) )
		            / w )**2 / 2. )


		# Calculate the "erf" terms.

		ret_erf_1 = 1.e3 * self.calc_arr_dot( dlk, -v ) * erf(
		            ( self['vel_strt']
		            - self.calc_arr_dot( dlk, -v ) )
		            / ( sqrt(2.) * w ) )
		ret_erf_2 = 1.e3 * self.calc_arr_dot( dlk, -v ) * erf(
		            ( self['vel_stop']
		            - self.calc_arr_dot( dlk, -v ) )
		            / ( sqrt(2.) * w ) )


		# Calculate the parenthetical expression.

		ret_prn = ( ( ret_exp_2 + ret_erf_2 ) -
		            ( ret_exp_1 + ret_erf_1 )   )


		# Calculate the expected current.

		ret = ( (   1.e12 ) * ( 1. / 2. ) * ( const['q_p'] )
		        * ( 1.e6 * n )
		        * ( 1.e-4 * self.spec.calc_eff_area( dlk, v ) )
		        * ( ret_prn ) )

		return ret 


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING EXPECTED CURRENT (BI-MAXWELLIAN).
	#-----------------------------------------------------------------------

	#FIXME 6

	#TODO Migrate to "fc_dat"

	def calc_curr_bmx( self,
	                   vel_cen, vel_wid,
                           dir_alt, dir_azm,
	                   mag_x, mag_y, mag_z,
                           n, v_x, v_y, v_z,
                           w_per,w_par          ) :


		# Note.  This function is based on Equation 2.34 from Maruca
		#        (PhD thesis, 2012), but differs by a factor of $2$
		#        (i.e., the factor of $2$ from Equation 2.13, which is
		#        automatically calibrated out of the Wind/FC data).

		# Compute the effective thermal speed along this look direction.


		w = sqrt( ( ( 1. - dmg_dlk**2 ) * w_per**2 ) + 
		             (     dmg_dlk**2   * w_par**2 )   )


                return self.calc_curr_max( vel_cen, vel_wid,
                                          dir_alt, dir_azm,
	                                  mag_x, mag_y, mag_z,
                                          n, v_x, v_y, v_z, w  )

        #-----------------------------------------------------------------------
        # DEFINE THE FUNCTION FOR CONVERT ALT-AZM TO A CARTESIAN UNIT VECTOR.
        #-----------------------------------------------------------------------

#        def calc_dir_look( self, dir_alt, dir_azm ) :
#
#                # Convert from spherical to rectangular coordinates and return
#                # the result.
#
#                the = self._the
#                phi = self._phi
#
#                ret = array( [
#                        sin( deg2rad( self._the ) ) * cos( deg2rad(self._phi ) ),
#                        sin( deg2rad( self._the ) ) * sin( deg2rad(self._phi ) ),
#                        cos( deg2rad( self._the ) )                          ] )
#
#                if ( ret.ndim > 1 ) :
#                        return transpose( ret )
#                else :
#                        return ret
