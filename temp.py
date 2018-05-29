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
