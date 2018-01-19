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

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QTextCursor

# Load the customized push button and one-line text editor.

from janus_format_TextEdit import format_TextEdit


################################################################################
## DEFINE CLASS "widget_ctrl_info" TO CUSTOMIZE "format_TextEdit" FOR STATUS.
################################################################################

class widget_ctrl_info( format_TextEdit ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_ctrl_info, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Initialize the the indicator of whether the text should be
		# cleared the next time a message is received.

		self.clear_for_next_mesg = True

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_mesg'), self.resp_mesg )
		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )

		# Set this text area as read only (for the user).

		self.setReadOnly( True )

		# This text area should be empty, so print a generic welcome
		# statement and reset the position of the vertical scroll bar
		# (in case printing the welcome statement has shifted it down).

		self.prnt_htm( '<b>Welcome to Janus!</b>' )
		self.prnt_brk( )
		self.prnt_brk( )

		self.prnt_htm( 'Version: ' + self.core.version )
		self.prnt_brk( )
		self.prnt_brk( )

		self.prnt_htm( 'To begin, use the text box to '      +
		                    'the left to enter a timestamp ' +
		                    'in this format:'                  )
		self.prnt_brk( )
		self.prnt_tab( 1 )
		self.prnt_htm( 'yyyy-mm-dd/hh:mm:ss' )
		self.prnt_brk( )
		self.prnt_brk( )

		self.prnt_htm( 'For more information, consult ' +
		                    'the user guide.'              )
		self.prnt_brk( )
		self.prnt_brk( )
		self.prnt_htm( 'Copyright &copy; 2016 Bennett A. Maruca ' +
		                    '(bmaruca@udel.edu)'                    )

		self.moveCursor( QTextCursor.Start )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR ADDING A MESSAGE TO THE TEXT AREA.
	#-----------------------------------------------------------------------

	def mesg_txt( self, mesg_src=None, mesg_typ=None, mesg_obj=None ) :

		# Attempt to extract the components of the argument "mesg",
		# which should contain strings indicating the source, type, and
		# (if applicable) the object of the message.  If anything seems
		# incorrectly formatted, abort.

		if ( ( mesg_src is None ) or ( mesg_typ is None ) ) :
			return

		mesg_src = mesg_src.lower( )
		mesg_typ = mesg_typ.lower( )

		if ( mesg_obj is None ) :
			mesg_obj = ''
		else :
			mesg_obj = mesg_obj.lower( )

		# If this widget had been instructed to clear itself the next
		# time it recieves a message, do so now.

		if ( self.clear_for_next_mesg ) :
			self.clear_for_next_mesg = False
			self.clear( )

		# Unless the text area is empty, add a line break.

		if ( not self.is_empty( ) ) :
			self.prnt_brk( )

		# If the message is from the Janus core itself, attept to add
		# a statement to the text area that is appropriate to the
		# message's type and (if applicable) object.

		if ( mesg_src == 'core' ) :

			if ( mesg_typ == 'begin' ) :

				if ( ( mesg_obj == 'fc'   ) or
				     ( mesg_obj == 'mfi'  ) or
				     ( mesg_obj == 'spin' )    ) :
					self.prnt_htm( 'Retrieving '    + 
					               mesg_obj.upper() +
					               ' data.'           )

				if ( mesg_obj == 'mom' ) :
					self.prnt_htm( 'Running ' +
					               'moments analysis.' )

				if ( mesg_obj == 'gss' ) :
					self.prnt_htm( 'Generating ' +
					               'NLN init. guess.' )

				if ( mesg_obj == 'sel' ) :
					self.prnt_htm( 'Generating ' +
					               'NLN point select.' )

				if ( mesg_obj == 'nln' ) :
					self.prnt_htm( 'Running ' +
					               'non-linear analysis.' )

				if ( mesg_obj == 'auto' ) :
					self.prnt_htm( 'Beginning ' +
					               'automated analysis.' )
					self.prnt_brk( )

				if ( mesg_obj == 'save' ) :
					self.clear( )
					self.prnt_htm( 'Saving results for ' +
					               'all spectra.'          )

				if ( mesg_obj == 'xprt' ) :
					self.clear( )
					self.prnt_htm( 'Exporting results ' +
					               'for all spectra.'     )

				if ( mesg_obj == 'debug' ) :
					self.clear( )
					self.prnt_htm( '<b>WARNING!</b>' )
					self.prnt_brk( )
					self.prnt_htm(
					     'Debugging mode has been '  +
					     'activated.  Incomplete '   +
					     'features may behave in '   +
					     'unexpected ways or casue ' +
					     'the program to crash.  '   +
					     'Proceed with caution.'       )

				if ( mesg_obj == 'haiku' ) :
					self.clear( )
					self.prnt_htm( 'Janus joint fitting:' )
					self.prnt_brk( )
					self.prnt_htm( 'powerful in principle,')
					self.prnt_brk( )
					self.prnt_htm( 'hard to implement' )

			if ( mesg_typ == 'norun' ) :

				if ( mesg_obj == 'mom' ) :
					self.prnt_htm( 'ERROR!  Can\'t ' +
					               'run moments.' , speak=True)

				if ( mesg_obj == 'nln' ) :
					self.prnt_htm( 'ERROR!  Can\'t ' +
					               'run NLN.' , speak=True)

			if ( mesg_typ == 'fail' ) :

				if ( mesg_obj == 'time' ) :
					self.prnt_htm( 'ERROR!  Invalid ' +
					               'timestamp.'         )

				if ( mesg_obj == 'mom' ) :
					self.prnt_tab( 1 )
					self.prnt_htm( 'ERROR!  Moments ' +
					               'failed.' , speak=True)

				if ( mesg_obj == 'nln' ) :
					self.prnt_tab( 1 )
					self.prnt_htm( 'ERROR!  NLN ' +
					               'analysis failed.' , speak=True)

				if ( mesg_obj == 'save' ) :
					self.prnt_tab( 1 )
					self.prnt_htm( 'ERROR!  Save failed.' , speak=True)
					self.clear_for_next_mesg = True

				if ( mesg_obj == 'xprt' ) :
					self.prnt_tab( 1 )
					self.prnt_htm( 'ERROR!  Export ' +
					               'failed.' , speak=True)
					self.clear_for_next_mesg = True

			if ( mesg_typ == 'abort' ) :

				if ( mesg_obj == 'auto' ) :
					self.prnt_brk( )
					self.prnt_htm( 'AUTO-RUN ABORTED!' , speak=True)

			if ( mesg_typ == 'end' ) :

				if ( mesg_obj == 'auto' ) :
					self.prnt_brk( )
					self.prnt_htm( 'Finished ' +
					               'automated analysis.' , speak=True)
				else :
					self.prnt_tab( 1 )

					speak = False
					if mesg_obj == 'nln': speak = True

					self.prnt_htm( 'Done.' , speak=speak)

				if ( mesg_obj == 'save' ) :
					self.clear_for_next_mesg = True

				if ( mesg_obj == 'xprt' ) :
					self.clear_for_next_mesg = True

				if ( mesg_obj == 'debug' ) :
					self.clear( )
					self.prnt_htm(
					     'Debugging mode has been ' +
					     'deactivated.'               )

		# If the message is from one of the data archives, attept to add
		# a statement to the text area that is appropriate to the
		# message's source, type, and (if applicable) object.

		if ( ( mesg_src == 'fc'   ) or
		     ( mesg_src == 'mfi'  ) or 
		     ( mesg_src == 'spin' )    ) :

			if ( mesg_typ == 'load' ) :
				self.prnt_tab( 1 )
				self.prnt_htm( mesg_obj )
				self.prnt_htm( ': loading.' )

			if ( mesg_typ == 'ftp' ) :
				self.prnt_tab( 1 )
				self.prnt_htm( mesg_obj )
				self.prnt_htm( ': downloading.' )

			if ( mesg_typ == 'fail' ) :
				self.prnt_tab( 1 )
				self.prnt_htm( mesg_obj )
				self.prnt_htm( ': FAILED!' )

			if ( mesg_typ == 'none' ) :
				self.prnt_tab( 1 )
				self.prnt_htm( 'ERROR!  No data found.',
				               speak=True                )

		# If the messae is a "val" message from "spin", then print the
		# spin period.

		if ( ( mesg_obj == 'spin' ) and ( mesg_typ == 'val' ) ) :

			if ( self.core.spin_period is None ) :
				txt = 'ASSUMED spin rate: '
			else :
				txt = 'Spin rate: '

			txt += str( self.core.fc_spec['rot'] )[0:5] + ' s'

			self.prnt_tab( 1 )
			self.prnt_htm( txt )

		# Scroll to the bottom of the text area.

		self.verticalScrollBar( ).setSliderPosition(
		                          self.verticalScrollBar( ).maximum( ) )

		# Force this widget to repaint (to ensure that the user will see
		# new messages promptly).

		self.repaint( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "mesg" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_mesg( self, mesg_src=None, mesg_typ=None, mesg_obj=None ) :

		# Add the message to the text area.

		self.mesg_txt( mesg_src, mesg_typ, mesg_obj )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Reset (i.e., clear) the text area.

		self.clear( )
