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

from janus_dialog_opt_para import dialog_opt_para
from janus_dialog_opt_file import dialog_opt_file

################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
################################################################################

class dialog_opt_super( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_super, self ).__init__( )

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

		self.grd.addWidget( self.wdg, 0, 0, 1, 1 )


		self.wdg_opt_para   = dialog_opt_para( self.core   )
		self.wdg_opt_file   = dialog_opt_file( self.core   )

		self.wdg.addTab( self.wdg_opt_para,  'Parameters' )
		self.wdg.addTab( self.wdg_opt_file,   'File Options' )

		# Execute this dialog.

		self.exec_( )
