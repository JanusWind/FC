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
from PyQt4.QtGui import QGridLayout, QLabel, QLineEdit, QWidget

# Load the customized push button and one-line text editor.

from janus_event_LineEdit import event_LineEdit

# Load the necessary "numpy" array modules.

from numpy import tile

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_nln_spc


################################################################################
## DEFINE THE "widget_nln_ion" CLASS TO CUSTOMIZE "QWidget" FOR NLN ION SPECIES.
################################################################################

class widget_nln_spc( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_nln_spc, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_nln_ion'),
		                                        self.resp_chng_nln_ion )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# |   0   |   1   |   2   |   3   |   4   |   5   |
		# +-------+-------+-------+-------+-------+-------+
		# | Name                  |  Sym  | m/m_p | q/q_p |
		# | LineEdit              | LineE | LineE | LineE |

		# Initialize the labels, check boxes, and text areas that 
		# comprise this widget.

		self.hdr_name  = QLabel( 'Species Name' )
		self.hdr_sym   = QLabel( 'Symbol'       )
		self.hdr_m     = QLabel( 'm / m_p'      )
		self.hdr_q     = QLabel( 'q / q_p'      )

		self.arr_name  = tile( None, self.core.nln_n_pop )
		self.arr_sym   = tile( None, self.core.nln_n_pop )
		self.arr_m     = tile( None, self.core.nln_n_pop )
		self.arr_q     = tile( None, self.core.nln_n_pop )

		for i in range( self.core.nln_n_spc ) :

			txt_i = str( i )

			self.arr_name[i] = event_LineEdit( self, 'n'+txt_i )
			self.arr_sym[i]  = event_LineEdit( self, 's'+txt_i )
			self.arr_m[i]    = event_LineEdit( self, 'm'+txt_i )
			self.arr_q[i]    = event_LineEdit( self, 'q'+txt_i )

		# Row by row, add the labels, check boxes, and text areas, to
		# this widget's grid.

		self.grd.addWidget( self.hdr_name, 0, 0, 1, 3 )
		self.grd.addWidget( self.hdr_sym , 0, 3, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_m   , 0, 4, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_q   , 0, 5, 1, 1, Qt.AlignCenter )

		for i in range( self.core.nln_n_spc ) :

			self.grd.addWidget( self.arr_name[i], i+1, 0, 1, 3 )
			self.grd.addWidget( self.arr_sym[i] , i+1, 3, 1, 1 )
			self.grd.addWidget( self.arr_m[i]   , i+1, 4, 1, 1 )
			self.grd.addWidget( self.arr_q[i]   , i+1, 5, 1, 1 )

		# Regularize the grid spacing.

		for i in range( 6 ) :
			self.grd.setColumnStretch( i, 1 )

		for i in range( self.core.nln_n_spc + 1 ) :
			self.grd.setRowStretch( i, 1 )

		# Populate the text areas.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR DISPLAYING TEXT AND CHECK MARKS.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Display the parameters for each ion species.

		for i in range( self.core.nln_n_spc ) :

			# Extract the values from the core.

			tmp_name = self.core.nln_plas.arr_spec[i]['name']
			tmp_sym  = self.core.nln_plas.arr_spec[i]['sym']
			tmp_m    = self.core.nln_plas.arr_spec[i]['m']
			tmp_q    = self.core.nln_plas.arr_spec[i]['q']

			# Update each widget's text.

			if ( tmp_name is not None ) :
				self.arr_name[i].setTextUpdate( tmp_name )

			if ( tmp_sym is not None ) :
				self.arr_sym[i].setTextUpdate( tmp_sym )

			if ( tmp_m is not None ) :
				self.arr_m[i].setTextUpdate( str( tmp_m ) )

			if ( tmp_q is not None ) :
				self.arr_q[i].setTextUpdate( str( tmp_q ) )

			# Format the text of each widget.

			ss_name = 'background-color: white;\n'
			ss_sym  = 'background-color: white;\n'
			ss_m    = 'background-color: white;\n'
			ss_q    = 'background-color: white;\n'

			if ( ( tmp_name is None                     ) and
			     ( len( self.arr_name[i].text( ) ) > 0 )     ) :
				ss_name += 'color: red;'
			else :
				ss_name += 'color: black;'

			if ( ( tmp_sym is None                     ) and
			     ( len( self.arr_sym[i].text( ) ) > 0 )     ) :
				ss_sym += 'color: red;'
			else :
				ss_sym += 'color: black;'

			if ( ( tmp_m is None                     ) and
			     ( len( self.arr_m[i].text( ) ) > 0 )     ) :
				ss_m += 'color: red;'
			else :
				ss_m += 'color: black;'

			if ( ( tmp_q is None                     ) and
			     ( len( self.arr_q[i].text( ) ) > 0 )     ) :
				ss_q += 'color: red;'
			else :
				ss_q += 'color: black;'

			self.arr_name[i].setStyleSheet( ss_name )
			self.arr_sym[ i].setStyleSheet( ss_sym  )
			self.arr_m[   i].setStyleSheet( ss_m    )
			self.arr_q[   i].setStyleSheet( ss_q    )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running, reset
		# the text in the text box and abort.

		if ( n_thread( ) != 0 ) :
			self.make_txt( )
			return

		# Determine which ion species has been changed by the user.

		i = int( fnc[1:] )

		# Determine which parameter has been changed and what its new
		# value is.

		if   ( fnc[0] == 'n' ) :

			param = 'name'
			val   = str( self.arr_name[i].text( ) )

		elif ( fnc[0] == 's' ) :

			param = 'sym'
			val   = str( self.arr_sym[i].text( ) )

		elif ( fnc[0] == 'm' ) :

			param = 'm'

			try :
				val = float( self.arr_m[i].text( ) )
			except :
				val = None

		elif ( fnc[0] == 'q' ) :

			param = 'q'

			try :
				val = float( self.arr_q[i].text( ) )
			except :
				val = None

		else :

			return

		# Instruct the core to update its ion-species parameter(s)
		# appropriately.

		Thread( target=thread_chng_nln_spc,
		        args=( self.core, i, param, val ) ).start( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_ion" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_ion( self ) :

		# Repopulate the text and checkmarks in this widget.

		self.make_txt( )
