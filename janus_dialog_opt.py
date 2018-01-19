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

from PyQt4.QtGui import QDialog, QGridLayout, QTabWidget

from janus_dialog_opt_par import dialog_opt_par
from janus_dialog_opt_fls import dialog_opt_fls
from janus_event_PushButton import event_PushButton

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_rstr_opt

################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
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

		# Make this a modal dialog (i.e., block user-interaction with
		# the main application window while this dialog exists).

		self.setModal( True )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Options Menu' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Add a QTabWidget.

		self.wdg = QTabWidget( )
		self.sg  = QGridLayout( )

		self.grd.addWidget( self.wdg, 0, 0, 1, 1 )
		self.grd.addLayout( self.sg,  2, 0, 1, 1 )

		self.wdg_opt_par   = dialog_opt_par( self.core   )
		self.wdg_opt_fls   = dialog_opt_fls( self.core   )

		self.wdg.addTab( self.wdg_opt_par, 'Results'   )
		self.wdg.addTab( self.wdg_opt_fls, 'File Options' )

		self.btn_rstr  = event_PushButton(
		                          self, 'rstr', 'Restore Default' )
		self.btn_close = event_PushButton( self, 'close', 'Close' )

		self.btn_rstr.setAutoDefault(  False )
		self.btn_close.setAutoDefault( False )

		self.sg.addWidget( self.btn_rstr , 1, 0, 1, 1 )
		self.sg.addWidget( self.btn_close, 1, 1, 1, 1 )

		# Execute this dialog.

		self.exec_( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# Take the appropriate action based on which button was pressed.

		if ( fnc == 'close' ) :

			# Close the window.

			self.close( )

		elif ( fnc == 'rstr' ) :

			# If no other threads are currently running, start a new
			# thread to restore the default values for all option.

			if ( n_thread( ) == 0 ) :

				Thread( target=thread_rstr_opt,
				        args=( self.core, )     ).start( )
