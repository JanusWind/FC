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

from janus_pl_dat import pl_dat
from datetime import timedelta
from scipy.interpolate import interp1d
from numpy import shape

################################################################################
## DEFINE THE "pl_spec" CLASS.
################################################################################

class pl_spec( ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self,
	              t_strt=None, t_stop=None, elev_cen=None, the_del=None,
	              azim_cen=None, phi_del=None, volt_cen=None, volt_del=None,
	              psd=None, rot=3.                                       ) :

		self._n_bin     = 14 #TODO Confirm
		self._n_the     = 5
		self._n_phi     = 5 #TODO Confirm this
		self._t_strt    = t_strt
		self._t_stop    = t_stop
		self._rot       = t_stop - t_strt

		if ( azim_cen is None ) :
			azim_cen = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			azim_cen = self.adjust(azim_cen)

		if ( phi_del is None ) :
			phi_del  = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			phi_del = self.adjust(phi_del)

		if ( elev_cen is None ) :
			elev_cen = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			elev_cen = self.adjust(elev_cen)


		if ( the_del is None ) :
			the_del  = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			the_del = self.adjust(the_del)

		if ( volt_cen is None ) :
			volt_cen = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			volt_cen = self.adjust(volt_cen)	

		if ( volt_del is None ) :
			volt_del = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			volt_del = self.adjust(volt_del)	

		if ( psd is None ) :
			psd      = [ [ [ None for b in range( self._n_bin ) ]
			                      for p in range( self._n_phi ) ]
			                      for t in range( self._n_the ) ]
		else:
			psd = self.adjust(psd)

		self.arr = [[[ pl_dat( spec=self,
		                       azim_cen = azim_cen[t][p][b],
		                       phi_del  = phi_del[t][p][b],
		                       elev_cen = elev_cen[t][p][b],
		                       the_del  = the_del[t][p][b],
		                       volt_cen = volt_cen[t][p][b], 
		                       volt_del = volt_del[t][p][b], 
		                       t_strt   = self._t_strt,
		                       t_stop   = self._t_stop,
		                       psd      = psd[t][p][b]       ) 
		                              for b in range( self._n_bin ) ]
		                              for p in range( self._n_phi ) ]
		                              for t in range( self._n_the ) ]

#		self.set_rot( rot )

		# Validate the data in the spectrum.

#		self.validate( )

		# List of shape [[[n_bin] n_the] n_phi] where
		# 'bin' is the voltage sweep number,
		# 'the' specifies theta of the look direction, and
		# 'phi' specifies phi of the look direction

	def adjust(self, matrix) :

	# This function 'adjust':
	# 1. takes data whose phi values and voltages are reversed and returns
	# them to their proper order (it does not affect theta values) and
	# 2. breaks 25 directions into 5 sets of 5 pairs of (theta, phi)

		new_matrix = [ [ [ None for b in range( self._n_bin ) ]
		                        for p in range( self._n_phi ) ]
		                        for t in range( self._n_the ) ]
		for t in range( self._n_the ):
			for p in range( self._n_phi ):
				for b in range( self._n_bin ):
					new_matrix[-t-1][p][b] = \
					    matrix[-(5*t+p)-1][-b-1]
		return new_matrix

	def __getitem__(self, key ) : #TODO not yet finished

		if ( key == 'n_the' ) :
			return self._n_the
		elif ( key == 'n_phi' ) :
			return self._n_phi
		elif ( key == 'n_bin' ) :
			return self._n_bin
		elif ( key == 'time' ) :
			return [ self.arr[p][0][0]['time']
					for p in range(self._n_phi)]
		elif ( key == 'elev_cen' ) :
			return [ self.arr[0][t][0]['elev_cen']
					for t in range(self._n_the)]
		elif ( key == 'the_del' ) :
			return [ self.arr[0][t][0]['the_del']
					for t in range(self._n_the)]
		elif ( key == 'azim_cen' ) :
			return [ self.arr[p][0][0]['azim_cen']
					for p in range(self._n_phi)]
		elif ( key == 'phi_del' ) :
			return [ self.arr[p][0][0]['phi_del']
					for p in range(self._n_phi)]
		elif ( key == 'volt_strt' ) :
			return  [ self.arr[0][0][b]['volt_strt'] 
					for b in range(self._n_bin)]
		elif ( key == 'volt_stop' ) :
			return  [ self.arr[0][0][b]['volt_stop'] 
					for b in range(self._n_bin)]
		elif ( key == 'volt_cen' ) :
			return  [ self.arr[0][0][b]['volt_cen'] 
					for b in range(self._n_bin)]
		elif ( key == 'volt_del' ) :
			return  [ self.arr[0][0][b]['volt_del'] 
					for b in range(self._n_bin)]
		elif ( key == 'vel_strt' ) :
			return  [ self.arr[0][0][b]['vel_strt'] 
					for b in range(self._n_bin)]
		elif ( key == 'vel_stop' ) :
			return  [ self.arr[0][0][b]['vel_stop'] 
					for b in range(self._n_bin)]
		elif ( key == 'vel_cen' ) :
			return  [ self.arr[0][0][b]['vel_cen'] 
					for b in range(self._n_bin)]
		elif ( key == 'vel_del' ) :
			return  [ self.arr[0][0][b]['vel_del'] 
					for b in range(self._n_bin)]
		elif ( key == 'psd' ) :
			return [ [ [ self.arr[p][t][b]['psd']
			             for b in range( self._n_bin ) ]
			             for t in range( self._n_the ) ]
			             for p in range( self._n_phi ) ]
		elif ( key == 'psd_valid' ) :
			return [ [ [ self.arr[p][t][b]['psd']
			             for b in range( self._n_bin ) ]
			             for t in range( self._n_the ) ]
			             for p in range( self._n_phi ) ]
		elif ( key == 'rot' ) :
			return self._rot
		else :
			raise KeyError( 'Invalid key for "pl_spec".' )

	def __setitem__( self, key, val ) :		

		raise KeyError( 'Reassignment not permitted except through'
		                                    + ' "set_*" functions.' )






