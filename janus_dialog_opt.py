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

# Load the customized push button and one-line text editor.

from janus_event_CheckBox import event_CheckBox
from janus_event_PushButton import event_PushButton

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR AUTO-RUN CONTROL.
################################################################################

class dialog_opt( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_opt'),
		                                            self.resp_chng_opt )

		# Make this a modal dialog (i.e., block user-interaction with
		# the main application window while this dialog exists).

		self.setModal( True )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Options Menu' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg1 = QGridLayout( )
		self.sg2 = QGridLayout( )
		self.sg3 = QGridLayout( )

		self.sg1.setContentsMargins( 0, 0, 0, 0 )
		self.sg2.setContentsMargins( 0, 0, 0, 0 )
		self.sg3.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg1, 0, 0, 1, 1 )
		self.grd.addLayout( self.sg2, 1, 0, 1, 1 )
		self.grd.addLayout( self.sg3, 2, 0, 1, 1 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_disp = QLabel( 'Display Options:'  )
		self.lab_temp = QLabel( 'Temperature:'      )
		self.lab_tvel = QLabel( 'Thermal Velocity:' )
		self.lab_skew = QLabel( 'Skewness:'         )
		self.lab_kurt = QLabel( 'Kurtosis:'         )

		# TODO: change labels to match keys in "self.core.opt"

		self.box = { 'thrm_t':event_CheckBox( self, 'thrm_t' }

		"""
		self.box_temp = event_CheckBox( self, 'thrm_t' )
		self.box_tvel = event_CheckBox( self, 'thrm_w' )
		self.box_skew = event_CheckBox( self, 'skew' )
		self.box_kurt = event_CheckBox( self, 'kurt' )
		"""

		# TODO: remove buttons (at least for now).

		self.btn_appl = event_PushButton( self, 'appl', 'Apply'  )
		self.btn_cncl = event_PushButton( self, 'cncl', 'Cancel' )

		# Adjust the button defaults.

		self.btn_appl.setDefault( False )
		self.btn_cncl.setDefault( False )

		self.btn_appl.setAutoDefault( False )
		self.btn_cncl.setAutoDefault( False )

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.sg1.addWidget( self.lab_disp, 0, 0, 1, 1 )

		self.sg2.addWidget( self.lab_temp, 0, 0, 1, 1 )
		self.sg2.addWidget( self.box_temp, 0, 1, 1, 1 )
		self.sg2.addWidget( self.lab_tvel, 1, 0, 1, 1 )
		self.sg2.addWidget( self.box_tvel, 1, 1, 1, 1 )
		self.sg2.addWidget( self.lab_skew, 2, 0, 1, 1 )
		self.sg2.addWidget( self.box_skew, 2, 1, 1, 1 )
		self.sg2.addWidget( self.lab_kurt, 3, 0, 1, 1 )
		self.sg2.addWidget( self.box_kurt, 3, 1, 1, 1 )

		self.sg3.addWidget( self.btn_appl, 0, 0, 1, 1 )
		self.sg3.addWidget( self.btn_cncl, 0, 1, 1, 1 )

		# Populate the menu with the options settings from core.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self ) :

		self.box_temp.setChecked( self.core.opt['thrm_t']

		#TODO: Rename "box_?" variables to match "self.core.opt."

		#TODO: Code to set state of other boxes.

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If no threads are running, make the change to the option with
		# core.  Otherwise, restore the original options settings.\

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
