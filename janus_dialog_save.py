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

from PyQt4.QtGui import QDialog, QGridLayout, QLabel

# Load the customized push button.

from janus_event_PushButton import event_PushButton


################################################################################
## DEFINE CLASS "dialog_save" TO CUSTOMIZE "QDialog" TO PROMPT TO SAVE.
################################################################################

class dialog_save( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_save, self ).__init__( )

		# Make this a modal dialog (i.e., block user-interaction with
		# the main application window while this dialog exists).

		self.setModal( True )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Save?' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Initialize the label and buttons that comprise this dialog
		# box.

		self.lab = QLabel( 'Save analysis results before exit?' )

		self.btn_save = event_PushButton( self, 'save', 'Save'    )
		self.btn_xprt = event_PushButton( self, 'xprt', 'Export'  )
		self.btn_exit = event_PushButton( self, 'exit', 'Discard' )
		self.btn_cncl = event_PushButton( self, 'cncl', 'Cancel'  )

		# Add the label and the buttons to the grid layout.

		self.grd.addWidget( self.lab     , 0, 0, 1, 3 )

		self.grd.addWidget( self.btn_save, 1, 0, 1, 1 )
		self.grd.addWidget( self.btn_exit, 1, 1, 1, 1 )
		self.grd.addWidget( self.btn_cncl, 1, 2, 1, 1 )

		###self.grd.addWidget( self.lab     , 0, 0, 1, 4 )

		###self.grd.addWidget( self.btn_save, 1, 0, 1, 1 )
		###self.grd.addWidget( self.btn_xprt, 1, 1, 1, 1 )
		###self.grd.addWidget( self.btn_exit, 1, 2, 1, 1 )
		###self.grd.addWidget( self.btn_cncl, 1, 3, 1, 1 )

		# Initialize the object to be returned to the user on the close
		# of this dialog window.

		self.resp = None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# Set the string-identifier of the button pressed to be the
		# value returned by this dialog box.

		self.resp = fnc

		# Close this dialog box.

		self.close( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROMPTING THE USER FOR A RANGE OF TIMESTAMPS.
	#-----------------------------------------------------------------------

	def get_resp( self ) :

		# Execute this dialog.

		self.exec_( )

		# Return the string-indentifier of the button pressed.

		return self.resp
