Changes from the previous version: (Development)

Version 0.4.0 ---> version 0.4.1

1. Added a new file 'janus_spin_arcv.py', so that the code no longer
   assumes a default spin value. Downloads the spin files and carry
   out further calculations.
2. Added the option to download either the low or high resolution
   magnetic field data.
3. Options menu working and stores all the options to a janus.cfg file.
4. Added beta (parallel) calculations and it is displayed under results.
5. Added option to control the number of downloaded files to be saved. 
6. Fixed some existing bugs in moments caclulation options.


Version 0.3.3 ---> version 0.4.0

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
