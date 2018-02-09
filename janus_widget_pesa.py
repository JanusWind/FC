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

from numpy import amax, amin, array, ceil, floor, log10, sqrt, tile, where

# Load the necessary threading modules.

from threading import Thread
from janus_thread import n_thread, thread_chng_mom_sel, thread_chng_nln_sel


################################################################################
## DEFINE THE "widget_fc_cup" CLASS TO CUSTOMIZE "QWidget" FOR Wind/FC PLOTS.
################################################################################

class widget_fc_cup( QWidget ) :

	#-----------------------------------------------------------------------
	# DEFINE THE INITIALIZATION FUNCTION.
	#-----------------------------------------------------------------------

	def __init__( self, core,
	              n_plt_x=None, n_plt_y=None, n_plt=None ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_pesa, self ).__init__( )

		# Initialize the counter of repaint events for this widget as
		# well as a maximum value for this counter.

		# Note.  For some reason, adjusting the individual plots to have
		#        uniform sizes is difficult to achieve before the widget
		#        is rendered.  Thus, once a paint event occurs, the
		#        "self.paintEvent( )" function picks it up and makes a
		#        call to "self.ajst_grd( )".  This counter and its
		#        maximum value are used ensure that "self.paintEvent( )"
		#        makes such a call only in response to the intial few
		#        painting (so as to prevent an infinite loop).

		# Note.  The first paint seems to be a "dummy" of some sort.
		#        Whatever the case, "self.n_paint_max = 1" seems to
		#        generally be insufficient.

		self.n_painted     = 0
		self.n_painted_max = 3

		self.core = core

		# Prepare to respond to signals received from the Janus core.

		self.connect( self.core, SIGNAL('janus_rset'), self.resp_rset )
		self.connect( self.core, SIGNAL('janus_chng_spc'),
		                                            self.resp_chng_spc )
		self.connect( self.core, SIGNAL('janus_chng_mom_sel_bin'),
		                                    self.resp_chng_mom_sel_bin )
		self.connect( self.core, SIGNAL('janus_chng_mom_sel_dir'),
		                                    self.resp_chng_mom_sel_dir )
		self.connect( self.core, SIGNAL('janus_chng_mom_sel_all'),
		                                    self.resp_chng_mom_sel_all )
		self.connect( self.core, SIGNAL('janus_chng_mom_res'),
		                                        self.resp_chng_mom_res )
		self.connect( self.core, SIGNAL('janus_chng_nln_gss'),
		                                        self.resp_chng_nln_gss )
		self.connect( self.core, SIGNAL('janus_chng_nln_sel_bin'),
		                                    self.resp_chng_nln_sel_bin )
		self.connect( self.core, SIGNAL('janus_chng_nln_sel_all'),
		                                    self.resp_chng_nln_sel_all )
		self.connect( self.core, SIGNAL('janus_chng_nln_res'),
		                                        self.resp_chng_nln_res )
		self.connect( self.core, SIGNAL('janus_chng_dsp'),
		                                            self.resp_chng_dsp )
		#TODO add more signals

		# Assign (if not done so already) and store the shape of the
		# plot-grid array.

		self.n_plt_x = 5 if ( n_plt_x is None ) else n_plt_x
		self.n_plt_y = 5 if ( n_plt_y is None ) else n_plt_y

		if ( n_plt is None ) :
			self.n_plt = self.n_plt_x * self.n_plt_y

		# Initizalize the pens, brushes, and fonts used by this widget.

		self.pen_plt   = mkPen( color='k' )
		self.pen_hst   = mkPen( color='k' )
		self.pen_pnt_c = mkPen( color='k' )
		self.pen_pnt_y = mkPen( color='k' )
		self.pen_pnt_r = mkPen( color='k' )
		self.pen_crv_b = mkPen( color='b' )
		self.pen_crv_g = mkPen( color='g' )

		self.bsh_pnt_c = mkBrush( color='c' )
		self.bsh_pnt_y = mkBrush( color='y' )
		self.bsh_pnt_r = mkBrush( color='r' )

		self.fnt = self.core.app.font( )

		# Set the maximum number of velocity channels and the maximum
		# number of ion species.

		self.n_k   = 14
		self.n_ion = self.core.nln_n_pop

		# Initialize the widget and it's plot's.

		self.init_plt( )

		# Populate the plots with the histograms (and labels), the
		# selection points, and the fit curves.

		self.make_hst( )
		self.make_pnt( )
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

		self.txt_axs_x = 'Projected Proton Inflow Velocity [km/s]'
		self.txt_axs_y = 'Phase-space Density [unit?]'

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

		self.hst = tile( None, [ self.n_plt_y, self.n_plt_x ] )
		self.lbl = tile( None, [ self.n_plt_y, self.n_plt_x ] )

		self.crv     = tile( None, [ self.n_plt_y, self.n_plt_x ] )
		self.crv_ion = tile( None, [ self.n_plt_y, self.n_plt_x,
		                             self.n_ion                  ] )

		self.pnt = tile( None, [ self.n_plt_y, self.n_plt_x, 
		                         self.n_k                    ] )

		# Initialize the scale-type for each axis, then generate the
		# (default) axis-limits and adjusted axis-limits.

		self.log_x = False
		self.log_y = True

		self.make_lim( )

		# Create, store, and add to the grid the individual axes: first
		# the horizontal and then the vertical.

		for i in range( self.n_plt_x ) :

			self.axs_x[i] = AxisItem( 'bottom', maxTickLength=5 )
			self.axs_x[i].setLogMode( self.log_x )
			self.axs_x[i].setRange( self.alm_x[0], self.alm_x[1] )
			self.axs_x[i].setTickFont( self.fnt )

			if ( self.core.app.res_lo ) :
				self.axs_x[i].setHeight( 10 )
			else :
				self.axs_x[i].setHeight( 20 )

			self.grd.addItem( self.axs_x[i], self.n_plt_y, i + 2 )

		for j in range( self.n_plt_y ) :

			self.axs_y[j] = AxisItem( 'left', maxTickLength=5 )
			self.axs_y[j].setLogMode( self.log_y )
			self.axs_y[j].setRange( self.alm_y[0], self.alm_y[1] )
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

				self.plt[j,i].setRange( xRange=self.alm_x,
				                        yRange=self.alm_y,
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

	def make_lim( self ) :

		# If no spectrum has been loaded, use the default limits;
		# otherwise, use the spectral data to compute axis limits.

		if ( self.core.pl_spec is None ) :

			self.lim_x = [ 250. , 750. ]
			self.lim_y = [   0.7,  70. ]

		else :

			self.lim_x = [self.core.pl_spec['vel_strt'][0 ],
			              self.core.pl_spec['vel_stop'][-1]]
			#TODO
			arr_curr_flat = self.core.fc_spec['curr_flat']

			self.lim_y = [ min(arr_curr_flat), max(arr_curr_flat)  ]
			#/TODO
			if ( self.log_y ) :
				self.lim_y[1] = self.lim_y[1] ** 1.1
			else :
				self.lim_y[1] += 0.1 * ( self.lim_y[1] -
				                         self.lim_y[0]   )

		# Compute the "adjusted limits" for each axis.

		if ( self.log_x ) :
			self.alm_x = [ log10( x ) for x in self.lim_x ]
		else :
			self.alm_x = self.lim_x

		if ( self.log_y ) :
			self.alm_y = [ log10( y ) for y in self.lim_y ]
		else :
			self.alm_y = self.lim_y

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CREATING THE PLOTS' HISTOGRAMS (AND LABELS).
	#-----------------------------------------------------------------------

	def make_hst( self, curr_min=0.69 ) :

		# If no spectrum has been loaded, clear any existing histograms
		# and abort.

		if ( self.core.fc_spec is None ) :

			self.rset_hst( )

			return

		# Use the spectral data to compute new axis-limits.

		self.make_lim( )

		# Generate a step function for each look direction associated
		# with this widget.

		self.stp = array( [ step(  self.core.fc_spec['vel_cen'][self.c] ,
					   self.core.fc_spec['vel_del'][self.c] ,
					   self.core.fc_spec['curr'][self.c][d])
						for d in range(self.core.fc_spec['n_dir']) ])

		stp_pnt = array( [ array( self.stp[d]\
		                              .calc_pnt( lev_min=curr_min ) )
		                for d in range( self.core.fc_spec['n_dir'] ) ] )

		self.stp_x = stp_pnt[:,0,:]
		self.stp_y = stp_pnt[:,1,:]

		self.asp_x = log10( self.stp_x ) if ( self.log_x ) else \
		                    self.stp_x
		self.asp_y = log10( self.stp_y ) if ( self.log_y ) else \
		                    self.stp_y

		# Adjust the individual axes to the new limits.

		for i in range( self.n_plt_x ) :
			self.axs_x[i].setRange( self.alm_x[0], self.alm_x[1] )

		for j in range( self.n_plt_y ) :
			self.axs_y[j].setRange( self.alm_y[0], self.alm_y[1] )

		# For each plot in the grid, adjust its limits, add a histogram,
		# and add a direction label.

		for d in range( min( self.core.fc_spec['n_dir'], self.n_plt ) ) :

			# Determine the location of this plot within the grid
			# layout.

			j = self.calc_ind_j( d )
			i = self.calc_ind_i( d )

			# If this plot does not exist, move onto the next one.

			if ( self.plt[j,i] is None ) :
				continue

			# If a histogram already exists for this plot, remove
			# and delete it.

			if ( self.hst[j,i] is not None ) :
				self.plt[j,i].removeItem( self.hst[j,i] )
				self.hst[j,i] = None

			# Clear this plot's label of text.

			self.lbl[j,i].setText( '' )

			# Adjust this plot's limits and then move it's label in
			# response.

			self.plt[j,i].setRange( xRange=self.alm_x,
			                        yRange=self.alm_y,
			                        padding=0.         )

			self.lbl[j,i].setPos( self.alm_x[1], self.alm_y[1] )

			# Update this plot's label with appropriate text
			# indicating the pointing direction.

			r_alt = round( self.core.fc_spec['elev'][self.c] )
			r_dir = round( self.core.fc_spec['azim'][self.c][d])

			txt = ( u'({0:+.0f}\N{DEGREE SIGN}, ' + 
			        u'{1:+.0f}\N{DEGREE SIGN})'     ).format(
			                                          r_alt, r_dir )

			self.lbl[j,i].setText( txt, color=(0,0,0) )
			#self.lbl[j,i].setFont( self.fnt           )

			# Generate the histogram for the data from this look
			# direction and display it in the plot.

			self.hst[j,i] = PlotDataItem( self.asp_x[d,:],
			                              self.asp_y[d,:],
			                              pen=self.pen_hst )

			self.plt[j,i].addItem( self.hst[j,i] )
