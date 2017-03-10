from janus_fc_dat import fc_dat

	#-----------------------------------------------------------------------
	# DEFINE THE Class FOR spec
	#-----------------------------------------------------------------------



class fc_spec():
	def __init__( self, n_bin, elev=None, azim=None, volt_cen=None, 
				        volt_del=None, curr=None, time=None, 
						  curr_jump=100., curr_min=1.) :

		self._n_cup=2
		self._n_dir=20
		self._n_bin=n_bin
		self._time=time
		self.curr_jump = curr_jump
		self.curr_min = curr_min


		if ( elev == None ) :
			elev = [ None for c in range( self._n_cup ) ]

		if ( azim == None ) :
			azim = [ [ None for d in range( self._n_dir )       ]
						for c in range(self._n_cup) ]

		if ( volt_cen == None ) :
			volt_cen = [ [ None for b in range( self._n_bin )   ]
						for c in range(self._n_cup) ]

		if ( volt_del == None ) :
			volt_del = [ [ None for b in range( self._n_bin )   ]
						for c in range(self._n_cup) ]		

		if ( curr == None ) :
			curr = [ [ [ None for b in range( self._n_bin ) ]
			                  for d in range( self._n_dir ) ]
			                  for c in range( self._n_cup ) ]

		#if ( len( elev ) != self._n_cup ) :
		#	raise TypeError( 'List elev must be length n_cup.' )

		self.arr = [[[ fc_dat( spec=self,
		                       elev=elev[c],
		                       azim=azim[c][d],
				       volt_cen=volt_cen[c][b], 
				       volt_del=volt_del[c][b], 
				       curr=curr[c][d][b]) 
							 for b in range(self._n_bin)]
		                                         for d in range(self._n_dir)]
		                                         for c in range(self._n_cup)]

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

	def __getitem__(self, key ) :

		if ( key == 'n_cup' ) :
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
					for c in range(self._n_cup)]
		elif ( key == 'azim' ) :
			return [[ self.arr[c][d][0]['azim'] 
					for d in range(self._n_dir) ]
					for c in range(self._n_cup) ]
		elif ( key == 'volt_strt' ) :
			return  [[ self.arr[c][0][b]['volt_strt'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'volt_stop' ) :
			return  [[ self.arr[c][0][b]['volt_stop'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'volt_cen' ) :
			return  [[ self.arr[c][0][b]['volt_cen'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'volt_del' ) :
			return  [[ self.arr[c][0][b]['volt_del'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'vel_strt' ) :
			return  [[ self.arr[c][0][b]['vel_strt'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'vel_stop' ) :
			return  [[ self.arr[c][0][b]['vel_stop'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'vel_cen' ) :
			return  [[ self.arr[c][0][b]['vel_cen'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]
		elif ( key == 'vel_del' ) :
			return  [[ self.arr[c][0][b]['vel_del'] 
					for b in range(self._n_bin)] 
					for c in range(self._n_cup)]

		elif ( key == 'curr' ) :
			return [ [ [ self.arr[c][d][b]['curr']
			             for b in range( self._n_bin ) ]
			             for d in range( self._n_dir ) ]
			             for c in range( self._n_cup ) ]

		elif ( key == 'curr_flat' ) :
			return [ self.arr[c][d][b]['curr']
			         for b in range( self._n_bin )
			         for d in range( self._n_dir )
			         for c in range( self._n_cup ) ]
		else :
			raise KeyError( 'Invalid key for "fc_spec".' )

	def __setitem__( self, key, val ) :		

		"""
		if ( key == 'time' ) :
			self._time = val
		else :
			raise KeyError( 'Invalid key for "fc_spec".' )
		"""

		raise KeyError( 'Reassignment not permitted after initialization.' )

	def validate( self ) :

		# Validate each datum in the spectrum.

		# Note.  Each datum should already contain a Boolean parameter,
		#        "valid", that is pre-valued to indicate whether all
		#        necessary values have been provided.

		for c in range( self._n_cup ) :

			for d in range( self._n_dir ) :

				for b in range( self._n_bin ) :

					# If the datum is not valid on its own
					# (e.g., a parameter value is missing),
					# move on to the next datum (since
					# nothing more needs to be done).

					if ( not self.arr[c][d][b]['valid'] ) :
						continue

					# If the current is too low, mark it as
					# invalid.

					if ( self.arr[c][d][b]['curr'] <
					                       self.curr_min ) :
						self.arr[c][d][b]._valid = False
						continue

					# If the bin appears to be an isolated
					# jump, mark it as invalid.

					if ( (b == 0                               )and
					     (self.arr[c][d][1]['curr'] is not None)and
					     (self.arr[c][d][0]['curr']
					          > self.curr_jump
					                * self.arr[c][d][1]['curr'])   ) :
						self.arr[c][d][0]._valid = False

					elif ( (b == ( self._n_bin - 1 )              )and
					       (self.arr[c][d][-2]['curr'] is not None)and
					       (self.arr[c][d][-1]['curr']
					          > self.curr_jump
					                  * self.arr[c][d][-2]['curr'])   ) :
						self.arr[c][d][-1]._valid = False

					elif ( ( self.arr[c][d][b-1]['curr']
					                                is not None ) and
					       ( self.arr[c][d][b+1]['curr']
					                                is not None ) and
					       ( self.arr[c][d][b]['curr']
					           > self.curr_jump
					              * self.arr[c][d][b-1]['curr'] ) and 
					       ( self.arr[c][d][b]['curr']
					           > self.curr_jump
					              * self.arr[c][d][b+1]['curr'] )     ) :
						self.arr[c][d][b]._valid = False

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING TOTAL CURRENT IN A GIVEN WINDOW
	#-----------------------------------------------------------------------

	def calc_curr( c, d, b, win=1 ) :

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

		return sum( [ self.arr[c][d][b+w]['curr_valid']
		                                       for w in range( win ) ] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION TO FIND THE INDEX OF WINDOW WITH MAXIMUM CURRENT
	#-----------------------------------------------------------------------

	def find_max_curr( c, d, win=1 ) :

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

		b_max   = 0
		curr_max = 0.

		for b in range( 0, self['n_bin'] - win + 1 ) :

			curr = sum( [ self.arr[c][d][b+w]['curr_valid']
			                               for w in range( win ) ] )

			if ( curr > curr_max ) :
				b_max   = b
				curr_max = curr

		# Return the location of the window with the maximum current.

		return b_max

   #-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING FIRST DIRECTION WITH MAXIMUM CURR
	#-----------------------------------------------------------------------

	def calc_cup_max_ind( c ) :

		# Validate the cup, direction, and bin indices.

		if ( ( c < 0 ) or ( c >= self['n_cup'] ) ) :
			raise ValueError( 'Cup index out of range.' )

      b_max = self.find_max_cur( c,d, win= self.mom_win_bin )
                                       for d in self['n_dir']
                                       for c in self['n_cup']
      dir_max = 0
      curr_max = 0.

		for di in range( 0, self['n_dir']- self.mom_win_dir + 1 ) :

         curr = sum( [ self.arr[c][d+di][b_max+w]['curr_valid'] 
                                        for w  in range( self.mom_win_bin ) ] )
                                        for di in range( self.mom_win_dir )
         if (curr > curr_max) :
            dir_max = di
            curr_max = curr

      # Return the location of of the direction with maximum current

      return dir_max
