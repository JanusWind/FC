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

# Load the modules necessary for one-line text editors.

from PyQt4.QtGui  import QCheckBox, QRadioButton
from PyQt4.QtCore import QSize

# Load the modules necessary for signal handling.

from PyQt4.QtCore import SIGNAL


################################################################################
## DEFINE THE "event_CheckBox" CLASS TO CUSTOMIZE "QCheckBox".
################################################################################

# Note.  When a widget or other object intializes and instance of this class,
#        it passes itself to the initialization function "self.__init__()",
#        which stores it to "self.owner".  When a certain event (such as
#        mouse button press) occurs, a call is made to "self.owner.user_event()"
#        so that "self.owner" can handle the event.

#        The "string" "self.fnc" is a string that indicates the function of this
#        text area.  When an event occurs, the value of "self.fnc" is returned
#        to "self.owner" via "self.owner.user_event()" so that the appropriate
#        action can be taken.

class event_CheckBox( QCheckBox ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, owner, fnc ) :

		# Inherit all attributes of an instance of "QLineEdit".

		super( event_CheckBox, self ).__init__( )

		# Store the user-provided instance of the initializing object.

		self.owner = owner

		# Store the string indicating the function of this text area.

		self.fnc = fnc

		# If the 'stateChanged()' signal is emitted (i.e., if the user
		# clicks on this check box), notify "self.owner".

		self.connect( self, SIGNAL('clicked(bool)'),
		              self.signal_clicked            )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "clicked" SIGNAL.
	#-----------------------------------------------------------------------

	def signal_clicked( self ) :

		# Alert the object that initialized this widget (i.e., its
		# "owner") that the check box has been clicked.

		self.owner.user_event( None, self.fnc )


################################################################################
## DEFINE THE "event_RadioBox" CLASS TO CUSTOMIZE "QRadioButton".
################################################################################

class event_RadioBox( QRadioButton ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, owner, fnc ) :

		# Inherit all attributes of an instance of "QLineEdit".

		super( event_RadioBox, self ).__init__( )

		# Store the user-provided instance of the initializing object.

		self.owner = owner

		# Store the string indicating the function of this text area.

		self.fnc = fnc

		# If the 'stateChanged()' signal is emitted (i.e., if the user
		# clicks on this check box), notify "self.owner".

		self.connect( self, SIGNAL('toggled(bool)'),
		              self.signal_toggled            )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "toggled" SIGNAL.
	#-----------------------------------------------------------------------

	def signal_toggled( self ) :

		# Alert the object that initialized this widget (i.e., its
		# "owner") that the check box has been toggled.

		self.owner.user_event( None, self.fnc )
