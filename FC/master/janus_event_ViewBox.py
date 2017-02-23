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


# Load the modules necessary for plotting.

from pyqtgraph import ViewBox



################################################################################
## DEFINE THE "event_PlotWidget" CLASS TO CUSTOMIZE "PlotWidget" EVENTS.
################################################################################


# Note.  When a widget or other object intializes and instance of this class,
#        it passes itself to the initialization function "self.__init__()",
#        which stores it to "self.owner".  When the plot is clicked on, a call
#        is made to the function "self.owner.user_event()" so that "self.owner"
#        can handle the event.


class event_ViewBox( ViewBox ) :


	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, owner,
	              border=None, enableMouse=True, enableMenu=True ) :


		# Inherit all attributes of an instance of "PlotWidget".

		super( event_ViewBox, self ).__init__( border=border,
		                enableMouse=enableMouse, enableMenu=enableMenu )


		# Store the user-provided instance of the initializing object.

		self.owner = owner


	#-----------------------------------------------------------------------
	# (RE)DEFINE THE FUNCTION FOR RESPONDING TO MOUSE CLICKS.
	#-----------------------------------------------------------------------

	def mousePressEvent( self, event ) :


		# Deligate the handling of the mouse-click event to
		# "self.owner", providing it with the details of the event.

		self.owner.user_event( event, self )

		return
