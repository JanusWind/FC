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

from PyQt4.QtGui import QComboBox


# Load the modules necessary for signal handling.

from PyQt4.QtCore import SIGNAL



################################################################################
## DEFINE THE "event_LineEdit" CLASS TO CUSTOMIZE "QLineEdit".
################################################################################


# Note.  When a widget or other object intializes and instance of this class,
#        it passes itself to the initialization function "self.__init__()",
#        which stores it to "self.owner".  When a certain event (such as
#        pressing "Return") occurs, a call is made to some function
#        "self.owner.*()" so that "self.owner" can handle the event.

#        The "string" "self.fnc" is a string that indicates the function of this
#        text area.  When an event occurs, the value of "self.fnc" is returned
#        to "self.owner" via the "self.owner.*()" function so that the
#        appropriate action can be taken.


class event_ComboBox( QComboBox ) :


	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, owner, fnc ) :


		# Inherit all attributes of an instance of "QLineEdit".

		super( event_ComboBox, self ).__init__( )


		# Store the user-provided instance of the initializing object.

		self.owner = owner


		# Store the string indicating the function of this text area.

		self.fnc = fnc


		# Intialize "text_index" with the index of this box's currently
		# displayed item.

		# Note.  This variable is useful for establishing if and how
		#        the displayed item has been changed.  For example, the
		#        "editingFinished()" signal is sent if a user removes
		#        focus from this widget even if no actual edits were
		#        made.

		self.index_old = self.currentIndex( )


		# If the 'currentIndexChanged()' signal is emitted (i.e., this
		# widget looses the "focus"), notify "self.owner".

		self.connect( self, SIGNAL('activated(int)'),
		              self.signal_activated        )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "activated" SIGNAL.
	#-----------------------------------------------------------------------

	def signal_activated( self ) :


		# If an actual change has been made to the selection, notify
		# "self.owner" that this has occured.

		if ( self.currentIndex( ) != self.index_old ) :

			self.index_old = self.currentIndex( )

			self.owner.user_event( None, self.fnc )
