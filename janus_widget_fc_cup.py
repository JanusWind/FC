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

	def __init__( self, core, cup,
	              n_plt_x=None, n_plt_y=None, n_plt=None ) :

		# Inherit all attributes of an instance of "QWidget".

		super( widget_fc_cup, self ).__init__( )

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

		# Store the Janus core and the cup number.

		# Note.  The cups are traditionally numbered "1" and "2", but,
		#        in this class, they are identified by the altitude
		#        index "t" which takes the values "0" and "1",
		#        respectively.

		self.core = core

		self.c = None
		self.c = 0 if ( cup == 1 ) else self.c
		self.c = 1 if ( cup == 2 ) else self.c

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

		# Assign (if not done so already) and store the shape of the
		# plot-grid array.

		self.n_plt_x = 4 if ( n_plt_x is None ) else n_plt_x
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

		self.n_k   = 31
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
		self.txt_axs_y = 'Current [pA]'

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

		if ( self.core.fc_spec is None ) :

			self.lim_x = [ 250. , 750. ]
			self.lim_y = [   0.7,  70. ]

		else :

			self.lim_x = [self.core.fc_spec['vel_strt'][self.c][0 ],
			              self.core.fc_spec['vel_stop'][self.c][-1]]

			arr_curr_flat = self.core.fc_spec['curr_flat']

			self.lim_y = [ min(arr_curr_flat), max(arr_curr_flat)  ]

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

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CREATING THE PLOTS' SELECTION POINTS.
	#-----------------------------------------------------------------------

	def make_pnt( self, curr_min=0.69 ) :

		# Add selection points to each plot.

		if ( self.core.fc_spec is None ) :

			return

		# Add selection points to each plot.

		for d in range( min( self.core.fc_spec['n_dir'], self.n_plt ) ) :

			# Determine the location of this plot within the grid
			# layout.

			j = self.calc_ind_j( d )
			i = self.calc_ind_i( d )

			# If this plot does not exist, move onto the next one.

			if ( self.plt[j,i] is None ) :
				continue

			# Add the selection points to this plot.

			for b in range( self.core.fc_spec['n_bin'] ) :

				sel_bin = False
				sel_dir = True
				sel_alt = None

				if ( ( self.core.dsp == 'mom'          ) and 
				     ( self.core.mom_sel_bin
						           is not None ) and
				     ( self.core.mom_sel_dir
					                   is not None )     ) :

					sel_bin = \
					       self.core.mom_sel_bin[self.c][d][b]
					sel_dir = \
					       self.core.mom_sel_dir[self.c][d]

				elif ( ( self.core.dsp == 'gsl'        ) and 
				       ( self.core.nln_sel is not None )     ) :

					sel_bin = self.core.nln_sel[self.c][d][b]

				elif ( ( self.core.dsp == 'nln'        ) and 
				       ( self.core.nln_res_sel
					                   is not None )     ) :

					sel_bin = \
					       self.core.nln_res_sel[self.c][d][b]

					if ( self.core.nln_sel is None ) :
						sel_alt = None
					else :
						sel_alt = \
						   self.core.nln_sel[self.c][d][b]

				self.chng_pnt( j, i, b, sel_bin,
					       sel_dir=sel_dir,
					       sel_alt=sel_alt   )

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
			d_lst = range( min( self.core.fc_spec['n_dir'],
			               self.n_plt                       ) )

		# If the results of the analysis are missing, abort; otherwise,
		# extract the current values to be plotted.

		if ( self.core.dsp == 'mom' ) :
			curr     = self.core.mom_curr
			curr_ion = None
		elif ( self.core.dsp == 'gsl' ) :
			curr     = self.core.nln_gss_curr_tot
			curr_ion = self.core.nln_gss_curr_ion
		elif ( self.core.dsp == 'nln' ) :
			curr     = self.core.nln_res_curr_tot
			curr_ion = self.core.nln_res_curr_ion
		else :
			curr     = None
			curr_ion = None

		# For each plot in the grid, generate and display a fit curve
		# based on the results of the analysis.

		vel_cen = self.core.fc_spec['vel_cen'][self.c]

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

			if ( self.crv[j,i] is not None ) :
				self.plt[j,i].removeItem( self.crv[j,i] )
				self.crv[j,i] = None

			for n in range( self.n_ion ) :
				if ( self.crv_ion[j,i,n] is not None ) :
					self.plt[j,i].removeItem(
					                   self.crv_ion[j,i,n] )
					self.crv_ion[j,i,n] = None

			# Create and add the curve of the individual
			# contributions to the modeled current to the plot.

			if ( curr_ion is not None ) :

				for n in range( len( curr_ion[self.c][d][0] ) ) :

					# Extract the points for this fit curve.

					x = array( vel_cen )
					y = array( [ curr_ion[self.c][d][b][n]
					      for b in range(
					        self.core.fc_spec['n_bin'] ) ] )

					# Select only those points for which
					# the fit current is strictly positive.

					tk = where( y > 0. )[0]

					# If fewer than two curve points were
					# selected, skip plotting this curve.

					if ( len( tk ) < 2 ) :
						continue

					# Generate the adjusted points for this
					# curve.

					if ( self.log_x ) :
						ax = log10( x[tk] )
					else :
						ax = x[tk]

					if ( self.log_y ) :
						ay = log10( y[tk] )
					else :
						ay = y[tk]

					# Create, store, and add to the plot
					# this fit curve.

					self.crv_ion[j,i,n] = PlotDataItem(
					            ax, ay, pen=self.pen_crv_g )

					self.plt[j,i].addItem(
					                   self.crv_ion[j,i,n] )

			# Create, store, and add to the plot a curve for the
			# total fit current.

			if ( curr is not None ) :

				# Extract the points of the fit curve.

				x = [ self.core.fc_spec.arr[self.c][0][b][
				                                    'vel_cen']
				      for b in range(
				                  self.core.fc_spec['n_bin'] ) ]

				y = curr[self.c][d]

				x = array( x )
				y = array( y )

				# Select only those points for which the fit
				# current is strictly positive.

				valid = [ yy > 0. for yy in y ]

				n_a = sum( valid )

				ax = [ xx for xx, vv in zip( x, valid ) if vv ]
				ay = [ yy for yy, vv in zip( y, valid ) if vv ]

				# If at least two points were selected, proceed
				# with plotting.

				if ( n_a >= 2 ) :

					# If needed, convert to a logarithmic
					# scale.

					if ( self.log_x ) :
						ax = [ log10( xx )
						       for xx in ax ]
					if ( self.log_y ) :
						ay = [ log10( yy )
					               for yy in ay ]

					# Create, store, and add to the plot
					# this fit curve.

					self.crv[j,i] = PlotDataItem(
					            ax, ay, pen=self.pen_crv_b )

					self.plt[j,i].addItem( self.crv[j,i] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR CHANGING THE VISIBILITY OF A DATUM'S POINTS.
	#-----------------------------------------------------------------------

	def chng_pnt( self, j, i, b, sel_bin,
	              sel_dir=True, sel_alt=None ) :

		# If this point already exists, remove it from its plot and
		# delete it.

		if ( self.pnt[j,i,b] is not None ) :
			self.plt[j,i].removeItem( self.pnt[j,i,b] )
			self.pnt[j,i,b] = None

		# If the user gave no alternative selection state for this
		# datum, use the primary state for the secondary state.

		sel_alt = sel_bin if ( sel_alt is None ) else sel_alt

		# If this point was not selected (based on both its primary and
		# secondary states), return (since there's nothing more to be
		# done).

		if ( ( not sel_bin ) and ( not sel_alt ) ) :
			return

		# Determine the "d" index corresponding to this look direction.

		d = self.calc_ind_d( j, i )

		# Computed the adjusted point location in the "ViewBox".

		if ( self.log_x ) :
			ax = log10( self.core.fc_spec['vel_cen'][self.c][b] )
		else :
			ax = self.core.fc_spec['vel_cen'][self.c][b]
		if ( self.log_y ) :
			ay = log10( self.core.fc_spec['curr'][self.c][d][b] )
		else :
			ay = self.core.fc_spec['curr'][self.c][d][b]

		# Select the color for the point (i.e., the brush and pen used
		# to render it) based on whether or not this datum's look
		# direction has been selected and whether or not the primary and
		# secondary selection states match.

		if ( sel_dir ) :
			if ( sel_bin == sel_alt ) :
				pen   = self.pen_pnt_c
				brush = self.bsh_pnt_c
			else :
				pen   = self.pen_pnt_y
				brush = self.bsh_pnt_y
		else :
			pen   = self.pen_pnt_r
			brush = self.bsh_pnt_r

		# Select the symbol based on the values of the primary and
		# secondary selection states.

		# Note.  At this point in the code, at least one of these two
		#        states must be "True" since this -- when both states
		#        are "False", this function returns before it reaches
		#        this point.

		if ( sel_bin ) :
			if ( sel_alt ) :
				symbol = 's'
			else :
				symbol = 'o'
		else :
			symbol = 't'

		# Create, store, and add this selection point to the plot.

		if ( self.core.app.res_lo ) :
			size = 3
		else :
			size = 6

		self.pnt[j,i,b] = PlotDataItem( [ax], [ay],
		                                symbol=symbol,
		                                symbolSize=size,
		                                symbolPen=pen,
		                                symbolBrush=brush )

		self.plt[j,i].addItem( self.pnt[j,i,b] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESETTING THE PLOTS' HISTOGRAMS (AND LABELS).
	#-----------------------------------------------------------------------

	def rset_hst( self, rset_lbl=False ) :

		# For each plot that exists in the grid, remove and delete it's
		# histogram.  Likewise, if requested, empty it's label (but
		# still leave the label itself intact).

		for j in range( self.n_plt_y ) :

			for i in range( self.n_plt_x ) :

				# If the plot does not exist, move onto the the
				# next one.

				if ( self.plt[j,i] is None ) :
					continue

				# If a histogram exists for this plot, remove
				# and delete it.

				if ( self.hst[j,i] is not None ) :
					self.plt[j,i].removeItem(
					                         self.hst[j,i] )
					self.hst[j,i] = None

				# If requested, reset this plot's label text to
				# the empty string.

				if ( rset_lbl ) :
					self.lbl[j,i].setText( '',
					                       color=(0,0,0) )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESETTING THE PLOTS' SELECTION POINTS.
	#-----------------------------------------------------------------------

	def rset_pnt( self ) :

		# For each plot that exists in the grid, hide and remove its
		# selection points.

		for j in range( self.n_plt_y ) :

			for i in range( self.n_plt_x ) :

				# If the plot does not exist, move onto the the
				# next grid element.

				if ( self.plt[j,i] is None ) :
					continue

				# Remove and then delete each of this plot's
				# selection points.

				for b in range( self.n_k ) :
					if ( self.pnt[j,i,b] is not None ) :
						self.plt[j,i].removeItem(
						               self.pnt[j,i,b] )
						self.pnt[j,i,b] = None

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESETTING THE PLOTS' FIT CURVES.
	#-----------------------------------------------------------------------

	def rset_crv( self ) :

		# For each plot that exists in the grid, remove and delete its
		# fit curves.

		for j in range( self.n_plt_y ) :

			for i in range( self.n_plt_x ) :

				# If the plot does not exist, move onto the the
				# next one.

				if ( self.plt[j,i] is None ) :
					continue

				# Remove and delete this plot's fit curve.

				if ( self.crv[j,i] is not None ) :
					self.plt[j,i].removeItem(
					                         self.crv[j,i] )
					self.crv[j,i] = None

				for n in range( self.n_ion ) :

					if ( self.crv_ion[j,i,n] is not None ) :
						self.plt[j,i].removeItem(
						           self.crv_ion[j,i,n] )
						self.crv_ion[j,i,n] = None

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
	# DEFINE THE FUNCTION FOR RESPONDING TO A USER-INITIATED EVENT.
	#-----------------------------------------------------------------------

	def user_event( self, event, plt_ji ) :

		# If a "thread_*" computation thread is already running, abort.

		if ( n_thread( ) != 0 ) :

			return

		# If no spectrum has been loaded, abort.

		if ( ( self.core.fc_spec is None       ) or
		     ( self.core.fc_spec['n_bin'] <= 0 )    ) :

			return

		# Extract the location of the plot in the grid.

		tk = where( self.plt == plt_ji )

		j = tk[0][0]
		i = tk[1][0]

		# Determine the look direction corresponding to this plot.

		d = self.calc_ind_d( j, i )

		# Extract the data shown in this plot.  Convert them first to
		# their adjusted values, and then to their equivalent pixel
		# positions in the "ViewBox".

		dat_x = self.core.fc_spec['vel_cen'][self.c]
		dat_y = self.core.fc_spec['curr'][self.c][d]

		dat_ax = log10( dat_x ) if ( self.log_x ) else dat_x
		dat_ay = log10( dat_y ) if ( self.log_y ) else dat_y

		dat_a = tile( None, self.core.fc_spec['n_bin'] )

		for b in range( self.core.fc_spec['n_bin'] ) :
			dat_a[b] = QPointF( dat_ax[b], dat_ay[b] )

		dat_p = array( [
		             self.plt[j,i].mapFromView( da ) for da in dat_a ] )

		dat_px = array( [ dp.x( ) for dp in dat_p ] )
		dat_py = array( [ dp.y( ) for dp in dat_p ] )

		# Extract the pixel position of the mouse-click event.

		evt_p = event.pos( )

		evt_px = evt_p.x( )
		evt_py = evt_p.y( )

		# Compute the distance (in pixels) of each datum's location from
		# the location of the mouse-click event.  Then, identify the
		# closest datum.

		dst = sqrt( ( dat_px - evt_px )**2 + ( dat_py - evt_py )**2 )

		b = where( dst == amin( dst ) )[0][0]

		# If the distance between the nearest datum and the mouse click
		# is within a set tolerance, invert the selection of that datum
		# (i.e., de-select it if its already selected or select it if it
		# isn't selected).

		tol = 25.

		if ( dst[b] <= tol ) :

			if ( self.core.dsp == 'mom' ) :

				Thread( target=thread_chng_mom_sel,
				        args=( self.core,
				               self.c, d, b ) ).start()

			elif ( self.core.dsp == 'gsl' ) :

				Thread( target=thread_chng_nln_sel,
				        args=( self.core,
				               self.c, d, b ) ).start()

			elif ( self.core.dsp == 'nln' ) :

				Thread( target=thread_chng_nln_sel,
				        args=( self.core,
				               self.c, d, b ) ).start()

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "rset" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_rset( self ) :

		# Clear the plots of all their elements.

		self.rset_crv( )
		self.rset_pnt( )
		self.rset_hst( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_spc" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_spc( self ) :

		# Clear the plots of all their elements and regenerate them.

		self.rset_crv( )
		self.rset_pnt( )
		self.rset_hst( )

		self.make_hst( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mom_sel_bin" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mom_sel_bin( self, c=None, d=None, b=None ) :

		# If one of the keyword arguments is missing, invalid, or
		# non-applicable to this widget, abort.

		if ( ( c is None ) or ( d is None ) or ( b is None ) ) :
			return

		try :
			c = int( c )
			d = int( d )
			b = int( b )
		except :
			return

		if ( c != self.c ) :
			return

		if ( ( d < 0 ) or ( d >= self.core.fc_spec['n_dir'] ) ) :
			return

		if ( ( b < 0 ) or ( b >= self.core.fc_spec['n_bin'] ) ) :
			return

		# If the results of the moments analysis are being displayed,
		# update the color and visibility of the corresponding plot
		# points based on a possible change in the selection status of
		# that datum or its pointing window.

		if ( self.core.dsp == 'mom' ) :

			# Determine the location of this plot within the grid
			# layout.

			j = self.calc_ind_j( d )
			i = self.calc_ind_i( d )

			# Update the color and visibility of the plot point
			# corresponding to the specified datum.

			self.chng_pnt( j, i, b,
			               self.core.mom_sel_bin[c][d][b],
			               sel_dir=self.core.mom_sel_dir[c][ d] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mom_sel_dir" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mom_sel_dir( self, c=None, d=None ) :

		# If one of the keyword arguments is missing, invalid, or
		# non-applicable to this widget, abort.

		if ( ( c is None ) or ( d is None ) ) :
			return

		try :
			c = int( c )
			d = int( d )
		except :
			return

		if ( c != self.c ) :
			return

		if ( ( d < 0 ) or ( d >= self.core.fc_spec['n_dir'] ) ) :
			return

		# If the results of the moments analysis are being displayed and
		# the "t" value passed to this function corresponds to that for
		# this widget, update the color and visibility of the
		# corresponding plot points based on a possible change in the
		# selection status of that pointing window.

		if ( self.core.dsp == 'mom' ) :

			# Determine the location of this plot within the grid
			# layout.

			j = self.calc_ind_j( d )
			i = self.calc_ind_i( d )

			# Update the color and visibility of the plot points
			# corresponding to each of this look direction's data.

			for b in range( self.core.fc_spec['n_bin'] ) :
				self.chng_pnt( j, i, b,
				            self.core.mom_sel_bin[c][d][b],
				            sel_dir=self.core.mom_sel_dir[c][d] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mom_sel_all" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mom_sel_all( self ) :

		# If the results of the moments analysis are being displayed,
		# reset any existing selection points and create new ones.

		if ( self.core.dsp == 'mom' ) :

			self.make_pnt( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_mom_res" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_mom_res( self ) :

		# If the results of the moments analysis are being displayed,
		# reset any existing fit curves and make new ones.

		if ( self.core.dsp == 'mom' ) :

			self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_gss" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_gss( self ) :

		# If the initial guess for the non-linear analysis is being
		# displayed, reset any existing fit curves and make new ones.

		if ( self.core.dsp == 'gsl' ) :

			self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_sel_bin" SIGNAL.
        #-----------------------------------------------------------------------

	def resp_chng_nln_sel_bin( self, c=None, d=None, b=None ) :

		# If one of the keyword arguments is missing, invalid, or
		# non-applicable to this widget, abort.

		if ( ( c is None ) or ( d is None ) or ( b is None ) ) :
			return

		try :
			c = int( c )
			d = int( d )
			b = int( b )
		except :
			return

		if ( c != self.c ) :
			return

		if ( ( d < 0 ) or ( d >= self.core.fc_spec['n_dir'] ) ) :
			return

		if ( ( b < 0 ) or ( b >= self.core.fc_spec['n_bin'] ) ) :
			return

		# Determine the location of this plot within the grid layout.

		j = self.calc_ind_j( d )
		i = self.calc_ind_i( d )

		# If the point selection for the non-linear analysis is being
		# displayed, update the color and visibility of the plot point
		# corresponding to the datum "[c,d,b]" based on a possible
		# change in the selection status of that datum.

		if ( self.core.dsp == 'gsl' ) :

			self.chng_pnt( j, i, b,
			               self.core.nln_sel[self.c][d][b] )

			self.make_crv( )

		elif ( self.core.dsp == 'nln' ) :

			if ( self.core.nln_res_sel is None ) :
				self.chng_pnt( j, i, b,
				              False,
				              sel_alt=self.core.nln_sel[self.c][d][b] )			
			else :
				self.chng_pnt( j, i, b,
				              self.core.nln_res_sel[self.c][d][b],
				              sel_alt=self.core.nln_sel[self.c][d][b] )

			self.make_crv( d_lst=[d] )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_sel_all" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_sel_all( self ) :

		# If the point selection for the non-linear analysis is being
		# displayed, reset any existing selection points and create new
		# ones.

		if ( ( self.core.dsp == 'gsl' ) or
		     ( self.core.dsp == 'nln' )    ) :

			self.make_pnt( )
			self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_nln_res" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_nln_res( self ) :

		# If the results of the non-linear analysis are being displayed,
		# reset any existing fit curves and make new ones.

		if ( self.core.dsp == 'nln' ) :

			self.make_pnt( )
			self.make_crv( )

	#-----------------------------------------------------------------------
	# DEFINE THE FUNCTION FOR RESPONDING TO THE "chng_dsp" SIGNAL.
	#-----------------------------------------------------------------------

	def resp_chng_dsp( self ) :

		# Reset the selection points and fit curves.

		self.make_pnt( )
		self.make_crv( )
