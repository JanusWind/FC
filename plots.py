plt.close()
#plt.clf()

n_fv=dat[0]['n_p']

n=dat_test['n_p']

sig_n_fv_s = np.array(dat[0]['sig_n_p_b'])+np.array(dat[0]['sig_n_p_c'])/n_fv

sig_n_s = np.array(dat[0]['sig_n_p_b'])+np.array(dat[0]['sig_n_p_c'])/n

indexx= linspace( 0, len(t_perp), len(t_perp) )

fig, ax = plt.subplots()

color = 'tab:red'
#colors = { 1:'red', 2:'blue', 3:'blue',4:'pink' }

ax.scatter(indexx, t_perp, color=color, marker='o')

color = 'tab:blue'

ax.scatter(indexx, t_perp_fv, color=color, marker='o')

ax.set_xlabel('Observation Number')
ax.set_ylabel('Temperature (kK)', color=color)

leg1= ['T',r'$T+\Delta V $']

ax.legend( leg, loc=2 )

ax1 = ax.twinx()

color = 'tab:green'

ax1.scatter(indexx, sig_n_s, color=color, marker='^')

color = 'tab:pink'

ax1.scatter(indexx, sig_n_fv_s, color=color, marker='^')

ax1.set_ylabel('Error in density', color=color)

leg2= [r'$\Delta n$', r'$\Delta n + \Delta V$']

ax1.legend( leg2, loc=1 )

plt.tight_layout()
plt.show()
