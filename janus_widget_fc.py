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

from janus_widget_fc_cup import widget_fc_cup


################################################################################
## DEFINE THE "widget_fcspec" CLASS TO CUSTOMIZE "QTabWidget" FOR Wind/FC PLOTS.
################################################################################

class widget_fc( QTabWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core,
	              n_plt_x=None, n_plt_y=None ) :

		# Inherit all attributes of an instance of "QTabWidget".

		super( widget_fc, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Create two instances of "widget_fc_cup" (one for each Faraday
		# cup) and add each as a tab.

		self.wdg_fc1 = widget_fc_cup( core=self.core, cup=1,
		                              n_plt_x=n_plt_x, n_plt_y=n_plt_y )
		self.wdg_fc2 = widget_fc_cup( core=self.core, cup=2,
		                              n_plt_x=n_plt_x, n_plt_y=n_plt_y )

		self.addTab( self.wdg_fc1, 'Faraday Cup 1' )
		self.addTab( self.wdg_fc2, 'Faraday Cup 2' )
