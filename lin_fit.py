from scipy import stats

def fitlin( b1, v1, sigma ) :

	def linfunc( b1, m1, c1 ) :

		return m1 * b1 + c1

	sigma = np.ones(len(b1))
#	sigma[ -1]= 1.E-5
	popt1, pcov1 = curve_fit( linfunc, b1, v1, sigma=sigma )
	m1, c1 = popt1

	fitfunc = lambda b1: m1 * b1 + c1

	return { "slope"   : m1,
	         "offset"  : c1,
	         "fitfunc" : fitfunc,
	         "rawres"  : ( popt1,pcov1 ) }

dat1_s_fv_p_c = np.array( [ x if x > 0 else float('nan') for x in dat1_s_fv_p_c ] )

dat1_s_sig_fv_p_c = np.array( dat1_s_sig_fv_p_c )
dat1_s_db_rng_avg = np.array( dat1_s_db_rng_avg )

x   = dat1_s_db_rng_avg[ np.logical_not( np.isnan( dat1_s_fv_p_c ) ) ]
y   = dat1_s_fv_p_c[ np.logical_not( np.isnan( dat1_s_fv_p_c ) ) ]
sig = dat1_s_sig_fv_p_c[ np.logical_not( np.isnan( dat1_s_fv_p_c ) ) ]

fit = stats.linregress( x, y )

#dat_fit_x = fitlin( x, y, sig )

m = fit.slope
c = fit.intercept
r = fit.rvalue
sigma = fit.stderr

#m_x = dat_fit_x['slope']
#c_x = dat_fit_x['offset']

ind = linspace( 0., max( x ), len( x ) )

#fit_x = dat_fit_x['fitfunc'](indx)

y_fit = [ m*i for i in ind ]

plt.figure()

#plt.scatter( dat1_s_db_rng_avg[0], dat1_s_fv_p_c[0], marker='*', color='b' )
plt.plot( ind, y_fit, marker='*', color='m' )

plt.errorbar( x, y, sig, marker='^', color='r', fmt='o', ecolor='g',
                                                           label='Proton Core' )

plt.text( 0.03, 0, 'Slope = %s\n intercept = %s' %( round( m, 4 ), round( c, 4 ) ) )
plt.xlabel( r'$\Delta{B}/|\vec B|$' )
plt.ylabel( r'$V_f/V_A$' )

plt.show()
