from janus_fc_spec import fc_spec
from spacepy import pycdf

cdf=pycdf.CDF('wi_sw-ion-dist_swe-faraday_20081017_v01.cdf')
#print cdf['cup1_qflux'][321]		# data 321 ...it's a list of size [963, 20, 31]


n_spec = len( cdf['Epoch'] )


s = 525



n_bin_max = 31

n_dir = 20

for n_bin_1 in range( n_bin_max ) :
	if ( n_bin_1 == n_bin_max + 1 ) :
		break
	if ( cdf['cup1_EperQ'][s][n_bin_1] >= cdf['cup1_EperQ'][s][n_bin_1+1] ) :
		break
n_bin_1 += 1

for n_bin_2 in range( n_bin_max ) :
	if ( n_bin_2 == n_bin_max + 1 ) :
		break
	if ( cdf['cup2_EperQ'][s][n_bin_2] >= cdf['cup2_EperQ'][s][n_bin_2+1] ) :
		break
n_bin_2 += 1

n_bin = min( [ n_bin_1, n_bin_2 ] )


#for b in range( n_bin_max ) :
#	print b, cdf['cup1_EperQ'][s][b], cdf['cup2_EperQ'][s][b]

#print n_bin

time = cdf['Epoch'][s]			# How to print it 

elev = [ float( cdf['inclination_angle'][0] ), float( cdf['inclination_angle'][1] ) ]

azim = [ [ float( cdf['cup1_azimuth'][s][d] ) for d in range( n_dir ) ],
         [ float( cdf['cup2_azimuth'][s][d] ) for d in range( n_dir ) ]  ]

volt_cen=[ [ float( cdf['cup1_EperQ'][s][b] ) for b in range( n_bin ) ],
           [ float( cdf['cup2_EperQ'][s][b] ) for b in range( n_bin ) ]  ]

volt_del=[ [ float( cdf['cup1_EperQ_DEL'][s][b] ) for b in range( n_bin ) ],
           [ float( cdf['cup2_EperQ_DEL'][s][b] ) for b in range( n_bin ) ]  ]

curr = [ [ [ float( cdf['cup1_qflux'][s][d][b] ) for b in range( n_bin ) ] for d in range( n_dir ) ],
         [ [ float( cdf['cup2_qflux'][s][d][b] ) for b in range( n_bin ) ] for d in range( n_dir ) ]  ]

spec = fc_spec( n_bin, time=time, elev=elev, azim=azim, volt_cen=volt_cen, volt_del=volt_del, curr=curr )

#print spec['n_bin']
'''
#spec.arr[0][0][0]._azim
for d in range( n_dir ) :

	for b in range( n_bin ) :

		spec.arr[0][d][b]['elev'] = float( cdf['inclination_angle'][0] )
		spec.arr[1][d][b]['elev'] = float( cdf['inclination_angle'][1] )

		spec.arr[0][d][b]['azim'] = float( cdf['cup1_azimuth'][s][d] )
		spec.arr[1][d][b]['azim'] = float( cdf['cup2_azimuth'][s][d] )

		spec.arr[0][d][b]['curr'] = float( cdf['cup1_qflux'][s][d][b] )
		spec.arr[1][d][b]['curr'] = float( cdf['cup2_qflux'][s][d][b] )
		
		spec.arr[0][d][b]['volt_cen'] = float( cdf['cup1_EperQ'][s][b] )
		spec.arr[1][d][b]['volt_cen'] = float( cdf['cup2_EperQ'][s][b] )

		spec.arr[0][d][b]['volt_del'] = float( cdf['cup1_EperQ_DEL'][s][b] )
		spec.arr[1][d][b]['volt_del'] = float( cdf['cup2_EperQ_DEL'][s][b] )

'''
