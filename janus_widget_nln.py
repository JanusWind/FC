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

# Load the modules necessary for the graphical interface.

from PyQt4.QtGui import QTabWidget

from janus_widget_nln_spc import widget_nln_spc
from janus_widget_nln_pop import widget_nln_pop
from janus_widget_nln_set import widget_nln_set
from janus_widget_nln_gss import widget_nln_gss
from janus_widget_nln_res import widget_nln_res


################################################################################
## DEFINE THE "widget_nln" CLASS TO CUSTOMIZE "QTabWidget" FOR NON-LIN ANALYSIS.
################################################################################

class widget_nln( QTabWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QTabWidget".

		super( widget_nln, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Intialize this widget's sub-widgets and add them as tabs.

		self.wdg_spc = widget_nln_spc( self.core )
		self.wdg_pop = widget_nln_pop( self.core )
		self.wdg_set = widget_nln_set( self.core )
		self.wdg_gss = widget_nln_gss( self.core )
		self.wdg_res = widget_nln_res( self.core )

		self.addTab( self.wdg_spc, 'Non-Linear Ions' )
		self.addTab( self.wdg_pop, 'Populations'     )
		self.addTab( self.wdg_set, 'Settings'        )
		self.addTab( self.wdg_gss, 'Initial Guess'   )
		self.addTab( self.wdg_res, 'Results'         )
