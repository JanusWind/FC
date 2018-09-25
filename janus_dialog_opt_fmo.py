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

from janus_helper import str_to_nni

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt_fmo" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
################################################################################

class dialog_opt_fmo( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_fmo, self ).__init__( )

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

		self.grd.addLayout( self.sg, 0, 0, 7, 2 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_hdr1 = QLabel( 'Select Algorithm' )
		self.lab_hdr2 = QLabel( 'Select the median Filter size' )
		self.lab_hdr3 = QLabel(
		                      'Select the running average window size' )

		self.lab1 = {
		     'mom_fit_crv' :QLabel( 'Use Curve Fit algorithm', self ),
		     'mom_fit_fft' :QLabel( 'Use Fourier algorithm'  , self ), }

		self.lab2 = {
		    'mom_med_fil':QLabel( 'Assign the size of median filter' ) }

		self.lab3 = {
		              'mom_run_win':QLabel(
		                 'Assign the size of running average window' ) }

		self.arr_txt = {
		          'mom_med_fil': event_LineEdit( self, 'mom_med_fil' ),
		          'mom_run_win': event_LineEdit( self, 'mom_run_win' ) }

		self.box = { 
		         'mom_fit_crv' :event_RadioBox( self, 'mom_fit_crv' ),
		         'mom_fit_fft' :event_RadioBox( self, 'mom_fit_fft' )  }


		self.order1 = [ 'mom_fit_crv', 'mom_fit_fft' ]

		self.order2 = [ 'mom_med_fil' ]

		self.order3 = [ 'mom_run_win' ]

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.lab_hdr1.setFont( QFont( "Helvetica", 12, QFont.Bold ) )
		self.lab_hdr2.setFont( QFont( "Helvetica", 12, QFont.Bold ) )
		self.lab_hdr3.setFont( QFont( "Helvetica", 12, QFont.Bold ) )

		self.sg.addWidget( self.lab_hdr1, 0, 0, 1, 3 )
		self.sg.addWidget( self.lab_hdr2, 3, 0, 1, 3 )
		self.sg.addWidget( self.lab_hdr3, 5, 0, 1, 3 )

		for i, key in enumerate( self.order1 ) :

			self.box[key].setFont(  QFont( "Helvetica", 12 ) )
			self.lab1[key].setFont( QFont( "Helvetica", 12 ) )
			self.sg.addWidget( self.box[key], 1+i, 0, 1, 1 )
			self.sg.addWidget( self.lab1[key], 1+i, 1, 1, 1 )
			self.box[key].setMaximumWidth( 40 )

		for i, key in enumerate( self.order2 ) :

			self.lab2[key].setFont(     QFont( "Helvetica", 12 ) )
			self.arr_txt[key].setFont( QFont( "Helvetica", 12 ) )

			self.sg.addWidget( self.arr_txt[key], 4+i, 0, 1, 1 )
			self.sg.addWidget( self.lab2[key],  4+i, 1, 1, 1 )
			self.arr_txt[key].setMaximumWidth( 60 )
			self.arr_txt[key].setMaximumWidth( 40 )

		for i, key in enumerate( self.order3 ) :

			self.lab3[key].setFont(     QFont( "Helvetica", 12 ) )
			self.arr_txt[key].setFont( QFont( "Helvetica", 12 ) )

			self.sg.addWidget( self.arr_txt[key], 6+i, 0, 1, 1 )
			self.sg.addWidget( self.lab3[key],  6+i, 1, 1, 1 )
			self.arr_txt[key].setMaximumWidth( 60 )
			self.arr_txt[key].setMaximumWidth( 40 )

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

		self.box['mom_fit_crv' ].setCheckedSilent(
		                                 self.core.opt['mom_fit_crv' ] )
		self.box['mom_fit_fft' ].setCheckedSilent(
		                                 self.core.opt['mom_fit_fft' ] )

		for key in self.arr_txt :

			val = self.core.opt[key]

			txt = self.arr_txt[key].text( )

			self.key = key

			if( txt == '' ) :
				val = None
			else :
				try:
					val = str_to_nni( txt )
				except :
					val = None
	
			if( ( ( val is None ) and ( txt == '' ) ) or
			      ( val == self.core.opt[key]     )   or
			      ( val%2 != 0                    )      ) :
	
				self.arr_txt[key].setStyleSheet(
				                               'color: black;' )
	
				txt = str( self.core.opt[key] )

			if( self.key == 'mom_med_fil' ) :

				if( ( val is not None )  and ( val%2 == 0 ) ) :

					self.arr_txt[key].setStyleSheet(
					                         'color: red;' )

			elif( self.key == 'mom_run_win' ) :

				if( ( val is not None ) and ( val%2 != 0 ) ) :

					self.arr_txt[key].setStyleSheet(
					                         'color: red;' )


#				raise TypeError('Median filter length must be odd')

			self.arr_txt[key].setTextUpdate( txt )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		if( ( fnc == 'mom_fit_crv' ) or ( fnc == 'mom_fit_fft' ) ) :

			if ( n_thread( ) == 0 ) :

			# Start a new thread that makes the change to the option
			# with core.

				Thread( target=thread_chng_opt,
				        args=( self.core, fnc,
				        self.box[fnc].isChecked( ) ) ).start( )

			else :

				self.make_opt( )

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

		# Regenerate the menu.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO RESTORING DEFAULT OPTIONS.
	#-----------------------------------------------------------------------

	def resp_rstr_opt( self ) :

		# Regenerate the menu.

		self.make_opt( clear=True )