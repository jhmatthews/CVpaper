#from plot_norm import *
import numpy as numpy
from pylab import *
import os, sys
from cobra_sub import smooth
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from plot_norm import *
from constants import *
from scipy import interp
import py_plot_util as util
import py_read_output as rd


rd.setpars()
util.parse_rcparams()

mode = sys.argv[1]


fname = "specs/cv_alpha15_r4r12_mdot1e9_rv7e10_opt"

fname2 = "specs/cv_alpha4_r4r12_mdot1e9_rv1e11_opt"

s = rd.read_spectrum(fname)
s2 = rd.read_spectrum(fname2)

if mode=="a":
	plot(s["Lambda"], 1e12*smooth(s["Emitted"]), linewidth=2, label="Total", c="k")
	plot(s["Lambda"], 1e12*smooth(s["Disk"]), label="Disk")
	plot(s["Lambda"], 1e12*smooth(s["Wind"]), label="Wind")

else:
	# plot(s["Lambda"], 1e12*smooth(s["Emitted"]), linewidth=2, c="k", alpha=0.7)
	# plot(s["Lambda"], 1e12*smooth(s["Disk"]), c="g", alpha=0.7)
	# plot(s["Lambda"], 1e12*smooth(s["Wind"]), c="r", alpha=0.7))

	plot(s2["Lambda"], 1e12*smooth(s2["Emitted"]), linewidth=2, label="Total", c="k")
	plot(s2["Lambda"], 1e12*smooth(s2["Disk"]),  linewidth=1, c="g", label="Disk")
	plot(s2["Lambda"], 1e12*smooth(s2["Wind"]),  linewidth=1, c="r", label="Wind")

xlabel("Wavelength (\AA)", fontsize=16)
ylabel("$\log [$Flux at 100pc $(10^{-12}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1})]$", fontsize=16)
semilogy()
legend()
xlim(3050,6800)

savefig('../../figures/model%s_escaping.eps' % (mode),facecolor='w',edgecolor='w',bbox_inches='tight')
savefig('model%s_escaping.png' % (mode))