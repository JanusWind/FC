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

from PyQt4.QtGui import QGridLayout, QWidget

# Load the customized push button and one-line text editor.

from janus_widget_ctrl_time   import widget_ctrl_time
from janus_widget_ctrl_dspdyn import widget_ctrl_dspdyn
from janus_widget_ctrl_run    import widget_ctrl_run
from janus_widget_ctrl_info   import widget_ctrl_info
from janus_widget_ctrl_save   import widget_ctrl_save


################################################################################
## DEFINE THE "widget_ctrl" CLASS TO CUSTOMIZE "QWidget" FOR CONTROL BUTTONS.
################################################################################

class widget_ctrl( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_ctrl, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Give this widget a grid layout, "self.grd".

		self.grd = QGridLayout( )

		self.grd.setContentsMargins( 6, 6, 6, 6 )

		self.setLayout( self.grd )

		# Initialize the sub-widgets.

		self.wdg_time   = widget_ctrl_time(   self.core )
		self.wdg_dspdyn = widget_ctrl_dspdyn( self.core )
		self.wdg_run    = widget_ctrl_run(    self.core )

		self.wdg_info   = widget_ctrl_info(   self.core )
		self.wdg_save   = widget_ctrl_save(   self.core )

		# Reduce the contents margins of each sub-widget to zero.

		self.wdg_time.grd.setContentsMargins(   0, 0, 0, 0 )
		self.wdg_dspdyn.grd.setContentsMargins( 0, 0, 0, 0 )
		self.wdg_run.grd.setContentsMargins(    0, 0, 0, 0 )
		self.wdg_save.grd.setContentsMargins(   0, 0, 0, 0 )

		self.wdg_info.setContentsMargins( 0, 0, 0, 0 )

		# Column-by-column, add each sub-widget to this widget's grid.

		self.grd.addWidget( self.wdg_time  , 0, 0, 1, 1 )
		self.grd.addWidget( self.wdg_dspdyn, 1, 0, 1, 1 )
		self.grd.addWidget( self.wdg_run   , 2, 0, 1, 1 )

		self.grd.addWidget( self.wdg_info  , 0, 1, 2, 1 )
		self.grd.addWidget( self.wdg_save  , 2, 1, 1, 1 )

		# Regularize the column widths.

		self.grd.setColumnStretch( 0, 1 )
		self.grd.setColumnStretch( 1, 1 )

		self.wdg_time.setMinimumWidth(   100 )
		self.wdg_dspdyn.setMinimumWidth( 100 )
		self.wdg_run.setMinimumWidth(    100 )
		self.wdg_info.setMinimumWidth(   100 )
		self.wdg_save.setMinimumWidth(   100 )
