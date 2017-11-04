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

from PyQt4.QtGui import QDialog, QGridLayout, QLabel, QProgressBar

# Load the customized push button module.

from janus_event_PushButton import event_PushButton

# Load the function for calculating time values.

from janus_time import calc_time_val


################################################################################
## DEFINE CLASS "dialog_auto_prog" TO CUSTOMIZE "QDialog" A FOR PROGRESS BAR.
################################################################################

class dialog_auto_prog( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, time_strt, time_stop ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_auto_prog, self ).__init__( )

		# Make this a non-modal dialog (i.e., allow the user to still
		# interact with the main application window).

		self.setModal( False )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Progress' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Initialize the progress bar and set its minimum, maximum, and
		# initial values.

		self.bar = QProgressBar( )

		self.bar.setMinimum( calc_time_val( time_strt ) )
		self.bar.setMaximum( calc_time_val( time_stop ) )

		self.bar.setValue( self.bar.minimum( ) )

		# Initialize the event button.

		self.btn_exit = event_PushButton( self, 'exit', 'Close' )

		# Initialize the label.

		self.lab = QLabel( 'Note: closing this window will *NOT* ' +
		                   'interrupt the automated analysis.'       )

		self.lab.setWordWrap( True )

		# Row by row, add the bar and buttons to the grid layout.

		self.grd.addWidget( self.bar     , 0, 0, 1, 1 )
		self.grd.addWidget( self.btn_exit, 0, 1, 1, 1 )

		self.grd.addWidget( self.lab     , 1, 0, 1, 2 )

		# Display this dialog.

		self.show( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR UPDATING THE PROGRESS BAR.
	#-----------------------------------------------------------------------

	def updt_bar( self, time ) :

		# Convert this functions argument (i.e., the timestamp of the
		# current spectrum) to Unix time.

		time_curr = calc_time_val( time )

		# If necessary, adjust the minimum or maximum of the progress
		# bar based on the new timestamp.

		if ( time_curr < self.bar.minimum( ) ) :
			self.bar.setMinimum( time_curr )

		if ( time_curr > self.bar.maximum( ) ) :
			self.bar.setMaximum( time_curr )

		# Update the value of the progress bar.

		self.bar.setValue( time_curr )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the close button was pressed, close this dialog.

		if ( fnc == 'exit' ) :

			self.close( )

			return
