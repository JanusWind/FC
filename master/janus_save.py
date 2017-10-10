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

# Load the modules for handling dates and times.

from janus_time import calc_time_sec

# Load the modules for generating file names.

import os.path


################################################################################
## DEFINE THE FUNCTION FOR GENERATING A BARE NAME FOR AN OUTPUT FILE.
################################################################################

def make_name( core ) :

	# Initialize the string to be returned.

	name = 'janus'


	# If the provided core has no results, return the file name as is.

	if ( len( core.series ) == 0 ) :

		return name

	# Retrieve the earliest and latest timestamps in the results of the
	# provided core, convert each to a string, and reformat each string.

	t1 = calc_time_sec( min( core.series['time'] ) )
	t2 = calc_time_sec( max( core.series['time'] ) )

	t1 = t1[0:10] + '-' + t1[11:13] + '-' + t1[14:16] + '-' + t1[17:19]
	t2 = t2[0:10] + '-' + t2[11:13] + '-' + t2[14:16] + '-' + t2[17:19]

	# Append the first timestamp to the file name.

	name += '_' + t1

	# If the provided coe only has only a signle result, return the file
	# name as is.

	if ( len( core.series ) == 1 ) :

		return name

	# Append the second timestamp to the file name.

	name += '_' + t2

	# Return the file name.

	return name


################################################################################
## DEFINE THE FUNCTION FOR GENERATING A FULL NAME FOR A SAVE FILE.
################################################################################

def make_name_save( core ) :

	# Return the the full name of the save file (complete with path and
	# extension).

	return os.path.join( os.path.dirname( __file__ ),
	                     'results', 'save',
	                     ( make_name( core ) + '.jns' ) )


################################################################################
## DEFINE THE FUNCTION FOR GENERATING A FULL NAME FOR AN EXPORT FILE.
################################################################################

def make_name_xprt( core ) :

	# Return the the full name of the export file (complete with path and
	# extension).

	return os.path.join( os.path.dirname( __file__ ),
	                     'results', 'export',
	                     ( make_name( core ) + '.dat' ) )
