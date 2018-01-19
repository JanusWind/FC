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

from numpy import amax, amin, append, argsort, array, ceil, floor, tile, where, arange

# Load the modules necessary for file I/O (including FTP).

from spacepy import pycdf

import os.path

from glob import glob

from ftplib import FTP

from scipy.io.idl import readsav


################################################################################
## DEFINE THE "mfi_arcv_lres" CLASS FOR ACCESSING THE ARCHIVE OF Wind/MFI DATA.
################################################################################

class mfi_arcv_lres( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core=None, buf=None, tol=None,
	                    use_h2=None,
	                    n_file_max=float('inf'), n_date_max=None,
	                    path=None, verbose=None                   ) :

		# Save the arguments for later use.

		# Note.  The "n_file_max" argument is handled at the end of this
		#        function with a call of "chng_n_file_max".

		self.core       = core

		self.buf        = float( buf )      if ( buf is not None )\
		                                    else 3600.

		self.tol        = float( tol )      if ( tol is not None )\
		                                    else 0.

		self.n_date_max = int( n_date_max ) if ( n_date_max 
		                                    is not None ) else 40

		self.use_h2     = bool( use_h2 )    if (use_h2 is not None )\
		                                    else False

		self.path       = str( path )       if ( path  is not None )\
		                                    else os.path.join( 
		                                    os.path.dirname( __file__ ), 
		                                    'data', 'mfi', 'lres' )

		self.verbose    = bool( verbose )   if ( verbose is not None )\
		                                    else True

		# Validate the values of the "self.max_*" parameters and, if
		# necessary, provide values for them.

		if ( self.buf < 0 ) :
			raise ValueError( 'Time buffer cannot be negative.'    )


		if ( self.n_date_max < 0 ) :
			raise ValueError( 'Maximum number of dates ' +
			                                 'cannot be negative.' )

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

		# Initialize "n_file_max".

		self.chng_n_file_max( n_file_max )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING (AND RETURNING) A range OF THE DATA.
	#-----------------------------------------------------------------------

	def load_rang( self, time_strt, dur_sec ) :

		# Compute the requested start and stop times as values, as
		# strings, and as "datetime" epochs.

		time_strt_val = calc_time_val( time_strt               )
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

		return ( list( ret_t ), list( ret_b_x ),
		                        list( ret_b_y ), list( ret_b_z ) )

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

		# Determine the name of the file that contains data
		# from the requested date.

		str_year = date_str[0:4]
		str_mon  = date_str[5:7]
		str_day  = date_str[8:10]

		fl0 = 'wi_h0_mfi_' + str_year + str_mon + str_day + '_v??.cdf'

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
				if ( self.use_h2 ) :
					ftp.cwd( 'mfi_h2/' )
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

		# Extract the data from the loaded file and select those data
		# which seem to have valid (versus fill) values.

		if ( self.use_h2 ) :

			# Extract the data from the loaded file.

			sub_t   = cdf['Epoch'][:,0]
			sub_b_x = cdf['BGSE'][:,0]
			sub_b_y = cdf['BGSE'][:,1]
			sub_b_z = cdf['BGSE'][:,2]

			sub_ind = tile( self.t_date, len( sub_t ) )

			# Select those data which seem to have valid (versus
			# fill) values.

			# TODO: Establish quality checks.

			n_tk = len( sub_t )
			tk   = arange( n_tk )

		else :

			# Extract the data from the loaded file.

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

		n_rmv = self.n_date - self.n_date_max

		ind_min = self.t_date - self.n_date_max

		self.date_str = self.date_str[n_rmv:]
		self.date_ind = self.date_ind[n_rmv:]

		self.n_date -= n_rmv

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

		if ( self.n_file_max >= float( 'inf' ) ) :
			return

		# Generate a list of the names of all files of the requested
		# type (as specified by the "use_*" keywords) in the data
		# directory.

		if ( self.use_h2 ) :
			file_name = list( glob(
			         os.path.join( self.path, 'wi_h2*' ) ) )
		else :
			file_name = list( glob(
			         os.path.join( self.path, 'wi_h0*' ) ) )

		# If the number of files is less than or equal to the maximum,
		# abort (as nothing needs to be done).

		if ( len( file_name )<= self.n_file_max ) :
			return

		# Determine the access time of each of the files, and then sort
		# the files in ascending value.

		file_time = [ os.path.getatime( fl )
		                     for fl in file_name    ]

		srt = sorted( range( len( file_time ) ),
		              key=file_time.__getitem__  )

		file_name = [ file_name[i] for i in srt ]
		file_time = [ file_time[i] for i in srt ]

#		srt = argsort( file_time )
#
#		file_name = file_name[srt]
#		file_time = file_time[srt]

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
		                'mfi', mesg_typ, mesg_obj )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE MAXIMUM NUMBER OF FILES.
	#-----------------------------------------------------------------------

	def chng_n_file_max( self, val ) :

		# Check the maximum file number input to ensure it is a postive
		# integer. Change the maximum file number if it is. Otherwise,
		# raise an error.

		if ( ( val != float( 'inf' ) ) and
		     ( type( val ) is not int     )     ) :

			raise ValueError( 'Max file number must be ' +
			                     'infinity or a positive integer.' )

			return

		if ( val < 0 ) :

			raise ValueError( 'Max file number cannot be ' +
			                                           'negative.' )

			return

		self.n_file_max = val

		self.cleanup_file( )
