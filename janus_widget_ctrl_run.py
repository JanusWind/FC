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

from PyQt4.QtGui import QDialog, QFileDialog, QGridLayout, QWidget
from PyQt4.QtCore import SIGNAL

# Load the customized push button.

from janus_event_PushButton import event_PushButton

# Load the customized dialog windows.

from janus_dialog_opt import dialog_opt
from janus_dialog_missing import dialog_missing
from janus_dialog_auto_ctrl import dialog_auto_ctrl
from janus_dialog_auto_prog import dialog_auto_prog

# Load the modules necessary for time convertion.

from janus_time import calc_time_epc

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_anls_mom, thread_anls_nln, \
                         thread_auto_run, thread_save_res


################################################################################
## DEFINE CLASS "widget_ctrl_run" TO CUSTOMIZE "QWidget" FOR RUNNING ANALYSES.
################################################################################

class widget_ctrl_run( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_ctrl_run, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_spc'),
		                                            self.resp_chng_spc )
		self.connect( self.core, SIGNAL('janus_done_auto_run'),
		                                       self.resp_done_auto_run )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Initialize the primary buttons.

		self.btn_mom  = event_PushButton( self, 'mom' , 'Moments'    )
		self.btn_nln  = event_PushButton( self, 'nln' , 'Non-Linear' )
		self.btn_opt  = event_PushButton( self, 'opt' , 'Options'    )
		self.btn_auto = event_PushButton( self, 'auto', 'Auto-Run'   )

		# Initialize and configure the stop button.

		self.btn_stop = event_PushButton( self, 'stop', 'Stop' )

		self.btn_stop.setStyleSheet( 'QPushButton {color:red}' )

		self.btn_stop.setVisible( False )

		# Add the buttons to this widget's grid.

		self.grd.addWidget( self.btn_stop, 1, 1, 1, 1 )

		self.grd.addWidget( self.btn_mom , 0, 0, 1, 1 )
		self.grd.addWidget( self.btn_nln , 0, 1, 1, 1 )
		self.grd.addWidget( self.btn_opt , 1, 0, 1, 1 )
		self.grd.addWidget( self.btn_auto, 1, 1, 1, 1 )

		# Intialize the variables that will store the user's last
		# requested settings for the automatic analysis.

		self.req_auto_strt = ''
		self.req_auto_stop = ''
		self.req_auto_next = False
		self.req_auto_halt = True

		self.req_opt_temp = True
		self.req_opt_tvel = False
		self.req_opt_skew = True
		self.req_opt_kurt = True

		# Initialize the variable that will hold the progress-bar dialog
		# (if an when one is created).

		self.dia_prog = None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the stop button has been pressed, inform the core to abort
		# the automatic analysis.

		if ( fnc == 'stop' ) :

			# Set the core's indicator of a premature-stop request
			# to "True".

			self.core.stop_auto_run = True

			# Return.

			return

		# If a "thread_*" computation thread is running, abort.

		if ( n_thread( ) != 0 ) :
			return

		# If the "Moments" or "Non-Linear" button has been pressed,
		# execute the requested analysis and return.

		if ( fnc == 'mom' ) :
			if ( n_thread( ) == 0 ) :
				Thread( target=thread_anls_mom,
				        args=( self.core, )     ).start()
			return

		if ( fnc == 'nln' ) :
			if ( n_thread( ) == 0 ) :
				Thread( target=thread_anls_nln,
				        args=( self.core, )     ).start()
			return

		# If the "Options" button has been pressed, launch a dialog box
		# that will allow the user to alter various settings.

		if ( fnc == 'opt' ) :

			# Launch a dialog box to request options from the user.

			dialog_opt( self.core )

			# Return.

			return

		# If the "Auto" button has been pressed, launch the auto-run
		# dialog box.  If the user-input is valid, start a thread to run
		# the reqested analyses on the specified spectra, enable the
		# "stop" button, and return.

		if ( fnc == 'auto' ) :

			# WARNING!  THIS FEATURE IS INCOMPLETE.  DURING
			#           DEVELOPMENT, IT IS ONLY AVAILABLE IN
			#           DEBUGGING MODE.

			# If debugging mode is not active, alert the user and
			# abort.

			if ( not self.core.debug ) :
				dialog_missing( ).alert( )
				return

			# Attempt to find suggested settings for the automated
			# analysis based on the current spectrum loaded (if any)
			# and the previous requests of the user.

			self.req_auto_strt = self.core.time_txt

			if ( self.req_auto_strt == '' ) :
				self.req_auto_stop = ''
				self.req_auto_next = False
			else :
				self.req_auto_next = True
				if ( self.req_auto_stop != '' ) :
					epc_strt = calc_time_epc(
					                    self.req_auto_strt )
					epc_stop = calc_time_epc(
					                    self.req_auto_stop )
					if ( ( epc_strt is None ) or 
					     ( epc_stop is None )    ) :
						self.req_auto_stop = ''
					elif ( epc_strt >= epc_stop ) :
						self.req_auto_stop = ''

			# Launch a dialog box to request a range of times from
			# the user.

			time_rang = dialog_auto_ctrl(
			        time_strt=self.req_auto_strt,
			        time_stop=self.req_auto_stop,
			        get_next=self.req_auto_next   ).get_time_rang( )

			# If the range of times is invalid (which can happen if
			# the user cancels the dialog), return.

			if ( time_rang is None ) :
				return

			# Store the new requested times from the user.

			self.req_auto_strt = time_rang[0]
			self.req_auto_stop = time_rang[1]
			self.req_auto_next = time_rang[2]
			self.req_auto_halt = time_rang[3]

			# Assuming that there still aren't any janus threads
			# running, start a new thread for the automatic analysis
			# and make the "stop" button available for the user to
			# abort that analysis (if so desired).

			if ( n_thread( ) == 0 ) :

				# Start a new thread that automatically loads
				# and processes each spectrum in the time range
				# specified by the user.

				Thread( target=thread_auto_run,
				        args=( self.core,
				               self.req_auto_strt, 
				               self.req_auto_stop,
				               self.req_auto_next,
				               self.req_auto_halt,
				               1                   ) ).start( )

				# Hide the "auto" button and make the "stop"
				# button visible (so that the user can abort the
				# automatic analyis).

				self.btn_auto.setVisible( False )
				self.btn_stop.setVisible( True  )

				self.dia_prog = dialog_auto_prog(
				                           self.req_auto_strt,
				                           self.req_auto_stop  )

			# Return.

			return

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO LOADING OF A NEW SPECTRUM.
	#-----------------------------------------------------------------------

	def resp_chng_spc( self ) :

		# If a progress-bar dialog exists, request that it update based
		# on the timestamp of the new spectrum.

		if ( ( self.dia_prog      is not None ) and
		     ( self.core.time_val is not None )     ) :
			self.dia_prog.updt_bar( self.core.time_val )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE COMPLETION OF AN AUTO-RUN.
	#-----------------------------------------------------------------------

	def resp_done_auto_run( self ) :

		# Hide the "stop" button and make the "auto" button visible.

		self.btn_stop.setVisible( False )
		self.btn_auto.setVisible( True  )

		# Close the progress-bar dialog (if one exists).

		if ( self.dia_prog is not None ) :
			self.dia_prog.close( )
