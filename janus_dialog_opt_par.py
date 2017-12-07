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

from janus_event_CheckBox import event_CheckBox
from janus_event_PushButton import event_PushButton

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
################################################################################

class dialog_opt_par( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_opt_par, self ).__init__( )

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

		self.sg1 = QGridLayout( )
		self.sg2 = QGridLayout( )
		self.sg3 = QGridLayout( )
		self.sg4 = QGridLayout( )
		self.sg5 = QGridLayout( )
		self.sg6 = QGridLayout( )

		self.sg1.setContentsMargins( 0, 0, 0, 0 )
		self.sg2.setContentsMargins( 0, 0, 0, 0 )
		self.sg3.setContentsMargins( 0, 0, 0, 0 )
		self.sg4.setContentsMargins( 0, 0, 0, 0 )
		self.sg5.setContentsMargins( 0, 0, 0, 0 )
		self.sg6.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg1, 0, 0, 1, 3 )
		self.grd.addLayout( self.sg2, 1, 0, 1, 3 )
		self.grd.addLayout( self.sg3, 2, 0, 1, 3 )
		self.grd.addLayout( self.sg4, 3, 0, 1, 1 )
		self.grd.addLayout( self.sg5, 4, 0, 1, 3 )
		self.grd.addLayout( self.sg6, 5, 0, 1, 1 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		#TODO Make font of 'lab_disp1' and 'lab_disp2' bold.
		# Not that setFont(QtGui.QFont().setBold(True)) doesn't work.

		self.lab_disp1  = QLabel( 'NLN 2nd Moment Paramters'  )
		self.lab_res_dt = QLabel( 'Temperature'               )
		self.lab_res_dw = QLabel( 'Thermal Speed'             )
		self.lab_disp2  = QLabel( 'Species NLN Parameters'    )
		self.lab_res_n  = QLabel( 'Number density (n)'        )
		self.lab_res_v  = QLabel( 'Velocity (v)'              )
		self.lab_res_d  = QLabel( 'Drift (dv)'                )
		self.lab_res_w  = QLabel( 'Thermal Speed/Temperature' )
		self.lab_res_r  = QLabel( 'Anisotropy (R)'            )
		self.lab_res_s  = QLabel( 'Skewness (S)'              )
		self.lab_res_k  = QLabel( 'Kurtosis (K)'              )
		self.lab_disp3  = QLabel( 'Uncertainties'             )
		self.lab_res_u  = QLabel( 'NLN Uncertainties'         )

		self.box = { 'res_dt':event_CheckBox( self, 'res_dt' ),
		             'res_dw':event_CheckBox( self, 'res_dw' ),
		             'res_n' :event_CheckBox( self, 'res_n'  ),
		             'res_v' :event_CheckBox( self, 'res_v'  ),
		             'res_d' :event_CheckBox( self, 'res_d'  ),
		             'res_w' :event_CheckBox( self, 'res_w'  ),
		             'res_r' :event_CheckBox( self, 'res_r'  ),
		             'res_s' :event_CheckBox( self, 'res_s'  ),
		             'res_k' :event_CheckBox( self, 'res_k'  ),
		             'res_u' :event_CheckBox( self, 'res_u'  )  }

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.sg1.addWidget( self.lab_disp1, 0, 0, 1, 3 )

		self.sg2.addWidget( self.box['res_dt'], 0, 1, 1, 1 )
		self.sg2.addWidget( self.lab_res_dt,    0, 2, 1, 1 )
		self.sg2.addWidget( self.box['res_dw'], 1, 1, 1, 1 )
		self.sg2.addWidget( self.lab_res_dw,    1, 2, 1, 1 )

		self.sg3.addWidget( self.lab_disp2, 0, 0, 1, 3 )

		self.sg4.addWidget( self.box['res_n'], 0, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_n,    0, 2, 1, 1 )
		self.sg4.addWidget( self.box['res_v'], 1, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_v,    1, 2, 1, 1 )
		self.sg4.addWidget( self.box['res_d'], 2, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_d,    2, 2, 1, 1 )
		self.sg4.addWidget( self.box['res_w'], 3, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_w,    3, 2, 1, 1 )
		self.sg4.addWidget( self.box['res_r'], 4, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_r,    4, 2, 1, 1 )
		self.sg4.addWidget( self.box['res_s'], 5, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_s,    5, 2, 1, 1 )
		self.sg4.addWidget( self.box['res_k'], 6, 1, 1, 1 )
		self.sg4.addWidget( self.lab_res_k,    6, 2, 1, 1 )

		self.sg5.addWidget( self.lab_disp3, 0, 0, 1, 3 )

		self.sg6.addWidget( self.box['res_u'], 0, 1, 1, 1 )
		self.sg6.addWidget( self.lab_res_u,    0, 2, 1, 1 )

		# Populate the menu with the options settings from core.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self ) :

		self.box['res_dt'].setChecked( self.core.opt['res_dt'] )
		self.box['res_dw'].setChecked( self.core.opt['res_dw'] )
		self.box['res_n' ].setChecked( self.core.opt['res_n' ] )
		self.box['res_v' ].setChecked( self.core.opt['res_v' ] )
		self.box['res_d' ].setChecked( self.core.opt['res_d' ] )
		self.box['res_w' ].setChecked( self.core.opt['res_w' ] )
		self.box['res_r' ].setChecked( self.core.opt['res_r' ] )
		self.box['res_s' ].setChecked( self.core.opt['res_s' ] )
		self.box['res_k' ].setChecked( self.core.opt['res_k' ] )
		self.box['res_u' ].setChecked( self.core.opt['res_u' ] )

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

		else :

			self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A CHANGE OF AN OPTION.
	#-----------------------------------------------------------------------

	def resp_chng_opt( self ) :

		# Regenerate the menu.

		self.make_opt( )
