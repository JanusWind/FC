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

# Load the customized push button and one-line text editor.

from janus_event_CheckBox import event_CheckBox
from janus_event_LineEdit import event_LineEdit
from janus_event_PushButton import event_PushButton

# Load the modules necessary for time conversion.

from janus_time import calc_time_epc, calc_time_sec, calc_time_str


################################################################################
## DEFINE CLASS "dialog_auto_ctrl" TO CUSTOMIZE "QDialog" FOR AUTO-RUN CONTROL.
################################################################################

class dialog_auto_ctrl( QDialog ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, time_strt='', time_stop='',
	                    get_next=False, err_halt=True ) :

		# Inherit all attributes of an instance of "QDialog".

		super( dialog_auto_ctrl, self ).__init__( )

		# Make this a modal dialog (i.e., block user-interaction with
		# the main application window while this dialog exists).

		self.setModal( True )

		# Set the title of this dialog window.

		self.setWindowTitle( 'Range of Spectra' )

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Create the sub-grids and add them to the widget's main grid.

		self.sg1 = QGridLayout( )
		self.sg2 = QGridLayout( )

		self.sg1.setContentsMargins( 0, 0, 0, 0 )
		self.sg2.setContentsMargins( 0, 0, 0, 0 )

		self.grd.addLayout( self.sg1, 0, 0, 1, 1 )
		self.grd.addLayout( self.sg2, 1, 0, 1, 1 )

		# Initialize the text boxes, buttons, and labels that comprise
		# this dialog box.

		self.lab_strt = QLabel( 'Start:' )
		self.lab_stop = QLabel( 'Stop:'  )
		self.lab_next = QLabel( 'Begin with next:'   )
		self.lab_halt = QLabel( 'Halt on NLN error:' )

		self.txt_strt = event_LineEdit( self, 'strt' )
		self.txt_stop = event_LineEdit( self, 'stop' )

		self.box_next = event_CheckBox( self, 'next' )
		self.box_halt = event_CheckBox( self, 'halt' )

		self.btn_auto = event_PushButton( self, 'auto', 'Auto-Run' )
		self.btn_cncl = event_PushButton( self, 'cncl', 'Cancel'   )

		# Set a minimum size for the text boxes.

		self.txt_strt.setMinimumWidth( 150 )
		self.txt_stop.setMinimumWidth( 150 )

		# Adjust the button defaults.

		self.btn_auto.setDefault( False )
		self.btn_cncl.setDefault( False )

		# Row by row, add the text boxes, buttons, and labels to this
		# widget's sub-grids.

		self.sg1.addWidget( self.lab_strt, 0, 0, 1, 1 )
		self.sg1.addWidget( self.txt_strt, 0, 1, 1, 1 )
		self.sg1.addWidget( self.lab_next, 0, 2, 1, 1 )
		self.sg1.addWidget( self.box_next, 0, 3, 1, 1 )

		self.sg1.addWidget( self.lab_stop, 1, 0, 1, 1 )
		self.sg1.addWidget( self.txt_stop, 1, 1, 1, 1 )
		self.sg1.addWidget( self.lab_halt, 1, 2, 1, 1 )
		self.sg1.addWidget( self.box_halt, 1, 3, 1, 1 )

		self.sg2.addWidget( self.btn_auto, 0, 0, 1, 1 )
		self.sg2.addWidget( self.btn_cncl, 0, 1, 1, 1 )

		# Initialize the requested start and stop timestamps using the
		# user-provided values (if any).

		# Note.  The call of "self.aply_time" below initializes the
		#        "self.time_????" and "self.vld_????" parameters and
		#        populates the text boxes approriately.


		self.aply_time( time_strt=time_strt, time_stop=time_stop,
		                get_next=get_next, err_halt=err_halt      )

		# Select (i.e., highlight) any and all text in the text box for
		# the start time.

		# Note.  By highlighting this text, the user can more easily
		#        delete any default start time that may have been
		#        provided (via the "time_strt" argument of this
		#        function).

		self.txt_strt.selectAll( )

		# Initialize the object to be returned to the user on the close
		# of this dialog window.

		# Note.  The value of "self.ret" should only ever be changed to
		#        something other than "None" in response to the "auto"
		#        button being pressed (or an equivalent action).

		self.ret = None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETRIEVING THE TIMESTAMPS.
	#-----------------------------------------------------------------------

	def rtrv_time( self ) :

		# Attempt to retrieve each timestamp.

		# Note.  If the function "calc_time_epc" is given input that it
		#        cannot process, it should return "None".

		self.time_strt = calc_time_epc( str( self.txt_strt.text( ) ) )
		self.time_stop = calc_time_epc( str( self.txt_stop.text( ) ) )
		self.get_next  = self.box_next.isChecked( )
		self.err_halt  = self.box_halt.isChecked( )

		# Validate the timestamps and update the text color of the text
		# boxes appropriately.

		self.vldt_time( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR VALIDATING THE TIMESTAMPS.
	#-----------------------------------------------------------------------

	def vldt_time( self ) :

		# Validate each timestamp.  Assume that each value is valid
		# unless it "is None".

		self.vld_strt = False if ( self.time_strt is None ) else True
		self.vld_stop = False if ( self.time_stop is None ) else True

		# Validate the range specified by the timestamps.  The range is
		# valid only if each of the individual timestamps is itself
		# valid and the stop timestamp occurs after the start timestamp.

		if ( ( self.vld_strt ) and ( self.vld_stop ) ) :

			if ( self.time_stop >= self.time_strt ) :
				self.vld_rang = True
			else :
				self.vld_rang = False

		else :

			self.vld_rang = False

		# For any valid timestamp, standardize the text shown in its
		# corresponding text box.

		if ( self.vld_strt ) :
			self.txt_strt.setTextUpdate(
			                       calc_time_sec( self.time_strt ) )

		if ( self.vld_stop ) :
			self.txt_stop.setTextUpdate(
			                       calc_time_sec( self.time_stop ) )

		# Update the text color of each text box to indicate the
		# validity of it's contents.

		if ( ( self.vld_strt ) and ( self.vld_stop ) ) :

			if ( self.vld_rang ) :
				self.txt_strt.setStyleSheet( 'color: black;' )
				self.txt_stop.setStyleSheet( 'color: black;' )
			else :
				self.txt_strt.setStyleSheet( 'color: red;' )
				self.txt_stop.setStyleSheet( 'color: red;' )
		else :

			if ( ( self.vld_strt                      ) or
			     ( str( self.txt_strt.text( ) ) == '' )    ) :
				self.txt_strt.setStyleSheet( 'color: black;' )
			else :
				self.txt_strt.setStyleSheet( 'color: red;' )

			if ( ( self.vld_stop                      ) or
			     ( str( self.txt_stop.text( ) == '' ) )    ) :
				self.txt_stop.setStyleSheet( 'color: black;' )
			else :
				self.txt_stop.setStyleSheet( 'color: red;' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR APPLYING SPECIFED TIMESTAMPS TO TEXT BOXES.
	#-----------------------------------------------------------------------

	def aply_time( self, time_strt=None, time_stop=None,
	                     get_next=None, err_halt=None    ) :

		# For each timestamp for which a new value was specified, apply
		# that new value.

		for ( bx, tm ) in [ ( self.txt_strt, time_strt ),
		                    ( self.txt_stop, time_stop )  ] :

			# If no new value was specified for this timestamp, more
			# onto the next one.

			if ( tm is None ) :
				continue

			# Convert the new timestamp value into a string
			# (accurate to the second).

			tm_str = calc_time_sec( tm )

			tm_str = '' if ( tm_str is None ) else tm_str

			# Update the corresponding text box with the string
			# generated for the new value.

			bx.setTextUpdate( tm_str )


		# If requested, update the state of the checkbox(es).

		if ( get_next is not None ) :
			self.box_next.setChecked( get_next )

		if ( err_halt is not None ) :
			self.box_halt.setChecked( err_halt )


		# Retrieve (and subsequently validate) the new timestamp
		# value(s).

		self.rtrv_time( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PURGING TIMESTAMP INFORMATION.
	#-----------------------------------------------------------------------

	def purg_time( self ) :

		# Remove all text from the text boxes (and subsequently retrieve
		# and validate the [now empty] timestamp values from the those
		# text boxes).

		self.aply_time( time_strt='', time_stop='',
		                get_next=False, err_halt=True )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, fnc ) :

		# If the event was from the cancel button, close this dialog
		# window.

		if ( fnc == 'cncl' ) :

			self.close( )

			return

		# Retrieve (and subsequently validate) the timestamp values in
		# the text boxes.

		self.rtrv_time( )

		# If the event was from the auto-run button and the timestamp
		# range is valid, generate the return object and close this
		# dialog window.

		if ( ( fnc == 'auto' ) and ( self.vld_rang ) ) :

			self.ret = ( self.time_strt, self.time_stop,
			             self.get_next, self.err_halt    )

			self.close( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROMPTING THE USER FOR A RANGE OF TIMESTAMPS.
	#-----------------------------------------------------------------------

	def get_time_rang( self ) :

		# Execute this dialog.

		self.exec_( )

		# Return the return object.

		return self.ret
