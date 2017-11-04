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
from janus_event_CheckBox import event_CheckBox

# Load the necessary "numpy" array modules.

from numpy import tile

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_nln_set


################################################################################
## DEFINE THE "widget_nln_set" CLASS TO CUSTOMIZE "QWidget" FOR NLN SETTINGS.
################################################################################

class widget_nln_set( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_nln_set, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_nln_ion'),
		                                        self.resp_chng_nln_ion )
		self.connect( self.core, SIGNAL('janus_chng_nln_set'),
		                                        self.resp_chng_nln_set )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# Initialize the labels, check boxes, and text areas that 
		# comprise this widget.

		# |   0   |   1   |   2   |   3   |   4   |   5   |   6   |
		# +-------+-------+-------+-------+-------+-------+-------+
		# | Name          |   init. guess ctrl.   | select ctrl.  |
		# |               |   n   |   v   |   w   | w_min | w_max |
		# | QLabel        | LineE | LineE | LineE | LineE | LineE |

		self.hdr_name = QLabel( 'Ion Population' )
		self.hdr_gss  = QLabel( 'Initial-Guess Generation' )
		self.hdr_sel  = QLabel( 'Data Selection' )

		self.hdr_gss_n = QLabel( 'n/n_m'  )
		self.hdr_gss_d = QLabel( 'dv/v_m' )
		self.hdr_gss_w = QLabel( 'w/w_m'  )

		self.hdr_sel_a = QLabel( 'w_-/w' )
		self.hdr_sel_b = QLabel( 'w_+/w' )

		self.arr_name  = tile( None, self.core.nln_n_pop )
		self.arr_gss_n = tile( None, self.core.nln_n_pop )
		self.arr_gss_d = tile( None, self.core.nln_n_pop )
		self.arr_gss_w = tile( None, self.core.nln_n_pop )
		self.arr_sel_a = tile( None, self.core.nln_n_pop )
		self.arr_sel_b = tile( None, self.core.nln_n_pop )

		for i in range( self.core.nln_n_pop ) :

			txt_i = str( i )

			self.arr_name[i]  = QLabel( '' )
			self.arr_gss_n[i] = event_LineEdit( self, 'gn'+txt_i )
			self.arr_gss_w[i] = event_LineEdit( self, 'gw'+txt_i )
			self.arr_sel_a[i] = event_LineEdit( self, 's-'+txt_i )
			self.arr_sel_b[i] = event_LineEdit( self, 's+'+txt_i )

			if ( i != 0 ) :
				self.arr_gss_d[i] =\
				              event_LineEdit( self, 'gd'+txt_i )

		# Row by row, add the labels, check boxes, and text areas, to
		# this widget's grid.

		self.grd.addWidget( self.hdr_name, 0, 0, 2, 2 )
		self.grd.addWidget( self.hdr_gss , 0, 2, 1, 3, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_sel , 0, 5, 1, 2, Qt.AlignCenter )

		self.grd.addWidget( self.hdr_gss_n, 1, 2, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_gss_d, 1, 3, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_gss_w, 1, 4, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_sel_a, 1, 5, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_sel_b, 1, 6, 1, 1, Qt.AlignCenter )

		for i in range( self.core.nln_n_pop ) :

			if ( self.arr_name[i] is not None ) :
				self.grd.addWidget( self.arr_name[i] ,
				                    ( i + 2 ), 0, 1, 2 )

			if ( self.arr_gss_n[i] is not None ) :
				self.grd.addWidget( self.arr_gss_n[i],
				                    ( i + 2 ), 2, 1, 1 )

			if ( self.arr_gss_d[i] is not None ) :
				self.grd.addWidget( self.arr_gss_d[i],
				                    ( i + 2 ), 3, 1, 1 )

			if ( self.arr_gss_w[i] is not None ) :
				self.grd.addWidget( self.arr_gss_w[i],
				                    ( i + 2 ), 4, 1, 1 )

			if ( self.arr_sel_a[i] is not None ) :
				self.grd.addWidget( self.arr_sel_a[i],
				                    ( i + 2 ), 5, 1, 1 )

			if ( self.arr_sel_b[i] is not None ) :
				self.grd.addWidget( self.arr_sel_b[i],
				                    ( i + 2 ), 6, 1, 1 )

		# Regularize the grid spacing.

		for i in range( 7 ) :
			self.grd.setColumnStretch( i, 1 )

		for i in range( self.core.nln_n_pop + 2 ) :
			self.grd.setRowStretch( i, 1 )

		# Populate the text areas.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR DISPLAYING TEXT IN THE TEXT AREAS.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Display the settings for for each ion species.

		for p in range( self.core.nln_n_pop ) :

			# Display the parameter values.

			if ( self.arr_name[p] is not None ) :
				self.arr_name[p].setText(
				            self.core.nln_plas.arr_pop[p][
				                              'full_name_sym'] )

			if ( ( self.arr_gss_n[p]          is not None ) and
			     ( self.core.nln_set_gss_n[p] is not None )     ) :
				self.arr_gss_n[p].setTextUpdate(
				             str( self.core.nln_set_gss_n[p] ) )

			if ( ( self.arr_gss_d[p]          is not None ) and
			     ( self.core.nln_set_gss_d[p] is not None )     ) :
				self.arr_gss_d[p].setTextUpdate(
				             str( self.core.nln_set_gss_d[p] ) )

			if ( ( self.arr_gss_w[p]          is not None ) and
			     ( self.core.nln_set_gss_w[p] is not None )     ) :
				self.arr_gss_w[p].setTextUpdate(
				             str( self.core.nln_set_gss_w[p] ) )

			if ( ( self.arr_sel_a[p]          is not None ) and
			     ( self.core.nln_set_sel_a[p] is not None )     ) :
				self.arr_sel_a[p].setTextUpdate(
				             str( self.core.nln_set_sel_a[p] ) )

			if ( ( self.arr_sel_b[p]          is not None ) and
			     ( self.core.nln_set_sel_b[p] is not None )     ) :
				self.arr_sel_b[p].setTextUpdate(
				             str( self.core.nln_set_sel_b[p] ) )

			# Select the background color of the text areas based on
			# whether or not the ion species is in use and on
			# whether or not a non-zero differential flow is
			# considered.

			if ( self.core.nln_pop_use[p] ) :
				ss_gss_n = 'background-color: white;\n'
				ss_gss_d = 'background-color: white;\n'
				ss_gss_w = 'background-color: white;\n'
				ss_sel_a = 'background-color: white;\n'
				ss_sel_b = 'background-color: white;\n'
			else :
				ss_gss_n = 'background-color: gray;\n'
				ss_gss_d = 'background-color: gray;\n'
				ss_gss_w = 'background-color: gray;\n'
				ss_sel_a = 'background-color: gray;\n'
				ss_sel_b = 'background-color: gray;\n'

			if ( not self.core.nln_plas.arr_pop[p]['drift'] ) :
				ss_gss_d = 'background-color: gray;\n'

			# Select the text color based on the validity of the
			# printed parameter value.

			if ( ( self.core.nln_set_gss_n[p] is None     ) and
			     ( self.arr_gss_n[p]          is not None ) and
			     ( len( self.arr_gss_n[p].text( ) ) > 0   )     ) :
				ss_gss_n += 'color: red;'
			else :
				ss_gss_n += 'color: black;'

			if ( ( self.core.nln_set_gss_d[p] is None     ) and
			     ( self.arr_gss_d[p]          is not None ) and
			     ( len( self.arr_gss_d[p].text( ) ) > 0   )     ) :
				ss_gss_d += 'color: red;'
			else :
				ss_gss_d += 'color: black;'

			if ( ( self.core.nln_set_gss_w[p] is None     ) and
			     ( self.arr_gss_w[p]          is not None ) and
			     ( len( self.arr_gss_w[p].text( ) ) > 0   )     ) :
				ss_gss_w += 'color: red;'
			else :
				ss_gss_w += 'color: black;'

			if ( ( self.core.nln_set_sel_a[p] is None     ) and
			     ( self.arr_sel_a[p]          is not None ) and
			     ( len( self.arr_sel_a[p].text( ) ) > 0   )     ) :
				ss_sel_a += 'color: red;'
			else :
				ss_sel_a += 'color: black;'

			if ( ( self.core.nln_set_sel_b[p] is None     ) and
			     ( self.arr_sel_b[p]          is not None ) and
			     ( len( self.arr_sel_b[p].text( ) ) > 0   )     ) :
				ss_sel_b += 'color: red;'
			else :
				ss_sel_b += 'color: black;'

			# Apply the changes to the style sheets.

			if ( self.arr_gss_n[p] is not None ) :
				self.arr_gss_n[p].setStyleSheet( ss_gss_n )

			if ( self.arr_gss_d[p] is not None ) :
				self.arr_gss_d[p].setStyleSheet( ss_gss_d )

			if ( self.arr_gss_w[p] is not None ) :
				self.arr_gss_w[p].setStyleSheet( ss_gss_w )

			if ( self.arr_sel_a[p] is not None ) :
				self.arr_sel_a[p].setStyleSheet( ss_sel_a )

			if ( self.arr_sel_b[p] is not None ) :
				self.arr_sel_b[p].setStyleSheet( ss_sel_b )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running, reset
		# the text in the text box and abort.

		if ( n_thread( ) != 0 ) :
			self.make_txt( )
			return

		# Determine which ion population has been changed by the user.

		i = int( fnc[2:] )

		# Determine which parameter has been changed and what its new
		# value is.

		if   ( fnc[0:2] == 'gn' ) :

			param = 'gss_n'

			try :
				val = float( self.arr_gss_n[i].text( ) )
			except :
				val = None

		elif ( fnc[0:2] == 'gd' ) :

			param = 'gss_d'

			try :
				val = float( self.arr_gss_d[i].text( ) )
			except :
				val = None

		elif ( fnc[0:2] == 'gw' ) :

			param = 'gss_w'

			try :
				val = float( self.arr_gss_w[i].text( ) )
			except :
				val = None

		elif ( ( fnc[0:2] == 's-' ) or ( fnc[0:2] == 's+' ) ) :

			param = 'sel'

			try :
				val_a = float( self.arr_sel_a[i].text( ) )
			except :
				val_a = None

			try :
				val_b = float( self.arr_sel_b[i].text( ) )
			except :
				val_b = None

			val = [ val_a, val_b ]

		else :

			return

		# Instruct the core to update its ion parameters appropriately.

		Thread( target=thread_chng_nln_set,
		        args=( self.core, i, param, val ) ).start( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_ion" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_ion( self ) :

		# Regenerate the text in this widget.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_set" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_set( self ) :

		# Regenerate the text in this widget.

		self.make_txt( )
