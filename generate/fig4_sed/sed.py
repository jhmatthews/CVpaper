'''
sed.py

Create the plot of disk and BL seds for the
CV paper 2014.

Requireds JAMES's disk subtourines
'''
import disk
from pylab import *
import numpy as np 
import os, sys
from constants import *
from cosmolopy.magnitudes import *
from read_output import *
from py_plot_util import *

# set some matplotlib parameters
setpars()
parse_rcparams()

# minimum and max wavelengths for rings
lmin = (C / 1e12) / ANGSTROM
lmax = (C / 1e19) / ANGSTROM


# make nr rings in a disk
nr = 100	# number of rings
r = disk.make_rings(lmin, lmax,0.8,1e-8,7e8,2.4e10, nrings = nr, mode="bb2")
r2 = disk.make_rings(lmin, lmax,0.7,5e-9,8e8,2.4e10, nrings = nr, mode="bb2")




# frequency resolution
nfreq = 10000


# create arrays for nu and fnu
nu = np.logspace(np.log10(1e9), np.log10(1e19), num = nfreq)
fnu = np.zeros(len(nu))
fnu2 = np.zeros(len(nu))


for j in range(nr - 1):
	Bnu = disk.planck_nu (r.T[j], nu)
	Bnu2 = disk.planck_nu (r2.T[j], nu)
	print r.T[j]
	for i in range(len(nu)):
		fnu[i] += Bnu[i] * r.area[j] * PI
		fnu2[i] += Bnu2[i] * r2.area[j] * PI




L_acc = 0.5 * G * 0.8 * MSOL * 1e-8 * MSOL / YR / 7e8

dnu = nu[1:] - nu[:-1]
dnu = np.append(dnu, dnu[-1])

Lacc = 2.0*np.sum(fnu*dnu)




area8 = L_acc / STEFAN_BOLTZMANN / 80000.0**4
area20 = L_acc / STEFAN_BOLTZMANN / 200000.0**4


f8 = disk.planck_nu(80000,nu) * area8 * PI
f20 = disk.planck_nu(200000,nu) * area20 * PI


L8 = np.sum(f8*dnu)
L20 = np.sum(f20*dnu)

print L_acc, Lacc, L8, L20


#figure(figsize=(8,8))
loglog(nu, nu*fnu, label="Blackbody Disk", linewidth=2.5, c="k")
#loglog(nu, nu*fnu2, label=r"Disk, HD91", linewidth=2.5, c="#839096")

# we used to calcualte boundayr layer spectra here- but ignore those now
# loglog(nu, nu*f8, label="BL, $T_{bl}=80000$K", linewidth=2, linestyle="--")
# loglog(nu, nu*f20, label="BL, $T_{bl}=200000$K", linewidth=2, linestyle="-.")

### WD spectrum
area_wd = 4.0 * PI * (7.0e8 ** 2)
fwd = disk.planck_nu(40000,nu) * area_wd * PI
loglog(nu, nu*fwd, label="White Dwarf", linewidth=2.5, c="k", linestyle="--")






ymin=1e17 
ymax = 1e37
ylim(ymin, ymax)
xlim(1e14,1e17)


x = [(24.31038 / HEV), (54.422791/ HEV), (13.6/ HEV)]
vlines(x, ymin, ymax, colors='k', linewidth=1)

delta = 1.1

text(x[0]*delta, 1e21,r"He~\textsc{i}", rotation="vertical", fontweight="bold", fontsize=14)
text(x[1]*delta, 1e21,r"He~\textsc{ii}", rotation="vertical", fontweight="bold", fontsize=14)
text(x[2]*delta, 1e21,r"H", rotation="vertical", fontweight="bold", fontsize=14)



#xlim(100,4000)
legend(loc=3)
xlabel(r"$\nu$ (Hz)", fontsize=16)
ylabel(r"$\nu F_{\nu}$ (erg~s$^-1$)", fontsize=16)



savefig("sed.png")
savefig("../../figures/sed_figure.eps",facecolor='w',edgecolor='w',bbox_inches='tight')
os.system("open -a preview sed.png")
clf()




