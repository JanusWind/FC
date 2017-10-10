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

# Load the modules necessary for mathematical and array operations.

from numpy import array, floor, where

# Load the Python modules necessary handling dates and times.

from time import gmtime

from calendar import timegm

from datetime import datetime, timedelta


## +----------+----------+-----------------------------------------------------+
## |          |          |                                                     |
## | Variable |          |                                                     |
## |   Name   |   Type   | Comments                                            |
## |          |          |                                                     |
## +----------+----------+-----------------------------------------------------+
## |          |          |                                                     |
## | time_val |   float  | Number of seconds (rounded to third decimal place)  |
## |          |          | since "1970-01-01/00:00:00.000"                     |
## |          |          |                                                     |
## | time_str |    str   | xxxx-xx-xx/xx:xx:xx.xxx                             |
## |          |          | 01234567890123456789012                             |
## |          |          | 0         1          2                              |
## |          |          |                                                     |
## | time_sec |    str   | Same format as "time_str" but without final four    |
## |          |          | characters                                          |
## |          |          |                                                     |
## | time_epc | datetime |                                                     |
## |          |          |                                                     |
## +----------+----------+-----------------------------------------------------+


################################################################################
## DEFINE THE FUNCTION FOR COMPUTING TIME AS A VALUE.
################################################################################

def calc_time_val( time ) :

	# If this function has been called on "None" or an empty string, simply
	# return "None".

	if ( ( time is None ) or ( time == '' ) ) :
		return None

	# If "time" is a "datetime" epoch or a string, compute the elapsed time
	# of "time" since "1970-01-01/00:00:00.000".  Otherwise, assume that
	# "time" is a numerical quantity, and return "time" recast as a "float"
	# rounded to three decimal places (to "standardize" it).

	if ( ( type( time ) == datetime ) or 
	     ( type( time ) == str      )    ) :

		# Attempt to standardize the "datetime" epoch "time".  If this
		# fails, abort (returning "None").

		time_epc = calc_time_epc( time )

		if ( time_epc is None ) :
			return None

		# Create a "datetime" object for "1970-01-01/00:00:00.000".

		unix_epc = datetime( 1970, 1, 1, 0, 0, 0, 0 )

		# Return the number of seconds elased from "unix_epc" to
		# "time_epc" rounded to the thrid decimal place.

		return round( float( 
		                 ( time_epc - unix_epc ).total_seconds( ) ), 3 )

	else :

		# Assume that "time" is a numerical quantity, and attempt to
		# return it recast as a "float" rounded to three decimal places.
		# If this fails, return "None" instead.

		try :
			return round( float( time ), 3 )
		except :
			return None


################################################################################
## DEFINE THE FUNCTION FOR COMPUTING TIME AS A STRING.
################################################################################

def calc_time_str( time ) :

	# If this function has been called on "None" or an empty string, simply
	# return "None".

	if ( ( time is None ) or ( time == '' ) ) :
		return None

	# If "time" is a string, return a standardized form of it.  Otherwise,
	# convert/standardize it to a "datetime" epoch and convert and return
	# that to a strandardized string time.

	if ( type( time ) == str ) :

		# Initialize the array of sub-string components with just the
		# string argument itself.

		comp = array( [ time ] )

		# Specify the list of valid separator characters.

		sep = array( [ '-', ' ', ',', '/', ':' ] )

		# Progressively break each of the sub-string componets into yet
		# small components using each of the seperator characters.

		for s in sep :

			# Break-up each sub-string based on the current
			# separation character.

			comp = array( [ c.split( s ) for c in comp ] )

			# Flatten the array of sub-string components.

			comp = array( [ c for sub in comp for c in sub ] )

		# Remove any empty strings from the array of sub-string
		# components.

		tk = where( comp != '' )[0]

		comp = comp[tk]

		# Determine the number of sub-string components.  If that number
		# is too small to even specify a date, return "None"

		n_comp = len( comp )

		if ( n_comp < 3 ) :
			None

		# Try converting the sub-string components into numerical
		# values.  If it doesn't work, return "None".

		try :

			t_year =   int( comp[0] )
			t_mon  =   int( comp[1] )
			t_day  =   int( comp[2] )
			t_hour =   int( comp[3] ) if ( n_comp > 3 ) else 0
			t_min  =   int( comp[4] ) if ( n_comp > 4 ) else 0
			t_sec  = float( comp[5] ) if ( n_comp > 5 ) else 0.

		except :

			return None

	else :

		# Try to convert/standardize "time" to a "datetime" epoch.  If
		# this fails, return "None".

		time_epc = calc_time_epc( time )

		if ( time_epc is None ) :
			return None

		# Extract the individual components of the "datetime" epoch.

		t_year = time_epc.year
		t_mon  = time_epc.month
		t_day  = time_epc.day
		t_hour = time_epc.hour
		t_min  = time_epc.minute
		t_sec  = round( time_epc.second +
		                ( time_epc.microsecond / 1.E6 ), 3 )

	# Create and return a standard-form string time.

	return '{:04d}-{:02d}-{:02d}/{:02d}:{:02d}:{:06.3f}'.format(
	                            t_year, t_mon, t_day, t_hour, t_min, t_sec )


################################################################################
## DEFINE THE FUNCTION FOR COMPUTING TIME AS A "datetime" EPOCH.
################################################################################

def calc_time_epc( time ) :

	# Note.  This function assumes that "time" is either a numerical
	#        quantity or a string in the formats described above.

	# If this function has been called on "None" or an empty string, simply
	# return "None".

	if ( ( time is None ) or ( time == '' ) ) :
		return None

	# If "time" is already an "datetime" epoch, return it unmodified.

	if ( type( time ) == datetime ) :
		return time

	# If "time" is a string, standardize it, extract its individual time
	# components, and return the equivalant "datetime" epoch.  Otherwise,
	# assume that it is a value, standardize it, and return the equivalant
	# "datetime" epoch.

	if ( type( time ) == str ) :

		# Try to standardize the string.  If this doesn't work, return
		# "None".

		time_str = calc_time_str( time )

		# Try to Extract/compute the year, month, day, hour, minute,
		# second, and microsecond numbers and to use them to compute the
		# corresponding "datetime" epoch.  If this works, return the
		# "datetime" epoch; otherwise, return "None".

		try :

			t_year = int( time_str[0:4]           )
			t_mon  = int( time_str[5:7]           )
			t_day  = int( time_str[8:10]          )
			t_hour = int( time_str[11:13]         )
			t_min  = int( time_str[14:16]         )
			t_sec  = int( time_str[17:19]         )
			t_mcsc = int( time_str[20:23] + '000' )

			return datetime( t_year, t_mon, t_day,
			                 t_hour, t_min, t_sec, t_mcsc )

		except :

			return None

	else :

		# Assume the "time" is a numerical value and try to construct a
		# corresponding "timedelta" object.  If this doesn't work,
		# return "None".

		try :
			td = timedelta( seconds=time )
		except :
			return None

		# Return the equivalant "datetime" epoch.

		return datetime( 1970, 1, 1, 0, 0, 0, 0 ) + td


################################################################################
## DEFINE THE FUNCTION FOR COMPUTING TIME AS A STRING (ROUNDED TO SECONDS).
################################################################################

def calc_time_sec( time ) :

	# If this function has been called on "None" or an empty string, simply
	# return "None".

	if ( ( time is None ) or ( time == '' ) ) :
		return None

	# Try to convert the argument "time" to a value and to round that value
	# to the nearest second.  If this fails, abort (returning "None").

	time_val = calc_time_val( time )

	if ( time_val is None ) :
		return None

	time_val_sec = round( time_val, 0 )

	# Convert the rounded time value to a string and truncate it.

	time_str_sec = ( calc_time_str( time_val_sec ) )[0:19]

	# Return the truncated string.

	return time_str_sec
