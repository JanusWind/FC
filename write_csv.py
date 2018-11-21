with open("b_x.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_b_x )

with open("b_y.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_b_y )

with open("b_z.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_b_z )

with open("b_t.csv",'wb') as resultFile:

	wr = csv.writer(resultFile, dialect='excel')
	wr.writerow( mfi_t )
