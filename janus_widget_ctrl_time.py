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

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QGridLayout, QWidget

# Load the customized push button and one-line text editor.

from janus_event_PushButton import event_PushButton
from janus_event_LineEdit import event_LineEdit

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_load_spec, thread_anls_mom, \
                         thread_anls_nln


################################################################################
## DEFINE CLASS "widget_ctrl_time" TO CUSTOMIZE "QWidget" FOR TIMESTAMP CONTROL.
################################################################################

class widget_ctrl_time( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_ctrl_time, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_spc'),
		                                            self.resp_chng_spc )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Initialize the text areas and buttons that comprise this
		# control panel.

		self.txt_timestp = event_LineEdit(   self, 'goto' )
		self.btn_goto_sp = event_PushButton( self, 'goto', 'Go' )

		self.btn_prev_hr = event_PushButton( self, '-1hr', '<<' )
		self.btn_prev_sp = event_PushButton( self, '-1sp', '<'  )
		self.btn_next_sp = event_PushButton( self, '+1sp', '>'  )
		self.btn_next_hr = event_PushButton( self, '+1hr', '>>' )

		# Row by row, add the text areas and buttons to this widget's
		# grid.

		self.grd.addWidget( self.txt_timestp, 0, 0, 1, 3 )
		self.grd.addWidget( self.btn_goto_sp, 0, 3, 1, 1 )

		self.grd.addWidget( self.btn_prev_hr, 1, 0, 1, 1 )
		self.grd.addWidget( self.btn_prev_sp, 1, 1, 1, 1 )
		self.grd.addWidget( self.btn_next_sp, 1, 2, 1, 1 )
		self.grd.addWidget( self.btn_next_hr, 1, 3, 1, 1 )

		# Populate the text area.

		self.make_txt( )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR DISPLAYING TEXT IN THE TEXT AREAS.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Clear any existing text from the text areas.

		self.txt_timestp.setTextUpdate( '' )

		# Set the text in "self.txt_timestp" to be that for the
		# timestamp of "self.core".  Adjust the text color based on the
		# stated validity of this timestamp.

		self.txt_timestp.setTextUpdate( self.core.time_txt )

		if ( self.core.time_vld ) :
			self.txt_timestp.setStyleSheet( 'color: black;' )
		else :
			self.txt_timestp.setStyleSheet( 'color: red;' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running, reset
		# the text in the text box and abort.

		if ( n_thread( ) != 0 ) :
			self.make_txt( )
			return

		# Note.  All of the remaining cases spawn a "thread_load_spec"
		#        thread.  I have found that having "core.load_spec" only
		#        emit the "janus_rset" signal for itself (i.e., from
		#        within the thread) causes irregularities in the
		#        display.  Emitting this signal immediately before this
		#        thread is spwaned ensures that all the relevent widgets
		#        reset before any new data are loaded.

		# If the "Go To" button has been pressed or the user has pressed
		# "Return" from the text area, go to the spectrum with the
		# timestamp closest to the one specified by the user in the text
		# area "self.txt_timesto".

		if ( fnc == 'goto' ) :
			if ( n_thread( ) == 0 ) :
				self.core.emit( SIGNAL('janus_rset') )
				time_req = str( self.txt_timestp.text( ) )
				Thread( target=thread_load_spec,
				        args=( self.core, time_req ) ).start()
			return

		# If a spectrum has not already been loaded, abort (since the
		# remaining buttons all function relative to the timestamp of
		# "self.core").

		if ( self.core.time_epc is None ) :
			return

		# Load a Wind/FC ion spectrum based the type of button pressed.

		if ( fnc == '-1hr' ) :
			if ( n_thread( ) == 0 ) :
				self.core.emit( SIGNAL('janus_rset') )
				Thread( target=thread_load_spec,
				        args=( self.core,
				          self.core.time_val - 3600. ) ).start()
			return

		if ( fnc == '-1sp' ) :
			if ( n_thread( ) == 0 ) :
				self.core.emit( SIGNAL('janus_rset') )
				Thread( target=thread_load_spec,
				        args=( self.core,
				               self.core.time_val,
				               True, False         ) ).start()
			return

		if ( fnc == '+1sp' ) :
			if ( n_thread( ) == 0 ) :
				self.core.emit( SIGNAL('janus_rset') )
				Thread( target=thread_load_spec,
				        args=( self.core,
				               self.core.time_val,
				               False, True         ) ).start()
			return

		if ( fnc == '+1hr' ) :
			if ( n_thread( ) == 0 ) :
				self.core.emit( SIGNAL('janus_rset') )
				Thread( target=thread_load_spec,
				        args=( self.core,
				          self.core.time_val + 3600. ) ).start()
			return

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING A CHANGE TO THE FC ION SPECTRUM.
	#-----------------------------------------------------------------------

	def resp_chng_spc( self ) :

		# Update the text areas.

		self.make_txt( )
