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

# Load the modules for displaying text output.

from janus_format_TextEdit import format_TextEdit

################################################################################
## DEFINE THE "widget_mfi_info" CLASS TO CUSTOMIZE "format_TextEdit".
################################################################################

class widget_mfi_info( format_TextEdit ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attribues of an instance of "format_TextEdit".

		super( widget_mfi_info, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_mfi'),
		                                            self.resp_chng_mfi )

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

		if ( self.core.fc_spec is None ) :
			return

		# If a Wind/FC ion spectrum has been (successfully) loaded, but
		# there are no Wind/MFI data (yet), return.

		if ( self.core.n_mfi <= 0 ) :
			return

		# Print a summary of the Wind/MFI data.

		self.prnt_htm( 'Number of Data:&nbsp;&nbsp;' )
		self.prnt_int( self.core.n_mfi )
		self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_htm( '<i>B</i> = ' )
		self.prnt_dcm( self.core.mfi_avg_mag, 1, 'nT' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i><font color="#FF0000">B<sub>x</sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_avg_vec[0], 1, 'nT' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i><font color="#00FF00">B<sub>y</sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_avg_vec[1], 1, 'nT' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i><font color="#0000FF">B<sub>z</sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_avg_vec[2], 1, 'nT' )
		self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i><font color="#8B008B">B<sub>&lambda;</sub></i> = ')
		self.prnt_dcm( self.core.mfi_amag_ang[0], 1, '<sup>o</sup>' )
		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i><font color="#FFD700">B<sub>&phi;</sub></i> = ')
		self.prnt_dcm( self.core.mfi_amag_ang[1], 1, '<sup>o</sup>' )
		self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_tab( 1 )
		self.prnt_htm( '<i>&Psi;<sub>B<sub><i> = ' )
		self.prnt_dcm( self.core.mfi_psi_b_avg, 1, '<sup>o</sup>')


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Clear the text.

		self.clear( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mfi" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mfi( self ) :

		# Regenerate the text.

		self.make_txt( )
