'''
James Matthews, 30/04/14

plotting script for comparing Tardis and Python level populations
'''

#import modules
import sys, os
from tardis.io import config_reader
from tardis import model, simulation
import numpy as np
import logging
import warnings
from numpy import exp
from pylab import *
from astropy import units


def run_tardis(yml_file="basic.yml"):
	'''
	runs a tardis model and returns a class instance of Radial1dModel type
	'''
	#read the config file and create a model
	tardis_config = config_reader.TARDISConfiguration.from_yaml(yml_file)
	radial1d = model.Radial1DModel(tardis_config)
	simulation.run_radial1d(radial1d)

	return radial1d


def set_model_params(radial1d, t_r, w, t_e, ne, tau):
	'''
	set the model parameters in tardis, returns model 
	of same type as input
	'''
	radial1d.t_rads[:] = t_r * units.K
	radial1d.ws[:] = w
	radial1d.plasma_array.electron_densities.values[:] = ne

	##interfere with any details - e.g. electron temperature - like this ...can also do electron density etc.
	frac_te = t_e / t_r
	radial1d.plasma_array.link_t_rad_to_t_electron = frac_te
	##might want to set tau_sobolev optical depths to zero (or some other set of values) for ease of comparison
	radial1d.plasma_array.tau_sobolevs.values[:] = tau

	#calculate the mean intensities in the lines for chosen conditions
	radial1d.calculate_j_blues()

	#propagate rad field settings to plasma
	radial1d.plasma_array.j_blues = radial1d.j_blues
	radial1d.plasma_array.t_rads = radial1d.t_rads.value

	return radial1d


def get_tardis_pops(radial1d, t_r, w, t_e, ne, tau):

	'''
	takes a tardis model and calculates the level populations 
	in these physical conditions (t_r, w, t_e, ne, tau)

	returns a numpy array, x, which contains the level populations summed so that 
	Python and Tardis can be compared.
	'''

	# set the model parameters and Jblues
	radial1d = set_model_params(radial1d, tr, w, te, ne, 0.0)
	radial1d.plasma_array.calculate_nlte_level_populations()

	# get He I level populations
	ch = radial1d.plasma_array.level_populations[0].ix[2,0]

	# x is the new array we will return. It just sums up some of the substructure
	# so we can compare with Python
	x = np.zeros(15)
	x[0:3] = ch[0:3]
	x[3] = np.sum(ch[3:6])
	x[4] = ch[6]
	x[5] = ch[7]
	x[6] = ch[8]
	x[7] = np.sum(ch[9:12])
	x[8] = np.sum(ch[12:15])
	x[9] = ch[15]
	x[10] = ch[16]
	x[11] = ch[17]
	x[12] = ch[18]
	x[13] = np.sum(ch[19:22])
	x[14] = np.sum(ch[22:25])

	return x


chianti_to_python_map = np.array([ 0, 1, 2, 3, 3, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 9, 10, 11, 12, 13, 13, 13, 14, 14, 14, 15])

level_strings = np.array([ "1s2", "1s.2s", "1s.2s", "1s.2p", "1s.2p", "1s.2p", "1s.2p", "1s.3s", "1s.3s", "1s.3p","1s.3p", "1s.3p", "1s.3d", "1s.3d", "1s.3d", "1s.3p", "1s.4s", "1s.4s", "1s.4p", "1s.4p","1s.4p", "1s.4p", "1s.4d", "1s.4d", "1s.4d","1s.4d"])




# read in the level populations from the Python data file
n, levpops, dep_coefs = np.loadtxt("py_level_pops.dat", comments="#", unpack=True)


# set physical conditions for tardis (in py_level_pops.dat)
ne = 5.9638e+04
te = 3.0600e+04
tr = 4.3482e+04 
tau = 0.0
w = 9.6511e-05

radial1d=run_tardis()
tardis_levs= get_tardis_pops(radial1d, tr, w, te, ne, tau)

x = np.zeros(15)



# number of tardis levels to plot
nlevs_tardis = len(tardis_levs)




# MAKE THE PLOTS, relative to ground state in this example
figure()
scatter(n[:nlevs_tardis], np.log10(levpops[:nlevs_tardis]/levpops[0]), label="Python", s = 80, marker = "o", facecolors="none", c="k", label="Python")
scatter(n[:nlevs_tardis], np.log10(tardis_levs/tardis_levs[0]), label="Tardis", s=80, marker=".", c="k", label="Tardis")
xlabel("Helium level")
ylabel("Fraction population")


show()








