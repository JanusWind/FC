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
from PyQt4.QtGui import QGridLayout, QLabel, QWidget

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

		# Initialize the check boxes that comprise this widget.

		self.lab_dsp     = QLabel( 'Display:'     )
		self.lab_dsp_mom = QLabel( '  Moments'    )
		self.lab_dsp_gsl = QLabel( '  Guess/Sel.' )
		self.lab_dsp_nln = QLabel( '  Non-Linear' )

		self.box_dsp_mom = event_CheckBox( self, 'dsp_mom' )
		self.box_dsp_gsl = event_CheckBox( self, 'dsp_gsl' )
		self.box_dsp_nln = event_CheckBox( self, 'dsp_nln' )

		self.lab_dyn     = QLabel( 'Dynamic:'      )
		self.lab_dyn_mom = QLabel( '  Moments'     )
		self.lab_dyn_gss = QLabel( '  Init. Guess' )
		self.lab_dyn_sel = QLabel( '  Data Sel.'   )
		self.lab_dyn_nln = QLabel( '  Non-Linear'  )

		self.box_dyn_mom = event_CheckBox( self, 'dyn_mom' )
		self.box_dyn_gss = event_CheckBox( self, 'dyn_gss' )
		self.box_dyn_sel = event_CheckBox( self, 'dyn_sel' )
		self.box_dyn_nln = event_CheckBox( self, 'dyn_nln' )

		# Row by row, add the boxes to this widget's grid.

		self.grd.addWidget( self.lab_dsp    , 1, 0, 1, 2 )
		self.grd.addWidget( self.lab_dsp_mom, 2, 0, 1, 1 )
		self.grd.addWidget( self.box_dsp_mom, 2, 1, 1, 1 )
		self.grd.addWidget( self.lab_dsp_gsl, 3, 0, 2, 1 )
		self.grd.addWidget( self.box_dsp_gsl, 3, 1, 2, 1 )
		self.grd.addWidget( self.lab_dsp_nln, 5, 0, 1, 1 )
		self.grd.addWidget( self.box_dsp_nln, 5, 1, 1, 1 )

		self.grd.addWidget( self.lab_dyn    , 1, 2, 1, 1 )
		self.grd.addWidget( self.lab_dyn_mom, 2, 2, 1, 1 )
		self.grd.addWidget( self.box_dyn_mom, 2, 3, 1, 1 )
		self.grd.addWidget( self.lab_dyn_gss, 3, 2, 1, 1 )
		self.grd.addWidget( self.box_dyn_gss, 3, 3, 1, 1 )
		self.grd.addWidget( self.lab_dyn_sel, 4, 2, 1, 1 )
		self.grd.addWidget( self.box_dyn_sel, 4, 3, 1, 1 )
		self.grd.addWidget( self.lab_dyn_nln, 5, 2, 1, 1 )
		self.grd.addWidget( self.box_dyn_nln, 5, 3, 1, 1 )

		# Populate the check boxes.

		self.make_box( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SETTING THE VALUES OF THE TICK BOXES.
	#-----------------------------------------------------------------------

	def make_box( self ) :

		# Set the values of the "display" tick boxes.

		if ( self.core.dsp == 'mom' ) :
			self.box_dsp_mom.setChecked( True  )
			self.box_dsp_gsl.setChecked( False )
			self.box_dsp_nln.setChecked( False )
		elif ( self.core.dsp == 'gsl' ) :
			self.box_dsp_mom.setChecked( False )
			self.box_dsp_gsl.setChecked( True  )
			self.box_dsp_nln.setChecked( False )
		elif ( self.core.dsp == 'nln' ) :
			self.box_dsp_mom.setChecked( False )
			self.box_dsp_gsl.setChecked( False )
			self.box_dsp_nln.setChecked( True  )
		else :
			self.box_dsp_mom.setChecked( False )
			self.box_dsp_gsl.setChecked( False )
			self.box_dsp_nln.setChecked( False )

		# Set the values of the "dynamic" tick boxes.

		self.box_dyn_mom.setChecked( self.core.dyn_mom )
		self.box_dyn_gss.setChecked( self.core.dyn_gss )
		self.box_dyn_sel.setChecked( self.core.dyn_sel )
		self.box_dyn_nln.setChecked( self.core.dyn_nln )

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

		if ( fnc == 'dsp_mom' ) :
			if ( self.box_dsp_mom.isChecked( ) ) :
				self.box_dsp_gsl.setChecked( False )
				self.box_dsp_nln.setChecked( False )
				Thread( target=thread_chng_dsp,
				        args=( self.core, 'mom' ) ).start()
			else :
				Thread( target=thread_chng_dsp,
				        args=( self.core, None ) ).start()

		if ( fnc == 'dsp_gsl' ) :
			if ( self.box_dsp_gsl.isChecked( ) ) :
				self.box_dsp_mom.setChecked( False )
				self.box_dsp_nln.setChecked( False )
				Thread( target=thread_chng_dsp,
				        args=( self.core, 'gsl' ) ).start()
			else :
				Thread( target=thread_chng_dsp,
				        args=( self.core, None ) ).start()

		if ( fnc == 'dsp_nln' ) :
			if ( self.box_dsp_nln.isChecked( ) ) :
				self.box_dsp_mom.setChecked( False )
				self.box_dsp_gsl.setChecked( False )
				Thread( target=thread_chng_dsp,
				        args=( self.core, 'nln' ) ).start()
			else :
				Thread( target=thread_chng_dsp,
				        args=( self.core, None ) ).start()

		# If one of the "Dynamic" boxes has been (un)checked, update the
		# value of the corresponding "self.core.dyn_???".

		if ( fnc == 'dyn_mom' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'mom',
			               self.box_dyn_mom.isChecked( ) ) ).start()

		if ( fnc == 'dyn_gss' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'gss',
			               self.box_dyn_gss.isChecked( ) ) ).start()

		if ( fnc == 'dyn_sel' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'sel',
			               self.box_dyn_sel.isChecked( ) ) ).start()

		if ( fnc == 'dyn_nln' ) :
			Thread( target=thread_chng_dyn,
			        args=( self.core, 'nln',
			               self.box_dyn_nln.isChecked( ) ) ).start()

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
