'''
plot_nl_figure.py 

This script creates the figure for the Nova like spectra
in the 2014 CV paper. The data were scraped from Dexter.
'''


from constants import *
import numpy as np
from pylab import *
import os, sys
from cobra_sub import smooth
import read_output as rd
rd.setpars()

# some fontsizes for figure
font1 = 16				# fontsize for x label
font2 = 12				# fontsize for Y label
font3 = 16				# fontsize for text on figures
weight = 1.5			# lineweight



# standard plot parameters for mnras
fig_width_pt=120.0 #Figure parameters
inches_per_pt=1.0/72.27
golden_mean=(math.sqrt(5)-1.0)/2.0
fig_width=fig_width_pt*inches_per_pt
fig_height=fig_width*golden_mean
fig_size=(fig_width*8, fig_height*8)
params={'font size' :10, 'axes.labelsize': 10, 'text.fontsize': 10, 'legend.fontsize': 10, 'xticks.labelsize': 8, 'yticks.labelsize': 8}
plt.rcParams.update(params)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True
matplotlib.rcParams['text.usetex'] = True


figure(figsize=fig_size)
colour = "b"

# read the RW Sex data
x1,y1 = np.loadtxt("rwsex/data11.dat", unpack=True, comments="#", usecols=(0,1))

# read the IX Vel daata
x, y = np.loadtxt("ixvel/data2.dat", unpack=True, comments="#", usecols=(0,1))
a,b = np.loadtxt("ixvel/data.dat", unpack=True, comments="#", usecols=(0,1))

# read the RW Tri data 
cc,dd = np.loadtxt("rwtri/new_eclipse.dat", unpack=True, comments="#", usecols=(0,1))
cc_no, dd_no = np.loadtxt("rwtri/rwtri_opt_noeclipse.dat", unpack=True, comments="#", usecols=(0,1))






# adjust RW Tri from MJy to F_lambda in CGS units
nus = (C) / (cc*ANGSTROM)
dd = dd * nus / cc

nus_no = (C) / (cc_no*ANGSTROM)
dd_no = dd_no * nus_no / cc_no





##############
# plot RW Sex
##############
subplot(311)
plot(x1,y1, c=colour ,linewidth=weight)
xlim( 3900, 6900)
ylabel("Flux ($10^{-13}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)", fontsize = font2)
text( 6000, 3.5,"RW Sex", fontsize = font3)




##############
# plot IX Vel
##############
subplot(312)
plot(x[(y > 0.92745)][20:-10],smooth(y[(y > 0.92745)][20:-10] , window_len=20), c=colour,linewidth=weight)
plot( a[45:], b[45:], c=colour, linewidth=weight)
xlim(3700, 6900)

# text and labels
ylabel("Relative Flux", fontsize = font2)
text( 6000, 1.15, "IX Vel", fontsize =font3)




##############
# plot RW Tri
##############

subplot(313)
plot( cc, smooth(dd, window_len=5)*1e-23*1e11,  c=colour, linewidth=weight)
plot( cc_no, smooth(dd_no, window_len=5)*1e-23*1e11,  c=colour, linewidth=weight)
xlim(3700,6900)

# text and labels
ylabel("Flux ($10^{-11}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)", fontsize = font2)
xlabel("Wavelength (\AA)", fontsize = font1)
text(6000,0.9,"RW Tri, in eclipse", fontsize = font3)
text(6000,3,"RW Tri, out of eclipse", fontsize = font3)


tight_layout(pad=0.1)

# finally, save
savefig("fig2.eps", bbox_inches = "tight")
savefig("fig2.png")




















