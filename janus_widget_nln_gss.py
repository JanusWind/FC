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
from PyQt4.QtGui import QFrame, QGridLayout, QLabel, QLineEdit, QSizePolicy, \
                        QWidget

# Load the customized push button and one-line text editor.

from janus_event_LineEdit import event_LineEdit
from janus_event_CheckBox import event_CheckBox

# Load the necessary "numpy" array modules.

from numpy import tile

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_nln_gss


################################################################################
## DEFINE THE "widget_nln_gss" CLASS TO CUSTOMIZE "QWidget" FOR NLN INIT. GUESS.
################################################################################

class widget_nln_gss( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_nln_gss, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_nln_ion'),
		                                        self.resp_chng_nln_ion )
		self.connect( self.core, SIGNAL('janus_chng_nln_gss'),
		                                        self.resp_chng_nln_gss )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Initialize the labels, check boxes, and text areas that 
		# comprise this widget.

		self.hdr_name = QLabel( 'Ion Population' )
		self.hdr_n    = QLabel( 'n [cm^-3]'      )
		self.hdr_d    = QLabel( 'dv [km/s]'      )
		self.hdr_w    = QLabel( 'w [km/s]'       )

		self.hline = QFrame( )
		self.hline.setFrameStyle( QFrame.HLine )
		self.hline.setSizePolicy( QSizePolicy.Expanding,
		                          QSizePolicy.Minimum    )

		self.vel_lab = QLabel( 'v_vec [km/s]: ' )
		self.vel_x   = event_LineEdit( self, 'vx' )
		self.vel_y   = event_LineEdit( self, 'vy' )
		self.vel_z   = event_LineEdit( self, 'vz' )

		self.arr_name = tile( None, self.core.nln_n_pop )
		self.arr_n    = tile( None, self.core.nln_n_pop )
		self.arr_d    = tile( None, self.core.nln_n_pop )
		self.arr_ws   = tile( None, self.core.nln_n_pop )
		self.arr_we   = tile( None, self.core.nln_n_pop )
		self.arr_wa   = tile( None, self.core.nln_n_pop )

		for i in range( self.core.nln_n_pop ) :

			txt_i = str( i )

			self.arr_name[i] = QLabel( '' )
			self.arr_n[i]    = event_LineEdit( self, 'nn'+txt_i )
			self.arr_d[i]    = event_LineEdit( self, 'dd'+txt_i )
			self.arr_ws[i]   = event_LineEdit( self, 'ws'+txt_i )
			self.arr_we[i]   = event_LineEdit( self, 'we'+txt_i )
			self.arr_wa[i]   = event_LineEdit( self, 'wa'+txt_i )

		# Row by row, add the labels, check boxes, and text areas, to
		# this widget's grid.

		self.grd.addWidget( self.hdr_name, 0, 0, 1, 4 )
		self.grd.addWidget( self.hdr_n   , 0, 4, 1, 2, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_d   , 0, 6, 1, 2, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_w   , 0, 8, 1, 4, Qt.AlignCenter )

		for i in range( self.core.nln_n_pop ) :

			self.grd.addWidget( self.arr_name[i], i+1,  0, 1, 4 )
			self.grd.addWidget( self.arr_n[i]   , i+1,  4, 1, 2 )
			self.grd.addWidget( self.arr_d[i]   , i+1,  6, 1, 2 )
			self.grd.addWidget( self.arr_ws[i]  , i+1,  9, 1, 2 )
			self.grd.addWidget( self.arr_wa[i]  , i+1,  8, 1, 2 )
			self.grd.addWidget( self.arr_we[i]  , i+1, 10, 1, 2 )

		i = self.core.nln_n_pop + 1

		self.grd.addWidget( self.hline, i, 0, 1, 12 )

		i = self.core.nln_n_pop + 2

		self.grd.addWidget( self.vel_lab, i, 0, 1, 4, Qt.AlignRight  )
		self.grd.addWidget( self.vel_x  , i, 4, 1, 2, Qt.AlignCenter )
		self.grd.addWidget( self.vel_y  , i, 6, 1, 2, Qt.AlignCenter )
		self.grd.addWidget( self.vel_z  , i, 8, 1, 2, Qt.AlignCenter )

		# Regularize the grid spacing.

		for i in range( 12 ) :
			self.grd.setColumnStretch( i, 1 )

		for i in range( self.core.nln_n_pop + 3 ) :
				self.grd.setRowStretch( i, 1 )

		# Populate the text areas.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR DISPLAYING TEXT IN THE TEXT AREAS.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Display the bulk velocity.

		val_vel_x = self.core.nln_plas.v0_x
		val_vel_y = self.core.nln_plas.v0_y
		val_vel_z = self.core.nln_plas.v0_z

		if ( val_vel_x is not None ) :
			self.vel_x.setTextUpdate( str( val_vel_x ) )
		if ( val_vel_y is not None ) :
			self.vel_y.setTextUpdate( str( val_vel_y ) )
		if ( val_vel_z is not None ) :
			self.vel_z.setTextUpdate( str( val_vel_z ) )

		# Display the parameters for each ion popultion.

		for i in range( self.core.nln_n_pop ) :

			# Display the population's full name (with symbol)

			self.arr_name[i].setText(
			        self.core.nln_plas.arr_pop[i]['full_name_sym'] )

			# Extract the values of the population's bulk
			# parameters.

			val_n  = self.core.nln_plas.arr_pop[i]['n']
			val_d  = self.core.nln_plas.arr_pop[i]['dv']
			val_ws = self.core.nln_plas.arr_pop[i]['w']
			val_we = self.core.nln_plas.arr_pop[i]['w_per']
			val_wa = self.core.nln_plas.arr_pop[i]['w_par']

			# If possible, update the text.

			if ( val_n is not None ) :
				self.arr_n[i].setTextUpdate( str( val_n ) )
			elif ( self.core.dyn_gss ) :
				self.arr_n[i].setTextUpdate( '' )

			if ( val_d is not None ) :
				self.arr_d[i].setTextUpdate( str( val_d ) )
			elif ( self.core.dyn_gss ) :
				self.arr_d[i].setTextUpdate( '' )

			if ( val_ws is not None ) :
				self.arr_ws[i].setTextUpdate( str( val_ws ) )
			elif ( self.core.dyn_gss ) :
				self.arr_ws[i].setTextUpdate( '' )

			if ( val_we is not None ) :
				self.arr_we[i].setTextUpdate( str( val_we ) )
			elif ( self.core.dyn_gss ) :
				self.arr_we[i].setTextUpdate( '' )

			if ( val_wa is not None ) :
				self.arr_wa[i].setTextUpdate( str( val_wa ) )
			elif ( self.core.dyn_gss ) :
				self.arr_wa[i].setTextUpdate( '' )

			# Determine which text boxes should be visible.

			if ( self.core.nln_plas.arr_pop[i]['drift'] ) :
				self.arr_d[i].show( )
			else :
				self.arr_d[i].hide( )

			if ( self.core.nln_plas.arr_pop[i]['aniso'] ) :
				self.arr_ws[i].hide( )
				self.arr_we[i].show( )
				self.arr_wa[i].show( )
			else :
				self.arr_ws[i].show( )
				self.arr_we[i].hide( )
				self.arr_wa[i].hide( )

			# Select the background color of each text box based on
			# whether or not the ion species is in use and valid.

			if ( ( self.core.nln_pop_use[i]            ) and
			     ( self.core.nln_pop_vld[i]            ) and
			     ( ( self.core.nln_set_gss_vld[i] ) or
			       ( not self.core.dyn_gss        )    )     ) :
				ss_n  = 'background-color: white;\n'
				ss_d  = 'background-color: white;\n'
				ss_ws = 'background-color: white;\n'
				ss_we = 'background-color: white;\n'
				ss_wa = 'background-color: white;\n'
			else :
				ss_n  = 'background-color: gray;\n'
				ss_d  = 'background-color: gray;\n'
				ss_ws = 'background-color: gray;\n'
				ss_we = 'background-color: gray;\n'
				ss_wa = 'background-color: gray;\n'

			# Select the text color of each text box based on
			# whether the text therein is valid.

			if ( ( val_n is None                    ) and
			     ( len( self.arr_n[i].text( ) ) > 0 )     ) :
				ss_n += 'color: red;'
			else :
				ss_n += 'color: black;'

			if ( ( val_d is None                    ) and
			     ( len( self.arr_d[i].text( ) ) > 0 )     ) :
				ss_d += 'color: red;'
			else :
				ss_d += 'color: black;'

			if ( ( val_ws is None                    ) and
			     ( len( self.arr_ws[i].text( ) ) > 0 )     ) :
				ss_ws += 'color: red;'
			else :
				ss_ws += 'color: black;'

			if ( ( val_we is None                    ) and
			     ( len( self.arr_we[i].text( ) ) > 0 )     ) :
				ss_we += 'color: red;'
			else :
				ss_we += 'color: black;'

			if ( ( val_wa is None                    ) and
			     ( len( self.arr_wa[i].text( ) ) > 0 )     ) :
				ss_wa += 'color: red;'
			else :
				ss_wa += 'color: black;'

			# Apply the changes to the style sheets.

			self.arr_n[ i].setStyleSheet( ss_n  )
			self.arr_d[ i].setStyleSheet( ss_d  )
			self.arr_ws[i].setStyleSheet( ss_ws )
			self.arr_we[i].setStyleSheet( ss_we )
			self.arr_wa[i].setStyleSheet( ss_wa )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running, reset
		# the text in the text box and abort.

		if ( n_thread( ) != 0 ) :
			self.make_txt( )
			return

		# Determine which parameter of which ion has been changed by
		# the user.

		prfx = fnc[0:2]

		if ( prfx[0] == 'v' ) :
			i = None
		else :
			i = int( fnc[2:] )

		# Depending on the type of parameter, extract its new value.

		if   ( prfx == 'nn' ) :

			param = 'n'

			try :
				val = float( self.arr_n[i].text( ) )
			except :
				val = None

		elif ( prfx == 'dd' ) :

			param = 'dv'

			try :
				val = float( self.arr_d[i].text( ) )
			except :
				val = None

		elif ( prfx == 'ws' ) :

			param = 'w'

			try :
				val = float( self.arr_ws[i].text( ) )
			except :
				val = None

		elif ( prfx == 'we' ) :

			param = 'w_per'

			try :
				val = float( self.arr_we[i].text( ) )
			except :
				val = None

		elif ( prfx == 'wa' ) :

			param = 'w_par'

			try :
				val = float( self.arr_wa[i].text( ) )
			except :
				val = None

		elif ( prfx[0] == 'vx' ) :

			param = 'v_x'

			try :
				val = float( self.vel_x.text( ) )
			except :
				val = None

		elif ( prfx[0] == 'vy' ) :

			param = 'v_y'

			try :
				val = float( self.vel_y.text( ) )
			except :
				val = None

		elif ( prfx[0] == 'vz' ) :

			param = 'v_z'

			try :
				val = float( self.vel_z.text( ) )
			except :
				val = None

		else :

			return

		# Instruct the core to update its ion parameters 
		# appropriately.

		Thread( target=thread_chng_nln_gss,
		        args=( self.core, i, param, val ) ).start()

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Regenerate the text in this widget.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_ion" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_ion( self ) :

		# Regenerate the text in this widget.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_gss" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_gss( self ) :

		# Regenerate the text in this widget.

		self.make_txt( )
