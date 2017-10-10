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

from PyQt4.QtGui import QFileDialog, QMainWindow
from PyQt4.QtCore import SIGNAL

from janus_dialog_save import dialog_save

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_auto_run, thread_save_res, \
                         thread_xprt_res

# Load the modules for generating file names.

from janus_save import make_name_save, make_name_xprt

# Load the module for sleeping.

from time import sleep


################################################################################
## DEFINE THE "custom_MainWindow" CLASS TO CUSTOMIZE "QMainWindow".
################################################################################

class custom_MainWindow( QMainWindow ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inheret all attributes of the "QMainWindow" class.

		super( custom_MainWindow, self ).__init__( )

		# Save the Janus "core" to be associated with this object.

		self.core = core

		# Prepare to respond to signals received from the core.

		self.connect( self.core, SIGNAL('janus_exit'), self.resp_exit )

		# Indicate that if a "closeEvent" is received, that a dialog
		# should be shown.

		self.show_dialog = True

	#-----------------------------------------------------------------------
	# RE-DEFINE THE RESPONSE TO THE CLOSE SIGNAL.
	#-----------------------------------------------------------------------

	def closeEvent( self, event ) :

		# Request that the core stop any automatic analysis that might
		# be in progress.

		self.core.stop_auto_run = True

		# Wait until any running Janus threads have finished.

		# WARNING!  THIS APPROACH IS VERY LIMITED AND HAS SEVERAL FLAWS!
		#           A BETTER SOLUTION WOULD BE TO GLOBALLY BLOCK ANY NEW
		#           JANUS THREADS.  A CHECK COULD THEN BE MADE TO SEE IF
		#           ANY SUCH THREADS ARE CURRENTLY RUNNING, IF THEY ARE,
		#           THIS FUNCTION WOULD THEN RETURN AND BE RECALLED IN
		#           RESPONSE TO A SIGNAL INDICATING THAT ALL JANUS
		#           THREADS HAD FINISHED.

		while ( n_thread( ) > 0 ) :
			sleep( 0.1 )

		# If no results have been generated, simply exit the program
		# (without launching a dialog).

		if ( len( self.core.series ) == 0 ) :
			self.show_dialog = False
			event.accept( )
			return

		# If requested, launch a dialog to ask the user whether or not
		# the analysis results should be saved.  Otherwise, exit this
		# application immediately (and return).

		if ( self.show_dialog ) :
			event.ignore( )
			resp = dialog_save( ).get_resp( )
		else :
			event.accept( )
			return

		# Carry out the action requested by the user (via the save
		# dialog).

		if ( resp == 'save' ) :

			# Launch a dialog for the user to select a name and
			# location for the save file.

			nm_fl = str( QFileDialog.getSaveFileName(
			               caption='Save',
			               directory=make_name_save( self.core ) ) )

			# If the user canceled the dialog, abort the exit of
			# this application (i.e., return).

			if ( len( nm_fl ) == 0 ) :
				return

			# Assuming that there still aren't any janus threads
			# running, start a new thread to have the core save its
			# log of analysis results to the user-specified file.
			# If a new thread has somehow been launched, abort the
			# exit of this application (i.e., return).

			if ( n_thread( ) == 0 ) :
				Thread( target=thread_save_res,
				        args=( self.core, nm_fl,
				                           True  ) ).start( )
			else :
				return

		elif ( resp == 'xprt' ) :

			# Launch a dialog for the user to select a name and
			# location for the export text-file.

			nm_fl = str( QFileDialog.getSaveFileName(
			               caption='Export',
			               directory=make_name_xprt( self.core ) ) )

			# If the user canceled the dialog, abort the exit of
			# this application (i.e., return).

			if ( len( nm_fl ) == 0 ) :
				return

			# Assuming that there still aren't any janus threads
			# running, start a new thread to have the core export
			# its log of analysis results to the text file specified
			# the user.  If a new thread has somehow been launched,
			# abort the exit of this application (i.e., return).

			if ( n_thread( ) == 0 ) :
				Thread( target=thread_xprt_res,
				        args=( self.core, nm_fl,
				                           True  ) ).start( )
			else :
				return

		elif ( resp == 'exit' ) :

			# Exit this application (without saving the analysis
			# results).

			self.show_dialog = False

			event.accept( )

			return

		else :

			# Abort the exit of this application (i.e., return).

			return

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "exit" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_exit( self ) :

		# Exit the application.

		self.show_dialog = False

		self.close( )
