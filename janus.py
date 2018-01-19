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

# Load the operating system modules.

import os

# Load the necessary "Qt" modules.

from PyQt4.QtGui import QFont, QGridLayout, QIcon, QWidget

# Load the necessary "janus" modules.

from janus_core import core

from janus_custom_Application import custom_Application
from janus_custom_MainWindow import custom_MainWindow

from janus_widget_fc import widget_fc
from janus_widget_ctrl import widget_ctrl
from janus_widget_mfi import widget_mfi
from janus_widget_mom import widget_mom
from janus_widget_nln import widget_nln


################################################################################
## DEFINE THE "janus" CLASS FOR LOADING, PLOTING, AND FITTING Wind/FC SPECTRA.
################################################################################

class janus( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, time=None ) :

		# If the necessary subdirectories do not exist, create them.

		dname = os.path.dirname( __file__ )

		lst = [ os.path.join( dname, 'data'                     ),
		        os.path.join( dname, 'data'   , 'fc'            ),
		        os.path.join( dname, 'data'   , 'mfi'           ),
			os.path.join( dname, 'data'   , 'mfi'   ,'hres' ),
			os.path.join( dname, 'data'   , 'mfi'   ,'lres' ),
		        os.path.join( dname, 'data'   , 'spin'          ),
		        os.path.join( dname, 'results'                  ),
		        os.path.join( dname, 'results', 'save'          ),
		        os.path.join( dname, 'results', 'export'        )  ]

		for d in lst :
			if ( not os.path.isdir( d ) ) :
				os.mkdir( d )

		# Initialize an instance of "fc_spec" with the Wind/FC ion
		# spectrum whose timestamp is closest to the time requested.

		self.core = core( time=time )

		# Initialize the application.

		self.app = custom_Application( self.core, res_lo=False )

		if ( self.app.res_lo ) :
			self.app.setFont( QFont( 'Helvetica', 8 ) )

		self.core.app = self.app

		# Load and set the application Icon

		self.icn = QIcon( 'janus.svg' )

		self.app.setWindowIcon( self.icn )

		# Initialize the application's main window.

		self.win = custom_MainWindow( self.core )

		self.win.setWindowTitle(
		               'Janus -- Wind/FC Data Navigation and Analysis' )

		# Display the application's main window.

		# Note.  Even though the application windows doesn't seem to be
		#        rendered on the screen until later, having these here
		#        (i.e., before the creation of the widgets) seems to
		#        help things to run more smoothly.  If issues arise with
		#        grid spacing in one (or more) of the widgets, reversing
		#        the order of these commands and/or moving them to right
		#        before "self.app_(exec)" may help.

		self.win.show( )

		if ( self.app.res_lo ) :
			self.win.resize(  600, 400 )
		else :
			self.win.resize( 1200, 800 )

		# Initialize a widget with a grid layout and set it as the main
		# window's central widget.

		self.grd = QGridLayout( )
		self.cen = QWidget( )

		self.cen.setLayout( self.grd )

		self.win.setCentralWidget( self.cen )

		# Initialize the widgets.

		self.wdg_fcs = widget_fc(   self.core )

		self.wdg_ctr = widget_ctrl( self.core )
		self.wdg_mfi = widget_mfi(  self.core )
		self.wdg_mom = widget_mom(  self.core )
		self.wdg_nln = widget_nln(  self.core )

		# Add the widgets to the grid layout of the main window's
		# central widget.

		#   |   0   |   1   |   2   |   3   |   4   |
		# --+-------+-------+-------+-------+-------+
		#   |                       |               |
		# 0 |                       |      ctr      |
		#   |                       |               |
		# --+                       +-------+-------+
		#   |                       |       |       |
		# 1 |          fcs          |  mfi  |  mom  |
		#   |                       |       |       |
		# --+                       +-------+-------+
		#   |                       |               |
		# 2 |                       |      nln      |
		#   |                       |               |
		# --+-----------------------+---------------+

		self.grd.addWidget( self.wdg_fcs, 0, 0, 3, 3 )

		self.grd.addWidget( self.wdg_ctr, 0, 3, 1, 2 )

		self.grd.addWidget( self.wdg_mfi, 1, 3, 1, 1 )
		self.grd.addWidget( self.wdg_mom, 1, 4, 1, 1 )

		self.grd.addWidget( self.wdg_nln, 2, 3, 1, 2 )

		# Set the minimum size of each widget.

		self.wdg_fcs.setMinimumSize( 300, 300 )

		self.wdg_ctr.setMinimumSize( 200, 100 )
		self.wdg_nln.setMinimumSize( 200, 100 )

		self.wdg_mfi.setMinimumSize( 100, 100 )
		self.wdg_mom.setMinimumSize( 100, 100 )

		# Regularize the grid spacing.

		self.grd.setColumnStretch( 0, 1 )
		self.grd.setColumnStretch( 1, 1 )
		self.grd.setColumnStretch( 2, 1 )
		self.grd.setColumnStretch( 3, 1 )
		self.grd.setColumnStretch( 4, 1 )

		self.grd.setRowStretch( 0, 1 )
		self.grd.setRowStretch( 1, 1 )
		self.grd.setRowStretch( 2, 1 )

		# Prepare for user interaction.

		self.app.exec_( )
