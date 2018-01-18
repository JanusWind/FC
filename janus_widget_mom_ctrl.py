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
from PyQt4.QtGui import QGridLayout, QLabel, QLineEdit, QWidget, QFont

# Load the customized push button and one-line text editor.

from janus_event_PushButton import event_PushButton
from janus_event_LineEdit import event_LineEdit

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_mom_win_dir, \
                         thread_chng_mom_win_bin


################################################################################
## DEFINE CLASS "widget_mom_ctrl" TO CUSTOMIZE "QWidget" FOR MOM. CONTROL.
################################################################################

class widget_mom_ctrl( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_mom_ctrl, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_mom_win'),
		                                       self.resp_chng_mom_win )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Initialize the text areas, buttons, and labels that comprise
		# this control panel.

		self.txt_win_dir = event_LineEdit( self, 'win_dir' )
		self.txt_win_bin = event_LineEdit( self, 'win_bin' )

		self.lab_win_dir = QLabel( 'Directions per cup:'    )
		self.lab_win_bin = QLabel( 'Bins per direction:'    )

		self.lab_win_dir.setFont( QFont( "Helvetica", 12 ) )
		self.lab_win_bin.setFont( QFont( "Helvetica", 12 ) )

		# Row by row, add the text areas, buttons, and labels to this
		# widget's grid.

		self.grd.addWidget( self.lab_win_dir, 0, 0, 1, 1 )
		self.grd.addWidget( self.txt_win_dir, 0, 1, 1, 1 )

		self.grd.addWidget( self.lab_win_bin, 1, 0, 1, 1 )
		self.grd.addWidget( self.txt_win_bin, 1, 1, 1, 1 )

		# Populate the text areas.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR DISPLAYING TEXT IN THE TEXT AREAS.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Update the "win_dir" text-box based on the value stored in
		# "core".

		if ( self.core.mom_win_dir is None ) :

			self.txt_win_dir.setStyleSheet( "color: red;" )

		else :

			self.txt_win_dir.setTextUpdate(
			                          str( self.core.mom_win_dir ) )

			self.txt_win_dir.setStyleSheet( "color: black;" )

		# Update the "win_bin" text-box based on the value stored in
		# "core". 

		if ( self.core.mom_win_bin is None ) :

			self.txt_win_bin.setStyleSheet( "color: red;" )

		else :

			self.txt_win_bin.setTextUpdate(
			                          str( self.core.mom_win_bin ) )

			self.txt_win_bin.setStyleSheet( "color: black;" )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running, reset
		# the text in the text boxes and abort.

		if ( n_thread( ) != 0 ) :
			self.make_txt( )
			return

		# If the button for automatic point selection has been pressed
		# or the user has pressed "Return" from "self.txt_win_???",
		# read in the values of "win_azm" and "win_cur" from their
		# respective "self.txt_win_???" text boxes and use those values
		# to run the point selection.  Also, ensure that the moments
		# analysis has been set for "dyanmic" mode (since the user
		# presumably wants it this way).

		if ( fnc == 'win_dir' ) :

			Thread( target=thread_chng_mom_win_dir,
				args=( self.core,
			               self.txt_win_dir.text( ) ) ).start( )

		elif ( fnc == 'win_bin' ) :

			Thread( target=thread_chng_mom_win_bin,
				args=( self.core,
			               self.txt_win_bin.text( ) ) ).start( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Update the text area.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mom_win" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mom_win( self ) :

		# Update the text area.

		self.make_txt( )
