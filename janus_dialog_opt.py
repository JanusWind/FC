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
from janus_event_LineEdit import event_LineEdit
from janus_event_PushButton import event_PushButton

# Load the modules necessary for time convertion.

from janus_time import calc_time_epc, calc_time_sec, calc_time_str


################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR AUTO-RUN CONTROL.
################################################################################

class dialog_opt( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, temp=True, tvel=True,
	                    skew=True, kurt= True ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt, self ).__init__( )

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
		self.sg4 = QGridLayout( )


		self.sg1.setContentsMargins( 0, 0, 0, 0 )
		self.sg2.setContentsMargins( 0, 0, 0, 0 )
		self.sg3.setContentsMargins( 0, 0, 0, 0 )
		self.sg4.setContentsMargins( 0, 0, 0, 0 )


		self.grd.addLayout( self.sg1, 0, 0, 1, 1 )
		self.grd.addLayout( self.sg2, 1, 0, 1, 1 )
		self.grd.addLayout( self.sg3, 2, 0, 1, 1 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_disp = QLabel( 'Display Options:'   )
		self.lab_temp = QLabel( 'Temperature:'      )
		self.lab_tvel = QLabel( 'Thermal Velocity:' )
		self.lab_skew = QLabel( 'Skewness:'         )
		self.lab_kurt = QLabel( 'Kurtosis:'         )

		self.box_temp = event_CheckBox( self, 'temp' )
		self.box_tvel = event_CheckBox( self, 'tvel' )
		self.box_skew = event_CheckBox( self, 'skew' )
		self.box_kurt = event_CheckBox( self, 'kurt' )


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

		self.aply_opt( temp=temp, tvel=tvel, skew=skew, kurt=kurt )

		self.ret = None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR APPLYING OPTIONS.
	#-----------------------------------------------------------------------

	def aply_opt( self, temp=None, tvel=None, skew=None, kurt=None ) :

		# If requested, update the state of checkbox(es).

		if ( temp is not None ) :
			self.box_temp.setChecked( temp )

		if ( tvel is not None ) :
			self.box_tvel.setChecked( tvel )


		if ( skew is not None ) :
			self.box_skew.setChecked( skew )


		if ( kurt is not None ) :
			self.box_kurt.setChecked( kurt )

		self.rtrv_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETRIEVING THE ROPTIONS.
	#-----------------------------------------------------------------------

	def rtrv_opt( self ) :

		# Attempt to retrieve each timestamp.

		# Note.  If the function "calc_time_epc" is given input that it
		#        cannot process, it should return "None".

		self.temp = self.box_temp.isChecked( )
		self.tvel = self.box_tvel.isChecked( )
		self.skew = self.box_skew.isChecked( )
		self.kurt = self.box_kurt.isChecked( )

		# Validate the timestamps and update the text color of the text
		# boxes appropriately.

		self.vldt_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR VALIDATING THE OPTIONS.
	#-----------------------------------------------------------------------

	def vldt_opt( self ) :

		return

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the event was from the cancel button, close this dialog
		# window.

		if ( fnc == 'cncl' ) :

			self.close( )

			return

		# If the event was from the auto-run button and the timestamp
		# range is valid, generate the return object and close this
		# dialog window.

		if ( ( fnc == 'appl' ) ) :

			self.ret = ( self.temp, self.tvel,
			             self.skew, self.kurt    )

			self.close( )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROMPTING THE USER FOR OPTIONS.
	#-----------------------------------------------------------------------

	def get_opt_men( self ) :

		# Execute this dialog.

		self.exec_( )

		# Return the return objects.

		return self.ret
