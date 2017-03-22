from janus_const import const
from math import sqrt, acos, pi
from janus_helper import calc_vec_norm, calc_vec_dot
from numpy import interp, sin, cos, deg2rad

	#-----------------------------------------------------------------------
				# DEFINE THE Class FOR datum
	#-----------------------------------------------------------------------

class fc_dat( ) :

	def __init__( self, spec=None, 
	              azim=None, elev=None,
	              volt_cen=None, volt_del=None,
	              curr= None, valid = False           ) :

		self._spec  = spec
		self._valid = valid
		self._azim  = azim
		self._elev  = elev
		self._volt_cen = volt_cen
		self._volt_del = volt_del
		self._volt_strt = (self._volt_cen - ( self._volt_del / 2. ) )
		self._volt_stop = (self._volt_cen + ( self._volt_del / 2. ) )
		self._vel_strt  = 1E-3*( sqrt((2.0*const['q_p']*self['volt_strt']/
								const['m_p'])))
		self._vel_stop  = 1E-3*( sqrt((2.0*const['q_p']*self['volt_stop']/
								const['m_p'])))
		self._vel_cen   = ( (self['vel_strt']+self['vel_stop'])/2. )
		self._vel_del   = (  self['vel_stop']-self['vel_strt'] )
		self._curr = curr

		self._the = 90 - self._elev     # TODO: Confirm these two formulae
		self._phi =    - self._azim

		self._dir_x = sin( deg2rad( self._the ) ) * cos( deg2rad( self._phi ) )
		self._dir_y = sin( deg2rad( self._the ) ) * sin( deg2rad( self._phi ) )
		self._dir_z = cos( deg2rad( self._the ) )

		self._norm_b_x = None
		self._norm_b_y = None
		self._norm_b_z = None

		if ( ( self._azim     is None ) or
		     ( self._elev     is None ) or
		     ( self._volt_cen is None ) or
		     ( self._volt_del is None ) or
		     ( self._curr     is None )    ) :
			self.valid = False
		else :
			self.valid = True

		# front underscore keeps the variable private to user
		# How to get 'spec', 'valid'
		# I can still set values to these arguments
		# Set 'valid' = False ad default 
		

	def __getitem__( self, key ) :

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

		raise KeyError( 'Reassignment not permitted after initialization.' )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SETIING THE MAGNETIC FIELD DIRECTION.
	#-----------------------------------------------------------------------

	def set_mag( self, b_vec ) :

		# Normalize the magnetic-field vector.

		norm_b = calc_vec_norm( b_vec )

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

		vn = calc_vec_norm( v )
		nvn = tuple( [ -c for c in vn ] )

		# Calculate the particle inflow angle (in degrees) relative to
		# the cup normal (i.e., the cup pointing direction).

		psi = acos( calc_vec_dot( self['dir'], nvn ) )*pi/180.
		if ( psi > 90. ) :
			return 0. 
 		
		# Return the effective collecting area corresponding to "psi".

		return interp( psi, self._spec._eff_deg, self._spec._eff_area )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING EXPECTED CURRENT (MAXWELLIAN).
	#-----------------------------------------------------------------------

	#TODO Make this not a stupid hack of the bi-Maxwellian version.

	def calc_cur_max( self,
	                  vel_cen, vel_wid,
	                  dir_alt, dir_azm,
	                  prm_n, prm_v_x, prm_v_y, prm_v_z, prm_w ) :

		# Return the equivalent bi-Maxwellian response for equal
		# perpendicular and parallel thermal speeds and a dummy
		# magnetic field.

		return self.calc_cur_bmx( vel_cen, vel_wid,
		                          dir_alt, dir_azm, 1., 0., 0.,
		                          prm_n, prm_v_x, prm_v_y, prm_v_z,
		                          prm_w, prm_w                      )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING EXPECTED CURRENT (BI-MAXWELLIAN).
	#-----------------------------------------------------------------------

	#FIXME 6

	#TODO Migrate to "fc_dat"

	def calc_cur_bmx( self,
	                  vel_cen, vel_wid,
	                  dir_alt, dir_azm,
	                  mag_x, mag_y, mag_z,
	                  prm_n, prm_v_x, prm_v_y, prm_v_z,		# Remove prm_
	                  prm_w            ) :


		# Note.  This function is based on Equation 2.34 from Maruca
		#        (PhD thesis, 2012), but differs by a factor of $2$
		#        (i.e., the factor of $2$ from Equation 2.13, which is
		#        automatically calibrated out of the Wind/FC data).


		# Calcualte the vector bulk velocity.

		prm_v = array( [ prm_v_x, prm_v_y, prm_v_z ] )

		if ( prm_v.ndim > 1 ) :
			prm_v = transpose( prm_v )


		# Calculate the look direction as a cartesian unit vector.

		dlk = self.calc_dir_look( )


		# Calculate the direction of the magnetic field as a cartesian
		# unit vector.

		mag = array( [ mag_x, mag_y, mag_z ] )

		if ( mag.ndim > 1 ) :
			mag = transpose( mag )

		dmg = self.calc_arr_nrm( mag )


		# Calculate the component of the magnetic field unit vector
		# along that lies along the look direction.

		dmg_dlk = self.calc_arr_dot( dmg, dlk )


		# Compute the effective thermal speed along this look direction.


		#prm_w = sqrt( ( ( 1. - dmg_dlk**2 ) * prm_w_per**2 ) + 
		 #             (        dmg_dlk**2   * prm_w_par**2 )   )


		# Calculate the exponential terms of the current.

		ret_exp_1 = 1.e3 * prm_w * sqrt( 2. / pi ) * exp(
		            - ( ( self['vel_strt']
		            - self.calc_arr_dot( dlk, -prm_v ) )
		            / prm_w )**2 / 2. )
		ret_exp_2 = 1.e3 * prm_w * sqrt( 2. / pi ) * exp(
		            - ( ( self['vel_stop'] 							#vel_cen + ( vel_wid / 2. )
		            - self.calc_arr_dot( dlk, -prm_v ) )
		            / prm_w )**2 / 2. )


		# Calculate the "erf" terms.

		ret_erf_1 = 1.e3 * self.calc_arr_dot( dlk, -prm_v ) * erf(
		            ( self['vel_strt']								#vel_cen - ( vel_wid / 2. )
		            - self.calc_arr_dot( dlk, -prm_v ) )
		            / ( sqrt(2.) * prm_w ) )
		ret_erf_2 = 1.e3 * self.calc_arr_dot( dlk, -prm_v ) * erf(
		            ( self['vel_stop']								#vel_cen + ( vel_wid / 2. )
		            - self.calc_arr_dot( dlk, -prm_v ) )
		            / ( sqrt(2.) * prm_w ) )


		# Calculate the parenthetical expression.

		ret_prn = ( ( ret_exp_2 + ret_erf_2 ) -
		            ( ret_exp_1 + ret_erf_1 )   )


		# Calculate the expected current.

		ret = ( ( 1.e12 ) * ( 1. / 2. ) * ( const['q_p'] )
		        * ( 1.e6 * prm_n )
		        * ( 1.e-4 * self.spec.calc_eff_area( dlk, prm_v ) )		# Effective area now is a spec object
		        * ( ret_prn ) )


		# Return the calculated value for the expected current.

		return ret

