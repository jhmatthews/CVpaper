#!/usr/bin/env python
import py_plot_util as util
import py_plot_output as plt
import py_read_output as rd 
import numpy as np
from pylab import * 
import os, sys
from astropy.io import ascii
import plot_norm as norm
from constants import C

util.parse_rcparams()
rd.setpars()

alphas = [15,4,4]
alphas_actual = [1.5,4,1.5,4]
RV = ["7e10", "1e11", "2e11"]

colours = ["#d3d3d3", "k", "r","b","g"]
labels=["A","B","X","Y"]

atomic_filenames = [ "data/atomic_macro/h10_lines.py", "data/atomic73/lines_linked_ver_2.py", 
                             "data/atomic_macro/he_top_lines.py" ]
lines = norm.get_linelist(atomic_filenames)

for i in range(len(alphas)):



	fname = "../../latest_outputs/cv_alpha%i_r4r12_mdot1e9_rv%s_opt" % (alphas[i], RV[i])

	s = rd.read_spectrum(fname)

	select = (s["Lambda"] > 6513)*(s["Lambda"] < 6613)

	a = norm.get_continuum(s["Lambda"], s["A80P0.50"], lines, lmin=5600,lmax=6700, deg = 1)
	ff = norm.make_f(a, s["Lambda"])
	f = s["A80P0.50"]-ff

	fmax = np.max(util.smooth(f[select],window_len=8))
	f = f / fmax

	XTOPLOT = C* 1e-7 *(s["Lambda"] - 6563) / 6563

	plot(XTOPLOT, util.smooth(f,window_len=8), c=colours[i], label=labels[i], linewidth=2)


legend()
xlim(-19.469118,19.469118)
ylim(0,1)
xlabel("Velocity (100 km/s)", fontsize=16)
ylabel("Normalised Flux", fontsize=16)




savefig("mc.png")
savefig("../../figures/mc.eps")


