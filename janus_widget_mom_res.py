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

# Load the necessary modules for signaling the graphical interface.

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QTextCursor

# Load the modules for displaying text output.

from janus_format_TextEdit import format_TextEdit


################################################################################
## DEFINE THE "widget_mom_res" CLASS TO CUSTOMIZE "format_TextEdit".
################################################################################

class widget_mom_res( format_TextEdit ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attribues of an instance of "format_TextEdit".

		super( widget_mom_res, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_mfi'),
		                                            self.resp_chng_mfi )
		self.connect( self.core, SIGNAL('janus_chng_mom_res'),
		                                        self.resp_chng_mom_res )

		# Set this text editor as read only (for the user).

		self.setReadOnly( True )

		# Populate this text editor with general information about this
		# spectrum's MFI data.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GENERATING THE TEXT FOR THIS TEXT AREA.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Clear the text area (just in case there's some text already
		# there).

		self.clear( )

		# If no Wind/FC ion spectrum has been (successfully) loaded,
		# return.

		if ( self.core.time_epc is None ) :
			return

		if ( self.core.n_bin == 0 ) :
			return

		# If the moments analysis has failed or has not been performed,
		# return.

		if ( self.core.mom_n is None ) :
			return

		# Print the results of the moments analysis.

		#self.prnt_htm( '<table border="0" width="100%">\n' +
		#               '<tr><td><i>n<sub>p</sub></i> = </td>' +
		#                   '<td>value</td></tr>\n' +
		#               '<tr><td>name</td>' +
		#                   '<td>value</td></tr>\n' +
		#               '<tr><td>name</td>' +
		#                   '<td>value</td></tr>\n' +
		#               '<tr><td>name</td>' +
		#                   '<td>value</td></tr>\n' +
		#               '<tr><td>name</td>' +
		#                   '<td>value</td></tr>\n' +
		#               '<tr><td>name</td>' +
		#                   '<td>value</td></tr>\n' +
		#               '</table>' )

		self.prnt_htm( '<i>n<sub>p</sub></i> = ' )
		self.prnt_dcm( self.core.mom_n, 2, 'cm<sup>-3</sup>' )
		self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_htm( '<i>v<sub>p</sub></i> = ' )
		self.prnt_dcm( self.core.mom_v, 0, 'km/s' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i>v<sub>xp</sub></i> = ' )
		self.prnt_dcm( self.core.mom_v_vec[0], 0, 'km/s' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i>v<sub>yp</sub></i> = ' )
		self.prnt_dcm( self.core.mom_v_vec[1], 0, 'km/s' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i>v<sub>zp</sub></i> = ' )
		self.prnt_dcm( self.core.mom_v_vec[2], 0, 'km/s' )
		self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_htm( '<i>w<sub>p</sub></i> = ' )
		self.prnt_dcm( self.core.mom_w, 0, 'km/s' )
		self.prnt_brk( )

		if ( self.core.mom_r is not None ) :

			self.prnt_tab( 1 )
			self.prnt_htm( '<i>w</i><sub>&perp;</sub>' )
			self.prnt_htm( '<sub><i>p</i></sub> = ')
			self.prnt_dcm( self.core.mom_w_per, 0, 'km/s' )
			self.prnt_brk( )

			self.prnt_tab( 1 )
			self.prnt_htm( '<i>w</i><sub>||</sub>' )
			self.prnt_htm( '<sub><i>p</i></sub> = ')
			self.prnt_dcm( self.core.mom_w_par, 0, 'km/s' )
			self.prnt_brk( )

			self.prnt_tab( 1 )
			self.prnt_htm( '<i>R<sub>p</sub></i> = ')
			self.prnt_dcm( self.core.mom_r, 2 )
			self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_htm( '<i>T<sub>p</sub></i> = ' )
		self.prnt_dcm( self.core.mom_t, 1, 'kK' )

		if ( self.core.mom_r is not None ) :

			self.prnt_brk( )

			self.prnt_tab( 1 )
			self.prnt_htm( '<i>T</i><sub>&perp;</sub>' )
			self.prnt_htm( '<sub><i>p</i></sub> = ')
			self.prnt_dcm( self.core.mom_t_per, 1, 'kK' )
			self.prnt_brk( )

			self.prnt_tab( 1 )
			self.prnt_htm( '<i>T</i><sub>||</sub>' )
			self.prnt_htm( '<sub><i>p</i></sub> = ')
			self.prnt_dcm( self.core.mom_t_par, 1, 'kK' )
			self.prnt_brk( )

			self.prnt_tab( 1 )
			self.prnt_htm( '<i>R<sub>p</sub></i> = ')
			self.prnt_dcm( self.core.mom_r, 2 )

		# Scroll to the top of the text area.

		self.moveCursor( QTextCursor.Start )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Reset the text area.

		self.clear( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mfi" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mfi( self ) :

		# Replace the text in the text area.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mom_res" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mom_res( self ) :

		# Replace the text in the text area.

		self.make_txt( )
