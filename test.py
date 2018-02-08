from scipy.io import readsav
from janus_pl_spec import pl_spec
import numpy as np
import matplotlib.pyplot as mpl

mpl.close('all')

a = readsav('wind-faces_esa_1997-01-08.idl')

data = np.zeros(4)

data = [pl_spec( t_strt=a['sec_beg'][i], t_stop=a['sec_end'][i],
                elev_cen=a['the'][i], the_del=a['d_the'][i],
                azim_cen=a['phi'][i], phi_del=a['d_phi'][i],
                volt_cen=a['nrg'][i], volt_del=a['d_nrg'][i], psd=a['psd'][i] ) for i in range(4)]
#data[0]
for k in range(5):
	c = np.zeros(14)
	b = np.sqrt(data[0]['volt_cen'])
	for j in range(14):
		for i in range(5):
			c[j] += data[0]['psd'][k][i][j]

	mpl.figure(0)
	mpl.scatter(b,np.log(c/sum(c)+1.))
	mpl.xlim(0, 1.1*np.sqrt(5000))
	mpl.show()
