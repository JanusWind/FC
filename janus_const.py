################################################################################
##
## Janus -- GUI Software for Processing Thermal-Ion Measurements from the
##          Wind Spacecraft's Faraday Cups
##
## Copyright (C) 2016 Bennett A. Maruca (bmaruca@udel.edu)
##
## This program is free software: you can redistribute it and/or modify it under
## the terms of the GNU General Public License as published by the Free Software
## Foundation, either version 3 of the License, or (at your option) any later
## version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
## FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
## details.
##
## You should have received a copy of the GNU General Public License along with
## this program.  If not, see http://www.gnu.org/licenses/.
##
################################################################################


################################################################################
## DEFINE THE DICTIONARY OF COMMON PHYSICAL CONSTANTS (IN "SI" UNITS).
################################################################################

const = dict( k_b       = 1.380650e-23,       # Boltzmann constant [J/K]
              epsilon_0 = 8.854188e-12,       # Electric constant  [F/m]
              mu_0      = 1.256637e-06,       # Magnetic constant  [H/m]
              m_p       = 1.672622e-27,       # Proton mass        [kg]
              q_p       = 1.602177e-19,       # Proton charge      [C]
              au        = 1.495979e+11  )     # Astronomical unit  [m]
