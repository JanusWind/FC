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

from janus_event_CheckBox import event_CheckBox
from janus_event_ComboBox import event_ComboBox
from janus_event_LineEdit import event_LineEdit

# Load the necessary "numpy" array modules.

from numpy import tile

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_nln_pop


################################################################################
## DEFINE THE "widget_nln_ion" CLASS TO CUSTOMIZE "QWidget" FOR NLN ION SPECIES.
################################################################################

class widget_nln_pop( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_nln_pop, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_chng_nln_ion'),
		                                        self.resp_chng_nln_ion )
		self.connect( self.core, SIGNAL('janus_chng_nln_pop'),
		                                        self.resp_chng_nln_pop )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.setLayout( self.grd )

		# |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |
		# +-----+-----+-----+-----+-----+-----+-----+-----+
		# |Use? |Species    |Pop. Name  | Sym |Drft?|Anis?|
		# |Check|           |LineE      |LineE|Check|Check|

		# Initialize the labels, check boxes, and text areas that 
		# comprise this widget.

		self.hdr_use   = QLabel( ''          )
		self.hdr_ion   = QLabel( 'Species'   )
		self.hdr_name  = QLabel( 'Pop. Name' )
		self.hdr_sym   = QLabel( 'Symbol'    )
		self.hdr_drift = QLabel( 'Drift'     )
		self.hdr_aniso = QLabel( 'Aniso'     )

		self.arr_use   = tile( None, self.core.nln_n_pop )
		self.arr_ion   = tile( None, self.core.nln_n_pop )
		self.arr_name  = tile( None, self.core.nln_n_pop )
		self.arr_sym   = tile( None, self.core.nln_n_pop )
		self.arr_drift = tile( None, self.core.nln_n_pop )
		self.arr_aniso = tile( None, self.core.nln_n_pop )

		for i in range( self.core.nln_n_pop ) :

			txt_i = str( i )

			self.arr_ion[i]   = event_ComboBox( self, 'i'+txt_i )
			self.arr_name[i]  = event_LineEdit( self, 'n'+txt_i )
			self.arr_sym[i]   = event_LineEdit( self, 's'+txt_i )
			self.arr_aniso[i] = event_CheckBox( self, 'a'+txt_i )

			if ( i == 0 ) :
				continue

			self.arr_use[i]   = event_CheckBox( self, 'u'+txt_i )
			self.arr_drift[i] = event_CheckBox( self, 'd'+txt_i )

		# Row by row, add the labels, check boxes, and text areas, to
		# this widget's grid.

		self.grd.addWidget( self.hdr_use  , 0, 0, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_ion  , 0, 1, 1, 2 )
		self.grd.addWidget( self.hdr_name , 0, 3, 1, 2 )
		self.grd.addWidget( self.hdr_sym  , 0, 5, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_drift, 0, 6, 1, 1, Qt.AlignCenter )
		self.grd.addWidget( self.hdr_aniso, 0, 7, 1, 1, Qt.AlignCenter )

		for i in range( self.core.nln_n_pop ) :

			if ( self.arr_use[i] is not None ) :
				self.grd.addWidget( self.arr_use[i],
				                    i+1, 0, 1, 1,
				                    Qt.AlignCenter   )

			if ( self.arr_ion[i] is not None ) :
				self.grd.addWidget( self.arr_ion[i],
			                            i+1, 1, 1, 2      )

			if ( self.arr_name[i] is not None ) :
				self.grd.addWidget( self.arr_name[i],
			                            i+1, 3, 1, 2      )

			if ( self.arr_sym[i] is not None ) :
				self.grd.addWidget( self.arr_sym[i],
				                    i+1, 5, 1, 1,
				                    Qt.AlignCenter   )

			if ( self.arr_drift[i] is not None ) :
				self.grd.addWidget( self.arr_drift[i],
				                    i+1, 6, 1, 1,
				                    Qt.AlignCenter     )

			if ( self.arr_aniso[i] is not None ) :
				self.grd.addWidget( self.arr_aniso[i],
				                    i+1, 7, 1, 1,
				                    Qt.AlignCenter     )

		# Regularize the grid spacing.

		for i in range( 8 ) :
			self.grd.setColumnStretch( i, 1 )

		for i in range( self.core.nln_n_pop + 1 ) :
			self.grd.setRowStretch( i, 1 )

		# Populate the text areas.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR DISPLAYING TEXT AND CHECK MARKS.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Display the parameters for each ion population.

		for i in range( self.core.nln_n_pop ) :

			# Extract the values from the core.

			tmp_use = self.core.nln_pop_use[i]

			tmp_ion   = self.core.nln_plas.arr_pop[i]['spec']
			tmp_name  = self.core.nln_plas.arr_pop[i]['name']
			tmp_sym   = self.core.nln_plas.arr_pop[i]['sym']
			tmp_drift = self.core.nln_plas.arr_pop[i]['drift']
			tmp_aniso = self.core.nln_plas.arr_pop[i]['aniso']

			# Construct the list of ion-species names/symbols.

			lst_ion = [ str( s['name'] )
			            for s in self.core.nln_plas.arr_spec ]

			lst_ion = [ '' ]

			for s in self.core.nln_plas.arr_spec :

				txt = ''

				if ( s['name'] is not None ) :
					txt += s['name']

				txt += ' ('

				if ( s['sym'] is not None ) :
					txt += s['sym']

				txt += ')'

				lst_ion.append( txt )

			# Update the text of each each "LineEdit" and "CheckBox"
			# widget.

			if ( self.arr_use[i] is not None ) :
				self.arr_use[i].setChecked( tmp_use )

			if ( ( self.arr_name[i] is not None ) and
			     ( tmp_name         is not None )     ) :
				self.arr_name[i].setTextUpdate( tmp_name )

			if ( ( self.arr_sym[i] is not None ) and
			     ( tmp_sym         is not None )     ) :
				self.arr_sym[i].setTextUpdate( tmp_sym )

			if ( self.arr_drift[i] is not None ) :
				self.arr_drift[i].setChecked( tmp_drift )

			if ( self.arr_aniso[i] is not None ) :
				self.arr_aniso[i].setChecked( tmp_aniso )

			# Update each "ComboBox" widget.

			if ( self.arr_ion[i] is not None ) :

				self.arr_ion[i].clear( )
				self.arr_ion[i].addItems( lst_ion )

				try :
					s = self.core.nln_plas.arr_spec.index(
					                           tmp_ion ) + 1
				except :
					s = 0

				if ( tmp_ion is None ) :
					s = 0

				self.arr_ion[i].setCurrentIndex( s )

			"""
			# If a spectrum has been loaded but it has no magnetic
			# field data, disable the option of temperature
			# anisotropy; otherwise, enable it.

			if ( self.arr_aniso[i] is not None ) :

				if ( ( self.core.n_vel >  0 ) and
				     ( self.core.n_mfi <= 0 )     ) :
					self.arr_aniso[i].setVisible( False )
				else :
					self.arr_aniso[i].setVisible( True )


			# Disable the paralle differential flow option if one of
			# more of the following conditions are met:
			#   -- A spectrum has been loaded but it has no magnetic
			#      field data.
			#   -- The species "i" is being modeled as having no
			#      differential flow.
			# Otherwise, enable this option.

			if ( self.arr_par[i] is not None ) :

				if ( ( ( self.core.n_vel >  0 ) and
				       ( self.core.n_mfi <= 0 )       ) or
				     ( not self.core.nln_ion_drift[i] )    ) :
					self.arr_par[i].setVisible( False )
				else :
					self.arr_par[i].setVisible( True )

			"""

			# Format the text boxes (background and text colors).

			if ( tmp_use ) :
				ss_name = 'background-color: white;\n'
				ss_sym  = 'background-color: white;\n'
			else :
				ss_name = 'background-color: gray;\n'
				ss_sym  = 'background-color: gray;\n'

			if ( ( self.arr_name[i] is not None        ) and
			     ( tmp_name is None                    ) and
			     ( len( self.arr_name[i].text( ) ) > 0 )     ) :
				ss_name += 'color: red;'
			else :
				ss_name += 'color: black;'

			if ( ( self.arr_sym[i] is not None        ) and
			     ( tmp_sym is None                    ) and
			     ( len( self.arr_sym[i].text( ) ) > 0 )     ) :
				ss_sym += 'color: red;'
			else :
				ss_sym += 'color: black;'

			self.arr_name[i].setStyleSheet( ss_name )
			self.arr_sym[i].setStyleSheet(  ss_sym  )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If a "thread_*" computation thread is already running, reset
		# the text in the text box and abort.

		if ( n_thread( ) != 0 ) :
			self.make_txt( )
			return

		# Determine which population has been changed by the user.

		i = int( fnc[1:] )

		# Determine which parameter has been changed by the user and
		# what its new value is.

		if   ( fnc[0] == 'u' ) :

			param = 'use'
			val   = self.arr_use[i].isChecked( )

		elif ( fnc[0] == 'i' ) :

			param = 'spec'
			val   = self.arr_ion[i].currentIndex( ) - 1

		elif ( fnc[0] == 'n' ) :

			param = 'name'
			val   = str( self.arr_name[i].text( ) )

		elif ( fnc[0] == 's' ) :

			param = 'sym'
			val   = str( self.arr_sym[i].text( ) )

		elif ( fnc[0] == 'd' ) :

			param = 'drift'
			val   = self.arr_drift[i].isChecked( )

		elif ( fnc[0] == 'a' ) :

			param = 'aniso'
			val   = self.arr_aniso[i].isChecked( )

		else :

			return

		# Instruct the core to update its ion-population parameters 
		# appropriately.

		Thread( target=thread_chng_nln_pop,
		        args=( self.core, i, param, val ) ).start( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_pop" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_pop( self, i ) :

		# If the value of "i" is invalid, abort.

		try :
			i = int( i )
		except :
			return

		if ( ( i < 0 ) or ( i >= self.core.nln_n_pop ) ) :
			return

		# Clear the stored text for the i-th population's name and
		# symbol.

		self.arr_name[i].clear( )
		self.arr_sym[i].clear( )

		# Repopulate the text and checkmarks in this widget.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_ion" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_ion( self ) :

		# Repopulate the text and checkmarks in this widget.

		self.make_txt( )
