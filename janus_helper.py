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

from math import log10, floor, sqrt, fsum


################################################################################
## DEFINE THE FUNCTION FOR ROUNDING A VALUE AND CONVERTING IT TO A STRING.
################################################################################

# Define the function for rounding a value to a specified number of significant
# digits.

def round_sig( val, sig ) :

	if ( val is None ) :

		return None

	elif ( val == 0. ) :

		return 0.

	else :

		return round( val,
		              sig - int( floor( log10( abs( val ) ) ) ) - 1 )


################################################################################
## DEFINE THE FUNCTION FOR COMPUTING UNIT VECTOR 
################################################################################

# Define the function for computing unit vector

def calc_arr_norm( v ):

	mag = sqrt( fsum( [ c**2 for c in v ]) )

	return tuple( [ ( c/mag) for c in v ] )


################################################################################
## DEFINE THE FUNCTION FOR COMPUTING DOT PRODUCT
################################################################################

# Define the function for computing dot product

def calc_arr_dot( u,v ) :
	if ( len(u) != len(v) ) :
		raise TypeError( 'Unequal lengths.' )
	return fsum([ x[0]*x[1] for x in zip(u,v) ]) 


################################################################################
## DEFINE THE FUNCTIONS FOR CONVERTING TO/FROM NNI'S
################################################################################

# Note.  The set of "NNI" values is defined to include all non-negative integers
#        and "float('inf')".

# Define the function for converting a string to an NNI.

def str_to_nni( v ) :

	# Standardize the argument by ensuring that it is a string, writing
	# all letters in lower case, and removing whitespace.

	val = str( v ).lower( ).replace( ' ', '' )

	# If the string indicates an infinite value, return 'float( 'inf' )'.
	# Otherwise, attempt to return a non-negative integer.

	if ( ( val == 'inf' ) or ( val == 'infinity' ) ) :

		return float( 'inf' )

	else :

		# Convert the argument to an integer.

		ret = int( val )

		# If the integer is negative, raise an error.  Otherwise, return
		# it.

		if ( ret < 0 ) :
			raise TypeError( 'Negative integer not permitted.' )
			return None
		else :
			return ret

"""
# Define the function for converting a numerical value to a string with a
# specified number of significant digits.

def conv_val_to_str( val, sig ) :

	# Round the value to the specified number of significant digits.

	rnd = round_sig( val, sig )

	# Convert the rounded value into an appropriately formatted string and
	# return it.

	if ( ( abs( rnd ) >= 0.01     ) and
	     ( abs( rnd ) <  10.**sig )     ) :

		return( '{:f}'.format( rnd ) )

	else :

		return( '{:e}'.format( rnd ) )
"""
