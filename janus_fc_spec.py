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

from janus_fc_dat import fc_dat
from datetime import timedelta
from scipy.interpolate import interp1d

################################################################################
## DEFINE THE "fc_spec" CLASS.
################################################################################

class fc_spec( ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, n_bin,
	              elev=None, azim=None, volt_cen=None, volt_del=None,
	              time=None, curr=None, rot=3., curr_jump=100.,
	              curr_min=1.                                            ) :

		self._n_cup     = 2
		self._n_dir     = 20
		self._n_bin     = n_bin
		self._time      = time
		self._curr_jump = curr_jump
		self._curr_min  = curr_min

		if ( elev == None ) :
			elev = [ None for c in range( self._n_cup ) ]

		if ( azim == None ) :
			azim = [ [ None for d in range( self._n_dir ) ]
			                for c in range( self._n_cup ) ]

		if ( volt_cen == None ) :
			volt_cen = [ [ None for b in range( self._n_bin ) ]
			                    for c in range( self._n_cup ) ]

		if ( volt_del == None ) :
			volt_del = [ [ None for b in range( self._n_bin ) ]
			                    for c in range( self._n_cup ) ]

		if ( curr == None ) :
			curr = [ [ [ None for b in range( self._n_bin ) ]
			                  for d in range( self._n_dir ) ]
			                  for c in range( self._n_cup ) ]

		#if ( len( elev ) != self._n_cup ) :
		#	raise TypeError( 'List elev must be length n_cup.' )

		self.arr = [ [ [ fc_dat( spec=self,
		                       elev=elev[c],
		                       azim=azim[c][d],
		                       volt_cen=volt_cen[c][b],
		                       volt_del=volt_del[c][b],
		                       curr=curr[c][d][b] )
		               for b in range(self._n_bin) ]
		               for d in range(self._n_dir) ]
		               for c in range(self._n_cup) ]

	        # Define the time offsets for the individual data in the
                # spectrum. 

                # Note.  These calibration parameters have been taken from the
                #        "calfile_mode_params" file in the old IDL code.  The
                #        meaning of the "integ" values is unknown, but has been
                #        assumed to represent integration times (possibly
                #        expressed in terms of the number of modulator-voltage
                #        oscillations).

                self._offset = [
                     [ 0.105350, 0.175650, 0.245850, 0.316150, 0.386350,
                       0.456600, 0.526850, 0.597050, 0.667350, 0.737550,
                       0.807850, 0.878050, 0.948350, 1.01855 , 1.08885 ,
                       1.15905 , 1.22930 , 1.29955 , 1.91670 , 2.54390   ],
                     [ 0.366300, 0.993500, 1.61065 , 1.68085 , 1.75115 ,
                       1.82135 , 1.89165 , 1.96185 , 2.03215 , 2.10235 ,
                       2.17265 , 2.24285 , 2.31305 , 2.38335 , 2.45355 ,
                       2.52385 , 2.59405 , 2.66435 , 2.73455 , 2.80485   ]  ]

                self._integ = [
                     [  6,  6, 6, 6, 6, 6, 6, 6,  6,  6,
                        6,  6, 6, 6, 6, 6, 6, 6, 24, 24  ],
                     [ 24, 24, 6, 6, 6, 6, 6, 6,  6,  6,
                        6,  6, 6, 6, 6, 6, 6, 6,  6,  6  ]  ]

		self.set_rot( rot )

		self._eff_deg  = [ float(i) for i in range(91) ]
		self._eff_area = [
		      33.820000, 33.830000, 33.830000, 33.820000, 33.810000,
		      33.800000, 33.780000, 33.770000, 33.760000, 33.740000,
		      33.720000, 33.690000, 33.680000, 33.640000, 33.620000,
		      33.590000, 33.550000, 33.510000, 33.470000, 33.430000,
		      33.387000, 33.341000, 33.293000, 33.243000, 33.182000,
		      33.128000, 33.063000, 32.996000, 32.928000, 32.859000,
		      32.778000, 32.707000, 32.616000, 32.535000, 32.445000,
		      32.346000, 32.249000, 32.001000, 31.615000, 31.140000,
		      30.588200, 29.971700, 29.300000, 28.570000, 27.790000,
		      26.940000, 25.869997, 24.650000, 23.299996, 21.830000,
		      20.259996, 18.590001, 16.829996, 14.970001, 13.019996,
		      10.990001, 8.8779956, 6.6850016, 4.5209962, 2.5750016,
		      0.96799784, 0.0053996863, 0.0000000, 0.0000000, 0.0000000,
		      0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
		      0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
		      0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
		      0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
		      0.0000000, 0.0000000, 0.0000000, 0.0000000, 0.0000000,
		      0.0000000                                              ]

		# Validate the data in the spectrum.

		self.validate( )

		#List of shape [[[n_bin] n_dir] n_cup]

	def __getitem__( self, key ) :

		if ( key == 'curr_min' ) :
			return self._curr_min
		elif ( key == 'n_cup' ) :
			return self._n_cup
		elif ( key == 'n_dir' ) :
			return self._n_dir
		elif ( key == 'n_bin') :
			return self._n_bin
		elif ( key == 'time') :
			return self._time
		elif ( key == 'eff_deg') :
			return self._eff_deg
		elif ( key == 'eff_area') :
			return self._eff_area
		elif ( key == 'elev' ) :
			return [  self.arr[c][0][0]['elev'] 
					for c in range( self._n_cup ) ]
		elif ( key == 'azim' ) :
			return [ [ self.arr[c][d][0]['azim'] 
					for d in range( self._n_dir ) ]
					for c in range( self._n_cup ) ]
		elif ( key == 'volt_strt' ) :
			return  [ [ self.arr[c][0][b]['volt_strt'] 
					for b in range( self._n_bin )] 
					for c in range( self._n_cup )]
		elif ( key == 'volt_stop' ) :
			return  [ [ self.arr[c][0][b]['volt_stop'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'volt_cen' ) :
			return  [ [ self.arr[c][0][b]['volt_cen'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'volt_del' ) :
			return  [ [ self.arr[c][0][b]['volt_del'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'vel_strt' ) :
			return  [ [ self.arr[c][0][b]['vel_strt'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'vel_stop' ) :
			return  [ [ self.arr[c][0][b]['vel_stop'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'vel_cen' ) :
			return  [ [ self.arr[c][0][b]['vel_cen'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'vel_del' ) :
			return  [ [ self.arr[c][0][b]['vel_del'] 
					for b in range( self._n_bin ) ] 
					for c in range( self._n_cup ) ]
		elif ( key == 'curr' ) :
			return [ [ [ self.arr[c][d][b]['curr']
			             for b in range( self._n_bin ) ]
			             for d in range( self._n_dir ) ]
			             for c in range( self._n_cup ) ]
		elif ( key == 'curr_valid' ) :
			return [ [ [ self.arr[c][d][b]['curr_valid']
			             for b in range( self._n_bin ) ]
			             for d in range( self._n_dir ) ]
			             for c in range( self._n_cup ) ]
		elif ( key == 'curr_flat' ) :
			return [ self.arr[c][d][b]['curr']
			         for b in range( self._n_bin )
			         for d in range( self._n_dir )
			         for c in range( self._n_cup ) ]

		elif ( key == 'curr_jump' ) :
			return self._curr_jump

		elif ( key == 'curr_min' ) :
			return self._curr_min
		elif ( key == 'rot' ) :
			return self._rot
		elif ( key == 'dur' ) :
			return self._dur
		else :
			raise KeyError( 'Invalid key for "fc_spec".' )

	def __setitem__( self, key, val ) :		

		raise KeyError( 'Reassignment not permitted except through'
		                                    + ' "set_*" functions.' )

	def validate( self ) :

		# Validate each datum in the spectrum.

		# Note.  Each datum should already contain a Boolean parameter,
		#        "valid", that is pre-valued to indicate whether all
		#        necessary values have been provided.

		for c in range( self._n_cup ) :

			for d in range( self._n_dir ) :

				for b in range( self._n_bin - 1 ) :

					# If the datum is not valid on its own
					# (e.g., a parameter value is missing),
					# move on to the next datum (since
					# nothing more needs to be done).

					if ( not self.arr[c][d][b]['valid'] ) :
						continue

					# If the current is too low, mark it as
					# invalid.

					if ( self.arr[c][d][b]['curr'] <
					                    self['curr_min'] ) :
						self.arr[c][d][b]._valid = False
						continue

					# If the bin appears to be an isolated
					# jump, mark it as invalid.

					if ( ( b == 0                     ) and
					     ( self.arr[c][d][1]['curr']
                                                               is not None ) and
					     ( self.arr[c][d][0]['curr']
					        > self['curr_jump']
					        * self.arr[c][d][1]['curr']) ) :
                                                self.arr[c][d][0]._valid = False

					elif ( ( b == ( self._n_bin - 1 )  ) and
					       ( self.arr[c][d][-2]['curr']
                                                               is not None ) and
					       ( self.arr[c][d][-1]['curr']
					          > self['curr_jump']
					       * self.arr[c][d][-2]['curr']) ) :
                                                self.arr[c][d][-1]._valid = False

					elif ( ( self.arr[c][d][b-1]['curr']
					                       is not None ) and
					       ( self.arr[c][d][b+1]['curr']
					                       is not None ) and
					       ( self.arr[c][d][b]['curr']
					           > self['curr_jump']
					     * self.arr[c][d][b-1]['curr'] ) and 
					       ( self.arr[c][d][b]['curr']
					           > self['curr_jump']
					     * self.arr[c][d][b+1]['curr'] ) ) :
						self.arr[c][d][b]._valid = False

        #-----------------------------------------------------------------------
        # DEFINE THE FUNCTION FOR CALCULATING THE TIMESTAMP OF A SINGLE DATUM.
        #-----------------------------------------------------------------------

        def calc_time( self, c, d, b ) :

                # Compute and return the timestamp of the specified datum.  If
                # this cannot be done (due to missing information), return
                # "None".

		if ( ( self._time is None ) or ( self._rot  is None ) ) :
			return

		else :

			return ( self._time
                                     + timedelta( seconds=(self._rot*b) )
                                     + timedelta( seconds=self._offset[c][d] ) )

        #-----------------------------------------------------------------------
        # DEFINE THE FUNCTION FOR MAKING A TIMESTAMP FOR EACH DATUM.
        #-----------------------------------------------------------------------

        def make_time( self ) :

                # Compute and apply each datum's timestamp.

                for c in range ( self._n_cup ) :

                        for d in range ( self._n_dir ) :

                                for b in range ( self._n_bin ) :

                                        self.arr[c][d][b]._time \
                                                     = self.calc_time( c, d, b )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION SETTING THE ROTATION PERIOD.
	#-----------------------------------------------------------------------

	def set_rot( self, rot ) :

		# Update the rotation period and the duration of this spectrum.

		self._rot = rot
		self._dur = rot * self['n_bin']

                # Update the timestamps of the individual data in this spectrum.

                self.make_time( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALC'ING EXPECTED CURRENT FROM A POPULATION.
	#-----------------------------------------------------------------------

	def calc_curr( self, m, q, v0, n, dv, w) :

		# Return a 3-D list with the calculated current for each bin in
		# the spectrum.

		return [ [ [ self.arr[c][d][b].calc_curr( 
		                    m, q, v0, n, dv, w      )
		                    for b in range( self['n_bin'] ) ]
		                    for d in range( self['n_dir'] ) ]
		                    for c in range( self['n_cup'] ) ]

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING TOTAL CURRENT IN A GIVEN WINDOW.
	#-----------------------------------------------------------------------

	def calc_tot_curr( self, c, d, b, win=1 ) :

		# Validate the cup, direction, and bin indices.

		if ( ( c < 0 ) or ( c >= self['n_cup'] ) ) :
			raise ValueError( 'Cup index out of range.' )

		if ( ( d < 0 ) or ( d >= self['n_dir'] ) ) :
			raise ValueError( 'Direction index out of range.' )

		if ( ( b < 0 ) or ( b >= self['n_bin'] ) ) :
			raise ValueError( 'Direction index out of range.' )

		# Validate the window size.

		if ( ( win < 1 ) or ( b + win > self['n_bin'] ) ) :
			raise ValueError( 'Window out of range.' ) 

		# Return the total (valid) current in the specified window.

		return sum( [ self.arr[c][d][b+w]['curr']
		                                       for w in range( win ) ] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION TO FIND THE INDEX OF WINDOW WITH MAXIMUM CURRENT
	#-----------------------------------------------------------------------

	def find_max_curr( self, c, d, win=1 ) :

		# Validate the cup and direction indices.

		if ( ( c < 0 ) or ( c >= self['n_cup'] ) ) :
			raise ValueError( 'Cup index out of range.' )

		if ( ( d < 0 ) or ( d >= self['n_dir'] ) ) :
			raise ValueError( 'Direction index out of range.' )

		# Validate the window size.

		if ( ( win < 1 ) or ( win > self['n_bin'] ) ) :
			raise ValueError( 'Window out of range.' ) 

		# Search the specified direction for the "win"-bin range that
		# contains the maximum total current.

		b_max    = 0
		curr_max = 0.

		for b in range( 0, self['n_bin'] - win + 1 ) :

			curr = sum( [ self.arr[c][d][b+w]['curr']
			                               for w in range( win ) ] )

			if ( curr > curr_max ) :
				b_max    = b
				curr_max = curr

		# Return the location of the window with the maximum current.

		return b_max

        #-----------------------------------------------------------------------
	# DEFINE THE FUNCTION TO ASSIGN THE MAGNETIC FIELD TO EACH DATUM. 
	#-----------------------------------------------------------------------

	def set_mag( self, mfi_t, mfi_b_x, mfi_b_y, mfi_b_z ) :

		mfi_s = [ ( t - mfi_t[0] ).total_seconds( ) for t in mfi_t ]

		fnc_b_x = interp1d( mfi_s, mfi_b_x )
		fnc_b_y = interp1d( mfi_s, mfi_b_y )
		fnc_b_z = interp1d( mfi_s, mfi_b_z )

		try :

			for c in range( self['n_cup'] ) :

				for d in range( self['n_dir'] ) :

					for b in range( self['n_bin'] ) :

						s = ( self.arr[c][d][b]['time']
                                                  - mfi_t[0] ).total_seconds( )

						b_x = fnc_b_x( s )
						b_y = fnc_b_y( s )
						b_z = fnc_b_z( s )

						self.arr[c][d][b].set_mag( (
						            b_x, b_y, b_z ) )
		except :

			avg_b_x = sum( mfi_b_x ) / float( len( mfi_b_x ) )
			avg_b_y = sum( mfi_b_y ) / float( len( mfi_b_y ) )
			avg_b_z = sum( mfi_b_z ) / float( len( mfi_b_z ) )

			for c in range( self['n_cup'] ) :

                                for d in range( self['n_dir'] ) :

                                        for b in range( self['n_bin'] ) :

                                                self.arr[c][d][b].set_mag( (
						avg_b_x, avg_b_y, avg_b_z ) )

