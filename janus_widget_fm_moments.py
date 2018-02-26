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

from PyQt4.QtCore import QPointF, Qt, SIGNAL
from PyQt4.QtGui import QGridLayout, QWidget

# Load the modules necessary for plotting.

from pyqtgraph import AxisItem, GraphicsLayoutWidget, LabelItem, mkBrush, \
                      mkPen, PlotDataItem, TextItem

from janus_event_ViewBox import event_ViewBox

# Load the module necessary handling step functions.

from janus_step import step

# Load the necessary "numpy" array modules and numeric-function modules.

from numpy import amax, amin, array, ceil, floor, log10, sqrt, tile, where, mean, std

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_opt

from scipy.signal      import medfilt


################################################################################
## DEFINE THE "widget_fm_moments" CLASS TO CUSTOMIZE "QWidget" FOR Wind/FC PLOTS.
################################################################################

class widget_fm_moments( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core, cup,
	              n_plt_x=None, n_plt_y=None, n_plt=None ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_fm_moments, self ).__init__( )

		# Initialize the counter of repaint events for this widget as
		# well as a maximum value for this counter.

		# Note.  For some reason, adjusting the individual plots to have
		#        uniform sizes is difficult to achieve before the widget
		#        is rendered.  Thus, once a paint event occurs, the
		#        "self.paintEvent( )" function picks it up and makes a
		#        call to "self.ajst_grd( )".  This counter and its
		#        maximum value are to used ensure that "self.paintEvent( )"
		#        makes such a call only in response to the intial few
		#        painting (so as to prevent an infinite loop).

		# Note.  The first paint seems to be a "dummy" of some sort.
		#        Whatever the case, "self.n_paint_max = 1" seems to
		#        generally be insufficient.

		self.n_painted     = 0
		self.n_painted_max = 3

		# Store the Janus core.

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_mfi'),
		                                            self.resp_chng_mfi )
		self.connect( self.core, SIGNAL('janus_chng_opt'),
		                                            self.resp_chng_opt )
		self.connect( self.core, SIGNAL('janus_rstr_opt'),
		                                            self.resp_rstr_opt )

		# Assign (if not done so already) and store the shape of the
		# plot-grid array.

		self.n_plt_x = 1 if ( n_plt_x is None ) else n_plt_x
		self.n_plt_y = 3 if ( n_plt_y is None ) else n_plt_y

		if ( n_plt is None ) :
			self.n_plt = self.n_plt_x * self.n_plt_y

		# Initizalize the pens, brushes, and fonts used by this widget.

		self.pen_plt   = mkPen( color='k' )
		self.pen_plt   = mkPen( color='k' )
		self.pen_pnt_c = mkPen( color='k' )
		self.pen_pnt_y = mkPen( color='k' )
		self.pen_pnt_r = mkPen( color='k' )
		self.pen_crv_c = mkPen( color='c' )
		self.pen_crv_r = mkPen( color='r' )
		self.pen_crv_g = mkPen( color='g' )
		self.pen_crv_b = mkPen( color='b' )

		self.pen_crv = [self.pen_crv_r, self.pen_crv_g, self.pen_crv_b]    
		self.bsh_pnt_c = mkBrush( color='c' )
		self.bsh_pnt_y = mkBrush( color='y' )
		self.bsh_pnt_r = mkBrush( color='r' )

		self.fnt = self.core.app.font( )

		# Initialize the widget and it's plot's.

		self.init_plt( )

		# Populate the plots with the histograms (and labels), the
		# selection points, and the fit curves.

		self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR INITIALIZING THE WIDGET AND ITS PLOTS.
	#-----------------------------------------------------------------------

	def init_plt( self ) :

		# Initialize the "GraphicsLayoutWidget" for this widget.  This
		# will allow a grid of "GraphicsItem" objects, which will
		# include the plots themselves, the axes, and the axis labels.

		# Note.  The "QGridLayout" object given to this widget as its
		#        layout is essentially a dummy.  I tried to just having
		#        this widget be an extention of "GraphicsLayoutWidget"
		#        (i.e., having it inheret that type), but I couldn't get
		#        it to display anything at all.

		self.setLayout( QGridLayout( ) )

		self.grd = GraphicsLayoutWidget( )
		self.grd.setBackground( 'w' )
		self.layout( ).addWidget( self.grd )

		self.layout().setContentsMargins( 0, 0, 0, 0 )

		# Initialize the text for the x- and y-axis labels.  Then,
		# create the labels themselves and add them to the grid.

		self.txt_axs_x = 'Time [s]'
		self.txt_axs_y = 'Magnetic Field [nT]'

		if ( self.core.app.res_lo ) :
			size =  '8pt'
		else :
			size = '10pt'

		self.lab_axs_x = LabelItem( self.txt_axs_x, angle=0  ,
		                            color='b', size=size       )
		self.lab_axs_y = LabelItem( self.txt_axs_y, angle=270, 
		                            color='b', size=size       )

		self.grd.addItem( self.lab_axs_x, self.n_plt_y + 1, 2,
		                                  1, self.n_plt_x      )
		self.grd.addItem( self.lab_axs_y, 0, 0,
		                                  self.n_plt_y, 1      )

		# Initialize the arrays that will contain the individual axes,
		# plots, and plot elements (i.e., the histograms, fit curves,
		# labels, and selection points).

		self.plt = tile( None, [ self.n_plt_y, self.n_plt_x ] )

		self.axs_x = tile( None, self.n_plt_x )
		self.axs_y = tile( None, self.n_plt_y )

		self.tsp = tile( None, [ self.n_plt_y, self.n_plt_x ] )
		self.lbl = tile( None, [ self.n_plt_y, self.n_plt_x ] )

		self.crv_dat = tile( None, [ self.n_plt_y, self.n_plt_x ] )
		self.crv_fit = tile( None, [ self.n_plt_y, self.n_plt_x ] )

		# Initialize the scale-type for each axis, then generate the
		# (default) axis-limits and adjusted axis-limits.

		self.log_x = False
		self.log_y = False

		self.make_lim( 0 )

		# Create, store, and add to the grid the individual axes: first
		# the horizontal and then the vertical.

		for i in range( self.n_plt_x ) :

			self.axs_x[i] = AxisItem( 'bottom', maxTickLength=5 )
			self.axs_x[i].setLogMode( self.log_x )
			self.axs_x[i].setRange( self.lim_x[0], self.lim_x[1] )
			self.axs_x[i].setTickFont( self.fnt )

			if ( self.core.app.res_lo ) :
				self.axs_x[i].setHeight( 10 )
			else :
				self.axs_x[i].setHeight( 20 )

			self.grd.addItem( self.axs_x[i], self.n_plt_y, i + 2 )

		for j in range( self.n_plt_y ) :

			self.axs_y[j] = AxisItem( 'left', maxTickLength=5 )
			self.axs_y[j].setLogMode( self.log_y )
			self.axs_y[j].setRange( self.lim_y[0], self.lim_y[1] )
			self.axs_y[j].setTickFont( self.fnt )

			if ( self.core.app.res_lo ) :
				self.axs_y[j].setWidth( 32 )
			else :
				self.axs_y[j].setWidth( 40 )

			self.grd.addItem( self.axs_y[j], j, 1 )

		# Create, store, and add to the grid the individual plots.
		# Likewise, create, store, and add to each plot a label.

		for j in range( self.n_plt_y ) :

			for i in range( self.n_plt_x ) :

				# Compute the plot number of this plot.

				d = self.calc_ind_d( j, i )


				# If creating this plot would exceed the
				# specified number of plots, don't create it.

				if ( d >= self.n_plt ) :
					continue

				# Create and store this plot, adjust its limits,
				# and add it to the grid.

				self.plt[j,i] = event_ViewBox( self,
				                          border=self.pen_plt,
				                          enableMouse=False,
				                          enableMenu=False     )

				self.plt[j,i].setRange( xRange=self.lim_x,
				                        yRange=self.lim_y,
				                        padding=0.         )

				self.grd.addItem( self.plt[j,i], j, i + 2 )

				# Create and store an (empty) label and add it
				# to this plot.

				self.lbl[j,i] = TextItem( anchor=(1,0) )

				self.lbl[j,i].setFont( self.fnt )

				self.plt[j,i].addItem( self.lbl[j,i] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR GENERATING AXIS-LIMITS (AND ADJUSTED LIMITS).
	#-----------------------------------------------------------------------

	def make_lim( self, d ) :

		# If no spectrum has been loaded, use the default limits;
		# otherwise, use the spectral data to compute axis limits.

		if ( self.core.fc_spec is None ) :

			self.lim_x = [ 0., 90. ]
			self.lim_y = [ -3., 3. ]

		else :

			data = self.core.mfi_b_vec_t[d]

			self.lim_x = [ min( self.core.mfi_s ),
			               max( self.core.mfi_s ) ]

			self.lim_y = [
			              1.1*mean( data ) - 2*std( data )*2.**0.5,
			              1.1*mean( data ) + 2*std( data )*2.**0.5 ]

#			            -1.1*abs( min( self.core.mfi_b_vec_t[d] ) ),
#			             1.1*max( self.core.mfi_b_vec_t[d] )       ]

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CREATING THE PLOTS' FIT CURVES.
	#-----------------------------------------------------------------------

	def make_crv( self, d_lst=None ) :

		# If no "list" of "p" index-values has been provided by the
		# user, assume that the curves in all plots should be
		# (re-)rendered.

		if ( self.core.fc_spec is None ) :
			return

		if ( d_lst is None ) :
			d_lst = range( self.n_plt )

		text = [ 'X-component', 'Y-component', 'Z-component' ]

		x     = array( self.core.mfi_s )
		y_dat = array( self.core.mfi_b_vec_t )

		if( self.core.mfi_b_vec_fit is None ) :
			return
		else :
			y_fit = array( self.core.mfi_b_vec_fit )

		# Adjust the individual axes to the new limits.

		for l in range( self.n_plt_x ) :
			self.axs_x[l].setRange( self.lim_x[0], self.lim_x[1] )

		for m in range( self.n_plt_y ) :
			self.axs_y[m].setRange( self.lim_y[0], self.lim_y[1] )

		# For each plot in the grid, generate and display a fit curve
		# based on the results of the analysis.

		for d in d_lst :

			# Determine the location of this plot within the grid
			# layout.

			j = self.calc_ind_j( d )
			i = self.calc_ind_i( d )

			# If this plot does not exist, move onto the next grid
			# element.

			if ( self.plt[j,i] is None ) :
				continue

			# If any curves already exist for this plot, remove and
			# delete them.

			if ( self.crv_dat[j,i] is not None ) :
				self.plt[j,i].removeItem( self.crv_dat[j,i] )
				self.crv_dat[j,i] = None

			if ( self.crv_fit[j,i] is not None ) :
				self.plt[j,i].removeItem( self.crv_fit[j,i] )
				self.crv_fit[j,i] = None

			# Clear this plot's label of text.

			self.lbl[j,i].setText( '' )

			# Update this plot's label with appropriate text
			# indicating the pointing direction.

			txt = text[d]

			self.lbl[j,i].setText( txt, color=(0,0,0) )
			self.lbl[j,i].setFont( self.fnt           )

			# Create and add the curve of the individual
			# contributions to the modeled current to the plot.

#			x     = array( self.core.mfi_s )
#			y_dat = array( self.core.mfi_b_vec_t[d] )
#
#			if( self.core.mfi_b_vec_fit == None ) :
#				continue
#			else :
#				y_fit = array( self.core.mfi_b_vec_fit[d] )

			# Adjust this plot's limits and then move it's label in
			# response.
			try :

				self.make_lim( d )

				self.plt[j,i].setRange( xRange=self.lim_x,
				                        yRange=self.lim_y,
				                        padding=0.         )

				self.lbl[j,i].setPos( self.lim_x[1],
				                      self.lim_y[1] )

				self.crv_dat[j,i] = PlotDataItem(
				                 x, medfilt(y_dat[d],
				                 self.core.opt['fit_med_fil'] ),
				                 pen = self.pen_crv_c         )

				self.crv_fit[j,i] = PlotDataItem(
				                 x, medfilt(y_fit[d],
				                 self.core.opt['fit_med_fil'] ),
				                 pen = self.pen_crv[d]        )
				self.plt[j,i].addItem( self.crv_dat[j][i] )
				self.plt[j,i].addItem( self.crv_fit[j][i] )

			except :
				raise TypeError('Median filter length must be odd')
	#			pass


	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESETTING THE PLOTS' FIT CURVES.
	#-----------------------------------------------------------------------

	def rset_crv( self, rset_lbl=False ) :

		# For each plot that exists in the grid, remove and delete its
		# fit curves.

		for j in range( self.n_plt_y ) :

			for i in range( self.n_plt_x ) :

				# If the plot does not exist, move onto the the
				# next one.

				if ( self.plt[j,i] is None ) :
					continue

				# Remove and delete this plot's fit curve.

				if ( self.crv_dat[j,i] is not None ) :
					self.plt[j,i].removeItem(
					                     self.crv_dat[j,i] )
					self.crv_dat[j,i] = None

				if ( self.crv_fit[j,i] is not None ) :
					self.plt[j,i].removeItem(
					                     self.crv_fit[j,i] )
					self.crv_fit[j,i] = None
				# If requested, reset this plot's label text to
				# the empty string.

				if ( rset_lbl ) :
					self.lbl[j,i].setText( '',
					                       color=(0,0,0) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION CALCULATING THE INDEX "i" FROM THE INDEX "d".
	#-----------------------------------------------------------------------

	def calc_ind_i( self, d ) :

		# Return the index "i" (i.e., column in the grid of plots)
		# corresponding to the index "d" (i.e., look direction value)
		# passed by the user.

		return d % self.n_plt_x

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION CALCULATING THE INDEX "j" FROM THE INDEX "d".
	#-----------------------------------------------------------------------

	def calc_ind_j( self, d ) :

		# Return the index "j" (i.e., row in the grid of plots)
		# corresponding to the index "d" (i.e., look direction value)
		# passed by the user.

                return int( floor( d / ( 1. * self.n_plt_x ) ) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION CALCULATING INDEX "d" FROM INDICES "j" AND "i".
	#-----------------------------------------------------------------------

	def calc_ind_d( self, j, i ) :

		# Return the index "d" (i.e., look direction value) 
		# corresponding to the indices "j" and "i" (i.e., location in 
		# the grid of plots) passed by the user.

		return i + ( j * self.n_plt_x )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Clear the plots of all their elements.

		self.rset_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mfi" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mfi( self ) :

		# Clear the plots of all their elements and regenerate them.

		self.rset_crv( )

		self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO A CHANGE OF AN OPTION.
	#-----------------------------------------------------------------------

	def resp_chng_opt( self ) :

		# Regenerate the menu.

		self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO RESTORING DEFAULT OPTIONS.
	#-----------------------------------------------------------------------

	def resp_rstr_opt( self ) :

		# Regenerate the menu.

		self.make_crv( )
