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

################################################################################
## DEFINE THE "pl_spec" CLASS.
################################################################################

class pl_spec( ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, n_bin,
	              t_strt=None, t_stop=None, phi_cen=None, phi_del=None
	              the_cen=None, the_del=None, volt_cen=None, volt_del=None,
	              psd=None, rot=3.                                       ) :

		self._n_the     = 16
		self._n_phi     = 64 #TODO Confirm this
		self._n_bin     = n_bin
		self._time      = time

		if ( phi_cen == None ) :
			phi_cen = [ None for p in range( self._n_phi ) ]

		if ( phi_del == None ) :
			phi_del = [ None for p in range( self._n_phi ) ]

		if ( the_cen == None ) :
			the_cen = [ None for t in range( self._n_the )    ]

		if ( the_del == None ) :
			the_del = [ None for t in range( self._n_the )    ]

		if ( volt_cen == None ) :
			volt_cen = [ [ None for b in range( self._n_bin )   ]	

		if ( volt_del == None ) :
			volt_del = [ [ None for b in range( self._n_bin )   ]	

		if ( psd == None ) :
			psd = [ [ [ None for b in range( self._n_bin ) ]
			                  for t in range( self._n_the ) ]
			                  for p in range( self._n_phi ) ]

		self.arr = [[[ pl_dat( spec=self,
		                       phi_cen = phi_cen[p],
		                       phi_del = phi_del[p],
		                       the_cen = the_cen[t],
		                       the_del = the_del[t],
		                       volt_cen=volt_cen[b] 
		                       volt_del=volt_del[b], 
		                       psd=psd[b][t][p]      ) 
		                   for b in range(self._n_bin) ]
		                   for t in range(self._n_the) ]
		                   for p in range(self._n_phi) ]

		self.set_rot( rot )

