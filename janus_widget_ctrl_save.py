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

# Load the customized push button.

from janus_event_PushButton import event_PushButton

# Load the customized dialog windows.

from janus_dialog_missing import dialog_missing

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_auto_run, thread_save_res, \
                         thread_xprt_res

# Load the modules for generating file names.

from janus_save import make_name_save, make_name_xprt


################################################################################
## DEFINE CLASS "widget_ctrl_save" TO CUSTOMIZE "QWidget" FOR SAVING TO FILE.
################################################################################

class widget_ctrl_save( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_ctrl_save, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Initialize the buttons that comprise this control panel.

		self.btn_save = event_PushButton( self, 'save', 'Save'    )
		self.btn_xprt = event_PushButton( self, 'xprt', 'Export'  )
		self.btn_rstr = event_PushButton( self, 'rstr', 'Restore' )

		# Add the buttons to this widget's grid.

		self.grd.addWidget( self.btn_save, 0, 0, 1, 1 )
		self.grd.addWidget( self.btn_xprt, 0, 1, 1, 1 )
		self.grd.addWidget( self.btn_rstr, 0, 2, 1, 1 )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is running, abort.

		if ( n_thread( ) != 0 ) :
			return

		# If the "Save" button has been pressed, execute the save of
		# analysis results.

		if ( fnc == 'save' ) :

			# Launch a dialog for the user to select a name and
			# location for the save file.

			nm_fl = str( QFileDialog.getSaveFileName(
			               caption='Save',
			               directory=make_name_save( self.core ) ) )

			# If the user canceled the dialog, abort.

			if ( len( nm_fl ) == 0 ) :
				return

			# Assuming that there still aren't any janus threads
			# running, start a new thread to have the core save its
			# log of analysis results to the user-specified file.

			if ( n_thread( ) == 0 ) :
				Thread( target=thread_save_res,
				        args=( self.core, nm_fl ) ).start()

			# Return

			return

		# If the "Export" button has been pressed, execute the export of
		# analysis results to a plain text file.

		if ( fnc == 'xprt' ) :

			# Launch a dialog for the user to select a name and
			# location for the save file.

			nm_fl = str( QFileDialog.getSaveFileName(
			               caption='Export',
			               directory=make_name_xprt( self.core ) ) )

			# If the user canceled the dialog, abort.

			if ( len( nm_fl ) == 0 ) :
				return

			# Assuming that there still aren't any janus threads
			# running, start a new thread to have the core save its
			# log of analysis results to the user-specified file.

			if ( n_thread( ) == 0 ) :
				Thread( target=thread_xprt_res,
				        args=( self.core, nm_fl ) ).start()

			# Return

			return

		# If the "Restore" button has been pressed, launch a dialog box
		# to load and restore saved results.

		if ( fnc == 'rstr' ) :

			# WARNING!  THIS FEATURE IS INCOMPLETE.  DURING ITS
			#           DEVELOPMENT, IT IS ONLY AVAILABLE IN
			#           DEBUGGING MODE.

			# If debugging mode is not active, alert the user and
			# abort.

			if ( not self.core.debug ) :
				dialog_missing( ).alert( )
				return

			# Return.

			return
