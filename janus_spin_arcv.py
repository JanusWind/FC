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

# Load the modules necessary handling dates and times.

from datetime import datetime, timedelta

from janus_time import calc_time_str, calc_time_val, calc_time_epc

# Load the modules necessary for data handling.

from numpy import median, pi

# Load the modules necessary for file I/O (including FTP).

from spacepy import pycdf

import os.path

from glob import glob

from ftplib import FTP


################################################################################
## DEFINE THE "spin_arcv" CLASS FOR ACCESSING THE ARCHIVE OF Wind SPIN DATA.
################################################################################

class spin_arcv( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core=None, buf=None, win=None,
	                    n_file_max=float('inf'), n_date_max=None,
	                    path=None, verbose=None                   ) :

		# Save the arguments for later use and, if necessary,
		# provide values

		# Note.  The value of "n_file_max" is set at the end of this
		#        function via the "chng_n_file_max" function.

		self.core = core

		self.buf  = float( buf )            if ( buf is not None )\
		                                    else 3600.

		self.win  = int( win   )            if ( win is not None )\
		                                    else 5

		self.n_date_max = int( n_date_max ) if ( n_date_max 
		                                    is not None ) else 40

		self.path       = str( path )       if ( path  is not None )\
		                                    else os.path.join( 
		                                    os.path.dirname( 
		                                    __file__ ), 'data', 'spin' )

		self.verbose    = bool( verbose )   if ( verbose is not None )\
		                                    else True

		# Validate the values of the parameters.

		if ( self.buf < 0 ) :
			raise ValueError( 'Time buffer cannot be negative.'    )

		if ( self.win <= 0 ) :
			raise ValueError( 'Median window must be at least 1.'  )

		if ( self.n_date_max < 0 ) :
			raise ValueError( 'Maximum number of dates ' +
			                                 'cannot be negative.' )

		# Initialize the list of dates loaded.

		self.arr_date = [ ]

		# Initialize the data lists.

		self.arr_spin_t   = [ ]
		self.arr_spin_w   = [ ]
		self.arr_spin_ind = [ ]

		# Initialize "n_file_max"

		self.chng_n_file_max( n_file_max )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING (AND RETURNING) A SPIN RATE.
	#-----------------------------------------------------------------------

	def load_spin( self, time ) :

		# Compute the requested time both as a standard-format string
		# and a "datetime" object.

		time_str = calc_time_str( time )
		time_epc = calc_time_epc( time )

		# Construct a list of the dates requested.

		req_date = [ ]

		tm_strt = time_epc - timedelta( seconds=self.buf )
		tm_stop = time_epc + timedelta( seconds=self.buf )

		dt_strt = datetime( tm_strt.year, tm_strt.month, tm_strt.day )
		dt_stop = datetime( tm_stop.year, tm_stop.month, tm_stop.day )

		dt_i = dt_strt

		while ( dt_i <= dt_stop ) :
			date_i = ( calc_time_str( dt_i ) )[0:10]
			req_date.append( date_i )
			dt_i += timedelta( 1 )

		# For each date in "date_i", load the data (if necessary).

		for date in req_date :
			self.load_date( date )

		# Compute the absolute time difference between the requested
		# time and the timestamp of each loaded datum.

		adt = [ abs( ( t - time_epc ).total_seconds( ) )
		                                      for t in self.arr_spin_t ]

		# Determine the ordering of the absolute time differences.

		arg = sorted( range( len( adt ) ), key=adt.__getitem__ )

		# If the smallest time difference is greater than the tolerance,
		# return 'None'.

		if ( adt[arg[0]] > self.buf ) :
			return None

		# Compute and the median spin rate for the data with the
		# smallest time difference.

		w = median( [ self.arr_spin_w[arg[i]]
		              for i in range( self.win ) ] )

		# Request a cleanup of the data loaded into this archive.

		self.cleanup_date( )

		# Return the spin period.

		return ( 2. * pi / w )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING ALL DATA FROM DATE-SPECIFIED FILE.
	#-----------------------------------------------------------------------

	def load_date( self, date_str ) :

		# Determine whether or not the requested date has already been
		# loaded.  If it has, abort.

		if ( date_str in self.arr_date ) :

			return

		# Extract the year, month, day, and day of year of the requested
		# date.

		year = int( date_str[0:4]  )
		mon  = int( date_str[5:7]  )
		day  = int( date_str[8:10] )

		# Determine the name of the file that contains data from the
		# requested date.

		str_year = date_str[0:4]
		str_mon  = date_str[5:7]
		str_day  = date_str[8:10]

		fl0 = 'wi_k0_spha_' + str_year + str_mon + str_day + '_v??.cdf'

		fl0_path = os.path.join( self.path, fl0 )

		# Search for the file in the local data directory.  If it is not
		# found, attempt to download it.

		gb = glob( fl0_path )

		if ( len( gb ) > 0 ) :

			fl_path = gb[-1]

		else :

			try :

				self.mesg_txt( 'ftp', date_str )

				ftp = FTP( 'cdaweb.gsfc.nasa.gov' )

				ftp.login( )

				ftp.cwd( 'pub/data/wind/orbit/spha_k0' )

				ftp.cwd( str_year )

				ls = ftp.nlst( fl0 )

				fl = ls[-1]

				fl_path = os.path.join( self.path, fl )

				ftp.retrbinary( "RETR " + fl,
				           open( fl_path, 'wb' ).write )

			except :

				self.mesg_txt( 'fail', date_str )

				return

		# If the file now exists locally, try to load it; otherwise,
		# abort.

		self.mesg_txt( 'load', date_str )

		if ( os.path.isfile( fl_path ) ) :

			try :

				cdf = pycdf.CDF( fl_path )

			except :

				self.mesg_txt( 'fail', date_str )

				return

		else :

			self.mesg_txt( 'fail', date_str )

			return

		# Append the requested date to the list of dates loaded.

		ind = len( self.arr_date )

		self.arr_date.append( date_str )

		# Extract the data from the loaded file.

		self.arr_spin_t += list( cdf['Epoch'        ][:] )
		self.arr_spin_w += list( cdf['AVG_SPIN_RATE'][:] )

		self.arr_spin_ind += [ ind for ep in cdf['Epoch'] ]

		# Request a clean-up of the files in the data directory.

		self.cleanup_file( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CLEANING UP THIS ARCHIVE.
	#-----------------------------------------------------------------------

	def cleanup_date( self ) :

		# For each date over the maximum number, remove that date and
		# all loaded data.

		while ( len( self.arr_date ) > self.n_date_max ) :

			# Remove the least recently loaded date from the list
			# of loaded dates.

			self.arr_date = self.arr_date[1:]

			# Remove the timestamps and spin rates from the removed
			# date.

			rng = range( len( self.arr_spin_ind ) )

			self.arr_spin_t = [ self.arr_spin_t[i]
			                    for i in rng
			                    if  self.arr_spin_ind[i] != 0 ]

			self.arr_spin_w = [ self.arr_spin_w[i]
			                    for i in rng
			                    if  self.arr_spin_ind[i] != 0 ]

			# Remove the indices for the removed data and decrement
			# the remaining indices.

			self.arr_spin_ind = [ ind - 1
			                      for ind in self.arr_spin_ind
			                      if  ind != 0                 ]

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CLEANING UP THE DATA DIRECTORY.
	#-----------------------------------------------------------------------

	def cleanup_file( self ) :

		# If there is no limit on the number files in the data
		# directory, abort (as there's nothing to be done).

		if ( self.n_file_max >= float( 'infinity' ) ) :
			return

		# Generate a list of the names of all spin data files.

		file_name = list( glob(
				  os.path.join( self.path, 'wi_k0_spha_*' ) ) )

		# If the number of files is less than or equal to the maximum,
		# abort (as nothing needs to be done).

		if ( len( file_name ) <= self.n_file_max ) :
			return

		# Determine the access time of each of the files, and then sort
		# the files in ascending value.

		file_time = [ os.path.getatime( fl ) for fl in file_name ]

		srt = sorted( range( len( file_time ) ),
		              key=file_time.__getitem__  )

		file_name = [ file_name[i] for i in srt ]
		file_time = [ file_time[i] for i in srt ]

		# Delete files so that the number of files equals the maximum
		# allowed.

		for f in range( len( file_name ) - self.n_file_max ) :
			os.remove( file_name[f] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SENDING INFORMATIONAL MESSAGES TO THE USER.
	#-----------------------------------------------------------------------

	def mesg_txt( self, mesg_typ, mesg_obj='' ) :

		# If this object is not associated with an instance of the
		# Janus "core", or if messaging has not been requested, abort.

		if ( ( self.core is None ) or ( not self.verbose ) ) :

			return

		# Emit a message signal (on behalf of the core) containing the
		# message parameters.

		self.core.emit( SIGNAL('janus_mesg'),
		                'spin', mesg_typ, mesg_obj )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE MAXIMUM NUMBER OF FILES.
	#-----------------------------------------------------------------------

	def chng_n_file_max( self, val ) :

		# Check the maximum file number input to ensure it is a postive
		# integer. Change the maximum file number if it is. Otherwise,
		# raise an error.

		if ( ( val != float( 'inf' )  ) and
		     ( type( val ) is not int )     ) :

			raise ValueError( 'Max file number must be ' +
			                     'infinity or a positive integer.' )

			return

		if ( val < 0 ) :

			raise ValueError( 'Max file number cannot be ' +
			                                           'negative.' )

			return

		self.n_file_max = val

		self.cleanup_file( )
