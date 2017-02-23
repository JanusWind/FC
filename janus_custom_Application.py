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

# Load the modules necessary for the graphical interface.

from PyQt4.QtGui import QApplication, QCursor
from PyQt4.QtCore import Qt, SIGNAL


################################################################################
## DEFINE THE "custom_Application" CLASS TO CUSTOMIZE "QApplication".
################################################################################

class custom_Application( QApplication ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core, res_lo=False ) :

		# Inheret all attributes of the "QApplication" class.

		super( custom_Application, self ).__init__( [] )

		# Save the Janus "core" to be associated with this object.

		self.core = core

		# Save the indicator of reduced size for the application window.

		self.res_lo = ( True if ( res_lo ) else False )

		# Prepare to respond to signals received from the Wind/FC
		# spectrum.

		self.connect( self.core, SIGNAL('janus_busy_beg'),
		                                            self.resp_busy_beg )
		self.connect( self.core, SIGNAL('janus_busy_end'),
		                                            self.resp_busy_end )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "busy_beg" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_busy_beg( self ) :

		# Override the default cursor with the "wait" cursor.

		self.setOverrideCursor( QCursor( Qt.BusyCursor ) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "busy_end" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_busy_end( self ) :

		# Remove the cursor override.

		self.restoreOverrideCursor( )
