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

from janus_event_PushButton import event_PushButton

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt


################################################################################
## DEFINE CLASS "dialog_opt_par" TO CUSTOMIZE "QDialog" FOR OPTION CONTROL.
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
		self.connect( self.core, SIGNAL('janus_rstr_opt'),
		                                            self.resp_rstr_opt )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg = QGridLayout( )

		self.sg.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg, 0, 0, 13, 3 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab = {
		       'lab_1'     :QLabel( 'NLN 2nd Moment Paramters' , self ),
                       'res_par_dt':QLabel( 'Temperature (T)'          , self ),
                       'res_par_dw':QLabel( 'Thermal Speed (W)'        , self ),
                       'lab_2'     :QLabel( 'Species NLN Parameters'   , self ),
                       'res_par_n' :QLabel( 'Number density (n)'       , self ),
                       'res_par_v' :QLabel( 'Velocity (v)'             , self ),
                       'res_par_fv':QLabel( 'Fluctuating Velocity'     , self ),
                       'res_par_d' :QLabel( 'Drift (dv)'               , self ),
                       'res_par_w' :QLabel( 'Therm. Speed/Temp. (W/T)' , self ),
                       'res_par_r' :QLabel( 'Anisotropy (R)'           , self ),
                       'res_par_b' :QLabel( 'Beta ( parallel )'        , self ),
                       'res_par_av':QLabel( 'Alfven Speed'             , self ),
                       'res_par_s' :QLabel( 'Skewness (S)'             , self ),
                       'res_par_k' :QLabel( 'Kurtosis (K)'             , self ),
                       'lab_3'     :QLabel( 'Uncertainties'            , self ),
                       'res_par_u' :QLabel( 'NLN Uncertainties'        , self ), }

		self.box = { 'res_par_dt':event_CheckBox( self, 'res_par_dt' ),
		             'res_par_dw':event_CheckBox( self, 'res_par_dw' ),
		             'res_par_n' :event_CheckBox( self, 'res_par_n'  ),
		             'res_par_v' :event_CheckBox( self, 'res_par_v'  ),
		             'res_par_d' :event_CheckBox( self, 'res_par_d'  ),
		             'res_par_w' :event_CheckBox( self, 'res_par_w'  ),
		             'res_par_r' :event_CheckBox( self, 'res_par_r'  ),
		             'res_par_b' :event_CheckBox( self, 'res_par_b'  ),
		             'res_par_av':event_CheckBox( self, 'res_par_av' ),
		             'res_par_s' :event_CheckBox( self, 'res_par_s'  ),
		             'res_par_fv':event_CheckBox( self, 'res_par_fv' ),
		             'res_par_k' :event_CheckBox( self, 'res_par_k'  ),
		             'res_par_u' :event_CheckBox( self, 'res_par_u'  ) }


		self.order = [ 'lab_1'    , 'res_par_dt', 'res_par_dw', 'lab_2',
		               'res_par_n', 'res_par_v' , 'res_par_fv',
		               'res_par_d','res_par_w'  , 'res_par_r' ,
		               'res_par_b', 'res_par_av', 'res_par_s' ,
		               'res_par_k', 'lab_3'     , 'res_par_u'          ]

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		for i, key in enumerate( self.order ) :

			if ( ( key == 'lab_1' ) or ( key == 'lab_2' ) or
			     ( key == 'lab_3' )                          ) :

				self.lab[key].setFont(
				        QFont( "Helvetica", 12, QFont.Bold ) )

				self.sg.addWidget( self.lab[key], i, 0, 1, 3 )
			else :
				self.box[key].setFont( QFont( "Helvetica", 12 ) )
				self.lab[key].setFont( QFont( "Helvetica", 12 ) )
				self.sg.addWidget( self.box[key], i, 0, 1, 1 )
				self.sg.addWidget( self.lab[key], i, 1, 1, 1 )

		# Populate the menu with the options settings from core.

		self.make_opt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING MENU.
	#-----------------------------------------------------------------------

	def make_opt( self ) :

		self.box['res_par_dt'].setChecked( self.core.opt['res_par_dt'] )
		self.box['res_par_dw'].setChecked( self.core.opt['res_par_dw'] )
		self.box['res_par_n' ].setChecked( self.core.opt['res_par_n' ] )
		self.box['res_par_v' ].setChecked( self.core.opt['res_par_v' ] )
		self.box['res_par_fv'].setChecked( self.core.opt['res_par_fv'] )
		self.box['res_par_d' ].setChecked( self.core.opt['res_par_d' ] )
		self.box['res_par_w' ].setChecked( self.core.opt['res_par_w' ] )
		self.box['res_par_r' ].setChecked( self.core.opt['res_par_r' ] )
		self.box['res_par_b' ].setChecked( self.core.opt['res_par_b' ] )
		self.box['res_par_av'].setChecked( self.core.opt['res_par_av'] )
		self.box['res_par_s' ].setChecked( self.core.opt['res_par_s' ] )
		self.box['res_par_k' ].setChecked( self.core.opt['res_par_k' ] )
		self.box['res_par_u' ].setChecked( self.core.opt['res_par_u' ] )

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

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO RESTORING DEFAULT OPTIONS.
	#-----------------------------------------------------------------------

	def resp_rstr_opt( self ) :

		# Regenerate the menu.

		self.make_opt( )
