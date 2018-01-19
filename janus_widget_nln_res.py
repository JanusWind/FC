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
from PyQt4.QtGui import QTextCursor

# Load the modules for displaying text output.

from janus_format_TextEdit import format_TextEdit

# Load the necessary array modules and mathematical functions.

from numpy import sqrt

from math import log10, floor

from janus_helper import round_sig

#from tabulate import tabulate


################################################################################
## DEFINE CLASS "widget_nln_res" TO CUSTOMIZE "format_TextEdit" FOR NLN OUTPUT.
################################################################################

class widget_nln_res( format_TextEdit ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attribues of an instance of "format_TextEdit".

		super( widget_nln_res, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset  )
		self.connect( self.core, SIGNAL('janus_chng_opt'),
		                                            self.resp_chng_opt )
		self.connect( self.core, SIGNAL('janus_rstr_opt'),
		                                            self.resp_chng_opt )
		self.connect( self.core, SIGNAL('janus_chng_mfi'),
		                                            self.resp_chng_mfi )
		self.connect( self.core, SIGNAL('janus_chng_nln_res'),
		                                        self.resp_chng_nln_res )

		# Set this text editor as read only (for the user).

		self.setReadOnly( True )

		# Populate this text editor with the results of the non-linear
		# analysis.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GENERATING THE TEXT FOR THIS TEXT AREA.
	#-----------------------------------------------------------------------

	def make_txt( self ) :

		# Clear the text area (in case there's some text already there).

		self.clear( )

		# If there are no results from the non-linear analysis (either
		# because it was never run or it failed), abort.

		if ( self.core.nln_res_plas is None ) :

			return

                # Print the length of time it takes to run the non-linear
                # analysis

                self.prnt_htm( 'Non-linear run time = ' )
                self.prnt_dcm( self.core.nln_res_runtime, 4,'sec' )
                self.prnt_brk( )
                self.prnt_brk( )

		# If none of the display menus is selected, do not print
		# anything in the non-linear display widget.

		if (self.core.opt['res'] == False ) :

			return

		# Print the results for each population that was considered in
		# the non-linear analysis, grouping the populations by their
		# species.

		first_spc = True

		for spc in self.core.nln_res_plas.arr_spec :

			# Unless this is the first species, skip a line.

			self.prnt_htm(str(spc) + "\n\n\n")

			if ( not first_spc ) :
				self.prnt_brk( )
				self.prnt_brk( )

			# Print the name of the species

			self.prnt_htm( '<b><u>' + spc['name']
			              + ' (<i>' + spc['sym']
			              + '</i>):</b></u>'     )

			# Print the results for each population of this species.

			first_pop = True

			for pop in self.core.nln_res_plas.lst_pop( spc ) :

				# Skip a line.

				self.prnt_brk( )

				# Print the name of the population.

				self.prnt_brk( )
				self.prnt_tab( 1 )
				self.prnt_htm( '<u>' + pop['name'] + ' (<i>'
				                   + pop['sym'] + '</i>):</u>' )

				# Generate the mathematical labels.

				sym = spc['sym'] + pop['sym']

				lab_n     = '<i>n<sub>'  + sym + '</sub></i>'
				lab_v     = '<i>v<sub>'  + sym + '</sub></i>'
				lab_v_x   = '<i>v<sub>x' + sym + '</sub></i>'
				lab_v_y   = '<i>v<sub>y' + sym + '</sub></i>'
				lab_v_z   = '<i>v<sub>z' + sym + '</sub></i>'
				lab_dv    = '<i>&Delta;v</i><sub>||<i>' + \
				                 sym + '</i></sub>'
				lab_w     = '<i>w<sub>' + sym + '</sub></i>'
				lab_w_per = '<i>w</i><sub>&perp;<i>' + \
				                 sym + '</i></sub>'
				lab_w_par = '<i>w</i><sub>||<i>' + \
				                 sym + '</i></sub>'
				lab_r     = '<i>R<sub>' + sym + '</sub></i>'
				lab_b     = '<i>&beta;</i><sub>||<i>' + \
				                sym + '</i></sub>'
				lab_t     = '<i>T<sub>' + sym + '</sub></i>'
				lab_t_per = '<i>T</i><sub>&perp;<i>' + \
				                 sym + '</i></sub>'
				lab_t_par = '<i>T</i><sub>||<i>' + \
			                 sym + '</i></sub>'
				lab_s     = '<i>S<sub>' + spc['sym'] + \
				            '</sub></i>'
				lab_k     = '<i>K<sub>' + spc['sym'] + \
				            '</sub></i>'

				# Print the population's density.

				dcm = max( [ 1, 2 - int( floor( log10(
				                       abs( pop['n'] ) ) ) ) ] )

				if ( self.core.opt['res_n'] ) :

					self.prnt_brk( )
					self.prnt_tab( 2 )
					self.prnt_htm( lab_n + ' = ' )
					self.prnt_dcm( pop['n'], dcm )
					if ( self.core.opt['res_u'] ) :
						self.prnt_htm(
						        '&nbsp;&plusmn;&nbsp;' )
						self.prnt_dcm( pop['sig_n'],dcm)
					self.prnt_htm( 'cm<sup>-3</sup>' )
	
				# If this is the first population of the first
				# species, print the bulk velocity.  Otherwise,
				# if the population has drift, print its drift
				# speed.

				if ( ( first_spc ) and ( first_pop ) ) :

					if ( self.core.opt['res_v'] ) :

						self.prnt_brk( )
						self.prnt_tab( 2 )
						self.prnt_htm( lab_v + ' = '   )
						self.prnt_dcm(
						   self.core.nln_res_plas[
						        'v0'], 0, 'km/s'       )
						self.prnt_brk( )
						self.prnt_tab( 3 )
						self.prnt_htm( lab_v_x + ' = ' )
						self.prnt_dcm(
						   self.core.nln_res_plas[
						                    'v0_x'], 0 )

						if ( self.core.opt['res_u'] ) :

							self.prnt_htm( 
						        '&nbsp;&plusmn;&nbsp;' )
							self.prnt_dcm(
						        self.core.nln_res_plas[
						               'sig_v0_x'], 0  )
						self.prnt_htm( 'km/s'          )

						self.prnt_brk( )
						self.prnt_tab( 3 )
						self.prnt_htm( lab_v_y + ' = ' )
						self.prnt_dcm(
						   self.core.nln_res_plas[
						                    'v0_y'], 0 )

						if ( self.core.opt['res_u'] ):

							self.prnt_htm(
						        '&nbsp;&plusmn;&nbsp;' )
							self.prnt_dcm(
						         self.core.nln_res_plas[
						               'sig_v0_y'], 0  )
						self.prnt_htm( 'km/s'          )

						self.prnt_brk( )
						self.prnt_tab( 3 )
						self.prnt_htm( lab_v_z + ' = ' )
						self.prnt_dcm(
						   self.core.nln_res_plas[
						                    'v0_z'], 0 )

						if ( self.core.opt['res_u'] ):
							self.prnt_htm(
						        '&nbsp;&plusmn;&nbsp;' )
							self.prnt_dcm(
						         self.core.nln_res_plas[
						               'sig_v0_z'], 0  )
						self.prnt_htm( 'km/s'          )

				elif ( pop['drift'] ) :

					if ( self.core.opt['res_d'] ) :
						self.prnt_brk( )
						self.prnt_tab( 2 )
						self.prnt_htm( lab_dv + ' = ' )
						self.prnt_dcm( pop['dv'], 1 )
						if( self.core.opt['res_u'] ) :
							self.prnt_htm(
							'&nbsp;&plusmn;&nbsp;' )
							self.prnt_dcm(
							pop['sig_dv'], 1       )
						self.prnt_htm( 'km/s')

				# Print the population's thermal speed(s).

				if ( self.core.opt['res_dw'] ) :

					if ( pop['aniso'] ) :

						if ( self.core.opt['res_w'] ) :

							self.prnt_brk( )
							self.prnt_tab( 2 )
							self.prnt_htm(
							         lab_w + ' = ' )
							self.prnt_dcm(
							   pop['w'], 1, 'km/s' )
							self.prnt_brk( )
							self.prnt_tab( 3 )
							self.prnt_htm(
							     lab_w_per + ' = ' )
							self.prnt_dcm(
							       pop['w_per'], 1 )
							if (
							self.core.opt['res_u']
							                     ) :
								self.prnt_htm(
								'&nbsp;&plusmn;\
							         &nbsp;'       )
								self.prnt_dcm(
								pop[
								'sig_w_per'] ,1)
							self.prnt_htm( 'km/s' )

							self.prnt_brk( )
							self.prnt_tab( 3 )
							self.prnt_htm(
							     lab_w_par + ' = ' )
							self.prnt_dcm(
							       pop['w_par'], 1 )
							if (
							self.core.opt['res_u']
							                     ) :
								self.prnt_htm(
								'&nbsp;&plusmn;\
							         &nbsp;'       )
								self.prnt_dcm(
								pop[
								'sig_w_par'] ,1)
							self.prnt_htm( 'km/s' )

					else :
	
						if ( self.core.opt['res_w'] ) :

							self.prnt_brk( )
							self.prnt_tab( 2 )
							self.prnt_htm(
							         lab_w + ' = ' )
							self.prnt_dcm(
							           pop['w'], 1 )
							if (
							self.core.opt['res_u']
							                     ) :
								self.prnt_htm(
								'&nbsp;&plusmn;\
								 &nbsp;'       )
								self.prnt_dcm(
								pop[
							        'sig_w'],1     )
							self.prnt_htm( 'km/s'  ) 

				# Print the population's temperature(s).

				if ( ( self.core.opt['res_dt'] ) and
				     ( self.core.opt['res_w'] )     ) :

					self.prnt_brk( )
					self.prnt_tab( 2 )
					self.prnt_htm( lab_t + ' = ' )
					self.prnt_dcm( pop['t'], 1, 'kK' )

					if ( pop['aniso'] ) :
	
						self.prnt_brk( )
					 	self.prnt_tab( 3 )
					 	self.prnt_htm(
						             lab_t_per + ' = ' )
					 	self.prnt_dcm(
						         pop['t_per'], 1, 'kK' )
					 	self.prnt_brk( )
					 	self.prnt_tab( 3 )
					 	self.prnt_htm(
						             lab_t_par + ' = ' )
					 	self.prnt_dcm(
						         pop['t_par'], 1, 'kK' )

				if ( self.core.opt['res_r'] ) :

					self.prnt_brk( )
					self.prnt_tab( 2 )
					self.prnt_htm( lab_r + ' = ' )
					self.prnt_dcm( pop['r'], 2 )

				if ( self.core.opt['res_b'] ) :

					self.prnt_brk( )
					self.prnt_tab( 2 )
					self.prnt_htm( lab_b + ' = ' )
					self.prnt_dcm( pop['beta_par'],
					                             4 )

					# Clear the first population indicator.

				first_pop = False

			# Print the Skewness and Excess Kurtosis value

			if  ( len( self.core.nln_res_plas.lst_pop( spc )
			                                               ) > 1 ) :
				if ( ( self.core.opt['res_s'] == True ) or
				     ( self.core.opt['res_k'] == True )  )  :

					self.prnt_brk( )
					self.prnt_brk( )
	       				self.prnt_tab( 1 )
	  				self.prnt_htm(
					        '<u>Higher-Order Moments:</u>' )

				if ( self.core.opt['res_s'] == True ) :
	
	       				self.prnt_brk( )
	       				self.prnt_tab( 2 )
	       				self.prnt_htm( lab_s + ' = ' )
	       				self.prnt_dcm( spc['s'], 3 )

				if ( self.core.opt['res_k'] == True ) :

					self.prnt_brk( )
       					self.prnt_tab( 2 )
       					self.prnt_htm( lab_k + ' = ' )
       					self.prnt_dcm( spc['k'] - 3, 3 )

			# Clear the first-species indicator.

			first_spc = False

		# Scroll to the top of the text area.

		self.moveCursor( QTextCursor.Start )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Reset the text area.

		self.clear( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_opt" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_opt( self ) :

		# Regenerate the text in the text area.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mfi" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mfi( self ) :

		# Regenerate the text in the text area.

		self.make_txt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_res" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_res( self ) :

		# Regenerate the text in the text area.

		self.make_txt( )
