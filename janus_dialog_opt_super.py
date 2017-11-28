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

from PyQt4.QtGui import QDialog, QGridLayout, QTabWidget

from janus_widget_mfi_lin_plot   import widget_mfi_lin_plot
from janus_widget_mfi_lon_plot   import widget_mfi_lon_plot
from janus_widget_mfi_colat_plot import widget_mfi_colat_plot
from janus_widget_mfi_info       import widget_mfi_info

################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
################################################################################

class dialog_opt_super( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_super, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Make this a modal dialog (i.e., block user-interaction with
		# the main application window while this dialog exists).

		self.setModal( True )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Options Menu' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Add a QTabWidget.

		self.wdg = QTabWidget( )

		self.grd.addWidget( self.wdg, 0, 0, 1, 1 )


		self.wdg_lin_plot   = widget_mfi_lin_plot( self.core   )
		self.wdg_lon_plot   = widget_mfi_lon_plot( self.core   )
		self.wdg_colat_plot = widget_mfi_colat_plot( self.core )
		self.wdg_info       = widget_mfi_info( self.core       )

		self.wdg.addTab( self.wdg_lin_plot,  'MFI' )
		self.wdg.addTab( self.wdg_lon_plot,   'theta' )
		self.wdg.addTab( self.wdg_colat_plot, 'lambda' )
		self.wdg.addTab( self.wdg_info,      '<B>' )

		# Execute this dialog.

		self.exec_( )

	"""
	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self ) :

		self.box['thrm_dt'].setChecked( self.core.opt['thrm_dt'] )
		self.box['thrm_dw'].setChecked( self.core.opt['thrm_dw'] )
		self.box['spres_n'].setChecked( self.core.opt['spres_n'] )
		self.box['spres_v'].setChecked( self.core.opt['spres_v'] )
		self.box['spres_d'].setChecked( self.core.opt['spres_d'] )
		self.box['spres_t'].setChecked( self.core.opt['spres_t'] )
		self.box['spres_w'].setChecked( self.core.opt['spres_w'] )
		self.box['spres_r'].setChecked( self.core.opt['spres_r'] )
		self.box['spres_s'].setChecked( self.core.opt['spres_s'] )
		self.box['spres_k'].setChecked( self.core.opt['spres_k'] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the 'Done' button has been pressed, close the window and
		# return.

		if ( fnc == 'done' ) :

			self.close( )

			return

		# If no threads are running, make the change to the option with
		# core.  Otherwise, restore the original options settings.

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

		# Regenerate the menu.

		self.make_opt( )
	"""
