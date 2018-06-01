'''

dat4_b_x_raw     = [None]*nd4
dat4_b_y_raw     = [None]*nd4
dat4_b_z_raw     = [None]*nd4
dat4_b_y_sig_raw = [None]*nd4
dat4_b_z_sig_raw = [None]*nd4
dat4_sig_b_raw   = [None]*nd4
dat4_sig_bb      = [None]*nd4
dat4_fv_p        = [None]*nd4
dat4_sig_fv_p    = [None]*nd4
dat4_s_sig_fv_p  = [None]*nd4
dat4_alfvel      = [None]*nd4
dat4_s_fv        = [None]*nd4
dat4_ogyro       = [None]*nd4
dat4_ocycl       = [None]*nd4
dat4_thr_slp     = [None]*nd4
dat4_vmag        = [None]*nd4
dat4_vsig        = [None]*nd4
dat4_n           = [None]*nd4
dat4_nsig        = [None]*nd4
dat4_bmag        = [None]*nd4
dat4_bsig        = [None]*nd4
dat4_m           = [None]*nd4
dat4_rat         = [None]*nd4
time4            = [None]*nd4

for j in range( nd4 ) :

	time4[j] = dat4['time'][j].time().strftime("%H-%M")

	dat4_b_x_raw[j] = mean( np.array( dat4['b0_fields'][j]['raw_smt'] )[0] )

	dat4_b_y_raw[j] = mean( np.array( dat4['b0_fields'][j]['raw_smt'] )[1] )

	dat4_b_z_raw[j] = mean( np.array( dat4['b0_fields'][j]['raw_smt'] )[2] )

	dat4_b_y_sig_raw[j] = np.array(
	                            dat4['sig_b0_fields'][j]['sig_raw_smt'][1] )
	dat4_b_z_sig_raw[j] = np.array(
	                            dat4['sig_b0_fields'][j]['sig_raw_smt'][2] )

	dat4_sig_b_raw[j] = sqrt(
	                       dat4_b_y_sig_raw[j]**3 + dat4_b_z_sig_raw[j]**3 )

	dat4_sig_bb[j] = dat4_sig_b_raw[j] / dat4_b_x_raw[j]

plt.figure()
plt.plot(range(nd4), dat4_b_y_rot, color='r')
plt.plot(range(nd4), dat4_b_z_rot, color='b')
ind = [0, 10, 20, 30, 40 ,50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160,
       170, 180, 190]

label = [ time4[j] for j in ind ]

plt.xticks( ind, label, rotation = 'vertical', fontsize = 16 )
plt.show()

f1, ax41 = plt.subplots( )

ax41.set_ylabel( r'$\left< \frac{\Delta{\vec{B}}}{| \vec B|} \right >$',
fontsize = 32, color='m' )
#ax41.set_ylabel( r'$h$' , fontsize = 32, color='m' )
ax41.set_ylim( 0, 0.1 )
ax42 = ax41.twinx()

#ax42.scatter( range( len( time4 ) - k ), dat4_sig_bb[0:-k], color='r',
#                                                                    marker='D' )
if ( k > 0 ) :

	ax41.plot( range( len( time4 ) - k ), dat4_db_raw[0:-k], color='m',
	                                                            marker='^' )
	ax42.plot( range( len( time4 ) - k ), dat4_sig_bb[0:-k], color='g',
	                                                            marker='d' )
else :

	ax41.plot( range( len( time4 ) ), dat4_s_fv, color='m', marker='^'   )
	ax42.plot( range( len( time4 ) ), dat4_db_raw, color='g', marker='d' )

ax42.tick_params( 'y', colors='g' )
ax42.set_ylabel( r'$\frac{\sigma\vec{B}}{| \vec B|} $',
fontsize = 32, color='g' )
#ax42.set_ylabel( r'$\left< \frac{\Delta{\vec{B}}}{| \vec B|} \right >$',
#fontsize = 32, color='g' )
ax42.set_ylim( 0., 0.1 )
#plt.plot(range(nd4), dat4_b_y_rot, color='r')
#plt.plot(range(nd4), dat4_b_z_rot, color='b')
plt.xticks( ind, label, rotation = 'vertical', fontsize = 16 )

#ind=[0, 10, 20, 30, 40, 50, 60, 70]
#label = [ time4[j] for j in ind ]
#plt.xticks( ind, label )
#ax42.set_xticks( [0,10,20,30,40,50,60,70],
#[time4[0],time4[10],time4[20],time4[30],time4[40],time4[50],time4[60],time4[70]])

plt.xlabel('Time', fontsize = 26 )
plt.suptitle( 'Autorun: Yes, Filter Size: 11', fontsize = 24 )

plt.tight_layout()
plt.show( )
'''

fname3 = 'test_1_ms.jns'
dat3   = [0]*len( fname3 )

nd3 = len( dat3['b0'] )

dat3 = pickle.load( open( fname3, 'rb' ) )
dat4 = pickle.load( open( fname4, 'rb' ) )

time3 = [None]*len( dat3['time'] )
time4 = [None]*len( dat4['time'] )

for i in range( nd3 ) :

	time3[i] = dat3['time'][i].time().strftime("%H-%M")

for i in range( nd4 ) :

	time4[i] = dat4['time'][i].time().strftime("%H-%M")

t_p_3 = dat3['t_p_per']

t_p_4 = dat4['t_p_per']

t_p_4.pop(22)
t_p_4.pop(28)

diff = [ ( t_p_4[i] - t_p_3[i] ) for i in range( 72 ) ]

plt.figure( )

plt.scatter( range( len( time4 ) ), t_p_4, color='b', marker='^' )
plt.scatter( range( len( time4 ) ), t_p_3, color='r', marker='D' )

plt.ylim([35, 60])

plt.figure( )

plt.plot( range( 72 ), diff )
plt.show( )
