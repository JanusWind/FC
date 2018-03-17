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
		self.connect( self.core, SIGNAL('janus_rstr_opt'),
		                                            self.resp_rstr_opt )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg = QGridLayout( )

		self.sg.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg, 4, 3, 8, 3)

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_hdr1 = QLabel(
		                'Maximum number of saved downloaded files'  )
		self.lab_hdr2 = QLabel( '( Use "inf" for no limit )'        )
		self.lab_hdr3 = QLabel( 'MFI Resolution'                    )

		self.lab1 = { 'fls_max_fc'    :QLabel( 'FC Files'         ),
		              'fls_max_spin'  :QLabel( 'Spin Files'       ),
		              'fls_max_mfi_l' :QLabel(
		                              'Low Resolution MFI Files'  ),
		              'fls_max_mfi_h' :QLabel(
		                              'High Resolution MFI Files' )    }

		self.lab2 = {
		   'fls_src_low'  :QLabel( 'Low Resolution (0.3 Hz) ', self ),
		   'fls_src_high' :QLabel( 'High Resolution (11 Hz)' , self )  }

		self.arr_txt = {
		      'fls_max_fc'    :event_LineEdit( self, 'fls_max_fc'    ),
		      'fls_max_spin'  :event_LineEdit( self, 'fls_max_spin'  ),
		      'fls_max_mfi_l' :event_LineEdit( self, 'fls_max_mfi_l' ),
		      'fls_max_mfi_h' :event_LineEdit( self, 'fls_max_mfi_h' ) }

		self.box1 = {
		      'fls_src_low'  :event_RadioBox( self, 'fls_src_low'  ),
		      'fls_src_high' :event_RadioBox( self, 'fls_src_high'  )  }

		self.order1 = [ 'fls_max_fc', 'fls_max_spin', 'fls_max_mfi_l',
		                'fls_max_mfi_h'                                ]

		self.order2 = [ 'fls_src_low','fls_src_high' ]

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.lab_hdr1.setFont( QFont( "Helvetica", 12, QFont.Bold ) )
		self.lab_hdr2.setFont( QFont( "Helvetica", 12 ) )

		self.sg.addWidget( self.lab_hdr1, 0, 0, 1, 3 )
		self.sg.addWidget( self.lab_hdr2, 1, 0, 1, 3 )

		for i, key in enumerate( self.order1 ) :

			self.lab1[key].setFont( QFont(    "Helvetica", 12 ) )
			self.arr_txt[key].setFont( QFont( "Helvetica", 12 ) )

			self.sg.addWidget( self.arr_txt[key], 2+i, 0, 1, 1 )
			self.sg.addWidget( self.lab1[key],    2+i, 1, 1, 1 )
			self.arr_txt[key].setMaximumWidth( 40 )

		self.lab_hdr3.setFont( QFont( "Helvetica", 12, QFont.Bold ) )
		self.sg.addWidget( self.lab_hdr3, 6, 0, 1, 3 )

		for i, key in enumerate( self.order2 ) :

			self.lab2[key].setFont( QFont( "Helvetica", 12 ) )
			self.box1[key].setFont( QFont( "Helvetica", 12 ) )

			self.sg.addWidget( self.box1[key], 7+i, 0, 1, 1 )
			self.sg.addWidget( self.lab2[key], 7+i, 1, 1, 1 )
			self.box1[key].setMaximumWidth( 40 )

		# Populate the menu with the options settings from core.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self, clear=False ) :

		# If the clear option has been selected, delete the contents of
		# all text boxes prior to proceeding.

		if ( clear ) :

			for key in self.arr_txt :

				self.arr_txt[key].clear( )

		# Validate/update the displayed options.

		self.box1['fls_src_low' ].setCheckedSilent(
		                                 self.core.opt['fls_src_low' ] )
		self.box1['fls_src_high' ].setCheckedSilent(
		                                 self.core.opt['fls_src_high'] )

		for key in self.arr_txt :

			val = self.core.opt[key]

			txt = self.arr_txt[key].text( )

			if( txt == '' ) :
				val = None
			else :
				try:
					val = str_to_nni( txt )
				except :
					val = None
	
			if( ( ( val is None ) and ( txt == '' ) ) or
			      ( val == self.core.opt[key]     ) )   :
	
				self.arr_txt[key].setStyleSheet(
				                               'color: black;' )
	
				txt = str( self.core.opt[key] )
			else :
	
				self.arr_txt[key].setStyleSheet( 'color: red;' )

			self.arr_txt[key].setTextUpdate( txt )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		if( ( fnc == 'fls_src_low' ) or ( fnc == 'fls_src_high' ) ) :

			if ( n_thread( ) == 0 ) :

			# Start a new thread that makes the change to the option
			# with core.

				Thread( target=thread_chng_opt,
				        args=( self.core, fnc,
				        self.box1[fnc].isChecked( ) ) ).start( )

		else :
			txt = self.arr_txt[fnc].text( )

			try :
				val = str_to_nni( txt )
			except :
				val = None
        
			# If no threads are running, make the change to the 
			# option with core.  Otherwise, restore the original
			# options settings.
        
			if ( ( n_thread( ) == 0 ) and ( val is not None ) ) :
		
				# Start a new thread that makes the change to
				# the option with core.
		
				Thread( target=thread_chng_opt,
				        args=( self.core, fnc, val ) ).start( )
		
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

		self.make_opt( clear=True )
