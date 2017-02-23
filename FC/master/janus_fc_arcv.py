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

from numpy import abs, amax, amin, append, arange, argsort, array, tile, \
                  transpose, where

# Load the modules necessary for file I/O (including FTP).

from spacepy import pycdf

import os.path

from glob import glob

from ftplib import FTP

from scipy.io.idl import readsav


################################################################################
## DEFINE THE "fc_arcv" CLASS FOR ACCESSING THE ARCHIVE OF Wind/FC SPECTRA.
################################################################################

class fc_arcv( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core=None, buf=3600., tol=3600.,
	                    n_file_max=None, n_date_max=None,
	                    use_idl=False, path=None, verbose=True ) :

		# Save the arguments for later use.

		self.core       = core
		self.buf        = buf
		self.tol        = tol
		self.path       = path
		self.n_file_max = n_file_max
		self.n_date_max = n_date_max
		self.use_idl    = use_idl
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
			                          'data', 'fc'                 )

		# Initialize the array of dates loaded.

		self.date_str = array( [ ] )
		self.date_ind = array( [ ] )

		self.n_date = 0
		self.t_date = 0

		# Initialize the arrays that will store the data from the loaded
		# spectra.

		self.fc_time_epc   = tile(  0., ( 0 ) )
		self.fc_cup1_azm   = tile(  0., ( 0, 20 ) )
		self.fc_cup2_azm   = tile(  0., ( 0, 20 ) )
		self.fc_cup1_c_vol = tile(  0., ( 0, 31 ) )
		self.fc_cup2_c_vol = tile(  0., ( 0, 31 ) )
		self.fc_cup1_d_vol = tile(  0., ( 0, 31 ) )
		self.fc_cup2_d_vol = tile(  0., ( 0, 31 ) )
		self.fc_cup1_cur   = tile(  0., ( 0, 20, 31 ) )
		self.fc_cup2_cur   = tile(  0., ( 0, 20, 31 ) )
		self.fc_ind        = tile( -1 , ( 0 ) )

		self.n_fc = 0

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RETURNING THE NUMBER OF LOADED SPECTRA.
	#-----------------------------------------------------------------------

	def num_spec( self, tmin=None, tmax=None ) :

		# CAUTION!  This function only counts spectra that have already
		#           been loaded into this archive from the data files.

		# First, handle the easy cases: i.e., the case of no spectra
		# having been loaded into the archive and the case of both
		# "tm??" values being "None".

		if ( self.n_fc == 0 ) :
			return 0

		if ( ( tmin is None ) and ( tmax is None ) ) :
			return self.n_fc

		# Identify the subset of spectra with timestamps between "tmin"
		# and "tmax" and return the size of that subset.

		if ( tmin is not None ) :
			con_tmin = ( self.fc_time_epc >= calc_time_epc( tmin ) )
		else :
			con_tmin = tile( True, self.n_fc )

		if ( tmax is not None ) :
			con_tmax = ( self.fc_time_epc <= calc_time_epc( tmax ) )
		else :
			con_tmax = tile( True, self.n_fc )

		tk_con = where( con_tmin & con_tmax )[0]

		return len( tk_con )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING (AND RETURNING) AN ION SPECTRUM.
	#-----------------------------------------------------------------------

	def load_spec( self, time, get_prev=False, get_next=False,
	                           tmin=None, tmax=None            ) :

		# If both "get_????" keywords are "True", abort.

		if ( ( get_prev ) and ( get_next ) ) :
			self.mesg_txt( 'none' )
			return None

		# Convert/standardize the requested time.

		time_req_str = calc_time_str( time )
		time_req_val = calc_time_val( time )
		time_req_epc = calc_time_epc( time )

		# Extract requested date (as a string) and the requested time
		# (as a float indicating seconds since midnight).  Likewise,
		# determine the date of the previous day and the date of the
		# next day.

		date_req_str = time_req_str[0:10]
		scnd_req_val = time_req_val - calc_time_val( date_req_str )

		date_pre_str = ( calc_time_str( time_req_val - 86400. ) )[0:10]
		date_nex_str = ( calc_time_str( time_req_val + 86400. ) )[0:10]

		# Load all the spectra from the requested date.  If the
		# requested time is within "self.buf" seconds of either the
		# previous or next day, load all the spectra from that date as
		# well.

		# Note.  There is no need to check here whether a date has
		#        already been loaded as that's the first thing that
		#        "self.load_date( )" does.

		self.load_date( date_req_str )

		if ( scnd_req_val <= self.buf ) :
			self.load_date( date_pre_str )

		if ( ( 86400. - scnd_req_val ) <= self.buf ) :
			self.load_date( date_nex_str )

		# If no spectra have been loaded, abort.

		if ( self.n_fc <= 0 ) :
			self.mesg_txt( 'none' )
			return None

		# Identify the subset of spectra with timestamps between "tmin"
		# and "tmax".

		if ( tmin is not None ) :
			con_tmin = ( self.fc_time_epc >= calc_time_epc( tmin ) )
		else :
			con_tmin = tile( True, self.n_fc )

		if ( tmax is not None ) :
			con_tmax = ( self.fc_time_epc <= calc_time_epc( tmax ) )
		else :
			con_tmax = tile( True, self.n_fc )

		tk_con = where( con_tmin & con_tmax )[0]

		# If no spectra had timestamps in the specified range, abort.

		if ( len( tk_con ) <= 0 ) :
			self.mesg_txt( 'none' )
			return None

		# Compute the time difference between the timestamps within the
		# "tm??" range and the requested time.  Identify the index of
		# the smallest absolute in this array and the index of the
		# corresponding spectrum.

		dt = array( [ ( epc - time_req_epc ).total_seconds( )
		              for epc in self.fc_time_epc[tk_con]     ] )

		dt_abs = abs( dt )

		dt_abs_min = amin( dt_abs )

		tk_dt = where( dt_abs == dt_abs_min )[0][0]

		tk_req = tk_con[tk_dt]

		# Set the spectrum with index "tk_req" to be returned.  If the
		# (chronologically) next or previous spectrum has been
		# requested, find it and set it to be returned instead.

		tk = tk_req

		if ( ( get_prev ) and ( not get_next ) ) :

			tk_sub = where( dt < dt[tk_dt] )[0]

			if ( len( tk_sub ) <= 0 ) :
				self.mesg_txt( 'none' )
				return None

			tk_dt_prev = where( dt == amax( dt[tk_sub] ) )[0][0]

			tk = tk_con[tk_dt_prev]

		if ( ( get_next ) and ( not get_prev ) ) :

			tk_sub = where( dt > dt[tk_dt] )[0]

			if ( len( tk_sub ) <= 0 ) :
				self.mesg_txt( 'none' )
				return None

			tk_dt_next = where( dt == amin( dt[tk_sub] ) )[0][0]

			tk = tk_con[tk_dt_next]

		# If the selected spectrum is not within the the request
		# tolerence, abort.

		if ( abs( ( self.fc_time_epc[tk] - time_req_epc
		                             ).total_seconds( ) ) > self.tol ) :
			self.mesg_txt( 'none' )
			return None

		# Extract the spectrum to be returned.

		ret_time_epc = self.fc_time_epc[tk]
		ret_cup1_azm = self.fc_cup1_azm[tk]
		ret_cup2_azm = self.fc_cup2_azm[tk]
		ret_cup1_c_vol = self.fc_cup1_c_vol[tk]
		ret_cup2_c_vol = self.fc_cup2_c_vol[tk]
		ret_cup1_d_vol = self.fc_cup1_d_vol[tk]
		ret_cup2_d_vol = self.fc_cup2_d_vol[tk]
		ret_cup1_cur = self.fc_cup1_cur[tk]
		ret_cup2_cur = self.fc_cup2_cur[tk]

		# Request a cleanup of the data loaded into this archive.

		self.cleanup_date( )

		# Return the selected spetrum to the user.

		return ( ret_time_epc  ,
		         ret_cup1_azm  , ret_cup2_azm  ,
		         ret_cup1_c_vol, ret_cup2_c_vol,
		         ret_cup1_d_vol, ret_cup2_d_vol,
		         ret_cup1_cur  , ret_cup2_cur    )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING ALL SPECTRA FROM DATE-SPECIFIED FILE.
	#-----------------------------------------------------------------------

	def load_date( self, date_str ) :

		# Determine whether or not the requested date has already been
		# loaded.  If it has, abort.

		if ( self.n_date > 0 ) :

			tk = where( self.date_str == date_str )[0]

			if ( len( tk ) > 0 ) :
				return

		# Extract the year, month, and day portions of the "date_str"
		# string.

		str_year = date_str[0:4]
		str_mon  = date_str[5:7]
		str_day  = date_str[8:10]

		# Attempt to load and extract data from the appropriate file.

		# Note.  The default data file format is CDF, and the code will
		#        attempt to download the appropriate CDF file from
		#        CDAWeb if it doesn't find one in the specified
		#        directory.  However, the user may also request that
		#        IDL "SAVE" files be used instead.

		if ( self.use_idl ) :

			# Determine the path and name of the file corresponding
			# to the requested date.

			fl = 'wind_janus_fc_' + str_year + '-' + \
			                        str_mon + '-' + str_day + '.idl'

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

			# Determine the number of spectra loaded.  If no spectra
			# were loaded, return.

			n_sub = len( dat.sec )

			if ( n_sub <= 0 ) :
				self.mesg_txt( 'fail', date_str )
				return

			# Separate the loaded data into parameter arrays.

			sub_time_val = dat.sec + calc_time_val( date_str )

			sub_time_epc = array( [ calc_time_epc( t_val )
			                        for t_val in sub_time_val ] )

			sub_cup1_azm   = dat.cup1_angles
			sub_cup2_azm   = dat.cup2_angles
			sub_cup1_c_vol = dat.cup1_eperq
			sub_cup2_c_vol = dat.cup2_eperq
			sub_cup1_d_vol = dat.cup1_eqdel
			sub_cup2_d_vol = dat.cup2_eqdel

			sub_cup1_cur = 1E12 * array( [ 
			                  transpose( dat.currents[s,0,:,:] +
			                             dat.currents[s,2,:,:] )
			                  for s in range( n_sub )            ] )
			sub_cup2_cur = 1E12 * array( [ 
			                  transpose( dat.currents[s,1,:,:] +
			                             dat.currents[s,3,:,:] )
			                  for s in range( n_sub )            ] )

			sub_ind = tile( self.t_date, n_sub )

		else :

			# Determine the name of the file that contains data from
			# the requested date.

			fl0 = 'wi_sw-ion-dist_swe-faraday_' + \
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
					ftp.cwd(
					      'pub/data/wind/swe/swe_faraday/' )
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

			# Separate the loaded data into parameter arrays, and
			# determine the number of spectra loaded.

			sub_time_epc   = array( cdf['Epoch']          )
			sub_cup1_azm   = array( cdf['cup1_azimuth']   )
			sub_cup2_azm   = array( cdf['cup2_azimuth']   )
			sub_cup1_c_vol = array( cdf['cup1_EperQ']     )
			sub_cup2_c_vol = array( cdf['cup2_EperQ']     )
			sub_cup1_d_vol = array( cdf['cup1_EperQ_DEL'] )
			sub_cup2_d_vol = array( cdf['cup1_EperQ_DEL'] )
			sub_cup1_cur   = array( cdf['cup1_qflux']     )
			sub_cup2_cur   = array( cdf['cup2_qflux']     )

			n_sub = len( sub_time_epc )

			sub_ind = tile( self.t_date, n_sub )

		# Add the loaded and formatted Wind/FC spectra to the archive.

		self.fc_time_epc   = append( self.fc_time_epc  ,
		                                        sub_time_epc  , axis=0 )
		self.fc_cup1_azm   = append( self.fc_cup1_azm  ,
		                                        sub_cup1_azm  , axis=0 )
		self.fc_cup2_azm   = append( self.fc_cup2_azm  ,
		                                        sub_cup2_azm  , axis=0 )
		self.fc_cup1_c_vol = append( self.fc_cup1_c_vol,
		                                        sub_cup1_c_vol, axis=0 )
		self.fc_cup2_c_vol = append( self.fc_cup2_c_vol,
		                                        sub_cup2_c_vol, axis=0 )
		self.fc_cup1_d_vol = append( self.fc_cup1_d_vol,
		                                        sub_cup1_d_vol, axis=0 )
		self.fc_cup2_d_vol = append( self.fc_cup2_d_vol,
		                                        sub_cup2_d_vol, axis=0 )
		self.fc_cup1_cur   = append( self.fc_cup1_cur  ,
		                                        sub_cup1_cur  , axis=0 )
		self.fc_cup2_cur   = append( self.fc_cup2_cur  ,
		                                        sub_cup2_cur  , axis=0 )
		self.fc_ind        = append( self.fc_ind,  sub_ind    , axis=0 )

		self.n_fc = self.n_fc + n_sub

		# Append the array of loaded dates with this one.

		self.date_str = append( self.date_str, [ date_str    ] )
		self.date_ind = append( self.date_ind, [ self.n_date ] )

		self.n_date += 1
		self.t_date += 1

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

		tk   = where( self.fc_ind >= ind_min )[0]

		self.n_fc = len( tk )

		self.fc_time_epc   = self.fc_time_epc[tk]
		self.fc_cup1_azm   = self.fc_cup1_azm[tk]
		self.fc_cup2_azm   = self.fc_cup2_azm[tk]
		self.fc_cup1_c_vol = self.fc_cup1_c_vol[tk]
		self.fc_cup2_c_vol = self.fc_cup2_c_vol[tk]
		self.fc_cup1_d_vol = self.fc_cup1_d_vol[tk]
		self.fc_cup2_d_vol = self.fc_cup2_d_vol[tk]
		self.fc_cup1_cur   = self.fc_cup1_cur[tk]
		self.fc_cup2_cur   = self.fc_cup2_cur[tk]
		self.fc_ind        = self.fc_ind[tk]

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
			         os.path.join( self.path, 'wind_janus_fc*' ) ) )
		else :
			file_name = array( glob(
			         os.path.join( self.path, 'wi_sw-ion*'     ) ) )

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
		                'fc', mesg_typ, mesg_obj )
