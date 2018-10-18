db = dat1_s_db

y1p1 = dat1_s_fv_p_c[0]
y1p2 = dat1_s_fv_p_b[0]
y2p1 = dat2_s_fv_p_c[0]
y2p2 = dat2_s_fv_p_b[0]
y3p1 = dat3_s_fv_p_c[0]
y3p2 = dat3_s_fv_p_b[0]

y1p1s = dat1_s_sig_fv_p_c[0]
y1p2s = dat1_s_sig_fv_p_b[0]
y2p1s = dat2_s_sig_fv_p_c[0]
y2p2s = dat2_s_sig_fv_p_b[0]
y3p1s = dat3_s_sig_fv_p_c[0]
y3p2s = dat3_s_sig_fv_p_b[0]

plt.close('all')

f, axs1= plt.subplots(2, 1)

pl, cl, bl = axs1[0].errorbar(db, y2p1, y2p1s, fmt='o', ecolor='g', color='b', label='Proton Core')
axs1[0].errorbar(db, y2p2, y2p2s, fmt='o', ecolor='m', color='r', label='Proton Beam')
bl[0].set_linestyle("--")
axs1[0].legend()
axs1[0].set_title( 'fluctuating beam')

axs1[0].set_xlabel( r'$\Delta{B}/|\vec B|$' )
axs1[0].set_ylabel( r'$V_f/V_A$' )

pl, cl, bl = axs1[1].errorbar(db, y1p1, y1p1s, fmt='o', ecolor='g', color='b', label='Proton Core')
bl[0].set_linestyle("--")
pl, cl, bl = axs1[1].errorbar(db, y1p2, y1p2s, fmt='o', ecolor='m', color='r', label='Proton Beam')
bl[0].set_linestyle("--")
axs1[1].legend()
axs1[1].set_title( 'fixed beam')

axs1[1].set_xlabel( r'$\Delta{B}/|\vec B|$' )
axs1[1].set_ylabel( r'$V_f/V_A$' )


f, axs2 = plt.subplots(2, 1)

pl, cl, bl = axs2[0].errorbar(range(len(db)), y2p1, y2p1s, fmt='o', ecolor='g', color='b', label='Proton Core')
axs2[0].errorbar(range(len(db)), y2p2, y2p2s, fmt='o', ecolor='m', color='r', label='Proton Beam')
bl[0].set_linestyle('--')
axs2[0].legend()
axs2[0].set_title( 'fluctuating beam')

axs2[0].set_xlabel( 'Spectra Number' )
axs2[0].set_ylabel( r'$V_f/V_A$' )

pl, cl, bl = axs2[1].errorbar(range(len(db)), y1p1, y1p1s, fmt='o', ecolor='g', color='b', label='Proton Core')
bl[0].set_linestyle("--")

pl, cl, bl = axs2[1].errorbar(range(len(db)), y1p2, y1p2s, fmt='o', ecolor='m', color='r', label='Proton Beam')
bl[0].set_linestyle("--")
axs2[1].legend()
axs2[1].set_title( 'fixed beam')

axs2[1].set_xlabel( 'Spectra Number' )
axs2[1].set_ylabel( r'$V_f/V_A$' )

axlist = np.concatenate([axs, axs2])
ymin = np.min([x.get_ylim()[0] for x in axlist])
ymax = np.max([x.get_ylim()[1] for x in axlist])
for ax in axlist:
	ax.set_ylim(ymin, ymax)
	ax.grid(True, which="major", axis="both")

f, axs3 = plt.subplots(2, 1)

pl, cl, bl = axs3[0].errorbar(range(len(db)), y3p1, y3p1s, fmt='o', ecolor='g', color='b', label='Proton Core')
axs3[0].errorbar(range(len(db)), y3p2, y3p2s, fmt='o', ecolor='m', color='r', label='Proton Beam')
bl[0].set_linestyle('--')
axs3[0].legend()
axs3[0].set_title( 'fluctuating beam')

axs3[0].set_xlabel( 'Spectra Number' )
axs3[0].set_ylabel( r'$V_f/V_A$' )

pl, cl, bl = axs3[1].errorbar(range(len(db)), y3p1, y3p1s, fmt='o', ecolor='g', color='b', label='Proton Core')
bl[0].set_linestyle("--")

pl, cl, bl = axs3[1].errorbar(range(len(db)), y3p2, y3p2s, fmt='o', ecolor='m', color='r', label='Proton Beam')
bl[0].set_linestyle("--")
axs3[1].legend()
axs3[1].set_title( 'fixed beam')

axs3[1].set_xlabel( 'Spectra Number' )
axs3[1].set_ylabel( r'$V_f/V_A$' )

axlist = np.concatenate([axs, axs2, axs3])
ymin = np.min([x.get_ylim()[0] for x in axlist])
ymax = np.max([x.get_ylim()[1] for x in axlist])
for ax in axlist:
	ax.set_ylim(ymin, ymax)
	ax.grid(True, which="major", axis="both")

plt.figure()

plt.errorbar( db, y3p1, y3p1s, fmt='o', ecolor='g', color='b', marker='^', label='Proton core')

plt.xlabel( r'$\Delta{B}/|\vec B|$' )
plt.ylabel( r'$V_f/V_A$' )
plt.xlim(0, 0.025)
plt.ylim(0, 0.025)

plt.figure()

plt.scatter( db, y3p1, color='b', marker='^', label='Proton core')

plt.xlabel( r'$\Delta{B}/|\vec B|$' )
plt.ylabel( r'$V_f/V_A$' )
plt.xlim(0, 0.025)
plt.ylim(0, 0.025)

plt.show()
