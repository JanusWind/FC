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

from janus_dialog_opt import dialog_opt
#from janus_widget_nln_fls import widget_opt_fls

################################################################################
## DEFINE THE "widget_opt" CLASS TO CUSTOMIZE "QTabWidget" FOR OPTIONS MENU.
################################################################################

class widget_opt( QTabWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QTabWidget".

		super( widget_nln, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Intialize this widget's sub-widgets and add them as tabs.

		self.wdg_par = dialog_opt( self.core )
#		self.wdg_fls = widget_opt_fls( self.core )

		self.addTab( self.wdg_par, 'Display Options' )
#		self.addTab( self.wdg_fls, 'Files Options'   )
