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

# Load the necessary "numpy" array modules.

from numpy import amax, amin, append, argsort, array, ceil, floor, tile, where

# Load the modules necessary for file I/O (including FTP).

from spacepy import pycdf

import os.path

from glob import glob

from ftplib import FTP

from scipy.io.idl import readsav


################################################################################
## DEFINE THE "mfi_arcv" CLASS FOR ACCESSING THE ARCHIVE OF Wind/MFI DATA.
################################################################################

class mfi_arcv( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core=None, buf=3600., tol=0.,
	                    use_idl=False, use_k0=False,
	                    n_file_max=None, n_date_max=None,
	                    path=None, verbose=True           ) :

		# Save the arguments for later use.

		self.core       = core
		self.buf        = buf
		self.tol        = tol
		self.path       = path
		self.use_idl    = use_idl
		self.use_k0     = use_k0
		self.n_file_max = n_file_max
		self.n_date_max = n_date_max
		self.verbose    = verbose

		# Validate the values of the "self.max_*" parameters and, if
		# necessary, provide values for them.

		if ( use_idl ) :
			n_file_max_def = float( 'infinity' )
			n_date_max_def = 40
		else :
			n_file_max_def = float( 'infinity' )
			n_date_max_def = 40

		if ( self.n_file_max is None ) :
			self.n_file_max = n_file_max_def
		elif ( self.n_file_max < 0 ) :
			self.n_file_max = n_file_max_def

		if ( self.n_date_max is None ) :
			self.n_date_max = n_date_max_def
		elif ( self.n_date_max <= 0 ) :
			self.n_date_max = n_date_max_def

		# If no path has been requested by the user, use the default
		# one.

		if ( self.path is None ) :

			self.path = os.path.join( os.path.dirname( __file__ ),
			                          'data', 'mfi'                )

		# Initialize the array of dates loaded.

		self.date_str = array( [ ] )
		self.date_ind = array( [ ] )

		self.n_date = 0
		self.t_date = 0

		# Initialize the data arrays.

		self.mfi_t   = array( [ ] )
		self.mfi_b_x = array( [ ] )
		self.mfi_b_y = array( [ ] )
		self.mfi_b_z = array( [ ] )
		self.mfi_ind = array( [ ] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING (AND RETURNING) A range OF THE DATA.
	#-----------------------------------------------------------------------

	def load_rang( self, time_strt, dur_sec ) :

		# Compute the requested start and stop times as values, as
		# strings, and as "datetime" epochs.

		time_strt_val = calc_time_val( time_strt               )
                print time_strt_val
		time_stop_val = calc_time_val( time_strt_val + dur_sec )

		time_strt_str = calc_time_str( time_strt_val )
		time_stop_str = calc_time_str( time_stop_val )

		time_strt_epc = calc_time_epc( time_strt_val )
		time_stop_epc = calc_time_epc( time_stop_val )

		# Construct an array of the dates requested.

		date_req = array( [ ] )

		date_i = ( calc_time_str( time_strt_val - self.buf ) )[0:10]
		time_i = calc_time_val( date_i + '/00:00:00.000' ) 

		while ( time_i < ( time_stop_val + self.buf ) ) :

			# Add the current date to the array of dates to be
			# loaded.

			date_req = append( date_req, [ date_i ] )

			# Move on to the next date.

			# Note.  This may look a bit odd, but may be necessary
			#        to avoid issues with leap seconds.  An
			#        additional leap-second concern is the posiblity
			#        of "date_req" containing duplicates, but that
			#        shouldn't be too much of an issue even if it
			#        does occur.

			time_i = time_i + 86400.
			date_i = ( calc_time_str( time_i ) )[0:10]
			time_i = calc_time_val( date_i + '/00:00:00.000' )

		# For each date in "date_i", load the data (if necessary).

		[ self.load_date( dt ) for dt in date_req ]

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

		return ( ret_t, ret_b_x, ret_b_y, ret_b_z )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING ALL DATA FROM DATE-SPECIFIED FILE.
	#-----------------------------------------------------------------------

	def load_date( self, date_str ) :

		# Determine whether or not the requested date has already been
		# loaded.  If it has, abort.

		if ( self.n_date > 0 ) :

			tk = where( self.date_str == date_str )[0]

			if ( len( tk ) > 0 ) :
				return

		# Extract the year, month, day, and day of year of the requested
		# date.

		year = int( date_str[0:4]  )
		mon  = int( date_str[5:7]  )
		day  = int( date_str[8:10] )

		# Attempt to load and extract data from the appropriate file.

		# Note.  The default data file format is CDF, and the code will
		#        attempt to download the appropriate CDF file from
		#        CDAWeb if it doesn't find one in the specified
		#        directory.  However, the user may also request that
		#        IDL "SAVE" files be used instead.

		if ( self.use_idl ) :

			# Determine the name of the file that contains data from
			# the requested date.

			doy = 1 + int( round(
			      ( datetime( year, mon, day ) -
			        datetime( year,   1,   1 )   ).total_seconds( )
			      / 86400. ) )


			doy_min = int( round(
			                    20. * floor(   doy       / 20. ) ) )
			doy_max = int( round(
			                    20. *  ceil( ( doy + 1 ) / 20. ) ) )

			str_year    = '{:4}'.format( year )
			str_doy_min = '{:03}'.format( doy_min )
			str_doy_max = '{:03}'.format( doy_max )

			fl = 'wind_mag.' + str_year + '.' + \
			                str_doy_min + '.' + str_doy_max + '.idl'

			fl_path = os.path.join( self.path, fl )

			# If the file exists, attempt to load it; otherwise,
			# abort.

			self.mesg_txt( 'load', date_str )

			if ( os.path.isfile( fl_path ) ) :
				try :
					dat = readsav( fl_path )
				except :
					self.mesg_txt( 'fail', date_str )
					return
			else :
				self.mesg_txt( 'fail', date_str )
				return

			# Determine the number of data loaded.  If none were
			# loaded, abort.

			n_sub = len( dat.doymag )

			if ( n_sub <= 0 ) :
				self.mesg_txt( 'fail', date_str )
				return

			# Extract the data from the loaded file.

			sub_doy = dat.doymag
			sub_b_x = dat.bxmag
			sub_b_y = dat.bymag
			sub_b_z = dat.bzmag

			sub_ind = tile( -1, len( dat.doymag ) )

			# Convert the loaded time from floating-point
			# day-of-year to "datetime" epoch.

			sub_t = array( [ datetime( year, 1, 1 ) + 
					               timedelta( doy - 1. )
			                 for doy in sub_doy                  ] )

			# Construct an array of dates associated with the file
			# that was loaded.  For each of the 20 day-of-year
			# values that could (hypothetically, at least) be stored
			# in the file, determine whether that value is valid,
			# and, if it is, add it to the array of dates.  While
			# doing this, also populate the "sub_ind" array.

			new_date_str = array( [ ] )
			new_date_ind = array( [ ] )
			n_new_date   = 0

			for d in range( 20 ) :

				# Determine the "d"-th day-of-year value
				# associated with this file.

				doy_d = doy_min + d

				# If this day-of-year value is too small, move
				# on to the next one.

				if ( doy <= 0 ) :
					continue

				# Construct a "datetime" object to represent
				# this day-of-year value.

				# Note.  Noon is chosen for the time of day to
				#        avoid any potential issues with leap
				#        seconds.

				time_epc_d = datetime( year, 1, 1, 12 ) + \
				             timedelta( doy_d - 1 )

				time_epc_d_1 = datetime( year, 1, 1 ) + \
				               timedelta( doy_d - 1 )
				time_epc_d_2 = datetime( year, 1, 1 ) + \
				               timedelta( doy_d )

				# If the "datetime" object indicates a year
				# other than the one associated with the file,
				# continue onto the next day-of-year value.

				if ( time_epc_d.year != year ) :
					continue

				# Since this day-of-year value is valid, enter
				# it into the array of dates.

				date_str_d = calc_time_str( time_epc_d )[0:10]
				date_ind_d = self.t_date + n_new_date

				new_date_str = append( new_date_str,
				                       [ date_str_d ] )
				new_date_ind = append( new_date_ind,
				                       [ date_ind_d ] )

				n_new_date += 1

				# Select all data associated with this date
				# and assign each the date index.

				tk_d = where( ( sub_t >= time_epc_d_1 ) &
				              ( sub_t <  time_epc_d_2 )   )[0]

				n_tk_d = len( tk_d )

				if ( n_tk_d > 0 ) :
					sub_ind[tk_d] = date_ind_d

			# Select those data which seem to have valid (versus
			# fill) values.

			tk   = where( ( abs( sub_b_x ) <  1000. ) &
			              ( abs( sub_b_y ) <  1000. ) &
			              ( abs( sub_b_z ) <  1000. ) &
			              ( sub_ind        >=    0  )   )[0]

			n_tk = len( tk )

		else :

			# Determine the name of the file that contains data
			# from the requested date.

			str_year = date_str[0:4]
			str_mon  = date_str[5:7]
			str_day  = date_str[8:10]

			if ( self.use_k0 ) :
				fl0 = 'wi_k0_mfi_' + \
				      str_year + str_mon + str_day + '_v??.cdf'
			else :
				fl0 = 'wi_h0_mfi_' + \
				      str_year + str_mon + str_day + '_v??.cdf'

			fl0_path = os.path.join( self.path, fl0 )

			gb = glob( fl0_path )

			# If the file does not exist, attempt to download it.

			if ( len( gb ) > 0 ) :
				fl_path = gb[-1]
			else :
				try :
					self.mesg_txt( 'ftp', date_str )
					ftp = FTP( 'cdaweb.gsfc.nasa.gov' )
					ftp.login( )
					ftp.cwd( 'pub/data/wind/mfi/' )
					if ( self.use_k0 ) :
						ftp.cwd( 'mfi_k0/' )
					else :
						ftp.cwd( 'mfi_h0/' )
					ftp.cwd( str_year )
					ls = ftp.nlst( fl0 )
					fl = ls[-1]
					fl_path = os.path.join( self.path, fl )
					ftp.retrbinary( "RETR " + fl,
					           open( fl_path, 'wb' ).write )
				except :
					self.mesg_txt( 'fail', date_str )
					return

			# If the file now exists, try to load it; otherwise,
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

			# Extract the data from the loaded file.

			if ( self.use_k0 ) :
				sub_t   = cdf['Epoch'][:]
				sub_b_x = cdf['BGSEc'][:,0]
				sub_b_y = cdf['BGSEc'][:,1]
				sub_b_z = cdf['BGSEc'][:,2]
				sub_pnt = cdf['N'][:]
			else :
				sub_t   = cdf['Epoch3'][:,0]
				sub_b_x = cdf['B3GSE'][:,0]
				sub_b_y = cdf['B3GSE'][:,1]
				sub_b_z = cdf['B3GSE'][:,2]
				sub_pnt = cdf['NUM3_PTS'][:,0]

			sub_ind = tile( self.t_date, len( sub_t ) )

			# Select those data which seem to have valid (versus
			# fill) values.

			tk   = where( sub_pnt > 0 )[0]
			n_tk = len( tk )

			# Copy the date associated with this file into and
			# array.

			new_date_str = [ date_str ]
			new_date_ind = [ self.t_date ]
			n_new_date = 1

		# Append any valid, newly-loaded data to the saved arrays.

		if ( n_tk > 0 ) :
			self.mfi_t   = append( self.mfi_t  , sub_t[tk]   )
			self.mfi_b_x = append( self.mfi_b_x, sub_b_x[tk] )
			self.mfi_b_y = append( self.mfi_b_y, sub_b_y[tk] )
			self.mfi_b_z = append( self.mfi_b_z, sub_b_z[tk] )
			self.mfi_ind = append( self.mfi_ind, sub_ind[tk] )

		# Append the array of loaded dates with the date(s) loaded in
		# this call of this function.

		self.date_str = append( self.date_str, new_date_str )
		self.date_ind = append( self.date_ind, new_date_ind )

		self.n_date += n_new_date
		self.t_date += n_new_date

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
