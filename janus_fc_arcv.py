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

from janus_fc_spec import fc_spec

# Load the necessary "numpy" array modules.

from numpy import argsort, array

from operator import attrgetter		  

# Load the modules necessary for file I/O (including FTP).

from spacepy import pycdf

import os.path

from glob import glob

from ftplib import FTP


################################################################################
## DEFINE THE CLASS fc_tag TO HAVE SPECTRA FOR PARTICULAR TIME STAMP
################################################################################

class fc_tag() :
	
	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, c=None, s=None, epoch=None ) :

		self.c     = c
		self.s     = s
		self.epoch = epoch


################################################################################
## DEFINE THE "fc_arcv" CLASS FOR ACCESSING THE ARCHIVE OF Wind/FC SPECTRA.
################################################################################

class fc_arcv( object ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core=None, buf=None, tol=None,
	                    n_file_max=float('inf'), n_date_max=None,
	                    path=None, verbose=None                   ) :

		# Save the arguments for later use.

		# Note.  The "n_file_max" argument is handled at the end of this
		#        function with a call of "chng_n_file_max".

		self.core       = core

		self.buf        = float( buf )      if ( buf is not None )\
		                                    else 3600.

		self.tol        = float( tol )      if ( tol is not None )\
		                                    else 3600.

		self.n_date_max = int( n_date_max ) if ( n_date_max 
		                                    is not None ) else 40

		self.path       = str( path )       if ( path  is not None )\
		                                    else os.path.join( 
		                                    os.path.dirname( __file__ ), 
		                                    'data', 'fc' )

		self.verbose    = bool( verbose )   if ( verbose is not None )\
		                                    else True

		# Validate the values of the "self.max_*" parameters and, if
		# necessary, provide values for them.

		if ( self.buf < 0 ) :
			raise ValueError( 'Time buffer cannot be negative.'    )

		if ( self.n_date_max < 0 ) :
			raise ValueError( 'Maximum number of dates ' +
			                                 'cannot be negative.' )

		# Initialize arrays of date and times loaded.

		self.arr_cdf  = [ ]
		self.arr_date = [ ]

		self.arr_tag  = [ ]

		# Initialize "n_file_max"

		self.chng_n_file_max( n_file_max )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING (AND RETURNING) AN ION SPECTRUM.
	#-----------------------------------------------------------------------

	def load_spec( self, time, get_prev=False, get_next=False ) :	

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

		if ( len( self.arr_tag ) == 0 ) :
			self.mesg_txt( 'none' )
			return None

		# Locate the spectrum whose timestamp is closest to the
		# one requested.

		adt = [ abs(tag.epoch - time_req_epc) for tag in self.arr_tag ]

		adt_min = min( adt )

		tk = [ a for a in range( len( adt ) ) if adt[a] == adt_min ][0]

		if ( get_prev ) :
			tk -= 1
		if ( get_next ) :
			tk +=1

		if( ( tk <  0                   ) or
		    ( tk >= len( self.arr_tag ) )    ) :
			self.mesg_txt( 'none' )
			return None


		# If the selected spectrum is not within the the request
		# tolerence, abort.

		if ( ( adt[tk] ).total_seconds() > self.tol ) :# In case of long
		                                               # Data gap  
			self.mesg_txt( 'none' )
			return None


		# If the selected spectrum is not within the the request
		# tolerence, abort.
	
		# Extract the spectrum to be returned.

		cdf = self.arr_cdf[self.arr_tag[tk].c]
		s   = self.arr_tag[ tk ].s

		# Find actual no. of voltage bins 

		n_bin_max = 31
		n_dir = 20

		for n_bin_1 in range( n_bin_max ) :
			if ( n_bin_1 == n_bin_max + 1 ) :
				break
			if ( cdf['cup1_EperQ'][s][n_bin_1] >= 
					     cdf['cup1_EperQ'][s][n_bin_1+1] ) :
				break
		n_bin_1 += 1

		for n_bin_2 in range( n_bin_max ) :
			if ( n_bin_2 == n_bin_max + 1 ) :
				break
			if ( cdf['cup2_EperQ'][s][n_bin_2] >= 
					     cdf['cup2_EperQ'][s][n_bin_2+1] ) :
				break
		n_bin_2 += 1

		n_bin = min( [ n_bin_1, n_bin_2 ] )

		# Assigning all retrieved data to parameter values

		time = cdf['Epoch'][s]			

		elev = [ float( cdf['inclination_angle'][0] ),
		         float( cdf['inclination_angle'][1] ) ]

		azim = [ [ float( cdf['cup1_azimuth'][s][d] ) 
		                for d in range( n_dir )       ],
			 [ float( cdf['cup2_azimuth'][s][d] )
		                for d in range( n_dir )       ]  ]

		volt_cen=[ [ float( cdf['cup1_EperQ'][s][b] ) 
		                  for b in range( n_bin )     ],
			   [ float( cdf['cup2_EperQ'][s][b] )
		                  for b in range( n_bin )     ]  ]

		volt_del=[ [ float( cdf['cup1_EperQ_DEL'][s][b] )
		                  for b in range( n_bin )         ],
			   [ float( cdf['cup2_EperQ_DEL'][s][b] )
		                  for b in range( n_bin )         ]  ]

		curr = [ [ [ float( cdf['cup1_qflux'][s][d][b] )
		             for b in range( n_bin )             ] 
		             for d in range( n_dir )               ],
			 [ [ float( cdf['cup2_qflux'][s][d][b] )
		             for b in range( n_bin )             ]
		             for d in range( n_dir )               ]  ]


		spec = fc_spec( n_bin, elev=elev, azim=azim, volt_cen=volt_cen,\
		                       volt_del=volt_del, curr=curr, time=time )

		# Request a cleanup of the data loaded into this archive.

		self.cleanup_date( )	

		return spec

		#fc_arcv().load_spec(1224246301)

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING ALL SPECTRA FROM DATE-SPECIFIED FILE.
	#-----------------------------------------------------------------------

	def load_date( self, date_str ) :

		# Determine whether or not the requested date has already been
		# loaded.  If it has, abort.

		arr = [ date for date in self.arr_date if date == date_str ]

		if ( len( arr ) > 0 ) :
			return

		# Extract the year, month, and day portions of the "date_str"
		# string.

		str_year = date_str[0:4]
		str_mon  = date_str[5:7]
		str_day  = date_str[8:10]

		# Determine the name of the file that contains data from the
		# requested date.

		fl0 = 'wi_sw-ion-dist_swe-faraday_' + \
		       str_year + str_mon + str_day + '_v??.cdf'

		fl0_path = os.path.join( self.path, fl0 )

		gb = glob( fl0_path )	# returns all files with 
		                        # common names in argument

		# If the file does not exist, attempt to download it.

		if ( len( gb ) > 0 ) :	# Take the last one : gb[-1]
			fl_path = gb[-1]
		else :
			try :
				self.mesg_txt( 'ftp', date_str )
				ftp = FTP( 'cdaweb.gsfc.nasa.gov' )
				ftp.login( )
				ftp.cwd( 'pub/data/wind/swe/swe_faraday/' )
				ftp.cwd( str_year )
				ls = ftp.nlst( fl0 )
				fl = ls[-1]
				fl_path = os.path.join( self.path, fl )
				ftp.retrbinary( "RETR " + fl,
					        open( fl_path, 'wb' ).write )
			except :
				self.mesg_txt( 'fail', date_str )
				return

		# If the file now exists, try to load it; otherwise, abort.

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

		# Add the CDF object and tags for each spectrum to the arrays.

		c = len( self.arr_cdf )

		self.arr_cdf  = self.arr_cdf  + [ cdf ]	     # arr_cdf and	
		self.arr_date = self.arr_date + [ date_str ] # arr_date of
		                                             # same size

		n_spec = len( cdf['Epoch'] )
		self.arr_tag = self.arr_tag + [ fc_tag( c=c, s=s,
		                                epoch=cdf['Epoch'][s] )
		                                for s in range( n_spec ) ]

		self.arr_tag = sorted( self.arr_tag, key=attrgetter('epoch') )




		# Request a clean-up of the files in the data directory.

		#self.cleanup_file( )


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CLEANING UP THIS ARCHIVE.
	#-----------------------------------------------------------------------

	def cleanup_date( self ) :

		# If the number of dates is less than or equal to the maximum,
		# abort (as nothing needs to be done).

		if ( len(self.arr_date) <= self.n_date_max ) :
			return

		# How to get the entire list of arr_cdf, arr_data, arr_tag for 
		#all downloded data. ...Showing for only the requested one ...

		self.arr_tag = [ tag for tag in self.arr_tag if tag.c != 0 ]

		self.arr_cdf  = self.arr_cdf[1:]
		self.arr_date = self.arr_date[1:]

		for t in range( len( self.arr_tag ) ) :
			self.arr_tag[t].c -= 1

		# In case there are multiple dates to be removed; \
		#special case time 12 a.m.
		
		self.cleanup_date()

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
