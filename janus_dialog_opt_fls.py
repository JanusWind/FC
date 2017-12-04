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

class dialog_opt_fls( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_fls, self ).__init__( )

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

		self.sg = QGridLayout( )

		self.sg.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg, 0, 0, 14, 3 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_hdr1 = QLabel( 'Maximum # of saved downloaded files'  )
		self.lab_hdr2 = QLabel( '( Use "inf" for no limit)'            )
		self.lab_fc   = QLabel( 'FC Files'                             )
		self.lab_mfi  = QLabel( 'MFI Files'                            )
		self.lab_spin = QLabel( 'Spin Files'                           )

		self.txt_fc    = event_LineEdit( self, 'nfile_fc'   )
		self.txt_mfi   = event_LineEdit( self, 'nfile_mfi'  )
		self.txt_spin  = event_LineEdit( self, 'nfile_spin' )

		self.box = { 'nfile_fc'  :event_CheckBox( self, 'nfile_fc'   ),
		             'nfile_mfi' :event_CheckBox( self, 'nfile_mfi'  ),
		             'nfile_spin':event_CheckBox( self, 'nfile_spin' )   }

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.sg.addWidget( self.lab_hdr1, 0, 0, 1, 1 )
		self.sg.addWidget( self.lab_hdr2, 1, 0, 1, 1 )
		self.sg.addWidget( self.lab_fc,   2, 0, 1, 1 )
		self.sg.addWidget( self.txt_fc,   2, 1, 1, 1 )
		self.sg.addWidget( self.lab_mfi,  3, 0, 1, 1 )
		self.sg.addWidget( self.txt_mfi,  3, 1, 1, 1 )
		self.sg.addWidget( self.lab_spin, 4, 0, 1, 1 )
		self.sg.addWidget( self.txt_spin, 4, 1, 1, 1 )

		# Populate the menu with the options settings from core.
#
		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETRIEVING THE TEXT FROM INPUT BOXES.
	#-----------------------------------------------------------------------

#	def rtrv_txt( self ) :
#
#                # Attempt to retrieve each input text.
#
#                self.nfile_fc = self.txt

#	#-----------------------------------------------------------------------
#	# DEFINE THE FUNCTION FOR VALIDATING TEXT FROM INPUT.
#	#-----------------------------------------------------------------------
#
	def vldt_txt( self ) :

		txt = self.txt_fc.text( )
		print txt, '1'
		if( txt is ' ' ) :
			val = None
			print val,'2'
		else :
			try:
				val = str_to_nni ( txt )
				print val,'3'
			except :
				val = None
				print val,'4'
		if( ( ( val is None ) and ( txt == ' ' ) ) or
		      ( val == self.core.opt_fls['nfile_fc'] ) ) :

			self.txt_fc.setStyleSheet( 'color: black;' )
			self.txt_fc.setStyleSheet( 'color: black;' )
			print '5'
		else :
			self.txt_fc.setStyleSheet( 'color: red;' )
			self.txt_fc.setStyleSheet( 'color: red;' )
			print '6'

#	#-----------------------------------------------------------------------
#	# DEFINE THE FUNCTION FOR POPULATING MENU.
#	#-----------------------------------------------------------------------
#
	def make_opt( self ) :
#
		val = self.core.opt_fls['nfile_fc']
		print val,'7'

		self.vldt_txt( )
	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If no threads are running, make the change to the option with
		# core.  Otherwise, restore the original options settings.

		if ( self.vldt_txt ) :

			self.resp_chng_opt

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A CHANGE OF AN OPTION.
	#-----------------------------------------------------------------------

	def resp_chng_opt( self ) :

		# Regenerate the menu.

		self.make_opt( )
