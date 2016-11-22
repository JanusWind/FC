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


# Load the modules necessary for push buttons.

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPushButton



################################################################################
## DEFINE THE "event_PushButton" CLASS TO CUSTOMIZE "QPushButton".
################################################################################


# Note.  When a widget or other object intializes and instance of this class,
#        it passes itself to the initialization function "self.__init__()",
#        which stores it to "self.owner".  When the plot is clicked on, a call
#        is made to the function "self.owner.user_click()" so that "self.owner"
#        can handle the event.

#        The "string" "self.fnc" is a string that indicates the function of this
#        button.  The particular values of "self.fnc" is used give an
#        appropriate label to this button.  Additionally, when the button is
#        pressed, the value of "self.fnc" is returned to "self.owner" via
#        "self.owner.user_event()" so that the appropriate action can be taken.


class event_PushButton( QPushButton ) :


	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, owner, fnc, lab='' ) :


		# Inherit all attributes of an instance of "QPushButton".

		super( event_PushButton, self ).__init__( lab )


		# Store the user-provided instance of the initializing object.

		self.owner = owner


		# Store the string indicating the function of this button.

		self.fnc = fnc


	#-----------------------------------------------------------------------
	# (RE)DEFINE THE FUNCTION FOR RESPONDING TO MOUSE CLICKS.
	#-----------------------------------------------------------------------

	def mousePressEvent( self, event ) :


		# Deligate the handling of the mouse-click event to
		# "self.owner", providing it with the details of the event and
		# also the string identifying the function of this button.

		self.owner.user_event( event, self.fnc )


	#-----------------------------------------------------------------------
	# (RE)DEFINE THE FUNCTION FOR RESPONDING TO KEY PRESSES.
	#-----------------------------------------------------------------------

	def keyPressEvent( self, event ) :


		# If the "Enter" or "Return" key was pressed, interpret this as
		# an event and deligate handling thereof to "self.owner".

		if ( ( event.key( ) == Qt.Key_Enter  ) or
		     ( event.key( ) == Qt.Key_Return )    ) :

			self.owner.user_event( event, self.fnc )
