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


#################################################################################
## LOAD THE NECESSARY MODULES.
################################################################################

# Load the modules necessary for signaling the graphical interface.

from PyQt4.QtCore import QObject, SIGNAL, QThread

# Load the modules necessary for file operations.

import os.path

# Load the modules necessary for handling dates and times.

import time
from time import sleep
from datetime import datetime, timedelta
from janus_time import calc_time_epc, calc_time_sec, calc_time_val

# Load the module necessary handling step functions.

from janus_step import step

# Load the dictionary of physical constants.

from janus_const import const

# Load the modules necessary for loading Wind/FC and Wind/MFI data.

from janus_fc_arcv   import fc_arcv
from janus_spin_arcv import spin_arcv
from janus_mfi_arcv_lres import mfi_arcv_lres
from janus_mfi_arcv_hres import mfi_arcv_hres

# Load the necessary array modules and mathematical functions.

from numpy import amax, amin, append, arccos, arctan2, arange, argsort, array, \
                    average, cos, deg2rad, diag, dot, exp, indices, interp, \
                    mean, pi, polyfit, rad2deg, reshape, sign, sin, sum, sqrt, \
                    std, tile, transpose, where, zeros

from numpy.linalg import lstsq

from scipy.special     import erf
from scipy.interpolate import interp1d
from scipy.optimize    import curve_fit
from scipy.stats       import pearsonr, spearmanr

from janus_helper import round_sig

from janus_fc_spec import fc_spec

# Load the "pyon" module.

from janus_pyon import plas, series

# Load the modules necessary for saving results to a data file.

import pickle

# Load the modules necessary for copying.

from copy import deepcopy


################################################################################
## DEFINE THE "core" CLASS: THE ANLYSIS CORE OF JANUS.
################################################################################

class core( QObject ) :

	# +-------------------+------------------------------+
	# | SIGNAL('janus_*') | Arguments                    |
	# +-------------------+------------------------------+
	# | busy_beg          |                              |
	# | busy_end          |                              |
	# | mesg              | mesg_src, mesg_typ, mesg_obj |
	# | rset              |                              |
	# | chng_spc          |                              |
	# | chng_mfi          |                              |
	# | chng_spin         |                              |
	# | chng_mom_win      |                              |
	# | chng_mom_sel_bin  | c, d, b                      |
	# | chng_mom_sel_dir  | c, d                         |
	# | chng_mom_sel_all  |                              |
	# | chng_mom_res      |                              |
	# | chng_nln_pop      | i                            |
	# | chng_nln_ion      |                              |
	# | chng_nln_set      |                              |
	# | chng_nln_gss      |                              |
	# | chng_nln_sel_bin  | c, d, b                      |
	# | chng_nln_sel_all  |                              |
	# | chng_nln_res      |                              |
	# | chng_dsp          |                              |
	# | chng_dyn          |                              |
	# | chng_opt          |                              |
	# | rstr_opt          |                              |
	# | done_auto_run     |                              |
	# | exit              |                              |
	# +-------------------+------------------------------+

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, app=None, time=None ) :

		# Inherit all attributes of the "QObject" class.

		# Note.  This class does not directly provide any graphical
		#        interface.  Rather, the functions of the "QObject"
		#        class are used principally for signal the classes that
		#        do.

		super( core, self ).__init__( )

		self.app = app

		# Read and store the version information.

		# Note.  The "[:-1]" array operation used below trims the final
		#        character (which should be an end-line) from the line
		#        read from the file.

		fl = open( os.path.join( os.path.dirname( __file__ ),
		                         'janus.dat'                  ) )

		self.version = fl.readline( )[:-1]

		fl.close( )

		# Initialially deactiveate the debugging mode.

		self.debug = False

		# Initialize the variables that will contain the Wind/FC ion
		# spectrum's data, the associated Wind/MFI magnetic field data,
		# the ion spectrum's point selection, and the results of the
		# moments analysis of the ion spectrum.

		self.init_var( )

		# Initialize and store the archives for downloading, loading,
		# and managing data files.

		self.fc_arcv = fc_arcv( core=self,
		                            n_file_max=self.opt['fls_n_fc'  ]  )

		self.spin_arcv = spin_arcv( core=self,
		                            n_file_max=self.opt['fls_n_spin']  ) 

		self.mfi_arcv_lres  = mfi_arcv_lres( core=self,
		                          n_file_max=self.opt['fls_n_mfi_l' ]  )

		self.mfi_arcv_hres = mfi_arcv_hres( core=self,
		                          n_file_max=self.opt['fls_n_mfi_h' ]  )

		# Initialize a log of the analysis results.

		self.series = series( )

		# Load the requested Wind/FC ion spectrum (if one has been
		# requested).

		# Note.  After loading the Wind/FC ion spectrum,
		#        "self.load_spec" calls "self.load_mfi" to load the
		#        associated Wind/MFI magnetic field data and then calls
		#        "self.auto_sel" to make an automatic selection of the
		#        spectrum's data.  In turn, "self.auto_sel" calls
		#        "self.anls_mom" to perform a moments analysis on the
		#        selected data.

		if ( time is not None ) :

			self.load_spec( time )

	#-----------------------------------------------------------------------
	# INITIALIZE THE THE DATA AND ANALYSIS VARIABLES.
	#-----------------------------------------------------------------------

	def init_var( self ) :

		# Initialize the variables that will contain the Wind/FC ion
		# spectrum's data; the associated Wind/MFI magnetic field data;
		# and the settings, data selections, and results from all
		# analyses.

		self.rset_var( var_swe     = True, var_spin    = True,
		               var_mfi     = True, var_mom_win = True,
		               var_mom_sel = True, var_mom_res = True,
		               var_nln_ion = True, var_nln_set = True,
		               var_nln_gss = True, var_nln_sel = True,
		               var_nln_res = True, var_dsp     = True,
		               var_dyn     = True, var_opt     = True          )
		
		# Initialize the value of the indicator variable of whether the
		# automatic analysis should be aborted.

		# Note.  This variable provides the user with a means of
		#        prematurely stopping the automatic analysis of a series
		#        of spectra by the function "self.auto_run".  When that
		#        function is called, this indicator's value is set to
		#        "False".  After the function processes a given
		#        spectrum, it procedes on to the next one only if this
		#        indicator is still "False".

		self.stop_auto_run = False

	#-----------------------------------------------------------------------
	# RESET THE DATA AND ANALYSIS VARIABLES.
	#-----------------------------------------------------------------------

	def rset_var( self,
	              var_swe     = False, var_spin    = False,
	              var_mfi     = False, var_mom_win = False,
	              var_mom_sel = False, var_mom_res = False,
	              var_nln_ion = False, var_nln_set = False,
	              var_nln_gss = False, var_nln_sel = False,
	              var_nln_res = False, var_dsp     = False,
	              var_dyn     = False, var_opt     = False   ) :

		# If requested, (re-)initialize the variables associated with
		# the ion spectrum's data.

		if ( var_swe ) :

			self.fc_spec  = None

			self.time_epc = None
			self.time_val = None
			self.time_txt = ''
			self.time_vld = True

		# If requested, (re-)initialize the variables associated with
		# the spin rate.

		if ( var_spin ) :

			self.spin_period = None

		# If requested, (re-)initialize the varaibles for the Wind/MFI
		# data associated with this spectrum.

		if ( var_mfi ) :

			self.n_mfi         = 0

			self.mfi_dur       = 0.

			self.mfi_t         = None
			self.mfi_b         = None
			self.mfi_b_x       = None
			self.mfi_b_y       = None
			self.mfi_b_z       = None

			self.mfi_avg_mag   = None
			self.mfi_avg_vec   = None
			self.mfi_avg_nrm   = None

			self.mfi_s         = None

			self.mfi_b_colat   = None
			self.mfi_b_lon     = None
			self.mfi_psi_b     = None
			self.mfi_psi_b_avg = None

			self.mfi_amag_ang  = None

		# If requested, (re-)initialize the varaibles for the windows
		# associated with automatic data selection for the moments
		# analysis.

		if ( var_mom_win ) :

			self.mom_win_dir = 7
			self.mom_win_bin = 7

		# If requested, (re-)initialize the variables associated with
		# the data seleciton for the moments analysis.

		if ( var_mom_sel ) :

			self.mom_min_sel_dir =  5
			self.mom_min_sel_bin =  3

			self.mom_max_sel_dir = 20

			self.mom_sel_dir     = None
			self.mom_sel_bin     = None

		# If requested, (re-)initialize and store the variables
		# associated with the results of the moments analysis.

		if ( var_mom_res ) :

			self.mom_res  = None

			self.mom_curr = None

		# If requested, (re-)initialize the variables associated with
		# the ion species and populations for the non-linear analysis.

		# Note.  This includes both the "self.nln_spc_?" and
		#        "self.nln_pop_?" arrays.  These are done together since
		#        they are so interconnected by the "self.nln_plas"
		#        object, which is also handled here.

		if ( var_nln_ion ) :

			self.nln_n_spc = 4
			self.nln_n_pop = 5

			self.nln_plas = plas( enforce=True )

			self.nln_pop_use = tile( False, self.nln_n_pop )
			self.nln_pop_vld = tile( False, self.nln_n_pop )

			for s in range ( self.nln_n_spc ) :

				if ( s == 0 ) :
					self.nln_plas.add_spec( name='Proton',
					                   sym='p', m=1., q=1. )
				elif ( s == 1 ) :
					self.nln_plas.add_spec( name='Alpha' ,
					                   sym='a', m=4., q=2. )
				else :
					self.nln_plas.add_spec( )

			for p in range ( self.nln_n_pop ) :

				if ( p == 0 ) :
					self.nln_pop_use[p] = True
					self.nln_pop_vld[p] = True
					self.nln_plas.add_pop(
					        'p', name='Core', sym='c',
					        drift=False, aniso=True    )
				elif ( p == 1 ) :
					self.nln_pop_use[p] = False
					self.nln_pop_vld[p] = True
					self.nln_plas.add_pop(
					        'p', name='Beam', sym='b',
					        drift=True , aniso=False   )
				elif ( p == 2 ) :
					self.nln_pop_use[p] = True
					self.nln_pop_vld[p] = True
					self.nln_plas.add_pop(
					        'a', name='Core', sym='c',
					        drift=True , aniso=True    )
				elif ( p == 3 ) :
					self.nln_pop_use[p] = False
					self.nln_pop_vld[p] = True
					self.nln_plas.add_pop(
					        'a', name='Beam', sym='b',
					        drift=True , aniso=False   )
				else :
					self.nln_pop_use[p] = False
					self.nln_pop_vld[p] = False
					self.nln_plas.add_pop( None )

		# If requested, (re-)initialize the variables associated with
		# the settings for the automatic initial guess generation and
		# the automatic point selection.

		if ( var_nln_set ) :

			self.nln_set_gss_n   = tile( None , self.nln_n_pop )
			self.nln_set_gss_d   = tile( None , self.nln_n_pop )
			self.nln_set_gss_w   = tile( None , self.nln_n_pop )
			self.nln_set_gss_vld = tile( False, self.nln_n_pop )

			self.nln_set_sel_a   = tile( None , self.nln_n_pop )
			self.nln_set_sel_b   = tile( None , self.nln_n_pop )
			self.nln_set_sel_vld = tile( False, self.nln_n_pop )

			self.nln_set_gss_n[0]   =  1.00
			self.nln_set_gss_n[1]   =  0.20
			self.nln_set_gss_n[2]   =  0.02
			self.nln_set_gss_n[3]   =  0.01

			self.nln_set_gss_d[1]   =  0.03
			self.nln_set_gss_d[2]   =  0.01
			self.nln_set_gss_d[3]   =  0.05

			self.nln_set_gss_w[0]   =  1.00
			self.nln_set_gss_w[1]   =  1.25
			self.nln_set_gss_w[2]   =  1.00
			self.nln_set_gss_w[3]   =  1.25

			self.nln_set_gss_vld[0] = True
			self.nln_set_gss_vld[1] = True
			self.nln_set_gss_vld[2] = True
			self.nln_set_gss_vld[3] = True

			self.nln_set_sel_a[0]   = -3.00
			self.nln_set_sel_a[1]   = -3.00
			self.nln_set_sel_a[2]   = -3.00
			self.nln_set_sel_a[3]   = -3.00
			self.nln_set_sel_a[4]   = -3.00

			self.nln_set_sel_b[0]   =  3.00
			self.nln_set_sel_b[1]   =  3.00
			self.nln_set_sel_b[2]   =  3.00
			self.nln_set_sel_b[3]   =  3.00
			self.nln_set_sel_b[4]   =  3.00

			self.nln_set_sel_vld[0] = True
			self.nln_set_sel_vld[1] = True
			self.nln_set_sel_vld[2] = True
			self.nln_set_sel_vld[3] = True
			self.nln_set_sel_vld[4] = True

		# If requested, (re-)initialize the variables associated with
		# the initial guesses for the non-linear analysis.

		if ( var_nln_gss ) :

			for p in range( self.nln_n_pop ) :
				self.nln_plas.arr_pop[p]['n']     = None
				self.nln_plas.arr_pop[p]['dv']    = None
				self.nln_plas.arr_pop[p]['w']     = None
				self.nln_plas.arr_pop[p]['w_per'] = None
				self.nln_plas.arr_pop[p]['w_par'] = None

			self.nln_gss_vld = tile( False, self.nln_n_pop )

			self.nln_gss_pop      = [ ]
			self.nln_gss_prm      = [ ]

			self.nln_gss_curr_tot = None
			self.nln_gss_curr_ion = None

		# If requested, (re-)initialize the variables associated with
		# the data selection for the non-linear analysis.

		if ( var_nln_sel ) :

			self.nln_sel     = None

			self.nln_n_sel   = 0
			self.nln_min_sel = 30

		# If requested, (re-)initialize the variables associated with
		# the results of the non-linear analysis.

		if ( var_nln_res ) :

			self.nln_res_runtime  = 0.

			self.nln_res_plas     = None

			self.nln_res_sel      = None

			self.nln_res_curr_tot = None
			self.nln_res_curr_ion = None

		# If requested, (re-)initialize the variables which indicate of
		# the analyses have their results displayed in widgets which
		# support output from multiple analyses.

		if ( var_dsp ) :

			self.dsp = 'mom'

		# If requested, (re-)initialize the variables which indicate
		# which analyses are updated automatically when a change is
		# made to their settings.

		if ( var_dyn ) :

			self.dyn_mom = True
			self.dyn_gss = True
			self.dyn_sel = True
			self.dyn_nln = False

		# If requested, (re-)initialize the variables which indicate
		# the various options for the GUI's option menu.

		if ( var_opt ) :

			# Define the file name of the configuration file for the
			# options menu.

			self.opt_flnm = os.path.join( 'data', 'janus.cfg' )

			# Load the default options 'silently' (i.e., without
			# overwriting the configuration file or emitting a
			# signal).

			self.rstr_opt( save=False, signal=False,
			               propagate=False           )

			# If a configuration file exists, open it and load the
			# options therein line by line.

			if( os.path.isfile( self.opt_flnm ) ) :

				# Load each line of the file and, if it contains
				# configuration information, add it to the
				# options dictionary.

				for ln in open( self.opt_flnm, 'r' ).readlines( ) :

					# If the line is blank or is a comment,
					# skip it.

					if ( ( len( ln ) == 0   ) or
					     ( ln[0]     == '#' )    ) :
						continue

					# Attempt to parse the line into its key
					# and value.  If this fails, skip to the
					# next line. 

					prsd = ln.lower( ).split( )

					if ( len( prsd ) != 2 ) :
						continue

					[ key, val ] = prsd

					# If the key is invalid or is not
					# already in the options dictionary,
					# skip to the next line.

					if ( ( len( key ) < 3           ) or
					     ( key not in
					               self.opt.keys( ) )    ) :
						continue

					# Store the loaded key's value (with the
					# appropriate type) to the dictionary.

					if ( ( val == 'inf'      ) or
					     ( val == 'infinity' )    ) :
						val = float( 'inf' )
					else :
						val = int( val )

					prefix = key[0:3]

					if ( ( prefix == 'res' ) or
					     ( prefix == 'mfi' )    ) :
						self.opt[key] = bool( val )
					else :
						self.opt[key] = val

			# Save the options dictionary to the configuration file.

			self.save_opt( )

	#-----------------------------------------------------------------------
	# LOAD THE REQUESTED WIND/FC SPECTRUM.
	#-----------------------------------------------------------------------

	def load_spec( self, time_req=None,
	               get_prev=False, get_next=False ) :

		# Reset the variables that contain the Wind/FC ion spectrum's
		# data, the associated Wind/MFI magnetic field data, and the
		# results of all analyses.

		# Note.  Not all of the "self.rset_var" keywords are set to
		#        "True" so as to retain the general settings (even
		#        though a new spectrum is being loaded).

		self.emit( SIGNAL('janus_rset') )

		self.rset_var( var_swe     = True, var_spin    = True,
		               var_mfi     = True, var_mom_sel = True,
		               var_mom_res = True, var_nln_gss = True,
		               var_nln_sel = True, var_nln_res = True  )

		# If a special code has been entered, take the specified action.

		if ( str( time_req ).lower( ) == 'iddqd' ) :

			self.emit( SIGNAL('janus_chng_spc') )

			if ( self.debug ) :
				self.debug = False
				self.emit( SIGNAL('janus_mesg'),
				           'core', 'end', 'debug' )
			else :
				self.debug = True
				self.emit( SIGNAL('janus_mesg'),
				           'core', 'begin', 'debug' )

			return

		if ( str( time_req ).lower( ) == 'haiku' ) :

			self.emit( SIGNAL('janus_chng_spc') )

			self.emit( SIGNAL('janus_mesg'),
			           'core', 'begin', 'haiku' )

			return

		# Convert the argument "time_req" into the standard, second-
		# precision, string format.  If this conversion returns "None",
		# label the requested time as invalid.

		self.time_txt = calc_time_sec( time_req )

		if ( self.time_txt is None ) :

			if ( type( time_req ) == str ) :
				self.time_txt = time_req
			else :
				self.time_txt = ''

			self.time_vld = False

		else :

			self.time_vld = True

		# If necessary, adjust "self.dsp" and "self.dyn_???" keywords to
		# make them a bit more mutually consistent.

		if ( ( self.dsp == 'gsl' ) or ( self.dsp == 'nln' ) ) :

			self.dyn_mom = True
			self.dyn_gss = True
			self.dyn_sel = True

			if ( ( self.dsp == 'nln' ) and ( not self.dyn_nln ) ) :

				self.dsp = 'gsl'

			self.emit( SIGNAL('janus_chng_dyn') )
			self.emit( SIGNAL('janus_chng_dsp') )

		# If no valid time was requested, alert the user and abort.

		if ( not self.time_vld ) :

			self.emit( SIGNAL('janus_mesg'),
			           'core', 'fail', 'time' )

			return

		# Message the user that a new Wind/FC ion spectrum is about to
		# be loaded.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'fc' )

		# Load the Wind/FC ion spectrum with a timestamp closest to that
		# requested.

		self.fc_spec = self.fc_arcv.load_spec( self.time_txt,
		                                       get_prev=get_prev,
		                                       get_next=get_next )

		# If no spectrum was found, abort.

		if ( self.fc_spec is None ) :
			self.emit( SIGNAL('janus_chng_spc') )
			return

		# Extract the parameters of the loaded Wind/FC ion spectrum.
		  
		time_epc = self.fc_spec[ 'time' ]

		# Calculate and store the spectrum's properly formatted
		# timestamp both as a float and as a string.

		self.time_epc = time_epc
		self.time_val = calc_time_val( time_epc )
		self.time_txt = calc_time_sec( time_epc )
		self.time_vld = True

		# Message the user that a new Wind/FC ion spectrum has been
		# loaded.

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'fc' )

		# Emit a signal that indicates that a new Wind/FC ion spectrum
		# has now been loaded.

		self.emit( SIGNAL('janus_chng_spc') )

		# Load the associated Wind/SPIN data associated with this
		# spectrum.

		self.load_spin( )

		# Load the associated Wind/MFI magnetic field data associated
		# with this spectrum.

		self.load_mfi( )

		# If requested, run the moments analysis.

		if ( self.dyn_mom ) :
			self.auto_mom_sel( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING THE Wind/SPIN DATA.
	#-----------------------------------------------------------------------

	def load_spin( self ) :

		# Reset the spin variables.

		self.rset_var( var_spin=True )

		# If no Wind/FC ion spectrum has been loaded, abort.

		if ( self.fc_spec is None ) :
			self.emit( SIGNAL('janus_chng_spin') )
			return

		# Message the user that new Wind/SPIN data are about to be
		# loaded.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'spin' )

		# Load the Wind/SPIN data associated with this spectrum.

		self.spin_period = self.spin_arcv.load_spin( self.time_val )

		# If no spin data were returned, abort with a signal that the
		# data have changed.

		if ( self.spin_period is None ) :
			self.emit( SIGNAL('janus_chng_spin') )
			return

		# Assign the loaded spin rate to the spectrum rotation value.

		self.fc_spec.set_rot( self.spin_period )

		# Message the user that the spin period has been updated.

		self.emit( SIGNAL('janus_mesg'), 'core', 'val', 'spin' )

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'spin' )

		# Emit a signal that indicates that a new Wind/MFI data have now
		# been loaded.

		self.emit( SIGNAL('janus_chng_spin') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR LOADING THE Wind/MFI MAGNETIC FIELD DATA.
	#-----------------------------------------------------------------------

	def load_mfi( self ) :

		# Reset the contents of the "self.mfi_*" arrays.

		self.rset_var( var_mfi=True )

		# If no Wind/FC ion spectrum has been loaded, abort.

		if ( self.fc_spec is None ) :
			self.emit( SIGNAL('janus_chng_mfi') )
			return

		# Message the user that new Wind/MFI data are about to be
		# loaded.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'mfi' )

		# Load the Wind/MFI magnetic field data of appropriate
		# resolution associated with this spectrum.

		if ( self.opt['mfi_l'] ) :

			( self.mfi_t, self.mfi_b_x, self.mfi_b_y,
			  self.mfi_b_z ) = self.mfi_arcv_lres.load_rang(
			( self.time_val       - ( 2. * self.fc_spec['rot'] ) ),
			( self.fc_spec['dur'] + ( 4. * self.fc_spec['rot'] ) ) )

		elif ( self.opt['mfi_h'] ) :

			( self.mfi_t, self.mfi_b_x, self.mfi_b_y,
			  self.mfi_b_z ) = self.mfi_arcv_hres.load_rang(
			( self.time_val       - ( 2. * self.fc_spec['rot'] ) ),
			( self.fc_spec['dur'] + ( 4. * self.fc_spec['rot'] ) ) )

		# Establish the number of data.

		self.n_mfi = len( self.mfi_t )

		# If no magnetic field data were returned, abort with a signal
		# that the data have changed.

		if ( self.n_mfi == 0 ) :
			self.emit( SIGNAL('janus_chng_mfi') )
			return

		# Compute and store derived paramters.

		self.mfi_s = [ ( t - self.fc_spec['time'] ).total_seconds( )
		                                       for t in self.mfi_t ]

		# Compute the magnetic field magnitude.

		self.mfi_b = [ sqrt( self.mfi_b_x[i]**2 +
                                     self.mfi_b_y[i]**2 +
                                     self.mfi_b_z[i]**2 )
                                     for i in range( len( self.mfi_b_x ) ) ]
    
		# Compute the average magetic field and its norm.

		self.mfi_avg_vec = array( [ mean( self.mfi_b_x ),
		                            mean( self.mfi_b_y ),
		                            mean( self.mfi_b_z ) ] )

		self.mfi_avg_mag = sqrt( self.mfi_avg_vec[0]**2 +
		                         self.mfi_avg_vec[1]**2 +
		                         self.mfi_avg_vec[2]**2   )

		self.mfi_avg_nrm = self.mfi_avg_vec / self.mfi_avg_mag

		mfi_nrm     = [ ( self.mfi_b_x[i], self.mfi_b_y[i],
		                  self.mfi_b_z[i] ) /self.mfi_b[i]
		                  for i in range( len( self.mfi_b ) ) ]

		# Compute the mfi angles.

		mfi_b_rho      = [sqrt( self.mfi_b_x[i]**2.0 
		                      + self.mfi_b_y[i]**2.0 )
		                        for i in range( len( self.mfi_b_x ) ) ]

		mfi_b_colat       = arctan2( self.mfi_b_z, mfi_b_rho )
		mfi_b_lon         = arctan2( self.mfi_b_y, self.mfi_b_x )

		self.mfi_b_colat  = rad2deg( mfi_b_colat )
		self.mfi_b_lon    = rad2deg( mfi_b_lon )

		self.mfi_amag_ang = array( [ mean( self.mfi_b_colat ),
		                                   mean( self.mfi_b_lon   )  ] )

		# Calculate the average angular deviation of magnetic field

		self.mfi_psi_b = [ arccos( [ sum ( mfi_nrm[i][j] *
		                               self.mfi_avg_nrm[j]
		                              for j in range( 3 )          ) ] )
	                                      for i in range( len( mfi_nrm ) ) ]

                self.mfi_psi_b_avg = rad2deg(sum ( self.mfi_psi_b )/self.n_mfi )

		# Use interpolation to estiamte the magnetic field vector for
		# each datum in the FC spectrum.

		self.fc_spec.set_mag( self.mfi_t, self.mfi_b_x,
		                                  self.mfi_b_y, self.mfi_b_z )

		# Message the user that new Wind/MFI data have been loaded.

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'mfi' )

		# Emit a signal that indicates that a new Wind/MFI data have now
		# been loaded.

		self.emit( SIGNAL('janus_chng_mfi') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE MOM. SELCTION DIRECTION WINDOW.
	#-----------------------------------------------------------------------
 
	def chng_mom_win_dir( self, val ) :

		# Try to convert the "val" argument to an integer and store it.
		# If this fails, store "None".
    
		if ( val is None ) :

			self.mom_win_dir = None

		else :

			try :

				self.mom_win_dir = int( val )

				if ( self.mom_win_dir < self.mom_min_sel_dir ) :
					self.mom_win_dir = None

				if ( self.mom_win_dir > self.mom_max_sel_dir ) :
					self.mom_win_dir = None

			except :

				self.mom_win_dir = None

		# Emit a signal that a change has occured to the moments window
		# parameters.

		self.emit( SIGNAL('janus_chng_mom_win') )

		# Call the automatic selection of data for the moments analysis.

		self.auto_mom_sel( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE MOMENTS SELCTION BIN WINDOW.
	#-----------------------------------------------------------------------
  
	def chng_mom_win_bin( self, val ) :

		# Try to convert the "val" argument to an integer and store it.
		# If this fails, store "None".

		if ( val is None ) :
			self.mom_win_bin = None
		else :
			try :
				self.mom_win_bin = int( val )
				if( ( self.mom_win_bin < self.mom_min_sel_bin  )
				or  ( self.mom_win_bin > self.fc_spec['n_bin'] )
				                                             ) :
					self.mom_win_bin = None
			except :
				self.mom_win_bin = None

		# Emit a signal that a change has occured to the moments window
		# parameters.

		self.emit( SIGNAL('janus_chng_mom_win') )

		# Call the automatic selection of data for the moments analysis.

		self.auto_mom_sel( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR AUTOMATIC DATA SELECTION FOR THE MOMENTS ANLS.
	#-----------------------------------------------------------------------

	def auto_mom_sel( self ) :

		# Re-initialize the data-selection variables for the moments
		# analysis.

		self.rset_var( var_mom_sel=True )

		# If no spectrum has been loaded, abort.

		if ( self.fc_spec is None ) :

			return

		# Initially, deselect all look directions and bins.

		self.mom_sel_dir = [ [ False 
		                       for d in range(self.fc_spec['n_dir']) ]
		                       for c in range(self.fc_spec['n_cup']) ]

		self.mom_sel_bin = [ [ [ False 
		                         for b in range(self.fc_spec['n_bin']) ]
                                         for d in range(self.fc_spec['n_dir']) ]
		                         for c in range(self.fc_spec['n_cup']) ]

		# If the "mom_win_???" variables are invalid, abort.

		if ( ( self.mom_win_dir is None ) or
		     ( self.mom_win_bin is None )    ) :

			self.vldt_mom_sel( emit_all=True )

			self.anls_mom( )

			return

		# Find the maximum current window (of "self.mom_win_bin" bins)
		# for each direction
		dir_max_ind  = [ [ self.fc_spec.find_max_curr( c, d,
		                             win=self.mom_win_bin              )
		                        for d in range(self.fc_spec['n_dir'] ) ]
		                        for c in range(self.fc_spec['n_cup'] ) ]

		dir_max_curr = [ [ self.fc_spec.calc_tot_curr( c, d,
		                             dir_max_ind[c][d],
		                             win=self.mom_win_bin              )
		                        for d in range(self.fc_spec['n_dir'] ) ]
		                        for c in range(self.fc_spec['n_cup'] ) ]

		# Compute "cup_max_ind" (two element list)
		# List of indices with maximum current for each cup

		cup_max_ind  = [ 0 for c in range( self.fc_spec['n_cup'] ) ]

		for c in range( self.fc_spec['n_cup'] ) :

			curr_sum_max = 0.

			for d in range( self.fc_spec['n_dir'] ) :

				curr_sum = sum( [ dir_max_curr[c][
				                  (d+i)%self.fc_spec['n_dir']  ]
				                  for i in range(
				                           self.mom_win_dir) ] )

				if ( curr_sum > curr_sum_max ) :
					cup_max_ind[c] = d
					curr_sum_max   = curr_sum

		# Populate "self.mom_sel_bin" and "self.mom_sel_dir"
		# appropriately.

		for c in range( self.fc_spec['n_cup'] ) :

			for pd in range( cup_max_ind[c],
			                 cup_max_ind[c] + self.mom_win_dir ) :

				# Compute the actual direction-index (versus the
				# pseudo-direction-index).

				d = pd % self.fc_spec['n_dir'   ]
                                self.mom_sel_dir[c][d] = True

				# Select the bins in this look direction's
				# maximal window

				for b in range( dir_max_ind[c][d],
				                dir_max_ind[c][d]
				                          + self.mom_win_bin ) :
					self.mom_sel_bin[c][d][b] = True

                # Validate the new data selection (which includes populating
		# the "self.mom_sel_dir" array).

		self.vldt_mom_sel( emit_all=True )

		# Run the moments analysis (and then, if the non-linear analysis
		# is set to be dynamically updated, run that analysis as well).

		self.anls_mom( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE SELECTION OF A SINGLE POINT.
	#-----------------------------------------------------------------------

	def chng_mom_sel( self, c, d, b ) :

		# Change the selection of the requested datum.

		self.mom_sel_bin[c][d][b] = not self.mom_sel_bin[c][d][b]

		# Emit a signal that indicates that the datum's selection status
		# for the moments analysis has changed.

		self.emit( SIGNAL('janus_chng_mom_sel_bin'), c, d, b )

		# Validate the new data selection (i.e., make sure that the two
		# "self.sel_???" arrays are mutually-consistent) and update the
		# "self.n_sel_???" counters.

		self.vldt_mom_sel( )

		# Ensure that the moments analysis has been set for "dyanmic"
		# mode (since the user presumably wants it this way).  Rerun the
		# moments analysis.

		# Note.  An alternative behavior would be to check the value of
		#        "self.dyn_mom" (without changing it) and then rerunning
		#        the moments analysis only if this parameter has the
		#        value "True".

		self.chng_dyn( 'mom', True, rerun=False )

		self.anls_mom( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR VALIDATING THE DATA SELECTION.
	#-----------------------------------------------------------------------

	def vldt_mom_sel( self, emit_all=False ) :

		# Note.  This function ensures that the two "self.mom_sel_???"
		#        arrays are mutually consistent.  For each set of "c"-
		#        and "d"-values, "self.mom_sel_dir[c,d]" can only be
		#        "True" if at least "self.min_sel_bin" of the elements
		#        in "self.mom_sel_bin[c,d,:]" are "True".  However, if
		#        fewer than "self.mom_min_sel_dir" sets of "c"- and
		#        "d"-values satisfy this criterion, all elements of
		#        "self.mom_sel_dir" are given the value "False".		
		#
		#        Additionally, this functions serves to update the
		#        "self.mom_n_sel_???" counters.


		# Save the initial selection of pointing directions.

		old_mom_sel_dir = deepcopy( self.mom_sel_dir )

		# Update the counter "self.mom_n_sel_bin" (i.e., the number of
		# selected data in each pointing direction).

		self.mom_n_sel_bin = [ [ sum( self.mom_sel_bin[c][d] )
		                       for d in range( self.fc_spec['n_dir'] ) ]
		                       for c in range( self.fc_spec['n_cup'] ) ]

		# Create a new selection of pointing directions based on the
		# data selection, and then update the counter
		# "self.mom_n_sel_dir".

		self.mom_sel_dir = [ [
		              self.mom_n_sel_bin[c][d] >= self.mom_min_sel_bin
		                       for d in range( self.fc_spec['n_dir'] ) ]
		                       for c in range( self.fc_spec['n_cup'] ) ]

		# Determine the total number of selected pointing directions; if
		# this number is less than the minimum "self.mom_min_sel_dir",
		# deselect all pointing directions.

		self.mom_n_sel_dir = \
		               sum( [ sum( sub ) for sub in self.mom_sel_dir ] )

		if ( self.mom_n_sel_dir < self.mom_min_sel_dir ) :

			self.mom_sel_dir = [ [ False
			               for d in range( self.fc_spec['n_dir'] ) ]
			               for c in range( self.fc_spec['n_cup'] ) ]

			self.mom_n_sel_dir = 0

		# Emit (if necessary) the appropriate update signal(s).

		if ( emit_all ) :

			self.emit( SIGNAL('janus_chng_mom_sel_all') )

		else :

			# Identify differences between the new and old versions
			# of "self.mom_sel_dir".  For each pointing direction
			# whose selection status for the moments analysis has
			# changed, emit a signal indicating this.

			for c in range( self.fc_spec['n_cup'] ) :

				for d in range( self.fc_spec['n_dir'] ) :

					if ( self.mom_sel_dir[c][d]
					            != old_mom_sel_dir[c][d] ) :

						self.emit( SIGNAL(
						      'janus_chng_mom_sel_dir'),
						      c, d )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RUNNING THE MOMENTS ANALYSIS.
	#-----------------------------------------------------------------------

	def anls_mom( self ) :

		# Re-initialize and the output of the moments analysis.

		self.rset_var( var_mom_res=True )

		# If the point-selection arrays have not been populated, run
		# the automatic point selection.

		if ( ( self.mom_sel_dir is None ) or
		     ( self.mom_sel_bin is None )    ) :

			self.auto_mom_sel( )

		# If any of the following conditions are met, emit a signal that
		# indicates that the results of the moments analysis have
		# changed, and then abort.
		#   -- No (valid) ion spectrum has been requested.
		#   -- Insufficient data have been selected.

		if ( ( self.fc_spec is None                       ) or
		     ( self.mom_n_sel_dir < self.mom_min_sel_dir  ) or
		     ( self.mom_n_sel_dir > self.fc_spec['n_dir'] )    ) :

			self.emit( SIGNAL('janus_mesg'),
			                  'core', 'norun', 'mom' )

			self.emit( SIGNAL('janus_chng_mom_res') )

			return

		# Message the user that the moments analysis has begun.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'mom' )

		# Extract the "c"- and "d"-indices of each selected pointing
		# direction.

		( tk_c, tk_d ) = where( self.mom_sel_dir )

		# Initialize the "eta_*" arrays.

		# Note.  Only some of these arrays will ultimate be saved.

		# Note.  The arrays "eta_?" define the density, inflow speed,
		#        thermal speed, and temperature derived for each of the
		#        analyzed look directions.

		n_eta = self.mom_n_sel_dir

		eta_dlk = tile( 0., [ n_eta, 3 ] )  # Cartesian look direction

		eta_eca = tile( 0., n_eta )         # effective collecting area

		eta_n   = tile( 0., n_eta )         # number density
		eta_v   = tile( 0., n_eta )         # inflow speed
		eta_w   = tile( 0., n_eta )         # thermal speed
		eta_t   = tile( 0., n_eta )         # temperature

		# For each of the selected look directions, identify the
		# selected data therefrom and calculate the estimator of the
		# projected inflow speed along that direction.

		# Note.  Equations 3.11, 3.13, and 3.15 of my dissertation
		#        (Maruca, PhD thesis, 2012) contain an extra factor of
		#        $2$ that is omitted below in the calculation of the
		#        estimators.  This factor reflects the half-efficiency
		#        that is inherent to the use of demodulation and has
		#        already been taken into account in the calibration of
		#        the current measurments.

		for k in range( n_eta ) :

			# Extract the "c"- and "d"-values for this direction.

			c = tk_c[k]
			d = tk_d[k]

			# Calculate the look direction using "c"- and "d"-values

			eta_dlk[k] = self.fc_spec.arr[c][d][0]['dir']

			# Extract the "b" values of the selected data from this
			# look direction.

                        b = [i for i, x in enumerate( self.mom_sel_bin[c][d] )
                                                                  if x==True    ]

			eta_v[k] = - sum( [ self.fc_spec['curr'][c][d][i] 
                                                for i in b] ) / \
                                     sum( [ self.fc_spec['curr'][c][d][i]    /
                                            self.fc_spec['vel_cen'][c][i]
                                                for i in b]   )

		# Use singular value decomposition (in the form of least squares
		# analysis) to calculate the best-fit bulk speed for the solar
		# wind.

		mom_v_vec = lstsq( eta_dlk, eta_v )[0]

		# For each of the selected look directions, use the derived
		# value of "mom_v_vec" to estimate its effective collecting
		# area, the number density, and the thermal speed.

		for k in range( n_eta ) :

			# Extract the "c"- and "d"-values for this direction.

			c = tk_c[k]
			d = tk_d[k]

			# Calculate the effective collecting area for this look
			# direction.

			eta_eca[k] = self.fc_spec.arr[c][d][0].\
                                                  calc_eff_area( mom_v_vec )

			# Extract the "b" indices of the selected data from this
			# look direction.

                        b = [i for i, x in enumerate( self.mom_sel_bin[c][d] )
                                                                if x==True   ]

			# Estimate the number density and thermal speed based on
			# the selected data from this look direction.

			eta_n[k] = 1e-6 * ( ( 1. / const['q_p'] ) /
			           ( 1.e-4 * eta_eca[k] ) *
			             sum([
                                   ( 1.e-12 * self.fc_spec['curr'][c][d][i] ) /
			           ( 1.e3 *   self.fc_spec['vel_cen'][c][i] )
                                              for i in b ]                  ) )

			eta_w[k] = 1.e-3 * sqrt( max( [ 0.,
			           ( ( 1. / const['q_p']  ) /
			           ( 1.e-4 * eta_eca[k]   ) /
			           ( 1.e6 * eta_n[k]      ) *
			             sum( [
                                   ( 1.e-12 * self.fc_spec['curr'][c][d][i] ) *
			           ( 1.e3   * self.fc_spec['vel_cen'][c][i] )
                                              for i in b ]                  ) )
			         - ( 1.e3 * eta_v[k] )**2             ]     ) )

		# Compute the effective temperature for each of the analyzed
		# look directions.

		eta_t = ( 1.E-3 / const['k_b'] ) * \
		        const['m_p'] * ( ( 1.E3  * eta_w )**2 )

		# Calculate a net estimators of the number density and thermal
		# speed.

		# Note.  The total signal for a look direction is roughly
		#        proportional to its effective collecting area.  Thus,
		#        the reciprical of the effective collecting area can be
		#        thought of a crude indicator of the uncertainty in the
		#        number-density estimators from the corresponding look
		#        direction.

		mom_n = average( eta_n, weights=eta_eca**2 )

		mom_w = mean( eta_w )

		# Save the results of the moments analysis in a plas object.

		self.mom_res = plas( )

		self.mom_res['v0_vec'] = mom_v_vec

		self.mom_res.add_spec( name='Proton', sym='p', m=1., q=1. )

		self.mom_res.add_pop( 'p',
		                      drift=False, aniso=False,
		                      name='Core', sym='c',
		                      n=mom_n,     w=mom_w          )

		# Calculate the expected currents based on the results of the
		# (linear) moments analysis.

		self.mom_curr = self.fc_spec.calc_curr(
		                                    self.mom_res['m_p'],
		                                    self.mom_res['q_p'],
		                                    self.mom_res['v0_vec'],
		                                    self.mom_res['n_p_c'], 0.,
		                                    self.mom_res['w_p_c']      )

		# Message the user that the moments analysis has completed.

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'mom' )

		# Emit a signal that indicates that the results of the moments
		# analysis have changed.

		self.emit( SIGNAL('janus_chng_mom_res') )

		# Update the initial guess for the non-linear analysis if
		# dynamic updating has been requested.  If it wasn't, make sure
		# that the new results of the moments analysis are being
		# displayed.

		# Note.  No call to "self.auto_nln_sel" is required here.  If
		#        "self.dyn_gss" is "True", then "self.auto_nln_gss"
		#        will call "self.auto_nln_sel" iff "self.dyn_sel" is
		#        also "True".  If "self.dyn_gss" is "False", then
		#        calling "self.auto_nln_sel" is completely unnecessary
		#        as its output would be no different than that from its
		#        last run (since no changes to the initial guess would
		#        have been made since then.
		#
		#        Likewise, no call is needed here to "self.anls_nln"
		#        since "self.suto_nln_gss" will handle this if
		#        necessary.  Again, if "self.dyn_gss" is "False", then
		#        calling "self.anls_nln" is completely unnecessary as
		#        its output would be no different than that from its
		#        last run (since no changes to the inital guess or to
		#        the point selection would have been made since then).

		if ( self.dyn_gss ) :
			self.auto_nln_gss( )
		else :
			self.chng_dsp( 'mom' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING A NLN SPECIES.
	#-----------------------------------------------------------------------

	def chng_nln_spc( self, s, param, val ) :

		# Ensure that "i" is a valid ion-species index.

		s = int( s )

		if ( ( s < 0 ) or ( s >= self.nln_n_spc ) ) :
			return

		# Change the parameter of the specified ion-species to the
		# specified value.

		if   ( param == 'name' ) :
			try :
				self.nln_plas.arr_spec[s]['name'] = str( val )
			except :
				self.nln_plas.arr_spec[s]['name'] = None

		elif ( param == 'sym' ) :
			try :
				self.nln_plas.arr_spec[s]['sym'] = str( val )
			except :
				self.nln_plas.arr_spec[s]['sym'] = None

		elif ( param == 'm' ) :
			try :
				val = float( val )
				if ( val >= 0 ) :
					self.nln_plas.arr_spec[s]['m'] = val
				else :
					self.nln_plas.arr_spec[s]['m'] = None
			except :
				self.nln_plas.arr_spec[s]['m'] = None

		elif ( param == 'q' ) :
			try :
				val = float( val )
				if ( val >= 0 ) :
					self.nln_plas.arr_spec[s]['q'] = val
				else :
					self.nln_plas.arr_spec[s]['q'] = None
			except :
				self.nln_plas.arr_spec[s]['q'] = None

		# Propagate the changes to the ion population.

		self.prop_nln_ion( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING A NLN POPULATION.
	#-----------------------------------------------------------------------

	def chng_nln_pop( self, i, param, val ) :

		# Ensure that "i" is a valid ion-population index.

		i = int( i )

		if ( ( i < 0 ) or ( i >= self.nln_n_pop ) ) :
			return

		# Change the parameter of the specified ion-population to the
		# specified value.

		if ( param == 'use' ) :

			self.nln_pop_use[i] = bool( val )

		if ( param == 'spec' ) :

			if ( ( val >= 0              ) and
			     ( val <  self.nln_n_spc )     ) :

				# If the population's name and/or symbol would
				# contradict with a population already
				# associated with the new species, clear out
				# both.

				if ( ( self.nln_plas.get_pop( 
				          self.nln_plas.arr_spec[
				                         val]['sym'],
				          self.nln_plas.arr_pop[
				                           i]['name'] )
				                             is not None) or
				     ( self.nln_plas.get_pop( 
				          self.nln_plas.arr_spec[
				                         val]['sym'],
				          self.nln_plas.arr_pop[
				                           i]['sym']  )
				                             is not None)    ) :

					self.nln_plas.arr_pop[i]['name'] = None
					self.nln_plas.arr_pop[i]['sym']  = None

					self.emit( SIGNAL(
					              'janus_chng_nln_pop'), i )
				try :
					self.nln_plas.arr_pop[i]['spec'] = \
					             self.nln_plas.arr_spec[val]
				except :
					self.nln_plas.arr_pop[i]['spec'] = None
			else :
				self.nln_plas.arr_pop[i]['spec'] = None

		if ( param == 'name' ) :

			try :
				self.nln_plas.arr_pop[i]['name'] = str( val )
			except :
				self.nln_plas.arr_pop[i]['name'] = None

		if ( param == 'sym' ) :

			try :
				self.nln_plas.arr_pop[i]['sym'] = str( val )
			except :
				self.nln_plas.arr_pop[i]['sym'] = None

		if ( param == 'drift' ) :

			try :
				self.nln_plas.arr_pop[i]['drift'] = bool( val )
			except :
				self.nln_plas.arr_pop[i]['drift'] = None

		if ( param == 'aniso' ) :

			try :
				self.nln_plas.arr_pop[i]['aniso'] = bool( val )
			except :
				self.nln_plas.arr_pop[i]['aniso'] = None

		# Propagate the changes to the ion population.

		self.prop_nln_ion( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROPAGATING INFO. ON THE ION SPECIES/POP.'S.
	#-----------------------------------------------------------------------

	def prop_nln_ion( self ) :

		# Record the validity of each ion population.

		for p in range( self.nln_n_pop ) :

			self.nln_pop_vld[p] = \
			     self.nln_plas.arr_pop[p].valid( require_val=False )

		# Emit a signal that indicates that the ion parameters for the
		# non-linear analysis have changed.

		self.emit( SIGNAL('janus_chng_nln_ion') )

		# If dynamic updating of the initial guess has been enabled, run
		# the automated guess-generator.  Otherwise, skip directly to
		# the function that generates the initial-guess arrays.

		if ( self.dyn_gss ) :
			self.auto_nln_gss( )
		else :
			self.make_nln_gss( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING A SETTING FOR THE NLN ANALYSIS.
	#-----------------------------------------------------------------------

	def chng_nln_set( self, i, param, val ) :

		# Ensure that the arguments are valid.

		if ( ( i < 0 ) or ( i >= self.nln_n_pop ) ) :
			return

		# Change the parameter(s) of the specified ion species to the
		# specified values.

		if   ( param == 'gss_n' ) :

			try :
				self.nln_set_gss_n[i] = float( val )
			except :
				self.nln_set_gss_n[i] = None

			if ( ( self.nln_set_gss_n[i] is not None ) and
			     ( self.nln_set_gss_n[i] <= 0        )     ) :
				self.nln_set_gss_n[i] = None

		elif ( param == 'gss_d' ) :

			try :
				self.nln_set_gss_d[i] = float( val )
			except :
				self.nln_set_gss_d[i] = None

		elif ( param == 'gss_w' ) :

			try :
				self.nln_set_gss_w[i] = float( val )
			except :
				self.nln_set_gss_w[i] = None

			if ( ( self.nln_set_gss_w[i] is not None ) and
			     ( self.nln_set_gss_w[i] <= 0        )     ) :
				self.nln_set_gss_w[i] = None

		elif ( param == 'sel' ) :

			try :
				self.nln_set_sel_a[i] = float( val[0] )
			except :
				self.nln_set_sel_a[i] = None

			try :
				self.nln_set_sel_b[i] = float( val[1] )
			except :
				self.nln_set_sel_b[i] = None

			if ( ( self.nln_set_sel_a[i] is not None       ) and
			     ( self.nln_set_sel_b[i] is not None       ) and
			     ( self.nln_set_sel_a[i]
			                      >= self.nln_set_sel_b[i] )     ) :
				self.nln_set_sel_a[i] = None
				self.nln_set_sel_b[i] = None
		else :
			return

		# Validate the settings for the specified ion population.

		if   ( ( self.nln_set_gss_n[i] is None ) or
		       ( self.nln_set_gss_w[i] is None )    ) :
			self.nln_set_gss_vld[i] = False

		elif ( ( self.nln_plas.arr_pop[i]['drift'] ) and
		       ( self.nln_set_gss_d[i] is None     )     ) :
			self.nln_set_gss_vld[i] = False
		else :
			self.nln_set_gss_vld[i] = True

		if ( ( self.nln_set_sel_a[i] is None ) or
		     ( self.nln_set_sel_b[i] is None )    ) :
			self.nln_set_sel_vld[i] = False

		else :
			self.nln_set_sel_vld[i] = True

		# Propagate the changes to the settings for the non-linear
		# analysis.

		self.prop_nln_set( param[0:3] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROPAGATING THE SETTINGS FOR THE NLN ANALYSIS.
	#-----------------------------------------------------------------------

	def prop_nln_set( self, chng ) :

		# Emit a signal that indicates that the settings for the
		# non-linear analysis have changed.

		self.emit( SIGNAL('janus_chng_nln_set') )

		# Regenerate the initial guess or data selection.

		# Note.  The functions called should make any necessay updates
		#        to the dynamic variables.

		if   ( chng == 'gss' ) :
			self.auto_nln_gss( )

		elif ( chng == 'sel' ) :
			self.auto_nln_sel( )
		else :
			return

		# If the above call of "auto_nln_???" did not cause the
		# non-linear fitting to be run, make sure that the initial guess
		# and data selection are being displayed.

		if ( not self.dyn_nln ) :
			self.chng_dsp( "gsl" )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR AUTO-GENERATING THE INITIAL GUESS FOR NLN.
	#-----------------------------------------------------------------------

	def auto_nln_gss( self ) :

		# Assume that, in calling this function, the user would like
		# futher adjustments to the initial guess to be automatic; i.e.,
		# enable dynamic generation of the initial guess.

		self.chng_dyn( 'gss', True, rerun=False )

		# Reset all variables associated with the initial guess.

		self.rset_var( var_nln_gss=True )

		# If the moments analysis does not seem to have been run
		# (sucessfully), run the "make_nln_gss" function (to update the
		# "self.nln_gss_" arrays, widgets, etc.) and then abort.

		if ( self.mom_res is None ) :

			self.make_nln_gss( )

			return

		# Attempt to generate an initial guess of the bulk velocity (of
		# non-drifting species).

		try :
			self.nln_plas['v0_vec'] = [
			         round( v, 1 ) for v in self.mom_res['v0_vec'] ]
		except :
			pass

		# Attempt to generate an initial guess of the parameters for
		# each ion population.

		for i in range( self.nln_n_pop ) :

			# If the ion population is not in use, is invalid, or
			# has invalid guess-settings, cotinue on to the next
			# one.

			if ( ( not self.nln_pop_use[i]     ) or
			     ( not self.nln_pop_vld[i]     ) or
			     ( not self.nln_set_gss_vld[i] )    ) :
				continue

			# Generate the initial guess for this population's
			# density.

			try :
				self.nln_plas.arr_pop[i]['n'] = round_sig(
				                      self.nln_set_gss_n[i]
				                      * self.mom_res['n_p'], 4 )
			except :
				self.nln_plas.arr_pop[i]['n'] = None

			# Generate (if necessary) the initial guess for this
			# population's differential flow.

			if ( self.nln_plas.arr_pop[i]['drift'] ) :
				try :
					sgn = sign( dot(
					             self.mom_res['v0_vec'],
					             self.mfi_avg_nrm        ) )
					if ( sgn == 0. ) :
						sgn = 1.
					self.nln_plas.arr_pop[i]['dv'] = \
					    round_sig( 
					        sgn * self.mom_res['v0_mag']
					            * self.nln_set_gss_d[i], 4 )
				except :
					self.nln_plas.arr_pop[i]['dv'] = None

			# Generate the initial guess of this population's
			# thermal speed(s).

			try :
				w = round_sig( self.nln_set_gss_w[i] 
				               * self.mom_res['w_p'], 4 )
			except :
				w = None

			if ( self.nln_plas.arr_pop[i].aniso ) :
				self.nln_plas.arr_pop[i]['w_per'] = w
				self.nln_plas.arr_pop[i]['w_par'] = w
			else :
				self.nln_plas.arr_pop[i]['w'] = w

		# Run the "make_nln_gss" function to update the "self.nln_gss_"
		# arrays, widgets, etc.

		self.make_nln_gss( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING A GUESS VALUE FOR ONE NLN PARAMETER.
	#-----------------------------------------------------------------------

	def chng_nln_gss( self, i, param, val ) :

		# Assume that, in calling this function, the user would like
		# futher adjustments to the initial guess to be manual; i.e.,
		# disable dynamic generation of an automatic initial-guess.

		self.chng_dyn( 'gss', False, rerun=False )

		# Ensure that the argument "p" is a valid population (unless
		# the "param" argument indicates a velocity component, in which
		# case "p" is irrelevant).

		if ( ( param != 'v_x' ) and
		     ( param != 'v_y' ) and ( param != 'v_z' ) ) :

			if ( ( i < 0 ) or ( i >= self.nln_n_pop ) ) :
				return

		# Change the requested parameter of the requested ion population
		# to the requested value.

		# Note.  Simply "pass"-ing in the event of an "except"-ion
		#        should be sufficient.  If the "pyon" class raises an
		#        "except"-ion during an assignment, it should set the
		#        parameter in question equal to "None".

		if   ( param == 'v_x' ) :

			try :
				self.nln_plas['v0_x'] = val
			except :
				self.nln_plas['v0_x'] = None

		elif ( param == 'v_y' ) :

			try :
				self.nln_plas['v0_y'] = val
			except :
				self.nln_plas['v0_y'] = None

		elif ( param == 'v_z' ) :

			try :
				self.nln_plas['v0_z'] = val
			except :
				self.nln_plas['v0_z'] = None

		elif ( param == 'n' ) :

			try :
				self.nln_plas.arr_pop[i]['n'] = val
			except :
				self.nln_plas.arr_pop[i]['n'] = None

		elif ( param == 'dv' ) :

			try :
				self.nln_plas.arr_pop[i]['dv'] = val
			except :
				self.nln_plas.arr_pop[i]['dv'] = None

		elif ( param == 'w' ) :

			try :
				self.nln_plas.arr_pop[i]['w'] = val
			except :
				self.nln_plas.arr_pop[i]['w'] = None

		elif ( param == 'w_per' ) :

			try :
				self.nln_plas.arr_pop[i]['w_per'] = val
			except :
				self.nln_plas.arr_pop[i]['w_per'] = None

		elif ( param == 'w_par' ) :

			try :
				self.nln_plas.arr_pop[i]['w_par'] = val
			except :
				self.nln_plas.arr_pop[i]['w_par'] = None

		# Run the "make_nln_gss" function to update the "self.nln_gss_"
		# arrays, widgets, etc.

		self.make_nln_gss( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR MAKING THE NLN INITIAL GUESS PARAMETER ARRAY.
	#-----------------------------------------------------------------------

	def make_nln_gss( self ) :

		# Establish which of the ion populations are in use, are valid,
		# and have initial guesses.

		for p in range ( self.nln_n_pop ) :

			if ( ( self.nln_pop_use[p]               ) and
			     ( self.nln_pop_vld[p]               ) and
			     ( self.nln_plas.arr_pop[p].valid(
			                      require_val=True ) )     ) :

				self.nln_gss_vld[p] = True

			else :

				self.nln_gss_vld[p] = False

		self.nln_gss_pop = list( where( self.nln_gss_vld )[0] )

		self.nln_gss_n_pop = len( self.nln_gss_pop )

		# Reset the "prm" and "cur_???" arrays.

		self.nln_gss_prm = [ ]

		self.nln_gss_curr_ion = None
		self.nln_gss_curr_tot = None

		# Abort if any of the following cases arise:
		#   -- No populations have been found to be valid.
		#   -- The primary population is not valid.
		#   -- The init. guess of any reference vel. comp. is invalid.
		#   -- No magnetic field data was loaded.
		# To abort, take the following actions:
		#   -- Emit the signal that the NLN guess has been updated.
		#   -- Return.

		if ( ( self.nln_gss_n_pop == 0         ) or
		     ( 0 not in self.nln_gss_pop       ) or
		     ( None in self.nln_plas['v0_vec'] ) or
		     ( self.n_mfi == 0                 )    ) :

			self.emit( SIGNAL('janus_chng_nln_gss') )

			return

		# Generate the intial guess array (beginning with the reference
		# velocity) and compute the expected  currents from each
		# population.

		pop_v0_vec = self.nln_plas['v0_vec']

		self.nln_gss_prm = list( pop_v0_vec )

		self.nln_gss_curr_ion = [ ]

		for p in self.nln_gss_pop :

			# Extract the drift and anisotropy states of the
			# population

			pop_drift = self.nln_plas.arr_pop[p]['drift']
			pop_aniso = self.nln_plas.arr_pop[p]['aniso']

			# Extract the population's density and add it to the
			# parameter array.

			pop_n = self.nln_plas.arr_pop[p]['n']

			self.nln_gss_prm.append( pop_n )

			# If the population is drifting, extract its drift and
			# add it to the parameter array.  Otherwise, set the
			# drift as zero.

			if ( pop_drift ) :

				pop_dv = self.nln_plas.arr_pop[p]['dv']

				self.nln_gss_prm.append( pop_dv )
			else :
				pop_dv = 0.

			# If the population is anisotropic, extract its
			# perpendicular and parallel thermal-speeds and add them
			# to the parameter array.  Otherwise, extract its scalar
			# thermal speed and add it to the parameter array.

			if ( pop_aniso ) :

				pop_w     = ( self.nln_plas.arr_pop[p]['w_per'],
				              self.nln_plas.arr_pop[p]['w_par'])

				self.nln_gss_prm.append( pop_w[0] )
				self.nln_gss_prm.append( pop_w[1] )
			else :
				pop_w     = self.nln_plas.arr_pop[p]['w']

				self.nln_gss_prm.append( pop_w )

			# For each datum in the spectrum, compute the expected
			# current from each population.

			self.nln_gss_curr_ion.append(
			     self.fc_spec.calc_curr(
			                    self.nln_plas.arr_pop[p]['m'],
			                    self.nln_plas.arr_pop[p]['q'],
			                    pop_v0_vec, pop_n, pop_dv, pop_w ) )

		# Alter the axis order of the array of currents.

		self.nln_gss_curr_ion = [ [ [ [ 
		                     self.nln_gss_curr_ion[p][c][d][b]
		                     for p in range( self.nln_gss_n_pop      ) ]
		                     for b in range( self.fc_spec['n_bin']   ) ]
		                     for d in range( self.fc_spec['n_dir']   ) ]
		                     for c in range( self.fc_spec['n_cup']   ) ]

		# For each datum in the spectrum, compute the total expected
		# current (from all populations).

		self.nln_gss_curr_tot = [ [ [ 
		                     sum( self.nln_gss_curr_ion[c][d][b]     )
		                     for b in range( self.fc_spec['n_bin']   ) ]
		                     for d in range( self.fc_spec['n_dir']   ) ]
		                     for c in range( self.fc_spec['n_cup']   ) ]

		# Propagate the new initial-guess for the non-linear analysis.

		self.prop_nln_gss( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROPAGATING THE GUESS FOR THE NLN ANALYSIS.
	#-----------------------------------------------------------------------

	def prop_nln_gss( self ) :

		# Emit a signal that indicates that the initial guess for the
		# non-linear analysis has changed.

		self.emit( SIGNAL('janus_chng_nln_gss') )

		# If warranted (based on the values of "self.dyn_???"), proceed
		# with dynamic updates to the non-linear analysis.  Otherwise,
		# make sure that the initial guess is being displayed.

		if ( self.dyn_sel ) :
			self.auto_nln_sel( )
		elif ( self.dyn_nln ) :
			self.anls_nln( )
		else :
			self.chng_dsp( 'gsl' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR AUTOMATIC DATA SELECT. FOR THE NON-LIN. ANAL.
	#-----------------------------------------------------------------------

	def auto_nln_sel( self ) :

		# Assume that, in calling this function, the user would like
		# futher adjustments to the point selection to be automatic;
		# i.e., enable dynamic point selection.

		self.chng_dyn( 'sel', True, rerun=False )

		# Re-initialize the data-selection variables for the non-linear
		# analysis.

		self.rset_var( var_nln_sel=True )

		# Intially deselect all data.

		self.nln_sel = tile( False, [ self.fc_spec['n_cup'],
                                              self.fc_spec['n_dir'],
		                              self.fc_spec['n_bin']   ] )

		# Determine which ion species have been selected for analysis
		# and have been given valid parameters, initial geusses, and
		# selection windows.

		pop = where( ( self.nln_gss_vld     ) &
		             ( self.nln_set_sel_vld )   )[0]

		# If point selection canott be run for any ion population or no
		# magentic-field data are available for this spectrum, run the
		# validation code (to update the registered widgets, etc.) and
		# abort.

		if ( ( len( pop ) == 0 ) or
		     ( self.n_mfi == 0 )    ) :

			self.vldt_nln_sel( )

			return

		# Select data based on the selection windows from each of the
		# look directions selected for the moments analysis.

		( tk_c, tk_d ) = where( self.mom_sel_dir )

		n_tk = len( tk_c )

		arr_curr_valid = self.fc_spec['curr_valid']
		arr_vel_cen    = self.fc_spec['vel_cen']

		for j in range( n_tk ) :

			# Extract the current look direction and convert it
			# from altitude-azimuth to rectangular coordiantes.

			c   = tk_c[j]
			d   = tk_d[j]

			dlk = self.fc_spec.arr[c][d][0]['dir']

			# Select data for each species.

			for i in pop :

				# Extract the estimated bulk velocity (and the
				# magnitude thereof) of this ion species (based
				# on the initial guess).

				vel = array( self.nln_plas['vec_v0'] )

				if ( self.nln_plas.arr_pop[i]['drift'] ) :
					vel += self.mfi_avg_nrm * \
					          self.nln_plas.arr_pop[i]['dv']

				v = sqrt( vel[0]**2 + vel[1]**2 + vel[2]**2 )

				# Compute the negative of the projected bulk
				# velocity along the look direction.

				v_proj = - dot( vel, dlk )

				# Compute the range of projected inflow speeds
				# specified by this ion species' charge-to-mass
				# ratio, initial geusses, and selection window.

				if ( self.nln_plas.arr_pop[i]['aniso'] ) :
					ang = abs( dot( dlk, self.mfi_avg_nrm ))
					w = sqrt(
					   ( self.nln_plas.arr_pop[i]['w_per']
					                     * sin(ang) )**2 +
					   ( self.nln_plas.arr_pop[i]['w_par']
					                     * cos(ang) )**2   )
				else :
					w = self.nln_plas.arr_pop[i]['w']

				v_min = v_proj + ( self.nln_set_sel_a[i] *
				                   w * v_proj / v          )
				v_max = v_proj + ( self.nln_set_sel_b[i] *
				                   w * v_proj / v          )

				v_min = v_min * sqrt(
				               self.nln_plas.arr_pop[i]['m'] /
				               self.nln_plas.arr_pop[i]['q']   )
				v_max = v_max * sqrt(
				               self.nln_plas.arr_pop[i]['m'] /
				               self.nln_plas.arr_pop[i]['q']   )

				# Select all seemingly valid measurements from
				# this look direction that fall into this range
				# range of inflow speeds.

				tk = where( 
				     ( array( arr_curr_valid[c][d] )
				            >= self.fc_spec['curr_min'] ) &
				     ( array( arr_vel_cen[c] ) >= v_min ) &
				     ( array( arr_vel_cen[c] ) <= v_max )   )[0]

				for b in tk :
					self.nln_sel[c,d,b] = True

		# Propagate the new data-selection for the non-linear analysis.

		self.prop_nln_sel( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE SELECTION OF A SINGLE POINT.
	#-----------------------------------------------------------------------

	def chng_nln_sel( self, c, d, b ) :

		# As this function was mostly likely called in response to the
		# user manually adjusting the point selection for the
		# non-linear analysis, disable the dynamic updating of this
		# point selection.

		self.chng_dyn( 'sel', False, rerun=False )

		# If necessary, initialize the selection array.

		if ( self.nln_sel is None ) :
			self.nln_sel = tile( False,
			                     [ self.fc_spec['n_cup'],
                                               self.fc_spec['n_dir'],
			                       self.fc_spec['n_bin']     ] )

		# Change the selection of the requested point.

		self.nln_sel[c,d,b] = not self.nln_sel[c,d,b]

		# Propagate the new data-selection for the non-linear analysis.

		self.prop_nln_sel( pnt=[c,d,b] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR PROPAGATING THE NLN DATA-SELECTION.
	#-----------------------------------------------------------------------

	def prop_nln_sel( self, pnt=None ) :

		# Update the count of selected data.

		self.nln_n_sel = len( where( self.nln_sel )[0] )

		# Emit a signal that indicates that the data-selection for the
		# non-linear analysis has changed.

		if ( pnt is None ) :
			self.emit( SIGNAL('janus_chng_nln_sel_all') )
		else :
			self.emit( SIGNAL('janus_chng_nln_sel_bin'),
			           pnt[0], pnt[1], pnt[2]            )

		# If dynamic updating of the non-linear fitting has been
		# enabled, run it.  Otherwise, make sure that the initial guess
		# and data selection are being displayed.

		if ( self.dyn_nln ) :
			self.anls_nln( )
		else :
			self.chng_dsp( 'gsl' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CALCULATING THE NLN MODEL CURRNET.
	#-----------------------------------------------------------------------

	def calc_nln_curr( self, dat, prm ) :

		# Initialize the returned list: the total calculated current for
		# each datum.

		curr = [ 0. for d in dat ]

		# For each ion species, extract the passed parameters and
		# calculate it's contribution to the total current.

		prm_v0 = ( prm[0], prm[1], prm[2] )

		k = 3

		for p in self.nln_gss_pop :

			# Extract the density of population "p".

			prm_n = prm[k]

			k += 1

			# Determine the bulk velocity of population "p",
			# extracting (if necessary) the population's drift.

			if ( self.nln_plas.arr_pop[p]['drift'] ) :

				prm_dv = prm[k]

				k += 1

			else :

				prm_dv = 0.

			# Extract the thermal speed(s).

			if ( self.nln_plas.arr_pop[p]['aniso'] ) :

				prm_w = ( prm[k], prm[k+1] )

				k += 2

			else :

				prm_w = prm[k]

				k += 1

			# Add the contribution of this ion species to
			# the total currents.

			for d in range( len( dat ) ) :

				curr[d] += dat[d].calc_curr(
				                self.nln_plas.arr_pop[p]['m'],
				                self.nln_plas.arr_pop[p]['q'],
				                prm_v0, prm_n, prm_dv, prm_w   )

		# Return the list of total currents from all modeled ion
		# species.

		return curr

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RUNNING THE NON-LINEAR ANALYSIS.
	#-----------------------------------------------------------------------

	def anls_nln( self ) :

		# Re-initialize the output of the non-linear analysis.

		start = time.time()
		self.rset_var( var_nln_res=True )

		# Load the list of ion populations to be analyzed and the intial
		# guess of their parameters.

		# If any of the following conditions are met, emit a signal that
		# indicates that the results of the non-linear analysis have
		# change, and abort.
		#   -- No ion spectrum has been loaded.
		#   -- No ion population is available for analysis.
		#   -- The primary ion species is not available for analysis.
		#   -- No initial guess has been generated.
		#   -- Insufficient data have been selected.

		if ( ( self.fc_spec is None              ) or
		     ( self.fc_spec['n_bin'] == 0        ) or
		     ( self.n_mfi == 0                   ) or
		     ( len( self.nln_gss_pop ) == 0      ) or
		     ( 0 not in self.nln_gss_pop         ) or
		     ( len( self.nln_gss_prm ) == 0      ) or
		     ( self.nln_n_sel < self.nln_min_sel )    ) :

			self.emit( SIGNAL('janus_mesg'),
			           'core', 'norun', 'nln' )

			self.emit( SIGNAL('janus_chng_nln_res') )

			return

		# Message the user that the non-linear analysis has begun.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'nln' )

		# Define the function for evaluating the modeled current.

		def model( x, *p ) :

			return self.calc_nln_curr( x, p )

                # Save the data selection and then use it to generate data
		# arrays for the non-linear fit.

		self.nln_res_sel = self.nln_sel.copy( )

		# Extract the data selection.

		x = [ ]

		for c in range( self.fc_spec['n_cup'] ) :

			for d in range( self.fc_spec['n_dir'] ) :

				for b in range( self.fc_spec['n_bin'] ) :

					if ( self.nln_res_sel[c][d][b] ) :

						x.append(
						     self.fc_spec.arr[c][d][b] )

		y = [ xx['curr'] for xx in x ]

		# Compute the uncertainties.

		sigma = [ sqrt( yy ) for yy in y ]

		# Attempt to perform the non-linear fit.  If this fails, reset
		# the associated variables and abort.

		try :

			( fit, covar ) = curve_fit( model, x, y, 
			                            self.nln_gss_prm,
			                            sigma=sigma       )

			sig = sqrt( diag( covar ) )

		except :

			self.emit( SIGNAL('janus_mesg'), 'core', 'fail', 'nln' )

			self.rset_var( var_nln_res=True )

			self.emit( SIGNAL('janus_chng_nln_res') )

			return

		# Save the properties and fit parameters for each ion species
		# used in this analysis.

		self.nln_res_plas = plas( enforce=False )

		self.nln_res_plas.covar       = covar.copy( )

		self.nln_res_plas['time']     = self.time_epc

		self.nln_res_plas['b0_x']     = self.mfi_avg_vec[0]
		self.nln_res_plas['b0_y']     = self.mfi_avg_vec[1]
		self.nln_res_plas['b0_z']     = self.mfi_avg_vec[2]

		pop_v0_vec                    = [fit[0], fit[1], fit[2]]
		self.nln_res_plas['v0_x']     =  fit[0]
		self.nln_res_plas['v0_y']     =  fit[1]
		self.nln_res_plas['v0_z']     =  fit[2]
		self.nln_res_plas['sig_v0_x'] =  sig[0]
		self.nln_res_plas['sig_v0_y'] =  sig[1]
		self.nln_res_plas['sig_v0_z'] =  sig[2]

		c = 3

		self.nln_res_curr_ion = []

		for p in self.nln_gss_pop :

			# If necessary, add this population's species to the
			# results.

			spc_name = self.nln_plas.arr_pop[p].my_spec['name']

			if ( self.nln_res_plas.get_spec( spc_name ) is None ) :

				spc_sym = \
				         self.nln_plas.arr_pop[p].my_spec['sym']
				spc_m   = \
				         self.nln_plas.arr_pop[p].my_spec['m'  ]
				spc_q   = \
				         self.nln_plas.arr_pop[p].my_spec['q'  ]

				self.nln_res_plas.add_spec(
				                   name=spc_name, sym=spc_sym,
				                   m=spc_m, q=spc_q            )

			# Add the population itself to the results.

			pop_drift = self.nln_plas.arr_pop[p]['drift']
			pop_aniso = self.nln_plas.arr_pop[p]['aniso']
			pop_name  = self.nln_plas.arr_pop[p]['name' ]
			pop_sym   = self.nln_plas.arr_pop[p]['sym'  ]

			pop_n     = fit[c]
			pop_sig_n = sig[c]
			c += 1

			if ( pop_drift ) :
				pop_dv     = fit[c]
				pop_sig_dv = sig[c]
				c += 1
			else :
				pop_dv     = None
				pop_sig_dv = None

			if ( pop_aniso ) :
				pop_w         = [ fit[c], fit[c+1] ]
				pop_sig_w     = None
				pop_sig_w_per = sig[c  ]
				pop_sig_w_par = sig[c+1]
				c += 2
			else :
				pop_w         = fit[c]
				pop_sig_w     = sig[c]
				pop_sig_w_per = None 
				pop_sig_w_par = None
				c += 1

			self.nln_res_plas.add_pop(
			       spc=spc_name, drift=pop_drift,
			       aniso=pop_aniso, name=pop_name,
			       sym=pop_sym, n=pop_n, dv=pop_dv, w=pop_w,
			       sig_n=pop_sig_n, sig_dv=pop_sig_dv, 
			       sig_w=pop_sig_w, sig_w_per=pop_sig_w_per,
			       sig_w_par=pop_sig_w_par                    )

			# For each datum in the spectrum, compute the expected
			# current from each population.

			self.nln_res_curr_ion.append(
			     self.fc_spec.calc_curr ( 
			                  self.nln_plas.arr_pop[p]['m'],
			                  self.nln_plas.arr_pop[p]['q'],
			                  pop_v0_vec, pop_n, pop_dv, pop_w ) )

		# Save the results of the this non-linear analysis to the
		# results log.

		self.series.add_spec( self.nln_res_plas )

		# Calculate the expected currents based on the results of the
		# non-linear analysis.

		self.nln_res_curr_ion = [ [ [ [
		                     self.nln_res_curr_ion[p][c][d][b]
		                     for p in range( len(
		                                 self.nln_res_plas.arr_pop ) ) ]
		                     for b in range( self.fc_spec['n_bin']   ) ]
		                     for d in range( self.fc_spec['n_dir']   ) ]
		                     for c in range( self.fc_spec['n_cup']   ) ]

		self.nln_res_curr_tot =[ [ [ 
		                           sum( self.nln_res_curr_ion[c][d][b] )
		                     for b in range( self.fc_spec['n_bin']   ) ]
		                     for d in range( self.fc_spec['n_dir']   ) ]
		                     for c in range( self.fc_spec['n_cup']   ) ]



		# Message the user that the non-linear analysis has finished.

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'nln' )

		# Emit a signal that indicates that the results of the
		# non-linear analysis have changed.

                self.nln_res_runtime = (time.time()-start)

		self.emit( SIGNAL('janus_chng_nln_res') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE DISPLAYED ANALYSIS.
	#-----------------------------------------------------------------------

	def chng_dsp( self, value ) :

		# If "self.dsp" already equals "value," abort (without any
		# notice to the registered widgets) as nothing needs to be done.

		if ( self.dsp == value ) :

			return

		# If "value" is a valid display setting, update the value of
		# "self.dsp"; otherwise, set "self.dsp" to "None".

		if ( ( value == 'mom' ) or ( value == 'gsl' ) or
		     ( value == 'nln' )                          ) :

			self.dsp = value

		else :

			self.dsp = None

		# Emit a signal that indicates that the "display" setting has
		# changed.

		self.emit( SIGNAL('janus_chng_dsp') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING IF AN ANALYSIS UPDATES DYNAMICALLY.
	#-----------------------------------------------------------------------

	def chng_dyn( self, anal, value, rerun=True ) :

		# Regularize "value" to ensure that it is a standard boolean.

		value = True if ( value ) else False

		# Based on "anal", update the appropriate "self.dyn_???".  If no
		# change is necessary, return (i.e., without requesting that the
		# widgets update).

		if ( anal == 'mom' ) :

			if ( self.dyn_mom != value ) :
				self.dyn_mom = value
			else :
				return

		elif ( anal == 'gss' ) :

			if ( self.dyn_gss != value ) :
				self.dyn_gss = value
			else :
				return

		elif ( anal == 'sel' ) :

			if ( self.dyn_sel != value ) :
				self.dyn_sel = value
			else :
				return

		elif ( anal == 'nln' ) :

			if ( self.dyn_nln != value ) :
				self.dyn_nln = value
			else :
				return
		else :

			return

		# Emit a signal that indicates that the "dynamic" settings have
		# changed.

		self.emit( SIGNAL('janus_chng_dyn') )

		# If dynamic updates has been turned on for the specified
		# analysis "anal", and the user hasn't requested otherwise,
		# re-run that analysis and adjust the display.

		if ( ( value ) and ( rerun ) ) :

			if ( anal == 'mom' ) :

				self.anls_mom( )

				if ( ( not self.dyn_sel ) and
				     ( not self.dyn_gss )     ) :
					self.chng_dsp( 'mom' )

				elif ( self.dyn_nln ) :
					self.chng_dsp( 'nln' )
				else :
					self.chng_dsp( 'gsl' )

			elif ( anal == 'gss' ) :

				self.auto_nln_gss( )

				if ( self.dyn_nln ) :
					self.chng_dsp( 'nln' )
				else :
					self.chng_dsp( 'gsl' )

			elif ( anal == 'sel' ) :

				self.auto_nln_sel( )

				if ( self.dyn_nln ) :
					self.chng_dsp( 'nln' )
				else :
					self.chng_dsp( 'gsl' )

			elif ( anal == 'nln' ) :

				self.anls_nln( )

				self.chng_dsp( 'nln' )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION CHANGING THE STATE OF AN OPTION.
	#-----------------------------------------------------------------------

	def chng_opt( self, key, value ) :

		# Extract the prefix of the key.  If the key is invalid, abort.

		if ( key in self.opt ) :
			prefix = key[0:3]
		else :
			self.emit( SIGNAL('janus_chng_opt') )
			return

		# Take the appropriate actions based on the prefix
		# provided.

		if ( prefix == 'res' ) :

			# Assign the provided value to the specified key.

			self.opt[key] = bool( value )

			# Validate the other keys' values.

			if ( not ( self.opt['res_dw'] or 
			           self.opt['res_dt'] ) ) :

				if ( key == 'res_dw' ) :
					self.opt['res_dt'] = True
				else :
					self.opt['res_dw'] = True

			if ( self.opt['res_n'] or self.opt['res_v'] or
			     self.opt['res_d'] or self.opt['res_w'] or
        	             self.opt['res_r'] or self.opt['res_b'] or
        	             self.opt['res_s'] or self.opt['res_k']     ) :
				self.opt['res'] = True
			else :
				self.opt['res'] = False

		elif ( prefix == 'mfi' ) :

			# Assign the provided value to the specified key.

			self.opt[key] = bool( value )

			# Validate the other keys' values.

			if ( not ( self.opt['mfi_l'] or 
			           self.opt['mfi_h'] ) ) :

				if ( key == 'mfi_l' ) :
					self.opt['mfi_h'] = True
				else :
					self.opt['mfi_l'] = True

		elif ( prefix == 'fls' ) :

			# Assign the provided value to the specified key.

			if ( key == 'fls_n_fc' ) :

				try :
					self.fc_arcv.chng_n_file_max( value )
				except :
					pass

				self.opt['fls_n_fc'] = self.fc_arcv.n_file_max

			if ( key == 'fls_n_spin' ) :

				try :
					self.spin_arcv.chng_n_file_max( value )
				except :
					pass

				self.opt['fls_n_spin'] =\
				                       self.spin_arcv.n_file_max

			if ( key == 'fls_n_mfi_l' ) :

				try :
					self.mfi_arcv_lres.chng_n_file_max(
					                                 value )
				except :
					pass

				self.opt['fls_n_mfi_l'] =\
				                    self.mfi_arcv_lres.n_file_max

			if ( key == 'fls_n_mfi_h' ) :

				try :
					self.mfi_arcv_hres.chng_n_file_max(
					                                 value )
				except :
					pass

				self.opt['fls_n_mfi_h'] =\
				                   self.mfi_arcv_hres.n_file_max

		# Save updated options to the config file.

		self.save_opt( )

		# Emit the signal that an option has changed.

		self.emit( SIGNAL('janus_chng_opt') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SAVING THE OPTIONS MENU TO A CONFIG FILE.
	#-----------------------------------------------------------------------

	def save_opt( self ) :

		# Attempt to open the configuration file (replacing any that
		# already exists).  If this fails, abort.

		try : 
			fl = open( self.opt_flnm, 'w' )
		except :
			return

		# Write a header.

		fl.write( '# Janus Version ' )
		fl.write( self.version )
		fl.write( '\n' )
		fl.write( '# This configuration file stores the values\n'   )
		fl.write( '# from the options menu that were used in the\n' )
		fl.write( '# last Janus session.\n'                         )

		# Write out the name and value of each key in the options
		# dictionary.

		keys = self.opt.keys( )
		keys.sort( )

		for key in keys :

			prefix = key[0:3]

			fl.write( '\n' )
			fl.write( key + ' ' )

			if ( ( prefix == 'res' ) or ( prefix == 'mfi' ) ) :

				if ( self.opt[key] ) :
					fl.write('1')
				else :
					fl.write('0')

			else :

				fl.write( str( self.opt[key] ) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESTORING THE DEFAULT OPTIONS.
	#-----------------------------------------------------------------------

	def rstr_opt( self,
	              propagate=True, save=True, signal=True ) :

		# Reset the options dictionary to its default values.

		self.opt = { 'res_dw'     :True,
		             'res_dt'     :True,
		             'res'        :True,
		             'res_u'      :True,
		             'res_n'      :True,
		             'res_v'      :True,
		             'res_d'      :True,
		             'res_w'      :True,
		             'res_r'      :True,
		             'res_b'      :True,
		             'res_s'      :True,
		             'res_k'      :True,
		             'mfi_l'      :True,
		             'mfi_h'      :False,
		             'fls_n_fc'   :float('inf'),
		             'fls_n_spin' :float('inf'),
		             'fls_n_mfi_l':float('inf'),
		             'fls_n_mfi_h':float('inf')    }

		# If requested, propagate any changes.

		if ( propagate ) :

			try :
				self.fc_arcv.chng_n_file_max(
				                       self.opt['fls_n_fc'] )
			except :
				pass

			try :
				self.spin_arcv.chng_n_file_max(
				                       self.opt['fls_n_spin'] )
			except :
				pass

			try :
				self.mfi_arcv_lres.chng_n_file_max(
				                       self.opt['fls_n_mfi_l'] )
			except :
				pass

			try :
				self.mfi_arcv_hres.chng_n_file_max(
				                       self.opt['fls_n_mfi_h'] )
			except :
				pass

			self.opt['fls_n_fc']    = self.fc_arcv.n_file_max
			self.opt['fls_n_spin']  = self.spin_arcv.n_file_max
			self.opt['fls_n_mfi_l'] = self.mfi_arcv_lres.n_file_max
			self.opt['fls_n_mfi_h'] = self.mfi_arcv_hres.n_file_max

		# If requested, save the options dictionary.

		if ( save ) :
			self.save_opt( )

		# If requested, emit the signal that the options have changed.

		if ( signal ) :
			self.emit( SIGNAL('janus_rstr_opt') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR AUTOMATICALLY RUNNING A RANGE OF SPECTRA.
	#-----------------------------------------------------------------------

	def auto_run( self, t_strt, t_stop,
	                    get_next=None, err_halt=None, pause=None ) :

		# Supply values for any missing keywords.

		get_next = False if ( get_next is None ) else get_next
		err_halt = False if ( err_halt is None ) else err_halt
		pause    = 0     if ( pause    is None ) else pause

		# Message the user that the automated analysis is about to
		# begin.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'auto' )

		# Attempt to convert the start and stop timestamps to epoch
		# times.  If one or more fails, or if the start time does not
		# strictly precede the stop time, abort.

		time_strt = calc_time_epc( t_strt )
		time_stop = calc_time_epc( t_stop )

		if ( ( time_strt is None ) or ( time_stop is None ) ) :
			return
		elif ( time_strt >= time_stop ) :
			return

		# Begin with the start time stamp.  Load and process spectra,
		# one by one, until the stop timestamp is reached (or a
		# premature stop has been requested).

		first_pass = True
		self.stop_auto_run = False

		while ( not self.stop_auto_run ) :

			# Load and analyze (according to the "self.dyn_???"
			# parameters) the first/next spectrum.

			if ( first_pass ) :
				first_pass = False
				self.load_spec( time_req=time_strt,
				                get_next=get_next   )
			else :
				self.load_spec( time_req=self.time_epc,
				                get_next=True           )

			# If no spectrum was able to be loaded, abort.

			if ( self.time_epc is None ) :
				self.stop_auto_run = True
				break

			# If requested by the user, check for errors from the
			# analyses that were run.  If any are found, abort.

			if ( err_halt ) :
				if ( self.n_mfi == 0 ) :
					self.stop_auto_run = True
					break
				if ( ( self.dyn_mom         ) and
				     ( self.mom_res is None )     ) :
					self.stop_auto_run = True
					break
				if ( ( self.dyn_nln               ) and
				     ( self.nln_res_ion_n is None )     ) :
					self.stop_auto_run = True
					break

			# If the spectrum just loaded was the last that needed
			# to be loaded, end.

			if ( self.time_epc > time_stop ) :
				break

			# If a request to abort has come from some source other
			# than this function (e.g., a user), do so.  Otherwise,
			# wait the specified period of time.

			if ( self.stop_auto_run ) :
				break
			else :
				sleep( pause )

		# Message the user that the automated analysis has finished.

		if ( self.stop_auto_run ) :
			self.emit( SIGNAL('janus_mesg'),
			           'core', 'abort', 'auto' )
		else :
			self.emit( SIGNAL('janus_mesg'),
			           'core', 'end'  , 'auto' )

		# Emit a signal that indicates that the automated analysis has
		# ended.

		self.emit( SIGNAL('janus_done_auto_run') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR SAVING THE RESULTS LOG TO A FILE.
	#-----------------------------------------------------------------------

	def save_res( self, nm_fl, exit=False ) :

		# Message the user that a save is about to begin.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'save' )

		# Try to create a new output file to hold the log of analysis
		# results.  If this fails, message the user and abort.

		try :
			fl = open( nm_fl, 'wb' )
		except :
			self.emit( SIGNAL('janus_mesg'),
			           'core', 'fail', 'save' )

		# Save the results log to the output file.

		pickle.dump( self.series, fl )

		# Close the output file.

		fl.close( )

		# Message the user that the save was successful.

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'save' )

		# If requested, exit the application.

		if ( exit ) :
			self.emit( SIGNAL('janus_exit') )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR EXPORTING THE RESULTS TO A TEXT FILE.
	#-----------------------------------------------------------------------

	def xprt_res( self, nm_fl, exit=False ) :

		# Message the user that an export is about to begin.

		self.emit( SIGNAL('janus_mesg'), 'core', 'begin', 'xprt' )

		# Try to create a new output file to hold the log of analysis
		# results in plain text.  If this fails, message the user and
		# abort.

		try :
			fl = open( nm_fl, 'w' )
		except :
			self.emit( SIGNAL('janus_mesg'),
			           'core', 'fail', 'xprt' )

		# Define the format for numerical quantities.

		txt_num = ' {:+10.4e}'
		txt_spc = 11 * ' '
		txt_sep = ( '#-----------------------------' +
		            '-----------------------------'    )

		# Write a header.

		fl.write( txt_sep )
		fl.write( '\n' )
		fl.write( '# Janus Version ' )
		fl.write( self.version )
		fl.write( '\n' )
		fl.write( txt_sep )
		fl.write( '\n' )
		fl.write( '# Comments:\n' )
		fl.write( '#   -- Timestamps are in the format\n'              )
		fl.write( '#      "YYYY-MM-DD/HH-MM-SS" and given in UTC.\n'   )
		fl.write( '#   -- Numerical quantities (except timestamps)\n'  )
		fl.write( '#      are in the format "+10.4e".\n'               )
		fl.write( '#   -- The mass and charge of a species appear\n'   )
		fl.write( '#      (in that order) on the line immediately\n'   )
		fl.write( '#      below that with its name.  These quanties\n' )
		fl.write( '#      are scaled to those for the proton.\n'       )
		fl.write( '#   -- The drift velocity is parallel to the \n'    )
		fl.write( '#      to the magnetic field.  A population with\n' )
		fl.write( '#      no differential flow listed was assumed\n'   )
		fl.write( '#      to not drift (relative to the bulk\n'        )
		fl.write( '#      velocity.)\n'                                )
		fl.write( '#   -- Three values are given for each velocity\n'  )
		fl.write( '#      and magnetic field; these, respecitively,\n' )
		fl.write( '#      are the "x"-, "y"-, and "z"-components in\n' )
		fl.write( '#      the GSE coordinate system.\n'                )
		fl.write( '#   -- Where two quantities are listed for\n'       )
		fl.write( '#      thermal speed, the first is the \n'          )
		fl.write( '#      perpendicular thermal speed and second is\n' )
		fl.write( '#      the parallel.\n'                             )
		fl.write( '#   -- A quantity with an uncertainty value has\n'  )
		fl.write( '#      that value written immediately below it.\n'  )
		fl.write( '#      Uncertainty values are absolute (versus\n'   )
		fl.write( '#      relative) uncertainties and are scaled so\n' )
		fl.write( '#      that the reduced chi-squared returned by\n'  )
		fl.write( '#      the non-linear fit is unity.\n'              )
		fl.write( '#   -- The units on numerical quantities are as\n'  )
		fl.write( '#      follows:\n'                                  )
		fl.write( '#        -- Magnetic field: nT\n'            )
		fl.write( '#        -- Mass:           proton mass\n'   )
		fl.write( '#        -- Charge:         proton charge\n' )
		fl.write( '#        -- Density:        cm^-3\n'         )
		fl.write( '#        -- Velocity:       km/s\n'          )
		fl.write( txt_sep )

		# Write the values of the parameters for each spectum.

		for plas in self.series.arr :

			# Write the timestamp.

			fl.write( '\n' )
			fl.write( 'Timestamp:  ' )
			fl.write( calc_time_sec( plas['time'] ) )

			# Write the magnetic field.

			fl.write( '\n' )
			fl.write( 'B-Field:   ' )
			fl.write( txt_num.format( plas['b0_x'] ) )
			fl.write( txt_num.format( plas['b0_y'] ) )
			fl.write( txt_num.format( plas['b0_z'] ) )

			# Write the bulk velocity and it's uncertainty.

			fl.write( '\n' )
			fl.write( 'Velocity:  ' )
			fl.write( txt_num.format( plas['v0_x'] ) )
			fl.write( txt_num.format( plas['v0_y'] ) )
			fl.write( txt_num.format( plas['v0_z'] ) )
			fl.write( '\n' )
			fl.write( txt_spc )
			fl.write( txt_num.format( plas['sig_v0_x'] ) )
			fl.write( txt_num.format( plas['sig_v0_y'] ) )
			fl.write( txt_num.format( plas['sig_v0_z'] ) )

			# Write the values for each species.

			for spec in plas.arr_spec :

				# Write the values for the general parameters of
				# the species.

				fl.write( '\n' )
				fl.write( 'Species:    ' )
			fl.write( txt_num.format( plas['v0_z'] ) )
			fl.write( '\n' )
			fl.write( txt_spc )
			fl.write( txt_num.format( plas['sig_v0_x'] ) )
			fl.write( txt_num.format( plas['sig_v0_y'] ) )
			fl.write( txt_num.format( plas['sig_v0_z'] ) )

			# Write the values for each species.

			for spec in plas.arr_spec :

				# Write the values for the general parameters of
				# the species.

				fl.write( '\n' )
				fl.write( 'Species:    ' )
				fl.write( spec['name'] )
				fl.write( ' (' )
				fl.write( spec['sym'] )
				fl.write( ')' )

				fl.write( '\n' )
				fl.write( txt_spc )
				fl.write( txt_num.format( spec['m'] ) )
				fl.write( ' ' )
				fl.write( txt_num.format( spec['q'] ) )

				# Write the values for the parameters of each
				# population of the species.

				for pop in plas.lst_pop( spec ) :

					# Write the population name.

					fl.write( '\n' )
					fl.write( txt_spc )
					fl.write( ' ' )
					fl.write( 'Population: ' )
					fl.write( pop['name'] )
					fl.write( ' (' )
					fl.write( pop['sym'] )
					fl.write( ')' )

					# Write the population's density (and
					# uncertainty therin).

					fl.write( '\n' )
					fl.write( txt_spc )
					fl.write( txt_spc )
					fl.write( '  ' )
					fl.write( 'Density:   ' )
					fl.write( txt_num.format( pop['n'] ) )
					fl.write( '\n' )
					fl.write( txt_spc )
					fl.write( txt_spc )
					fl.write( txt_spc )
					fl.write( '  ' )
					fl.write( txt_num.format( pop['sig_n'] ) )

					# If applicable, write the populations's
					# drift (and uncertainty therin).

					if ( pop.drift ):
						fl.write( '\n' )
						fl.write( txt_spc )
						fl.write( txt_spc )
						fl.write( '  ' )
						fl.write( 'Drift vel: ' )
						fl.write( txt_num.format(
						                   pop['dv'] ) )
						fl.write( '\n' )
						fl.write( txt_spc )
						fl.write( txt_spc )
						fl.write( txt_spc )
						fl.write( '  ' )
						fl.write( txt_num.format(
						                 pop['sig_dv'] ) )

					# Write the population's thermal
					# speed(s) (and uncertainty therin).

					fl.write( '\n' )
					fl.write( txt_spc )
					fl.write( txt_spc )
					fl.write( '  ' )
					fl.write( 'Thrm Speed:' )
					if ( pop.aniso ) :
						fl.write( txt_num.format(
						                pop['w_per'] ) )
						fl.write( txt_num.format(
						                pop['w_par'] ) )
					else :
						fl.write( txt_num.format(
						                    pop['w'] ) )
					fl.write( '\n' )
					fl.write( txt_spc )
					fl.write( txt_spc )
					fl.write( txt_spc )
					fl.write( '  ' )
					if ( pop.aniso ) :
						fl.write( txt_num.format(
						              pop['sig_w_per'] ) )
						fl.write( txt_num.format(
						              pop['sig_w_par'] ) )
					else :
						fl.write( txt_num.format(
						                  pop['sig_w'] ) )

			# Write a seperator.

			fl.write( '\n' )
			fl.write( txt_sep )

		# Close the output file.

		fl.close( )

		# Message the user that the export was successful.

		self.emit( SIGNAL('janus_mesg'), 'core', 'end', 'xprt' )

		# If requested, exit the application.

		if ( exit ) :
			self.emit( SIGNAL('janus_exit') )
