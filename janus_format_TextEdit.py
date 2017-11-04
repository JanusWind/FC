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

from PyQt4.QtGui import QTextEdit

import platform
import os


################################################################################
## DEFINE THE "format_TextEdit" CLASS TO EXTEND "QTextEdit" FORMATTING OPTIONS.
################################################################################

class format_TextEdit( QTextEdit ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self ) :

		# Inherit all attributes of an instance of "QTextEdit".

		super( format_TextEdit, self ).__init__( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PRINTING AN INDENTATION.
	#-----------------------------------------------------------------------

	def prnt_tab( self, t=1 ) :

		# Based on the value of "t", print an appropriate number of
		# white spaces.

		if ( t >= 1 ) :
			self.insertHtml( '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' )
		if ( t >= 2 ) :
			self.insertHtml( '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' )
			self.insertHtml( '&nbsp;&nbsp;'                   )
		if ( t >= 3 ) :
			self.insertHtml( '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' )
			self.insertHtml( '&nbsp;&nbsp;&nbsp;&nbsp;'       )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PRINTING A DECIMAL NUMBER.
	#-----------------------------------------------------------------------

	def prnt_dcm( self, num, dig=2, unt=None ) :

		# Convert "dig", the number of digits after the decimal place,
		# to a string.

		str_dig = '{:}'.format( int( round( dig ) ) )

		# Print the number "num" with "dig" digits after the decimal
		# point.

		self.insertHtml( ( '{:.' + str_dig + 'f}' ).format( num ) )

		# If "str_dig" is "0", then add in a decimal place (which is
		# otherwise omitted when no decimal places are requested.

		if ( str_dig == '0' ) :

			self.insertHtml( '.' )

		# If a string has been provided for the unit, print it as well.

		if ( unt is not None ) :

			self.insertHtml( '&nbsp;' + unt )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PRINTING AN INTEGER.
	#-----------------------------------------------------------------------

	def prnt_int( self, num ) :

		# In case "num" isn't already an integer, make it one by
		# rounding.

		int_num = int( round( num ) )

		# Print the integer "int_num".

		self.insertHtml( '{:}'.format( int_num ) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PRINTING A LINE BREAK.
	#-----------------------------------------------------------------------

	def prnt_brk( self ) :

		# Print a line break.

		self.insertHtml( '<br>' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PRINTING GENERAL HTML TEXT.
	#-----------------------------------------------------------------------

	def prnt_htm( self, s , speak=False) :

		# Print the string "s" (as HTML code)..

		self.insertHtml( s )

		# For analysis that can take a long time to run, this is a helpful
		# reminder to check the result.
		if speak and platform.system() == "Darwin":
			os.system('say "%s"' % s)

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR TESTING WHETHER THE TEXT AREA IS EMPTY.
	#-----------------------------------------------------------------------

	def is_empty( self ) :

		# If the text area contains no text, return "True"; otherwise,
		# return "False".

		if ( self.toPlainText( ) == '' ) :
			return True
		else :
			return False
