Changes from the previous version: (development)

1. Major changes in 'janus_core.py'. The code is parsed into three different
   files ('janus_core.py','janus_fc_dat.py' and 'janus_fc_spec.py').
2. Functions in 'janus_core.py' were re-written to be compatible with the two
   new files.
3. MFI widget now has 4 different tabs to show the magnetic field components
   in x,y and z directions, and then along the co-latitude and longitude, 
   and the fourth tab lists out the average value of all those parameters
   including the avarage variation from the mean magnetic field.
4. The result widget now shows results for 3rd and 4th order moments and
   the time taken to run the non-linear analysis.
