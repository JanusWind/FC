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

		self.grd.addWidget( self.wdg, 0, 0, 13, 3 )
		self.grd.addLayout( self.sg,  14, 1, 1, 1 )

		self.wdg_opt_par   = dialog_opt_par( self.core   )
		self.wdg_opt_fls   = dialog_opt_fls( self.core   )

		self.wdg.addTab( self.wdg_opt_par, 'Results'   )
		self.wdg.addTab( self.wdg_opt_fls, 'File Options' )

		self.btn_close = event_PushButton( self, 'close', 'Close' )

		self.btn_close.setAutoDefault( False )

		self.sg.addWidget( self.btn_close, 0, 0, 1, 1 )

		# Execute this dialog.

		self.exec_( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the 'Close' button has been pressed, close the window and
		# return.

		if ( fnc == 'close' ) :

			self.close( )

			return
