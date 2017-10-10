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

# Load the necessary "numpy" array modules.

from numpy import array, zeros


################################################################################
## DEFINE THE "step" CLASS FOR STORING AND MANIPULATING A STEP FUNCTION.
################################################################################

class step( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, cen, wid, lev, descending=False ) :

		# Note.  This function presumes that a step function has been
		#        defined in terms of the equal-length, linear arrays
		#        "cen", "wid", and "lev".  The array "cen" indicates the
		#        location of the center of each step, "wid" the width,
		#        and "lev" the height.  It is assumed that the bins are
		#        in assending order (unless it is specified to be
		#        descending) and to have no (or at least negligible)
		#        gaps between them.

		# CAUTION!  No checks are made to ensure that the bins are
		#           ascending/descending and that have no gaps between
		#           them.

		# Determine the number of steps based on the length of the
		# passed arrays.

		self.n = min( len( cen ), len( wid ), len( lev ) )

		# Store the center, width, and level of each steps.  If
		# necessary, truncate the user provided arrays to be the same
		# length.

		self.cen = array( cen[0:self.n] )
		self.wid = array( wid[0:self.n] )
		self.lev = array( lev[0:self.n] )

		# If the bins were passed in descending order, reverse them to
		# ascending order.

		if ( descending ) :

			self.cen = self.cen[::-1]
			self.wid = self.wid[::-1]
			self.lev = self.lev[::-1]

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR COMPUTING THE STEP FUNCTION'S PLOT POINTS.
	#-----------------------------------------------------------------------

	def calc_pnt( self, lev_min=None ) :

		# Note.  This function then returns two, equal-length, linear
		#        arrays, "pnt_x" and "pnt_y", that can be passed to the
		#        user's choice of plotting functions to display the step
		#        function.

		# If undefined, provide a value for "lev_min".

		lev_min = amin( self.lev ) if ( lev_min is None ) else lev_min

		# Initialize the arrays that will contain the computed points of
		# the step function.

		pnt_x = zeros( 2 * ( self.n + 1 ) )
		pnt_y = zeros( 2 * ( self.n + 1 ) )

		# Compute the points of the step function.

		pnt_x[0] = self.cen[0] - ( self.wid[0] / 2. )
		pnt_y[0] = lev_min

		for i in range( self.n ) :
			pnt_x[(2*i)+1] = self.cen[i] - ( self.wid[i] / 2. )
			pnt_x[(2*i)+2] = self.cen[i] + ( self.wid[i] / 2. )
			pnt_y[(2*i)+1] = self.lev[i]
			pnt_y[(2*i)+2] = self.lev[i]

		pnt_x[(2*self.n)+1] = self.cen[self.n-1] + \
		                                     ( self.wid[self.n-1] / 2. )
		pnt_y[(2*self.n)+1] = lev_min

		# Return the computed points of the step function.

		return ( pnt_x, pnt_y )
