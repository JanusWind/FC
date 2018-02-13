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
## DEFINE THE "widget_mfi_lin_plot" CLASS FOR "QWidget" TO PLOT MFI DATA.
################################################################################

class widget_fmo_info( format_TextEdit ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_fmo_info, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the core.

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

		self.prnt_htm( '<i>Amplitude</i>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#FF0000">A<sub>x\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_amp_x, 3, 'nT' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#00FF00">A<sub>y\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_amp_y, 3, 'nT' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#0000FF">A<sub>z\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_amp_z, 3, 'nT' )
		self.prnt_brk( )

		self.prnt_htm( '<i>Frequency</i>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#FF0000">&omega;<sub>x\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_frq_x, 3, 's <sup>-1<sup>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#00FF00">&omega;<sub>y\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_frq_y, 3, 's <sup>-1<sup>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#0000FF">&omega;<sub>z\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_frq_z, 3, 's <sup>-1<sup>' )
		self.prnt_brk( )

		self.prnt_brk( )

		self.prnt_htm( '<i>Phase</i>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#FF0000">&phi;<sub>x\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_phs_x, 3, '<sup>o<sup>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#00FF00">&phi;<sub>y\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_phs_y, 3, '<sup>o<sup>' )
		self.prnt_brk( )

		self.prnt_tab( 3 )
		self.prnt_htm( '<i><font color="#0000FF">&phi;<sub>z\
		                           </sub></font></i> = ' )
		self.prnt_dcm( self.core.mfi_phs_z, 3, '<sup>o<sup>' )
		self.prnt_brk( )

		self.prnt_brk( )

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
