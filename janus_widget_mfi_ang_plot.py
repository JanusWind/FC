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
from PyQt4.QtGui import QFont, QGridLayout, QWidget

# Load the modules necessary for plotting.

from pyqtgraph import mkPen, PlotDataItem, PlotWidget, setConfigOption

# Load the necessary "numpy" array modules and numeric-function modules.

from numpy import amax, amin


################################################################################
## DEFINE THE "widget_mfi_angular_plot" CLASS FOR "QWidget" TO PLOT MFI DATA.
################################################################################

class widget_mfi_ang_plot( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_mfi_ang_plot, self ).__init__( )

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_mfi'),
		                                            self.resp_chng_mfi )

		# Initialize this widget's instance of "PlotWidget", which will
		# contain the plot of MFI magnetic field data.

		# Note.  The "QGridLayout" object given to this widget as its
		#        layout is essentially a dummy.  I could have just had
		#        this class inherit "PlotWidget", but I think that this
		#        gives me a bit more control (and a similar structure
		#        "janus_widget_fc_cup").

		self.setLayout( QGridLayout( ) )

		self.plt = PlotWidget( )
		self.layout( ).addWidget( self.plt )

		self.layout().setContentsMargins( 0, 0, 0, 0 )

		# Extract the individual elements of the "PlotWidget" object
		# (e.g., it's axes) for more convenient access later.

		self.vbx = self.plt.getViewBox( )

		self.axs_x = self.plt.getAxis( 'bottom' )
		self.axs_y = self.plt.getAxis( 'left' )

		self.ptm = self.plt.getPlotItem( )

		# Initialize and store the pens and fonts.

		self.pen_vbx       = mkPen( color='k' )
		self.pen_crv_colat = mkPen( color='#8B008B' )
		self.pen_crv_lon   = mkPen( color='#FFD700' )


		self.fnt = self.core.app.font( )

		# Configure the plot: disable automatic adjustments and
		# adjustments made by the user, change the background and
		# foreground colors, enable grid lines for both axes, label the
		# axes, adjust the tick font size, adjust the "AxisItem" sizes,
		# and add a margin around the entire plot.

		self.plt.disableAutoRange( )
		self.plt.setMouseEnabled( False, False )
		self.plt.setMenuEnabled( False )
		self.plt.hideButtons( )

		self.plt.setBackground( 'w' )
		setConfigOption( 'foreground', 'k')

		#####self.plt.showGrid( True, True )

		labelStyle = {'color':'k'}
		self.axs_x.setLabel( 'Time [s]'           , **labelStyle )
		self.axs_y.setLabel( 'Elev. & Azim. [deg]', **labelStyle )


		self.axs_x.label.setFont( self.fnt )
		self.axs_y.label.setFont( self.fnt )

		self.axs_x.setTickFont( self.fnt )
		self.axs_y.setTickFont( self.fnt )

		self.axs_x.setHeight( 35 )
		self.axs_y.setWidth(  40 )

		self.vbx.border = self.pen_vbx

		self.ptm.setContentsMargins( 5, 5, 5, 5 )

		# Initialize the curves that will be added to this plot.

		self.crv_colat = None
		self.crv_lon   = None

		# Populate this plot and adjust it's settings.

		self.make_plt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR POPULATING THE PLOT.
	#-----------------------------------------------------------------------

	def make_plt( self ) :

		# Reset the plot (i.e., remove all plot elements).

		self.rset_plt( )

		# Establish the ranges of its time and magnetic field values.
		# If the core contains no data or only a single datum,
		# improvise (for the purpose of later establishing axis limits).

		if ( self.core.n_mfi >= 1 ) :

			# Establish the domain of the plot.

			t_min = min( amin( self.core.mfi_s ), 0. )
			t_max = max( amax( self.core.mfi_s ),
			             self.core.fc_spec['dur']      )

			# Establish the range of the plot.  As part of this,
			# ensure that the range satisfies a minimum size and has
			# sufficient padding.

			ang_max = max( [ max( self.core.mfi_b_colat),
			                 max( self.core.mfi_b_lon) ] )
			ang_min = min( [ min( self.core.mfi_b_colat), 
			                 min( self.core.mfi_b_lon) ] )

                        ang_max += 0.1 * ang_max
                        ang_min -= 0.1 * abs( ang_min )

			d_t_0 = t_max - t_min

			d_t = max( 1.5 + d_t_0, 3. )

			t_max = t_min + d_t

		else :

			t_min = 0.001
			t_max = 3.500

			ang_min = -360
			ang_max =  360

		# Set the range of the axis of each plot.

		self.plt.setXRange( t_min, t_max, padding=0.0 )
		self.plt.setYRange( ang_min, ang_max, padding=0.0 )


		# If the core contains no Wind/MFI magnetic field data, return.

		if ( self.core.n_mfi <= 0 ) :
			return

		# Generate and display each curve for the plot.

		self.crv_colat = PlotDataItem( self.core.mfi_s,
		                               self.core.mfi_b_colat,
		                               pen=self.pen_crv_colat )
		self.crv_lon   = PlotDataItem( self.core.mfi_s,
		                               self.core.mfi_b_lon,
		                               pen=self.pen_crv_lon   )

		self.plt.addItem( self.crv_colat )
		self.plt.addItem( self.crv_lon   )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESETTING THIS PLOT (CLEARING ALL ELEMENTS).
	#-----------------------------------------------------------------------

	def rset_plt( self ) :

		# Hide and remove each of this plot's elements.

		if ( self.crv_colat is not None ) :
		     self.plt.removeItem( self.crv_colat )

		if ( self.crv_lon is not None ) :
		     self.plt.removeItem( self.crv_lon   )

		# Permanently delete this plot's elements by setting each of the
		# variables that store them to "None".

		self.crv_colat = None
		self.crv_lon   = None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Reset the plot.

		self.rset_plt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mfi" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mfi( self ) :

		# Regenerate the plot.

		self.make_plt( )
