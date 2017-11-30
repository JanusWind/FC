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

from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QFont
from PyQt4.QtCore import SIGNAL

# Load the customized push button and one-line text editor.

from janus_event_CheckBox import event_CheckBox, event_RadioBox
from janus_event_LineEdit import event_LineEdit
from janus_event_PushButton import event_PushButton

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
################################################################################

class dialog_opt_file( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_file, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_opt'),
		                                            self.resp_chng_opt )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg1 = QGridLayout( )
		self.sg2 = QGridLayout( )

		self.sg1.setContentsMargins( 0, 0, 0, 0 )
		self.sg2.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg1, 0, 0, 1, 1 )
		self.grd.addLayout( self.sg2, 1, 0, 1, 1 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_ret   = QLabel( 'Retain all downloaded files'   )
		self.lab_lim   = QLabel( 'Limit maximum file number to:' )

		self.txt_lim   = event_LineEdit( self, 'lim' )

		self.box = { 'ret':event_RadioBox( self, 'ret' ),
		             'lim':event_RadioBox( self, 'lim' ) }

		self.btn_done = event_PushButton( self, 'done', 'Done' )

		self.btn_done.setAutoDefault( False )

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.sg1.addWidget( self.box['ret'], 0, 0, 1, 1 )
		self.sg1.addWidget( self.box['lim'], 1, 0, 1, 1 )
		self.sg1.addWidget( self.lab_ret, 0, 1, 1, 1 )
		self.sg1.addWidget( self.lab_lim, 1, 1, 1, 1 )
		self.sg1.addWidget( self.txt_lim, 1, 2, 1, 1 )

		self.sg2.addWidget( self.btn_done, 0, 0, 1, 1 )
		# Populate the menu with the options settings from core.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self ) :

		self.box['ret'].setChecked( self.core.opt['ret'] )
		self.box['lim'].setChecked( self.core.opt['lim'] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the 'Done' button has been pressed, close the window and
		# return.

		if ( fnc == 'done' ) :

			self.close( )

			return

		# If no threads are running, make the change to the option with
		# core.  Otherwise, restore the original options settings.

		if ( n_thread( ) == 0 ) :

			# Start a new thread that makes the change to the option
			# with core.

			Thread( target=thread_chng_opt,
			        args=( self.core, fnc,
			               self.box[fnc].isChecked( ) ) ).start( )

		else :

			self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A CHANGE OF AN OPTION.
	#-----------------------------------------------------------------------

	def resp_chng_opt( self ) :

		# Regenerate the menu.

		self.make_opt( )
