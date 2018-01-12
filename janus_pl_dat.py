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

from math import sqrt, acos, pi
from numpy import interp, sin, cos, deg2rad, exp, array
from scipy.special import erf

from janus_const import const
from janus_helper import calc_arr_norm, calc_arr_dot


################################################################################
## DEFINE THE CLASS FOR DATUM
################################################################################

class pl_dat( ) :

	def __init__( self,
	              t_strt=None, t_stop=None, phi_cen=None, phi_del=None
	              the_cen=None, the_del=None, volt_cen=None, volt_del=None,
	              psd=None, valid=False ) :

		self._t_strt    = t_strt
		self._t_stop    = t_stop
		self._phi_cen   = phi_cen
		self._phi_del   = phi_del
		self._the_cen   = the_cen
		self._the_del   = the_del
		self._volt_cen  = volt_cen
		self._volt_del  = volt_del
		self._psd       = psd
		self._valid     = valid

		self._t_cen     = ( self._t_strt + ( self._t_stop - self._t_strt )*
	                                     self._phi_cen / 360.           )

		#Note: The voltage sweeps from high to low voltage
		self._volt_strt = ( self._volt_cen + ( self._volt_del / 2. ) )
		self._volt_stop = ( self._volt_cen - ( self._volt_del / 2. ) )

		self._vel_strt  = 1E-3*( sqrt(2.0*const['q_p']*
		                         self['volt_strt']/const['m_p'])    )
		self._vel_stop  = 1E-3*( sqrt((2.0*const['q_p']*
		                         self['volt_stop']/const['m_p']))   )

		self._vel_cen   = 1E-3*( sqrt(2.0*const['q_p']*
		                         self['volt_cen']/const['m_p'])     )

		self._vel_del   = (  self['vel_strt']-self['vel_stop']      )

		self._norm_b_x  = None
		self._norm_b_y  = None
		self._norm_b_z  = None

		self._maglook   = None

