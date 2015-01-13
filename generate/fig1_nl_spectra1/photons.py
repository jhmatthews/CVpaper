from constants import *
import numpy as np
from pylab import *
import os, sys
from cobra_sub import smooth
import read_output as rd


def planck_l (T, lamb):

	''' 
	The planck function for wavelength lamb at temperature T

	Takes lambda in ANGSTROMS and return ergs cm^-2 s^-2 sr^-1 AA^-1
	'''

	# convert to cm for planck equation
	lamb2 = lamb*ANGSTROM

	x = H_OVER_K * C / (T * lamb2)
	Bnu = (2. * H * C**2.0) /  (lamb2**5.) / (np.exp(x) - 1.)

	# convert back to ANGSTROM
    
	return Bnu*ANGSTROM



x = np.arange(2000,5000,50)

# create a blackbody
y = planck_l(10000,x)

total = np.sum(y)





#generate photons
NPHOT = int (sys.argv[1])
photon_bins = np.zeros(len(y))

#weight = lum / NPHOT

weight = 1

binsize = 50

for i in range(NPHOT):


	# generate photon and locate in cdf
	z = np.random.random() * total

	j = -1
	c_sum = 0.0
	while c_sum < z:

		j += 1 
		c_sum += y[j]

	wave = x[j]
	

	photon_bins[j] += weight







#plot(x,yc)
scatter(x,photon_bins)

show()










