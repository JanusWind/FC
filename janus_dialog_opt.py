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

from PyQt4.QtGui import QDialog, QGridLayout, QLabel
from PyQt4.QtCore import SIGNAL

# Load the customized push button and one-line text editor.

from janus_event_CheckBox import event_CheckBox
from janus_event_PushButton import event_PushButton

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR AUTO-RUN CONTROL.
################################################################################

class dialog_opt( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_opt'),
		                                            self.resp_chng_opt )

		# Make this a modal dialog (i.e., block user-interaction with
		# the main application window while this dialog exists).

		self.setModal( True )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Options Menu' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg1 = QGridLayout( )
		self.sg2 = QGridLayout( )
		self.sg3 = QGridLayout( )

		self.sg1.setContentsMargins( 0, 0, 0, 0 )
		self.sg2.setContentsMargins( 0, 0, 0, 0 )
		self.sg3.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg1, 0, 0, 1, 1 )
		self.grd.addLayout( self.sg2, 1, 0, 1, 1 )
		self.grd.addLayout( self.sg3, 2, 0, 1, 1 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_disp    = QLabel( 'Display Options'  )
		self.lab_thrm_t  = QLabel( 'Temperature'      )
		self.lab_thrm_w  = QLabel( 'Thermal Velocity' )
		self.lab_spres_n = QLabel( 'Number density'   )
		self.lab_spres_v = QLabel( 'Velocity'         )
		self.lab_spres_d = QLabel( 'Drift'            )
		self.lab_spres_w = QLabel( 'Thermal Speed'    )
		self.lab_spres_r = QLabel( 'Anisotropy'       )
		self.lab_spres_s = QLabel( 'Skewness'         )
		self.lab_spres_k = QLabel( 'Kurtosis'         )
		self.lab_done    = QLabel( 'Done'             )

		self.box = { 'thrm_t' :event_CheckBox( self, 'thrm_t' ),
		             'thrm_w' :event_CheckBox( self, 'thrm_w' ),
		             'spres_n':event_CheckBox( self, 'spres_n'),
		             'spres_v':event_CheckBox( self, 'spres_v'),
		             'spres_d':event_CheckBox( self, 'spres_d'),
		             'spres_w':event_CheckBox( self, 'spres_w'),
		             'spres_r':event_CheckBox( self, 'spres_r'),
		             'spres_s':event_CheckBox( self, 'spres_s'),
		             'spres_k':event_CheckBox( self, 'spres_k')  }

		self.btn_done = event_PushButton( self, 'done', 'Done' )

		self.btn_done.setAutoDefault( False )

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.sg1.addWidget( self.lab_disp, 0, 0, 1, 1 )

		self.sg2.addWidget( self.lab_thrm_t,     0, 0, 1, 1 )
		self.sg2.addWidget( self.box['thrm_t'],  0, 1, 1, 1 )
		self.sg2.addWidget( self.lab_thrm_w,     1, 0, 1, 1 )
		self.sg2.addWidget( self.box['thrm_w'],  1, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_n,    2, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_n'], 2, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_v,    3, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_v'], 3, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_d,    4, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_d'], 4, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_w,    5, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_w'], 5, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_r,    6, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_r'], 6, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_s,    7, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_s'], 7, 1, 1, 1 )
		self.sg2.addWidget( self.lab_spres_k,    8, 0, 1, 1 )
		self.sg2.addWidget( self.box['spres_k'], 8, 1, 1, 1 )

		self.sg3.addWidget( self.btn_done, 0, 0, 1, 1 )

		# Populate the menu with the options settings from core.

		self.make_opt( )

		# Execute this dialog.

		self.exec_( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self ) :

		self.box['thrm_t' ].setChecked( self.core.opt['thrm_t' ] )
		self.box['thrm_w' ].setChecked( self.core.opt['thrm_w' ] )
		self.box['spres_n'].setChecked( self.core.opt['spres_n'] )
		self.box['spres_v'].setChecked( self.core.opt['spres_v'] )
		self.box['spres_d'].setChecked( self.core.opt['spres_d'] )
		self.box['spres_w'].setChecked( self.core.opt['spres_w'] )
		self.box['spres_r'].setChecked( self.core.opt['spres_r'] )
		self.box['spres_s'].setChecked( self.core.opt['spres_s'] )
		self.box['spres_k'].setChecked( self.core.opt['spres_k'] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If no threads are running, make the change to the option with
		# core.  Otherwise, restore the original options settings.

		if ( n_thread( ) == 0 ) :

			# Start a new thread that makes the change to the option
			# with core.

			Thread( target=thread_chng_opt,
			        args=( self.core, fnc,
			               self.box[fnc].isChecked( ) ) ).start( )

#			if ( fnc == 'done' ) :
#
#				self.close( )
#
#				return
		else :

			self.make_opt( )

#		if (fnc == 'done' ) :
#
#			self.close( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A CHANGE OF AN OPTION.
	#-----------------------------------------------------------------------

	def resp_chng_opt( self ) :

		# Regenerate the menu.

		self.make_opt( )
