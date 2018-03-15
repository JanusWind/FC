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
from numpy import inf

# Load the customized push button and one-line text editor.

from janus_event_CheckBox import event_CheckBox, event_RadioBox
from janus_event_LineEdit import event_LineEdit
from janus_event_PushButton import event_PushButton

from janus_helper import str_to_nni

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
################################################################################

class dialog_opt_mfi( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_mfi, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_opt'),
		                                            self.resp_chng_opt )
		self.connect( self.core, SIGNAL('janus_rstr_opt'),
		                                            self.resp_rstr_opt )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg = QGridLayout( )

		self.sg.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg, 4, 3, 4, 3)

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_hdr = QLabel( 'MFI Set Style'                     )

		self.lab = { 'mfi_set_raw' :QLabel( 'Raw Data ',     self ),
		             'mfi_set_fit' :QLabel( 'Fit Data' ,     self ),
		             'mfi_set_smt' :QLabel( 'Smoothed Data', self )   }

		self.box = {
		         'mfi_set_raw' :event_RadioBox( self, 'mfi_set_raw' ),
		         'mfi_set_fit' :event_RadioBox( self, 'mfi_set_fit' ),
		         'mfi_set_smt' :event_RadioBox( self, 'mfi_set_smt' ) }

		self.order = [ 'mfi_set_raw', 'mfi_set_fit', 'mfi_set_smt' ]

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.lab_hdr.setFont( QFont( "Helvetica", 12, QFont.Bold ) )

		self.sg.addWidget( self.lab_hdr, 0, 0, 1, 3 )

		for i, key in enumerate( self.order ) :

			self.lab[key].setFont( QFont( "Helvetica", 12 ) )
			self.box[key].setFont( QFont( "Helvetica", 12 ) )

			self.sg.addWidget( self.box[key], 1+i, 0, 1, 1 )
			self.sg.addWidget( self.lab[key], 1+i, 1, 1, 1 )
			self.box[key].setMaximumWidth( 40 )

		# Populate the menu with the options settings from core.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self, clear=False ) :

		self.box['mfi_set_raw'].setChecked( self.core.opt['mfi_set_raw'] )
		self.box['mfi_set_fit'].setChecked( self.core.opt['mfi_set_fit'] )
		self.box['mfi_set_smt'].setChecked( self.core.opt['mfi_set_smt'] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

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

		# Regenerate the menu (without clearing any contents already
		# therein).

		self.make_opt( clear=False )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A RESTORE OF OPTIONS.
	#-----------------------------------------------------------------------

	def resp_rstr_opt( self ) :

		# Clear the menu contents and regenerate it.

		self.make_opt( )
