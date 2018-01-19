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


from math import sqrt
from datetime import datetime

from janus_const import const


################################################################################
## DEFINE THE LIST OF RESERVED NAMES.
################################################################################

PARAM = [ 'b0', 'v0', 'n', 'v', 'dv', 'v0', 'w', 'w2', 'r', 't', 'beta',
          'ac', 'time', 's','m','q', 'k', 'beta_par', 'beta_per'               ]

COMP = [ 'x', 'y', 'z', 'per', 'par', 'vec', 'mag', 'hat'  ]

SIGMA = [ 'sig', 'sigma' ]


################################################################################
## DEFINE THE "series" CLASS TO CONTAIN A SERIES OF "plas" OBJECTS.
################################################################################

class series( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self,
	              replace=True, sort=True ) :

		self.replace = bool( replace )
		self.sort    = bool( sort    )

		self.arr = [ ]

		self.n = 0

	#-----------------------------------------------------------------------
	# DEFINE THE LENGTH FUNCTION.
	#-----------------------------------------------------------------------

	def __len__( self ) :

		# Return the number of "plas" objects stored in this object's
		# array.

		return self.n

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION TO FIND A "plas" OBJECT BASED ON ITS TIMESTAMP.
	#-----------------------------------------------------------------------

	def fnd_spec( self, time ) :

		# If a "None" timestamp has been provided, abort.

		if ( time == None ) :
			return None

		# Locate all occurances of the target timestamp among the
		# timestamps in the array.

		ret = [ i for ( i, j ) in enumerate( self.arr )
		                                             if j.time == time ]

		# If at least one match has been found, return in; otherwise,
		# return "None".

		if ( len( ret ) > 0 ) :
			return ret[0]
		else :
			return None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ADDING A SPECTRUM TO THE SERIES.
	#-----------------------------------------------------------------------

	def add_spec( self, spec ) :

		# Insert the new spectrum into the array (replacing an old
		# spectrum, if that behavior has been requested and one is
		# found).

		if ( self.replace ) :
			ind = self.fnd_spec( spec.time )
		else :
			ind = None

		if ( ind == None ) :
			self.arr.append( spec )
			self.n += 1
		else :
			self.arr[ind] = spec

		# If requested, sort the array.

		if ( self.sort ) :
			self.arr.sort( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETURNING A KEY.
	#-----------------------------------------------------------------------

	def __getitem__( self, key ) :

		return [ s[key] for s in self.arr ]


################################################################################
## DEFINE THE "plas" CLASS TO MODEL THE IONS POPULATIONS OF A PLASMA.
################################################################################

class plas( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, time=None, enforce=False ) :

		self.time = time

		self.arr_spec = [ ]
		self.arr_pop  = [ ]

		self.covar = None

		self.v0_x = None
		self.v0_y = None
		self.v0_z = None

		self.sig_v0_x = None
		self.sig_v0_y = None
		self.sig_v0_z = None

		self.b0_x = None
		self.b0_y = None
		self.b0_z = None

		self.enforce = bool( enforce )

	#-----------------------------------------------------------------------
	# DEFINE THE COMPARISON FUNCTION.
	#-----------------------------------------------------------------------

	def __cmp__( self, other ) :

		if ( type( self ) != type( other ) ) :
			raise TypeError( 'Cannot compare dissimilar types.' )

		if ( self.time is None ) :
			if ( other.time is None ) :
				return 0
			else :
				return -1
		else :
			if ( other.time is None ) :
				return 1
			else :
				if   ( self.time <  other.time ) :
					return -1
				elif ( self.time == other.time ) :
					return  0
				else :
					return  1

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PARSING A KEY.
	#-----------------------------------------------------------------------

	def parse( self, key ) :

		# Initialize the onary of return variables.

		elem = { 'param':None,
		         'sigma':None,
		          'comp':None,
		          'spec':None,
		           'pop':None  }

		# Attempting to split the "key" string into substrings based on
		# the "_" token.  If this fails, abort.

		try :
#			arr=arr.lower()
			arr = key.split( '_' )
			for i in range(len(arr)):
				arr[i] = arr[i].lower()
		except :
			return None

		# For each element from the key, attempt to identify and record
		# what it represents.  If this fails for any given element or if
		# elements are in conflict, abort. The parameters, components
		# and sigma are all changed to lower case independent of the
		# type of case used for input.

		# Note.  Additional verification is required for "ret['pop']" at
		#        the end of this loop.  It's value cannot be confirmed
		#        to be a valid population until the species has been
		#        established (and the key need not have the species
		#        identifier precede that for the population).

		for e in arr :

			if ( e.lower() in PARAM ) :

				if ( elem['param'] is None ) :
					elem['param'] = e.lower()
				else :
					return None

			elif ( e.lower() in COMP ) :

				if ( elem['comp'] is None ) :
					elem['comp'] = e.lower()
				else :
					return None

			elif ( e.lower() in SIGMA ) :

				if ( elem['sigma'] is None ) :
					elem['sigma'] = e.lower()
				else :
					return None

			elif ( self.get_spec( e ) is not None ) :

				if ( elem['spec'] is None ) :
					elem['spec'] = e
				else :
					return None

			else :

				if ( elem['pop'] is None ) :
					elem['pop'] = e
				else :
					return None

		if ( elem['pop'] is not None ) :

			if ( elem['spec'] is None ) :
				return None

			if ( self.get_pop(
			                 elem['spec'], elem['pop'] ) is None ) :
				return None

		return elem

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETRIEVING THE VALUE OF A GIVEN KEY.
	#-----------------------------------------------------------------------

	def __getitem__( self, key ) :
		
		# Attempt to parse the key.  If this fails, abort.

		elem = self.parse( key )

		if ( elem is None ) :
			return None

		# If no parameter has been specified but a species (and possibly
		# a population) has, attempt to return the corresponding object;
		# otherwise, abort.

		if ( elem['param'] is None ) :

			if ( elem['spec'] is None ) :

				return None

			else :

				if ( elem['pop'] is None ) :
					return self.get_spec( elem['spec'] )
				else :
					return self.get_pop( elem['spec'],
					                     elem['pop']   )

		# If the specified parameter is one stored by the "plas" class,
		# attempt to return its value.  If the component is invalid for
		# the specified parameter, abort (returning "None").

		if   ( elem['param'] == 'time' ) :

			return self.time

		elif ( elem['param'] == 'b0' ) :

			if ( elem['sigma'] is None ) :

				if ( ( elem['comp'] is None  ) or
				     ( elem['comp'] == 'mag' )    ) :
					return self.get_b0_mag( )
				elif ( elem['comp'] == 'vec' ) :
					return self.get_b0_vec( )
				elif ( elem['comp'] == 'hat' ) :
					return self.get_b0_hat( )
				elif ( elem['comp'] == 'x' ) :
					return self.b0_x
				elif ( elem['comp'] == 'y' ) :
					return self.b0_y
				elif ( elem['comp'] == 'z' ) :
					return self.b0_z
				else :
					return None

			else :

				return None

		elif ( elem['param'] == 'v0' ) :

			if ( elem['sigma'] is None ) :

				if ( ( elem['comp'] is None  ) or
				     ( elem['comp'] == 'mag' )    ) :
					return self.get_v0_mag( )
				elif ( elem['comp'] == 'vec' ) :
					return self.get_v0_vec( )
				elif ( elem['comp'] == 'x' ) :
					return self.v0_x
				elif ( elem['comp'] == 'y' ) :
					return self.v0_y
				elif ( elem['comp'] == 'z' ) :
					return self.v0_z
				else :
					return None

			else :

				if   ( elem['comp'] == 'x' ) :
					return self.sig_v0_x
				elif ( elem['comp'] == 'y' ) :
					return self.sig_v0_y
				elif ( elem['comp'] == 'z' ) :
					return self.sig_v0_z
				else :
					return None

		# Note.  If this point is reached, the parameter is one to be
		#        handled by the species or population.

		# If no species has been specified, abort.

		if ( elem['spec'] is None ) :
			return None

		# Convert "elem" into a string of standard form for the "spec"
		# and "pop" classes.

		arg = elem['param']

		if ( elem['comp'] is not None ) :
			arg = arg + '_' + elem['comp']

		if ( elem['sigma'] is not None ) :
			arg = 'sig_' + arg

		# Pass the string to the either the "spec" or "pop" class for
		# processing.  If an error is raised, catch it and abort quietly
		# (i.e., return "None").

		if ( elem['pop'] is None ) :

			try :
				return self.get_spec( elem['spec'] )[arg]
			except :
				return None

		else :

			try :
				return self.get_pop(
				                elem['spec'], elem['pop'] )[arg]
			except :
				return None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ASSIGNING A GIVEN VALUE TO A GIVEN KEY.
	#-----------------------------------------------------------------------

	def __setitem__( self, key, value ) :

		# Based on the "key" in question, validate the "value".  If it
		# is valid, store the new value (and make any appropriate
		# changes to other parameters).
		# Change all keys to lower case independent of the input type
		# used.
		
		key=key.lower()

		if ( key == 'time' ) :

			if ( value is None ) :
				self.time = None
			elif ( type( value ) == datetime ) :
				self.time = value
			else :
				raise TypeError(
				     'Type "datetime" required for timestamp.' )

		elif ( key == 'v0_x' ) :

			self.v0_x = None

			if ( value is not None ) :
				self.v0_x = float( value )

		elif ( key == 'v0_y' ) :

			self.v0_y = None

			if ( value is not None ) :

				self.v0_y = float( value )

		elif ( key == 'v0_z' ) :

			self.v0_z = None

			if ( value is not None ) :

				self.v0_z = float( value )

		elif ( key == 'v0_vec' ) :

			try :
				l = len( value )
			except :
				l = 0

			if ( l != 3 ) :
				raise TypeError( 'Array of length 3 required.' )
			else :
				if ( value[0] is not None ) :
					self.v0_x = float( value[0] )
				if ( value[1] is not None ) :
					self.v0_y = float( value[1] )
				if ( value[2] is not None ) :
					self.v0_z = float( value[2] )

		elif ( key == 'sig_v0_x' ) :

			self.sig_v0_x = None

			if ( value is not None ) :

				self.sig_v0_x = float( value )

		elif ( key == 'sig_v0_y' ) :

			self.sig_v0_y = None

			if ( value is not None ) :

				self.sig_v0_y = float( value )

		elif ( key == 'sig_v0_z' ) :

			self.sig_v0_z = None

			if ( value is not None ) :

				self.sig_v0_z = float( value )

		elif   ( key == 'b0_x' ) :

			self.b0_x = None

			if ( value is not None ) :

				self.b0_x = float( value )

		elif ( key == 'b0_y' ) :

			self.b0_y = None

			if ( value is not None ) :

				self.b0_y = float( value )

		elif ( key == 'b0_z' ) :

			self.b0_z = None

			if ( value is not None ) :

				self.b0_z = float( value )

		elif ( key == 'b0_vec' ) :

			try :
				l = len( value )
			except :
				l = 0

			if ( l != 3 ) :
				raise TypeError( 'Array of length 3 required.' )
			else :
				if ( value[0] is not None ) :
					self.b0_x = float( value[0] )
				if ( value[1] is not None ) :
					self.b0_y = float( value[1] )
				if ( value[2] is not None ) :
					self.b0_z = float( value[2] )

		else :

			raise KeyError( 'Invalid key.' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GETTING THE MAGNITUDE OF THE MAGNETIC FIELD.
	#-----------------------------------------------------------------------

	def get_b0_mag( self ) :

		# If any of the components of the magnetic field are undefined,
		# abort (returning "None").

		if ( ( self.b0_x is None ) or ( self.b0_y is None ) or
		     ( self.b0_z is None )                             ) :

			return None

		# Calculate and return the magnitude.

		return sqrt( self.b0_x**2 + self.b0_y**2 + self.b0_z**2 )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GETTING THE VECTOR OF THE MAGNETIC FIELD.
	#-----------------------------------------------------------------------

	def get_b0_vec( self ) :

		# If any of the components of the magnetic field are undefined,
		# abort (returning "None").

		if ( ( self.b0_x is None ) or ( self.b0_y is None ) or
		     ( self.b0_z is None )                             ) :

			return None

		# Return the vector.

		return ( self.b0_x, self.b0_y, self.b0_z )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GETTING THE UNIT VECTOR OF THE MAGNETIC FIELD.
	#-----------------------------------------------------------------------

	def get_b0_hat( self ) :

		# If any of the components of the magnetic field are undefined,
		# abort (returning "None").

		if ( ( self.b0_x is None ) or ( self.b0_y is None ) or
		     ( self.b0_z is None )                             ) :

			return None

		# Return the unit vector.

		b0 =  sqrt( self.b0_x**2 + self.b0_y**2 + self.b0_z**2 )

		return ( self.b0_x / b0, self.b0_y / b0, self.b0_z / b0 )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GETTING THE MAGNITUDE OF THE VELOCITY.
	#-----------------------------------------------------------------------

	def get_v0_mag( self ) :

		# If any of the components of the velocity are undefined, abort
		# (returning "None").

		if ( ( self.v0_x is None ) or ( self.v0_y is None ) or
		     ( self.v0_z is None )                             ) :

			return None

		# Calculate and return the magnitude.

		return sqrt( self.v0_x**2 + self.v0_y**2 + self.v0_z**2 )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GETTING THE VECTOR OF THE VELOCITY.
	#-----------------------------------------------------------------------

	def get_v0_vec( self ) :

		# If any of the components of the velocity are undefined, abort
		# (returning "None").

		if ( ( self.v0_x is None ) or ( self.v0_y is None ) or
		     ( self.v0_z is None )                             ) :

			return None

		# Return the vector.

		return ( self.v0_x, self.v0_y, self.v0_z )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ADDING A NEW SPECIES.
	#-----------------------------------------------------------------------

	def add_spec( self,
	              name=None, sym=None,
	              m=None, q=None       ) :

		self.arr_spec.append(
		                    spec( self, name=name, sym=sym, m=m, q=q ) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ADDING A NEW POPULATION.
	#-----------------------------------------------------------------------

	def add_pop( self, spc,
	             drift=False, aniso=False,
	             name=None, sym=None, n=None, dv=None,
	             w=None, w_per=None, w_par=None,
	             sig_n=None, sig_dv=None, sig_w=None,
	             sig_w_per=None, sig_w_par=None       ) :

		self.arr_pop.append( pop( self,
		                          self.get_spec( spc ),
		                          drift=drift, aniso=aniso,
		                          name=name, sym=sym,
		                          n=n, dv=dv, w=w,
		                          w_per=w_per, w_par=w_par,
		                          sig_n=sig_n, sig_dv=sig_dv, sig_w=sig_w,
		                          sig_w_per=sig_w_per, sig_w_par=sig_w_par ) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETREIVING A SPECIES.
	#-----------------------------------------------------------------------

	def get_spec( self, key ) :

		if ( key is None ) :
			return None

		for s in self.arr_spec :

			if ( ( s['name'] == key ) or
			     ( s['sym']  == key )    ) :

				return s

		return None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETREIVING A POPULATION.
	#-----------------------------------------------------------------------

	def get_pop( self, s_key, p_key ) :

		# Attempt to retrieve the species.  If this fails, abort.

		s = self.get_spec( s_key )

		if ( s is None ) :

			return None

		# Attempt to retrieve the requested population of this species
		# and return it to the user.

		for p in self.arr_pop :

			if ( ( p['spec'] == s            ) and
			     ( ( p['name'] == p_key ) or
			       ( p['sym']  == p_key )    )     ) :

				return p

		return None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETREIVING A LIST OF POPULATIONS.
	#-----------------------------------------------------------------------

	def lst_pop( self, key ) :

		lst = [ ]

		if ( key is None ) :

			return

		for p in self.arr_pop :

			if ( ( p['spec'] == key ) or
			     ( p['name'] == key ) or
			     ( p['sym']  == key )    ) :

				lst.append( p )

		return lst

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR REMOVING A SPECIES.
	#-----------------------------------------------------------------------

	def del_spec( self, key ) :



		# WARNING!

		# TODO: Special handling of populations that still reference
		#       this species.





		# Attempt to retrieve the species.  If this fails, abort.

		s = self.get_spec( key )

		if ( s is None ) :
			return

		# Identify the index of the species in the array of species.

		i = self.arr_spec.index( s )

		# Delete the requested species.

		del self.arr_spec[i]

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR REMOVING A POPULATION.
	#-----------------------------------------------------------------------

	def del_pop( self, key ) :

		# Attempt to retrieve the population.  If this fails, abort.

		p = self.get_pop( key )

		if ( p is None ) :
			return

		# Identify the index of the population in the array of
		# populations.

		i = self.arr_pop.index( p )

		# Delete the requested population.

		del self.arr_pop[i]


################################################################################
## DEFINE THE "spec" CLASS TO MODEL A SPECIES.
################################################################################

class spec( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, my_plas,
	              name=None, sym=None,
	              m=None, q=None       ) :

		self.my_plas = my_plas

		self.name  = None
		self.sym   = None
		self.m     = None
		self.q     = None

		self.__setitem__( "name", name )
		self.__setitem__( "sym" , sym  )
		self.__setitem__( "m"   , m    )
		self.__setitem__( "q"   , q    )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETRIEVING THE VALUE OF A GIVEN KEY.
	#-----------------------------------------------------------------------

	def __getitem__( self, key ) :

		key=key.lower()

		# Return the appropriate value for the provided "key".

		if ( key == 'plas' ) :

			return self.my_plas

		elif ( key == 'name' ) :

			return self.name

		elif ( key == 'sym' ) :

			return self.sym

		elif ( key == 'm' ) :

			return self.m

		elif ( key == 'q' ) :

			return self.q

		elif ( key == 'n' ) :

			arr_pop = self.my_plas.lst_pop( self )

			if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
				return None

			arr_n = [ p['n'] for p in arr_pop ]

			if ( None in arr_n ) :
				return None

			return sum( arr_n )

		elif ( ( key == 'dv' ) or ( key == 'dv_mag' )
		                       or ( key == 'dv_par' ) ) :

			arr_pop = self.my_plas.lst_pop( self )

			if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
				return None

			arr_n  = [ p['n' ] for p in arr_pop ]
			arr_dv = [ p['dv'] for p in arr_pop ]

			if ( ( None in arr_n ) or ( None in arr_dv ) ) :
				return None

			ret = 0.

			for ( p, obj ) in enumerate( arr_pop ) :
				ret += arr_n[p] * arr_dv[p]

			return ret / sum( arr_n )

		elif ( key == 'dv_vec' ) :

			dv_mag = self['dv']

			if   ( dv_mag is None ) :
				return None
			elif ( dv_mag == 0. ) :
				return ( 0., 0., 0. )

			b0_hat = self.my_plas.get_b0_hat( )

			if ( b0_hat is None ) :
				return None

			return ( dv_mag * b0_hat[0],
			         dv_mag * b0_hat[1],
			         dv_mag * b0_hat[2]  )

		elif ( key == 'v_vec' ) :

			dv_vec = self['dv_vec']

			if ( dv_vec is None ) :
				return None

			v0_vec = self.my_plas.get_v0_vec( )

			if ( v0_vec is None ) :
				return None

			return ( dv_vec[0] + v0_vec[0],
			         dv_vec[1] + v0_vec[1],
			         dv_vec[2] + v0_vec[2]  )

		elif ( ( key == 'v' ) or ( key == 'v_mag' ) ) :

			v_vec = self['v_vec']

			if ( v_vec is None ) :
				return None

			return sqrt( v_vec[0]**2 + v_vec[1]**2 + v_vec[2]**2 )

		elif ( key == 'w2_per' ) :

			arr_pop = self.my_plas.lst_pop( self )

			if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
				return None

			arr_n      = [ p['n'     ] for p in arr_pop ]
			arr_w2_per = [ p['w2_per'] for p in arr_pop ]

			if ( ( None in arr_n ) or ( None in arr_w2_per ) ) :
				return None

			ret = 0.

			for ( p, obj ) in enumerate( arr_pop ) :
				ret += arr_n[p] * arr_w2_per[p]

			return ret / sum( arr_n )

		elif ( key == 'w2_par' ) :

			arr_pop = self.my_plas.lst_pop( self )

			if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
				return None

			arr_n      = [ p['n'     ] for p in arr_pop ]
			arr_dv     = [ p['dv'    ] for p in arr_pop ]
			arr_w2_par = [ p['w2_par'] for p in arr_pop ]

			if ( ( None in arr_n ) or ( None in arr_dv     )
			                       or ( None in arr_w2_par ) ) :
				return None

			dv = self['dv']

			if ( dv is None ) :
				return None

			ret = 0.

			for ( p, obj ) in enumerate( arr_pop ) :
				ret += arr_n[p] * (
				                  arr_dv[p]**2 + arr_w2_par[p] )

			return ( ( ret / sum( arr_n ) ) - dv**2 )

		elif ( key == 'w2' ) :

			w2_per = self['w2_per']
			w2_par = self['w2_par']

			if ( ( w2_per is None ) or ( w2_par is None ) ) :
				return None

			return ( 2. * w2_per + w2_par ) / 3.

		elif ( key == 'w_per' ) :

			w2_per = self['w2_per']

			if ( w2_per is None ) :
				return None

			return sqrt( w2_per )

		elif ( key == 'w_par' ) :

			w2_par = self['w2_par']

			if ( w2_par is None ) :
				return None

			return sqrt( w2_par )

		elif ( key == 'w' ) :

			w2 = self['w2']

			if ( w2 is None ) :
				return None

			return sqrt( w2 )

		elif ( key == 'w3' ) :

			w = self['w']

			if ( w is None ) :
				return None

			return  w**3

		elif ( key == 'w4' ) :

			w = self['w']

			if ( w is None ) :
				return None

			return  w**4

		elif ( key == 'r' ) :

			w2_per = self['w2_per']
			w2_par = self['w2_par']

			if ( ( w2_per is None ) or ( w2_par is None ) ) :
				return None

			return w2_per / w2_par

		elif ( key == 't_per' ) :

			if ( self.m is None ) :
				return None

			w2_per = self['w2_per']

			if ( w2_per is None ) :
				return None

			return ( 1.E-3 / const['k_b'] ) * \
			       self.m * const['m_p'] * ( 1.E6 * w2_per )

		elif ( key == 't_par' ) :

			if ( self.m is None ) :
				return None

			w2_par = self['w2_par']

			if ( w2_par is None ) :
				return None

			return ( 1.E-3 / const['k_b'] ) * \
			       self.m * const['m_p'] * ( 1.E6 * w2_par )

		elif ( key == 't' ) :

			if ( self.m is None ) :
				return None

			w2 = self['w2']

			if ( w2 is None ) :
				return None

			return ( 1.E-3 / const['k_b'] ) * \
			       self.m * const['m_p'] * ( 1.E6 * w2 )

                elif ( key == 'w3_par' ) :

			w_par = self['w_par']

			if ( w_par is None ) :
				return None

			return  w_par**3

 
                elif ( key == 'w4_par' ) :

			w2_par = self['w2_par']

			if ( w2_par is None ) :
				return None

			return  w2_par**2

		elif ( key == 'beta_par' ) :
		
#		        arr_pop = self.my_plas.lst_pop( self )
#		
#		        if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
#		                return None
		
		        b0 = self.my_plas.get_b0_mag( )
		
		        n       = self['n']
		        t_par   = self['t_par']
		        
#		        arr_n      = [ p['n'] for p in arr_pop ]

			if ( t_par is None ) :
				return None

#		        for ( p, obj ) in enumerate( arr_pop ) : 
	                ret = ( n * 1.E6 ) * const['k_b'] * ( t_par * 1.E3 )
	                ret /= ( b0 / 1.E9 )**2 / ( 2. * const['mu_0'] )
		
		        return  ret

                elif ( key == 'beta_per' ) :

#                        arr_pop = self.my_plas.lst_pop( self )
#
#                        if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
#                                return None

                        b0 = self.my_plas.get_b0_mag( )

                        n       = self['n']
                        t_par   = self['t_per']
                        
#                        arr_n      = [ p['n'] for p in arr_pop ]

#                        for ( p, obj ) in enumerate( arr_pop ) : 
                        ret = ( n * 1.E6 ) * const['k_b'] * ( t_per * 1.E3 )
                        ret /= ( b0 / 1.E9 )**2 / ( 2. * const['mu_0'] )

			return  ret

                elif ( key == 's' ) :

			arr_pop = self.my_plas.lst_pop( self )

			if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
				return None

			if ( len( arr_pop ) == 1 ) :
				return 0.

			n       = self['n']
                        w_par   = self['w_par']
                        w2_par  = self['w2_par']
                        w3_par  = self['w3_par']
                        dv      = self['dv']
                        w3      = self['w3']

			arr_n      = [ p['n'     ] for p in arr_pop ]
			arr_dv     = [ p['dv'    ] for p in arr_pop ]
			arr_w2_par = [ p['w2_par'] for p in arr_pop ]

                        if ( ( None in arr_n      ) or
			     ( None in arr_dv     ) or
			     ( None in arr_w2_par )    ) :
				return None

                        ret = 0.

                        for ( p, obj ) in enumerate( arr_pop ) :
                                ret += ( arr_n[p] * arr_dv[p]**3 )
				ret += ( 3 * arr_n[p]
                                           * arr_dv[p] * arr_w2_par[p] )

                        return ( ( ret / ( n * w3 ) )
			           - ( ( dv**3  ) / w3 )
			           - ( ( 3 * dv*w2_par) / w3 ) )

                elif ( key == 'k' ) :

			arr_pop = self.my_plas.lst_pop( self )

			if ( ( arr_pop is None ) or ( len( arr_pop ) == 0 ) ) :
				return None

			if ( len( arr_pop ) == 1 ) :
				return 0.

			n       = self['n']
                        w_par   = self['w_par']
                        w2_par  = self['w2_par']
                        w4_par  = self['w4_par']
                        dv      = self['dv']
                        w4      = self['w4']

			arr_n      = [ p['n'     ] for p in arr_pop ]
			arr_dv     = [ p['dv'    ] for p in arr_pop ]
			arr_w2_par = [ p['w2_par'] for p in arr_pop ]
			arr_w4_par = [ p['w4_par'] for p in arr_pop ]

                        if ( ( None in arr_n      ) or
			     ( None in arr_dv     ) or
			     ( None in arr_w2_par )    ) :
				return None

                        ret = 0.

                        for ( p, obj ) in enumerate( arr_pop ) :
                                ret +=  arr_n[p] * ( arr_dv[p]**4 )
                                ret -= ( 4 * arr_n[p] 
                                            * dv * arr_dv[p]**3 )
				ret +=  ( 6 * arr_n[p]
                                            * arr_w2_par[p] * ( arr_dv[p]**2 ) )
				ret -= (12 * arr_n[p]
                                            * dv * arr_w2_par[p] * arr_dv[p] )
                                ret +=  ( 3 * arr_n[p] * arr_w4_par[p] )

                        return ( ( ret / ( n * w4 )               )
                                   + 6 * ( ( ( dv*w_par )**2/w4 ) )
                                   + 3 * (  dv**4/w4    )         )

		else :

			raise KeyError( 'Invalid key.' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ASSIGNING A GIVEN VALUE TO A GIVEN KEY.
	#-----------------------------------------------------------------------

	def __setitem__( self, key, value ) :

		key=key.lower()

		# Based on the "key" in question, validate the "value".  If it
		# is valid, store the new value (and make any appropriate
		# changes to other parameters).

		if ( key == 'plas' ) :

			raise KeyError(
			       'Invalid key: species ownership cannot change.' )

		elif ( key == 'name' ) :

			if ( value is None ) :

				self.name = None

			else :

				value = str( value )

				if ( value == '' ) :

					self.name = None

				elif ( value.find( '_' ) >= 0 ) :

					self.name = None

					ValueError(
					    'Name cannot contain underscores.' )

				elif ( ( value.lower( ) in PARAM ) or
				       ( value.lower( ) in COMP  ) or
				       ( value.lower( ) in SIGMA )    ) :

					self.name = None

					raise ValueError(
					    'Name cannot be a reserved value.' )

				elif ( ( self.name == value ) or
				       ( self.sym  == value )    ) :

					self.name = value

				elif ( ( self.my_plas.get_spec( value )
			                                    is not None ) or
				       ( len( self.my_plas.lst_pop(
				                          value ) ) > 0 )    ) :

					self.name = None

					raise ValueError( 'Name in use.' )

				else :

					self.name = value

		elif ( key == 'sym' ) :

			if ( value is None ) :

				self.sym = None

			else :

				value = str( value )

				if ( value == '' ) :

					self.sym = None

				elif ( value.find( '_' ) >= 0 ) :

					self.sym = None

					ValueError(
					  'Symbol cannot contain underscores.' )

				elif ( value.find( ' ' ) >= 0 ) :

					self.sym = None

					ValueError(
					       'Symbol cannot contain spaces.' )

				elif ( ( value.lower( ) in PARAM ) or
				       ( value.lower( ) in COMP  ) or
				       ( value.lower( ) in SIGMA )    ) :

					self.name = None

					raise ValueError(
					    'Name cannot be a reserved value.' )


				elif ( ( self.name == value ) or
				       ( self.sym  == value )    ) :

					self.sym = value

				elif ( ( self.my_plas.get_spec( value )
			                                    is not None ) or
				       ( len( self.my_plas.lst_pop(
				                          value ) ) > 0 )    ) :

					self.sym = None

					raise ValueError( 'Symbol in use.' )

				else :

					self.sym = value

		elif ( key == 'm' ) :

			if ( value is None ) :

				self.m = None

			else :

				value = float( value )

				if ( value <= 0 ) :

					self.m = None

					raise ValueError(
					              'Mass must be positive.' )

				else :

					self.m = value

		elif ( key == 'q' ) :

			if ( value is None ) :

				self.q = None

			else :

				value = float( value )

				if ( value <= 0 ) :

					self.q = None

					raise ValueError(
					            'Charge must be positive.' )

				else :

					self.q = value

		else :

			raise KeyError( 'Invalid key.' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ASSESSING THE EXISTANCE OF PARAMETERS VALUES.
	#-----------------------------------------------------------------------

	# Note.  This function does not make checks on the parameter values
	#        themselves -- only on whether they are not "None".  It is the
	#        responsibility of the "__setitem__" function to reject any
	#        invalid value that is provided for that parameter (instead
	#        setting the parameter to "None" and erroring).

	def valid( self ) :

		if ( ( self.name is None ) or
		     ( self.sym  is None ) or
		     ( self.m    is None ) or
		     ( self.q    is None )    ) :

			return False

		else :

			return True


################################################################################
## DEFINE THE "pop" CLASS TO MODEL A POPULATION OF A SPECIES.
################################################################################

class pop( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, my_plas, my_spec,
	              drift=False, aniso=False,
	              name=None, sym=None,
	              n=None, dv=None, w=None,
	              w_per=None, w_par=None,
	              sig_n=None, sig_dv=None, sig_w=None,
	              sig_w_per=None, sig_w_par=None       ) :

		self.my_plas = my_plas
		self.my_spec = my_spec
		self.drift   = bool( drift )
		self.aniso   = bool( aniso )

		self.name      = None
		self.sym       = None
		self.n         = None
		self.dv        = None
		self.w         = None
		self.w_per     = None
		self.w_par     = None
		self.sig_n     = None
		self.sig_dv    = None
		self.sig_w     = None
		self.sig_w_per = None
		self.sig_w_par = None

		if ( name is not None ) :
			self['name'] = name
		if ( sym is not None ) :
			self['sym'] = sym
		if ( n is not None ) :
			self['n'] = n
		if ( dv is not None ) :
			self['dv'] = dv
		if ( w is not None ) :
			self['w'] = w
		if ( w_per is not None ) :
			self['w_per'] = w_per
		if ( w_par is not None ) :
			self['w_par'] = w_par
		if ( sig_n is not None ) :
			self['sig_n'] = sig_n
		if ( sig_dv is not None ) :
			self['sig_dv'] = sig_dv
		if ( sig_w is not None ) :
			self['sig_w'] = sig_w
		if ( sig_w_per is not None ) :
			self['sig_w_per'] = sig_w_per
		if ( sig_w_par is not None ) :
			self['sig_w_par'] = sig_w_par

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETRIEVING THE VALUE OF A GIVEN KEY.
	#-----------------------------------------------------------------------

	def __getitem__( self, key ) :

		key=key.lower()	
		# Return the appropriate value for the provided "key".

		if   ( key == 'plas' ) :

			return self.my_plas

		elif ( key == 'spec' ) :

			return self.my_spec

		elif ( key == 'm' ) :

			return self.my_spec['m']

		elif ( key == 'q' ) :

			return self.my_spec['q']

		elif ( key == 'name' ) :

			return self.name

		elif ( key == 'sym' ) :

			return self.sym

		elif ( key == 'drift' ) :

			return self.drift

		elif ( key == 'aniso' ) :

			return self.aniso

		elif ( key == 'name_sym' ) :

			str_name = '' if ( self.name is None ) else self.name
			str_sym  = '' if ( self.sym  is None ) else self.sym

			ret = str_name

			if ( len( str_name ) > 0 ) :
				ret += ' '

			ret += '(' + str_sym + ')'

			return ret

		elif ( key == 'full_name' ) :

			if ( self.name is None ) :
				str_pop_name = ''
			else :
				str_pop_name = self.name

			if ( ( self.my_spec is None         ) or
			     ( self.my_spec['name'] is None )    ) :
				str_spec_name = ''
			else :
				str_spec_name = self.my_spec['name']

			if ( ( len( str_pop_name  ) > 0 ) and
			     ( len( str_spec_name ) > 0 )     ) :
				return str_spec_name + ' ' + str_pop_name
			else :
				return str_spec_name + str_pop_name

		elif ( key == 'full_name_sym' ) :

			if ( self.sym is None ) :
				str_pop_sym = ''
			else :
				str_pop_sym = self.sym

			if ( ( self.my_spec is None        ) or
			     ( self.my_spec['sym'] is None )    ) :
				str_spec_sym = ''
			else :
				str_spec_sym = self.my_spec['sym']

			ret = self['full_name']

			if ( len( ret ) > 0 ) :
				ret += ' '

			if ( ( len( str_spec_sym ) == 0 ) and
			     ( len( str_pop_sym  ) == 0 )     ) :
				return ret

			return ( ret + '(' + str_spec_sym + '_'
			                   + str_pop_sym  + ')' )

		elif ( key == 'n' ) :

			return self.n

		elif ( ( key == 'dv' ) or ( key == 'dv_mag' )
		                       or ( key == 'dv_per' ) ) :

			if ( self.drift ) :
				return self.dv
			else :
				return 0.

		elif ( key == 'dv_vec' ) :

			if ( not self.drift ) :
				return ( 0., 0., 0. )

			if ( self.dv is None ) :
				return None

			b0_hat = self.my_plas.get_b0_hat( )

			if ( b0_hat is None ) :
				return None

			return ( b0_hat[0] * self.dv,
			         b0_hat[1] * self.dv,
			         b0_hat[2] * self.dv  )

		elif ( key == 'v_vec' ) :

			dv_vec = self['dv_vec']
			v0_vec = self.my_plas.get_v0_vec( )

			if ( ( dv_vec is None ) or ( v0_vec is None ) ) :
				return None

			return ( v0_vec[0] + dv_vec[0],
			         v0_vec[1] + dv_vec[1],
			         v0_vec[2] + dv_vec[2]  )

		elif ( ( key == 'v' ) or ( key == 'v_mag' ) ) :

			v_vec = self['v_vec']

			if ( v_vec is None ) :
				return None

			return sqrt( v_vec[0]**2 + v_vec[1]**2 + v_vec[2]**2 )

		elif ( key == 'w' ) :

			if ( self.aniso ) :

				if ( ( self.w_per is None ) or
				     ( self.w_par is None )    ) :

					return None

				else :

					return sqrt( ( 2. * self.w_per**2
					                + self.w_par**2 ) / 3. )

			else :

				return self.w

		elif ( key == 'w_per' ) :

			if ( self.aniso ) :
				return self.w_per
			else :
				return self.w

		elif ( key == 'w_par' ) :

			if ( self.aniso ) :
				return self.w_par
			else :
				return self.w

		elif ( key == 'w2' ) :

			w = self['w']

			if ( w is None ):
				return None
			else :
				return w**2

		elif ( key == 'w2_per' ) :

			w_per = self['w_per']

			if ( w_per is None ):
				return None
			else :
				return w_per**2

		elif ( key == 'w2_par' ) :

			w_par = self['w_par']

			if ( w_par is None ):
				return None
			else :
				return w_par**2

		elif ( key == 'w4' ) :

			w = self['w']

			if ( w is None ):
				return None
			else :
				return w**4

		elif ( key == 'w4_per' ) :

			w_per = self['w_per']

			if ( w_per is None ):
				return None
			else :
				return w_per**4

		elif ( key == 'w4_par' ) :

			w_par = self['w_par']

			if ( w_par is None ):
				return None
			else :
				return w_par**4

		elif ( key == 'r' ) :

			if ( self.aniso ) :
				if ( ( self.w_per is None ) or
				     ( self.w_par is None )    ) :
					return None
				else :
					return ( self.w_per / self.w_par )**2
			else :
				return 1.

		elif ( key == 't' ) :

			w = self['w']
			m = self['m']

			if ( ( w is None ) or ( m is None ) ) :
				return None
			else :
				return ( 1.E-3 / const['k_b'] ) * \
				       m * const['m_p'] * ( 1.E6 * w**2 )

		elif ( key == 't_per' ) :

			w_per = self['w_per']
			m     = self['m'    ]

			if ( ( w_per is None ) or ( m is None ) ) :
				return None
			else :
				return ( 1.E-3 / const['k_b'] ) * \
				       m * const['m_p'] * ( 1.E6 * w_per**2 )

		elif ( key == 't_par' ) :

			w_par = self['w_par']
			m     = self['m'    ]

			if ( ( w_par is None ) or ( m is None ) ) :
				return None
			else :
				return ( 1.E-3 / const['k_b'] ) * \
				       m * const['m_p'] * ( 1.E6 * w_par**2 )

		elif ( key == 'sig_n' ) :

			return self.sig_n

		elif ( key == 'sig_dv' ) :

			if ( self.drift ) :
				return self.sig_dv
			else :
				return None

		elif ( key == 'sig_w' ) :

			if ( self.aniso ) :
				return None
			else :
				return self.sig_w

		elif ( key == 'sig_w_per' ) :

			if ( self.aniso ) :
				return self.sig_w_per
			else :
				return None

		elif ( key == 'sig_w_par' ) :

			if ( self.aniso ) :
				return self.sig_w_par
			else :
				return None

                elif ( key == 'beta_par' ) :

			b0 = self.my_plas.get_b0_mag( )

			n       = self['n']
			t_par   = self['t_par']

			ret = ( n * 1.E6 ) * const['k_b'] * ( t_par * 1.E3 )
			ret /= ( b0 / 1.E9 )**2 / ( 2. * const['mu_0'] )
			
			return  ret

                elif ( key == 'beta_per' ) :

			b0 = self.my_plas.get_b0_mag( )

			n       = self['n']
			t_per   = self['t_per']

			ret = ( n * 1.E6 ) * const['k_b'] * ( t_per * 1.E3 )
			ret /= ( b0 / 1.E9 )**2 / ( 2. * const['mu_0'] )
			
			return  ret

                elif ( key == 's' ) :

                        return 0.

                elif ( key == 'k' ) :

                        return 3.


		else :

			raise KeyError( 'Invalid key.' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ASSIGNING A GIVEN VALUE TO A GIVEN KEY.
	#-----------------------------------------------------------------------

	def __setitem__( self, key, value ) :


		# Based on the "key" in question, validate the "value".  If it
		# is valid, store the new value (and make any appropriate
		# changes to other parameters).
		# Change all keys to lower case independent of the input type
		# used.
		
		key=key.lower()
		
		if ( key == 'plas' ) :

			raise KeyError(
			       'Invalid key: species ownership cannot change.' )

		elif ( key == 'spec' ) :

			if ( ( value is not None             ) and
			     ( value.my_plas != self.my_plas )     ) :

				self.my_spec = None

				raise ValueError(
				'Species and population must share ownership.' )

			else :

				self.my_spec = value

			val_err = False

			tmp_name = self.name
			tmp_sym  = self.sym

			self.name = None
			self.sym  = None

			try :
				self['name'] = tmp_name
			except :
				self.name = None
				val_err   = True

			try :
				self['sym'] = tmp_sym
			except :
				self.sym = None
				val_err  = True

			if ( val_err ) :
				raise ValueError( 'Name/symbol in use.' )

		elif ( key == 'drift' ) :

			value = bool( value )

			if ( self.drift == value ) :
				return

			self.drift = value

			self.dv = 0. if ( self.drift ) else None

		elif ( key == 'aniso' ) :

			value = bool( value )

			if ( self.aniso == value ) :
				return

			if ( self.aniso ) :

				self.w = self['w']

				self.w_per = None
				self.w_par = None

				self.aniso = False

			else :

				self.w_per = self.w
				self.w_par = self.w

				self.w = None

				self.aniso = True

		elif ( key == 'name' ) :

			if ( value is None ) :

				self.name = None

			else :

				value = str( value )

				if ( value == '' ) :

					self.name = None

				elif ( value.find( '_' ) >= 0 ) :

					self.name = None

					ValueError(
					    'Name cannot contain underscores.' )

				elif ( ( self.name == value ) or
				       ( self.sym  == value )    ) :

					self.name = value

				elif ( ( self.my_plas.get_spec( value )
			                                    is not None ) or
				       ( self.my_plas.get_pop(
				           self.my_spec['sym'], value )
				                            is not None )    ) :

					self.name = None

					raise ValueError( 'Name in use.' )

				else :

					self.name = value

		elif ( key == 'sym' ) :

			if ( value is None ) :

				self.sym = None

			else :

				value = str( value )

				if ( value == '' ) :

					self.sym = None

				elif ( value.find( '_' ) >= 0 ) :

					self.sym = None

					ValueError(
					  'Symbol cannot contain underscores.' )

				elif ( value.find( ' ' ) >= 0 ) :

					self.sym = None

					ValueError(
					       'Symbol cannot contain spaces.' )

				elif ( ( self.name == value ) or
				       ( self.sym  == value )    ) :

					self.sym = value

				elif ( ( self.my_plas.get_spec( value )
			                                    is not None ) or
				       ( self.my_plas.get_pop(
				           self.my_spec['sym'], value )
				                            is not None )    ) :

					self.sym = None

					raise ValueError( 'Symbol in use.' )

				else :

					self.sym = value

		elif ( key == 'n' ) :

			if ( value is None ) :

				self.n = None

				return

			value = float( value )

			if ( ( self.my_plas.enforce ) and
			     ( value <= 0           )     ) :

				self.n = None

				raise ValueError(
				            'Density enforced to be positive.' )

				return

			self.n = value

		elif ( key == 'dv' ) :

			if ( value is None ) :

				self.dv = None

				return

			if ( not self.drift ) :

				raise KeyError( 'Population has no drift.' )

				return

			self.dv = float( value )

		elif ( key == 'w' ) :

			if ( value is None ) :

				self.w = None

				return

			if ( self.aniso ) :

				if ( ( hasattr( value, '__len__' ) ) and
				     ( len( value ) == 2     )     ) :

					self['w_per'] = value[0]
					self['w_par'] = value[1]

				else :

					raise KeyError(
					          'Population is anisotropic.' )

			else :

				if ( hasattr( value, '__len__' ) ) :

					raise KeyError(
					            'Population is isotropic.' )

				else :

					value = float( value )

					if ( ( self.my_plas.enforce ) and
					     ( value <= 0           )     ) :

						self.w = None

						raise ValueError(
						      'Thermal speed enforced to be positive.' )

					else :

						self.w = value

		elif ( key == 'w_per' ) :

			if ( value is None ) :

				self.w_per = None

				return

			if ( not self.aniso ) :

				raise KeyError(
				              'Population is not anisotropic.' )

				return

			value = float( value )

			if ( ( self.my_plas.enforce ) and
			     ( value <= 0           )     ) :

				self.w_per = None

				raise ValueError(
				      'Thermal speed enforced to be positive.' )

				return

			self.w_per = value

		elif ( key == 'w_par' ) :

			if ( value is None ) :

				self.w_par = None

				return

			if ( not self.aniso ) :

				raise KeyError(
				              'Population is not anisotropic.' )

				return

			value = float( value )

			if ( ( self.my_plas.enforce ) and
			     ( value <= 0           )     ) :

				self.w_par = None

				raise ValueError(
				      'Thermal speed enforced to be positive.' )

				return

			self.w_par = value

		elif ( key == 'sig_n' ) :

			if ( value is None ) :
				self.sig_n = None
			else :
				self.sig_n = float( value )

		elif ( key == 'sig_dv' ) :

			if ( value is None ) :

				self.sig_dv = None

				return

			if ( not self.drift ) :

				raise KeyError( 'Population has no drift.' )

				return

			self.sig_dv = float( value )

		elif ( key == 'sig_w' ) :

			if ( value is None ) :

				self.sig_w = None

				return

			if ( self.aniso ) :

				raise KeyError( 'Population is anisotropic.' )

				return

			self.sig_w = float( value )

		elif ( key == 'sig_w_per' ) :

			if ( value is None ) :

				self.sig_w_per = None

				return

			if ( not self.aniso ) :

				raise KeyError(
				              'Population is not anisotropic.' )

				return

			self.sig_w_per = float( value )

		elif ( key == 'sig_w_par' ) :

			if ( value is None ) :

				self.sig_w_par = None

				return

			if ( not self.aniso ) :

				raise KeyError(
				              'Population is not anisotropic.' )

				return

			self.sig_w_par = float( value )

		else :

			raise KeyError( 'Invalid key.' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ASSESSING THE EXISTANCE OF PARAMETERS VALUES.
	#-----------------------------------------------------------------------

	# Note.  This function does not make checks on the parameter values
	#        themselves -- only on whether they are not "None".  It is the
	#        responsibility of the "__setitem__" function to reject any
	#        invalid value that is provided for that parameter (instead
	#        setting the parameter to "None" and erroring).

	def valid( self, require_val=True ) :

		# If any of the most basic parameters have not be specified,
		# return "False".

		if ( ( self.my_plas is None ) or
		     ( self.my_spec is None ) or
		     ( self.name    is None ) or
		     ( self.sym     is None )    ) :

			return False

		if ( not self.my_spec.valid( ) ) :

			return False

		# If the use has only requested a minimal validity check, return
		# "True" (since, if this point has been reached, the minimal
		# requirements have been satisfied.

		if ( not require_val ) :

			return True

		# If any of the bulk-parameter values are missing, return
		# "False".

		if ( self.n is None ) :

			return False

		if ( ( self.drift      ) and
		     ( self.dv is None )     ) :

			return False

		if ( self.aniso ) : 

			if ( ( self.w_per is None ) or
			     ( self.w_par is None )    ) :

				return False

		else :

			if ( self.w is None ) :

				return False

		# Return "True".

		return True
