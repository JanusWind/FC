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

from PyQt4.QtGui import QLineEdit


# Load the modules necessary for signal handling.

from PyQt4.QtCore import SIGNAL



################################################################################
## DEFINE THE "event_LineEdit" CLASS TO CUSTOMIZE "QLineEdit".
################################################################################


# Note.  When a widget or other object intializes and instance of this class,
#        it passes itself to the initialization function "self.__init__()",
#        which stores it to "self.owner".  When a certain event (such as
#        pressing "Return") occurs, a call is made to "self.owner.user_click()"
#        so that "self.owner" can handle the event.

#        The "string" "self.fnc" is a string that indicates the function of this
#        text area.  When an event occurs, the value of "self.fnc" is returned
#        to "self.owner" via "self.owner.user_event()" so that the appropriate
#        action can be taken.


class event_LineEdit( QLineEdit ) :


	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, owner, fnc ) :


		# Inherit all attributes of an instance of "QLineEdit".

		super( event_LineEdit, self ).__init__( )


		# Store the user-provided instance of the initializing object.

		self.owner = owner


		# Store the string indicating the function of this text area.

		self.fnc = fnc


		# Intialize "text_old" with the current text in this text box.

		# Note.  This variable is useful for establishing if and how
		#        the text was changed.  For example, the
		#        "editingFinished()" signal is sent if a user removes
		#        focus from this widget even if no actual edits were
		#        made.

		self.text_old = self.text( )


		# If the 'editingFinished()' signal is emitted (i.e., this
		# widget looses the "focus"), notify "self.owner".

		self.connect( self, SIGNAL('editingFinished()'),
		              self.signal_editingFinished        )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SETTING THE TEXT AND UPDATING THE OLD TEXT.
	#-----------------------------------------------------------------------

	def setTextUpdate( self, text ) :


		# Set the text of this text box to that requested by the user.

		self.setText( text )


		# Update the record of the "old text" to the current text.

		self.text_old = self.text( )



	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE SIGNAL FOR EDITING FINISHED.
	#-----------------------------------------------------------------------

	def signal_editingFinished( self ) :


		# If an actual change has been made to the text of this text 
		# box, notify "self.owner" that this has occured.

		if ( self.text( ) != self.text_old ) :

			self.text_old = self.text( )

			self.owner.user_event( None, self.fnc )
