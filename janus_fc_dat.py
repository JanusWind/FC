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

		self._the = 90 - self._elev
		self._phi =    - self._azim
		self._dir_x =  sin( deg2rad( self._the ) ) * cos( deg2rad( self._phi ) )
		self._dir_y =  sin( deg2rad( self._the ) ) * sin( deg2rad( self._phi ) )
		self._dir_z =  cos( deg2rad( self._the ) )
		
		ndir = calc_vec_norm( self['dir'] )
		self._ndir_x = ndir[0]
		self._ndir_y = ndir[1]
		self._ndir_z = ndir[2]

		self._nb_x = None
		self._nb_y = None
		self._nb_z = None

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
			return (self._dir_x, self._dir_y, self._dir_z )
		elif ( key == 'ndir_x' ) :
			return self._ndir_x
		elif ( key == 'ndir_y' ) :
			return self._ndir_y
		elif ( key == 'ndir_z' ) :
			return self._ndir_z
		elif ( key == 'ndir' ) :
			return (self._ndir_x, self._ndir_y, self._ndir_z )
		else :
			raise KeyError( 'Invalid key for "fc_dat ".' )


	def __setitem__( self, key, val ) :

		raise KeyError( 'Reassignment not permitted after initialization.' )


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

		psi = acos( calc_vec_dot( self['ndir'], nvn ) )*pi/180.
		if ( psi > 90. ) :
			return 0. 
 		
		# Return the effective collecting area corresponding to "psi".

		return interp( psi, self._spec._eff_deg, self._spec._eff_area )
