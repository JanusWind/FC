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

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QFont

# Load the customized push button and one-line text editor.

from janus_event_CheckBox import event_CheckBox

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_dsp, thread_chng_dyn


################################################################################
## DEFINE CLASS "widget_ctrl_dspdyn" TO CUSTOMIZE "QWidget" FOR DISPLAY/DYNAMIC.
################################################################################

class widget_ctrl_dspdyn( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_ctrl_dspdyn, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_dsp'),
		                                            self.resp_chng_dsp )
		self.connect( self.core, SIGNAL('janus_chng_dyn'),
		                                            self.resp_chng_dyn )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg = QGridLayout( )

		self.sg.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg, 0, 0, 5, 4 )

		# Initialize the check boxes that comprise this widget.

		self.lab_dsp = { 'dsp':QLabel( 'Display:'   ),
		                 'mom':QLabel( 'Moments'    ),
		                 'gsl':QLabel( 'Guess/Sel.' ),
		                 'nln':QLabel( 'Non-Linear' )  }

		self.lab_dyn = { 'dyn': QLabel( 'Dynamic:'    ),
		                 'mom': QLabel( 'Moments'     ),
		                 'gss': QLabel( 'Init. Guess' ),
		                 'sel': QLabel( 'Data Sel.'   ),
		                 'nln': QLabel( 'Non-Linear'  )  }

		self.box_dsp = { 'mom':event_CheckBox( self, 'mom' ),
                                 'gsl':event_CheckBox( self, 'gsl' ),
                                 'nln':event_CheckBox( self, 'nln' )  }

		self.box_dyn = { 'mom':event_CheckBox( self, 'mom' ),
                                 'gss':event_CheckBox( self, 'gss' ),
                                 'sel':event_CheckBox( self, 'sel' ),
                                 'nln':event_CheckBox( self, 'nln' )  }

		self.order_dsp = [ 'dsp', 'mom', 'gsl', 'nln' ]

		self.order_dyn  = [ 'dyn', 'mom', 'gss', 'sel', 'nln' ]

		# Row by row, add the boxes to this widget's grid.

		for i, key in enumerate( self.order_dsp ) :

			if ( key == 'dsp') :

				self.lab_dsp[key].setFont(
				        QFont( "Helvetica", 12, QFont.Bold ) )

				self.grd.addWidget( self.lab_dsp[key], i, 0, 1, 2 )
			else :
				self.box_dsp[key].setFont( QFont( "Helvetica", 12 ) )
				self.lab_dsp[key].setFont( QFont( "Helvetica", 12 ) )
				self.grd.addWidget( self.box_dsp[key], i, 0, 1, 1 )
				self.grd.addWidget( self.lab_dsp[key], i, 1, 1, 1 )


		for i, key in enumerate( self.order_dyn ) :

			if ( key == 'dyn') :

				self.lab_dyn[key].setFont(
				        QFont( "Helvetica", 12, QFont.Bold ) )

				self.grd.addWidget( self.lab_dyn[key], i, 3, 1, 2 )
			else :
				self.box_dyn[key].setFont( QFont( "Helvetica", 12 ) )
				self.lab_dyn[key].setFont( QFont( "Helvetica", 12 ) )
				self.grd.addWidget( self.box_dyn[key], i, 3, 1, 1 )
				self.grd.addWidget( self.lab_dyn[key], i, 4, 1, 1 )

		# Populate the check boxes.

		self.make_box( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SETTING THE VALUES OF THE TICK BOXES.
	#-----------------------------------------------------------------------

	def make_box( self ) :

		# Set the values of the "display" tick boxes.

		if ( self.core.dsp == 'mom' ) :
			self.box_dsp['mom'].setChecked( True  )
			self.box_dsp['gsl'].setChecked( False )
			self.box_dsp['nln'].setChecked( False )
		elif ( self.core.dsp == 'gsl' ) :
			self.box_dsp['mom'].setChecked( False )
			self.box_dsp['gsl'].setChecked( True  )
			self.box_dsp['nln'].setChecked( False )
		elif ( self.core.dsp == 'nln' ) :
			self.box_dsp['mom'].setChecked( False )
			self.box_dsp['gsl'].setChecked( False )
			self.box_dsp['nln'].setChecked( True  )
		else :
			self.box_dsp['mom'].setChecked( False )
			self.box_dsp['gsl'].setChecked( False )
			self.box_dsp['nln'].setChecked( False )

		# Set the values of the "dynamic" tick boxes.

		self.box_dyn['mom'].setChecked( self.core.dyn_mom )
		self.box_dyn['gss'].setChecked( self.core.dyn_gss )
		self.box_dyn['sel'].setChecked( self.core.dyn_sel )
		self.box_dyn['nln'].setChecked( self.core.dyn_nln )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running,
		# regenerate the check boxes and abort.

		if ( n_thread( ) != 0 ) :
			self.make_box( )
			return

		# If one of the "Display" boxes has been (un)checked, update the
		# value of "self.core.dsp" appropriately.

		# Note.  When one of these boxes is checked, it is not abolutely
		#        necessary to uncheck the other boxes.  The call to
		#        "self.core.chng_dsp" will emit a signal that cause
		#        "self.make_box" to be run.  However, there tends to be
		#        a bit of lag in this process, so an immediate
		#        unchecking of these boxes is warranted.

		if ( fnc == 'mom' ) :
			if ( self.box_dsp['mom'].isChecked( ) ) :
				self.box_dsp['gsl'].setChecked( False )
				self.box_dsp['nln'].setChecked( False )
				Thread( target=thread_chng_dsp,
				        args=( self.core, 'mom' ) ).start()
			else :
				Thread( target=thread_chng_dsp,
				        args=( self.core, None ) ).start()

		if ( fnc == 'gsl' ) :
			if ( self.box_dsp['gsl'].isChecked( ) ) :
				self.box_dsp['mom'].setChecked( False )
				self.box_dsp['nln'].setChecked( False )
				Thread( target=thread_chng_dsp,
				        args=( self.core, 'gsl' ) ).start()
			else :
				Thread( target=thread_chng_dsp,
				        args=( self.core, None ) ).start()

		if ( fnc == 'nln' ) :
			if ( self.box_dsp['nln'].isChecked( ) ) :
				self.box_dsp['mom'].setChecked( False )
				self.box_dsp['gsl'].setChecked( False )
				Thread( target=thread_chng_dsp,
				        args=( self.core, 'nln' ) ).start()
			else :
				Thread( target=thread_chng_dsp,
				        args=( self.core, None ) ).start()

		# If one of the "Dynamic" boxes has been (un)checked, update the
		# value of the corresponding "self.core.dyn_???".

		if ( fnc == 'mom' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'mom',
			               self.box_dyn['mom'].isChecked( ) ) ).start()

		if ( fnc == 'gss' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'gss',
			               self.box_dyn['gss'].isChecked( ) ) ).start()

		if ( fnc == 'sel' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'sel',
			               self.box_dyn['sel'].isChecked( ) ) ).start()

		if ( fnc == 'nln' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'nln',
			               self.box_dyn['nln'].isChecked( ) ) ).start()

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_dsp" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_dsp( self ) :

		# Update the check boxes.

		self.make_box( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_dyn" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_dyn( self ) :

		# Update the check boxes.

		self.make_box( )
