################################################################################
## Plotting figures: Data Set 1
################################################################################

plt.figure( )

rcParams['figure.figsize'] = 10, 10

indx = linspace( -0.08, 0.08, 10 )

xx = [0]*len( indx )

plt.errorbar( dat1_db[0:-1], dat1_s_fv[0:-1], yerr=dat1_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind1, y1_fit_dat, color='r' )
plt.plot( ind1, y1_fit_thr, dashes=[1,1], color='m' )
plt.scatter( dat1_db[0:-1], dat1_thr, marker='*', color='r')
plt.plot( indx, xx, color='gray' )
plt.plot( xx, indx, color='gray' )

plt.ylim( [ -0.005, 0.08 ] )
plt.xlim( [ -0.005, 0.08 ] )

plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=24 )
plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=24 )

plt.text( 0.055, 0.0493, 'Fit Slope = ' '%s' r'$\, \pm \,$' '%s'
%( round( m1, 2 ), round( mean( dat1_m ), 2 ) ), fontsize = 20, rotation=33 )

plt.text( 0.052, 0.069, 'Expected Slope = 1', fontsize = 20, rotation=45 )

rc( 'text', usetex=True )

plt.xlabel( r'$\left< \delta B\right >/ B_0$', fontsize = 24 )
plt.ylabel( r'$\delta V/v_A$', fontsize = 24 )

plt.tight_layout()

plt.savefig('fv_delb_fz01'+'.eps', bbox_inches='tight', dpi=200)

#plt.show( )
'''
################################################################################
## Plotting figures: Data Set 2
################################################################################

plt.figure( )

plt.errorbar( dat2_db[0:-1], dat2_s_fv[0:-1], yerr=dat2_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind2, y2_fit_dat, color='r' )
plt.plot( ind2, y2_fit_thr, dashes=[6,2], color='m' )
plt.scatter( dat2_db[0:-1], dat2_thr, marker='*', color='r')

plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)
plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)

plt.text( 0.0, -0.003, 'Slope =' '%s' r'$\pm$' '%s'
%( round( m2, 2 ), round( mean( dat2_m ), 2 ) ), fontsize = 24 )

plt.xlabel( r'$\left< \Delta \vec {B}/|\vec B|\right >$', fontsize = 24 )
plt.ylabel( r'$\delta v/v_A$', fontsize = 24 )

#leg2 = [ 'Linear Fit', 'Theoretical Data', 'Observations' ]
#plt.legend( leg2, loc = 2, fontsize = 24 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error
#bars', fontsize = 24 )
plt.tight_layout()

#plt.savefig('fv_delb_fz11', format='eps', dpi=4000)

#plt.show( )

################################################################################
## Plotting figures: Data Set 3
################################################################################

plt.figure( )

#rc( 'text', usetex=True )

plt.xlabel( r'$\left< \delta B\right >\,/\,B_0$', fontsize = 24 )
plt.ylabel( r'$\delta V\,/\,v_A$', fontsize = 24 )

plt.errorbar( dat3_db[0:-1], dat3_s_fv[0:-1], yerr=dat3_s_sig_fv_p[0:-1],
                                                           fmt='o', ecolor='g' )
plt.plot( ind3, y3_fit_dat, color='r' )
plt.plot( ind3, y3_fit_thr, dashes=[4,2], color='m' )
plt.scatter( dat3_db[0:-1], dat3_thr, marker='*', color='r')

plt.xticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)
plt.yticks([0, 0.015, 0.03, 0.045, 0.06, 0.075], fontsize=20)

plt.text( 0.0, -0.003, r'${\rm Fit}\ {\rm Slope} =' '%s' r'\pm$' '%s$'
%( round( m3, 2 ), round( mean( dat3_m ), 2 ) ), fontsize = 24 )

#plt.text( 0.0, -0.003,
#          r'$\rm Fit\ \rm Slope = %.2f \pm %.2f$'.format(
#                                           m3, mean( dat3_m ) ),
#          fontsize = 24, rotation=45                             )
#
plt.text( 0.0, 0.1, r'${\rm Expected}\ {\rm Fit} = 1$' )

#leg3 = [ 'Linear Fit', 'Theoretical Data', 'Observations' ]
#plt.legend( leg3, loc = 2, fontsize = 24 )
#plt.title(r'$\frac{\sigma_B}{| \vec B|}$ vs Fluctuating Velocity with error
#bars', fontsize = 24 )
plt.tight_layout()

#plt.savefig('fv_delb_fz21', format='eps', dpi=4000)

#plt.show( )

'''
