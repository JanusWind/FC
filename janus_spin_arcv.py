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

	def __init__( self, core=None, buf=3600., tol=0., win=None,
	                    n_file_max=None, n_date_max=None,
	                    path=None, verbose=True                 ) :

		# Save the arguments for later use.

		self.core = core

		self.win = int( win ) if ( win is not None ) else self.win = 5

		self.verbose = bool( verbose ) if ( verbose is not None ) else self.verbose = True

		#TODO Rest of variables

		self.buf        = buf
		self.tol        = tol
		self.path       = path
		self.n_file_max = n_file_max
		self.n_date_max = n_date_max
		self.verbose    = verbose

		# Validate the values of the parameters and, if necessary,
		# provide values.

		if ( self.win <= 0 ) :
			raise ValueError( 'Median window must be at least 1.' )

		#TODO Rest of variables

		if ( ( self.n_file_max is None ) or ( self.n_file_max < 0 ) ) :
			self.n_file_max = float( 'infinity' )

		if ( ( self.n_date_max is None ) or ( self.n_date_max < 0 ) ) :
			self.n_date_max = 40

		if ( self.path is None ) :
			self.path = os.path.join( os.path.dirname( __file__ ),
			                          'data', 'spin'               )

		# Initialize the list of dates loaded.

		self.arr_date = [ ]

		# Initialize the data lists.

		self.arr_spin_t   = [ ]
		self.arr_spin_w   = [ ]
		self.arr_spin_ind = [ ]

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

		tm_strt = time_epc - timedelta( seconds=buf )
		tm_stop = time_epc + timedelta( seconds=buf )

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






		#TODO
		#FIXME






		# Identify and extract the requested range of Wind/MFI data.

		tk = where( ( self.mfi_t >= ( time_strt_epc -
		                              timedelta( 0, self.tol ) ) ) &
		            ( self.mfi_t <= ( time_stop_epc +
		                              timedelta( 0, self.tol ) ) )   )
		tk = tk[0]

		n_tk = len( tk )

		if ( n_tk <= 0 ) :

			self.mesg_txt( 'none' )

			ret_t   = array( [ ] )
			ret_b_x = array( [ ] )
			ret_b_y = array( [ ] )
			ret_b_z = array( [ ] )

		else :

			ret_t   = self.mfi_t[tk]
			ret_b_x = self.mfi_b_x[tk]
			ret_b_y = self.mfi_b_y[tk]
			ret_b_z = self.mfi_b_z[tk]

			srt = argsort( ret_t )

			ret_t   = ret_t[srt]
			ret_b_x = ret_b_x[srt]
			ret_b_y = ret_b_y[srt]
			ret_b_z = ret_b_z[srt]

		# Request a cleanup of the data loaded into this archive.

		self.cleanup_date( )

		# Return the requested range of Wind/MFI data.

		return ( list( ret_t ), list( ret_b_x ),
		                        list( ret_b_y ), list( ret_b_z ) )

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

		self.arr_date.append( [ date_str ] )

		# Extract the data from the loaded file.

		self.spin_t.append( list( cdf['Epoch'        ][:] ) )
		self.spin_w.append( list( cdf['AVG_SPIN_RATE'][:] ) )

		self.spin_ind.append( [ ind for t in sub_t ] )

		# Request a clean-up of the files in the data directory.

		self.cleanup_file( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CLEANING UP THIS ARCHIVE.
	#-----------------------------------------------------------------------

	def cleanup_date( self ) :

		# If the number of dates is less than or equal to the maximum,
		# abort (as nothing needs to be done).

		if ( self.n_date <= self.n_date_max ) :
			return

		# Delete dates (and all associated data) from this archive so
		# that the number of loaded dates equals the maximum allowed.

		n_rm = self.n_date - self.n_date_max

		ind_min = self.t_date - self.n_date_max

		self.date_str = self.date_str[n_rm:]
		self.date_ind = self.date_ind[n_rm:]

		self.n_date -= n_rm

		tk = where( self.mfi_ind >= ind_min )[0]

		self.mfi_t   = self.mfi_t[tk]
		self.mfi_b_x = self.mfi_b_x[tk]
		self.mfi_b_y = self.mfi_b_y[tk]
		self.mfi_b_z = self.mfi_b_z[tk]
		self.mfi_ind = self.mfi_ind[tk]

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CLEANING UP THE DATA DIRECTORY.
	#-----------------------------------------------------------------------

	def cleanup_file( self ) :

		# If there is no limit on the number files in the data
		# directory, abort (as there's nothing to be done).

		if ( self.n_file_max >= float( 'infinity' ) ) :
			return

		# Generate a list of the names of all files of the requested
		# type (as specified by the "use_*" keywords) in the data
		# directory.

		if ( self.use_idl ) :
			file_name = array( glob(
			              os.path.join( self.path, 'wind_mag*' ) ) )
		else :
			if ( self.use_k0 ) :
				file_name = array( glob(
				         os.path.join( self.path, 'wi_k0*' ) ) )
			else :
				file_name = array( glob(
				         os.path.join( self.path, 'wi_h0*' ) ) )

		n_file = len( file_name )

		# If the number of files is less than or equal to the maximum,
		# abort (as nothing needs to be done).

		if ( n_file <= self.n_file_max ) :
			return

		# Determine the access time of each of the files, and then sort
		# the files in ascending value.

		file_time = array( [ os.path.getatime( fl )
		                     for fl in file_name    ] )

		srt = argsort( file_time )

		file_name = file_name[srt]
		file_time = file_time[srt]

		# Delete files so that the number of files equals the maximum
		# allowed.

		for f in range( n_file - self.n_file_max ) :
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
		                'mfi', mesg_typ, mesg_obj )
