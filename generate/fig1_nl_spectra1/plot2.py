from constants import *
import numpy as np
from pylab import *
import os, sys
from cobra_sub import smooth
import py_read_output as rd
rd.setpars()

def gauss(sigma, x0, x):

	term = 1.0 / (2.0*np.pi) / sigma

	exp_term = ( (x - x0)**2 )  /  (2.0*sigma*sigma)

	term *= np.exp(-exp_term)

	return term

# def convolve(FWHM, x, y, mode="gaussian"):

# 	'''
# 	convolve arrays
# 	'''

# 	sigma = FWHM / (np.sqrt(8.0*np.log(2.0)))

# 	n_points = len(x)

# 	for i in range(n_points):

def get_linelist(filenames, ionreturn=False):

	lines = np.array([])
	z = np.array([])

	for i in range(len(filenames)):

		x = np.loadtxt(filenames[i], comments="#", usecols=(2,3), unpack=True)

		lines = np.concatenate((lines, x[1]))

		z = np.concatenate((z, x[0]))

	if ionreturn:
		return lines, z
	else:
		return lines







# some fontsizes for figure
font1 = 16				# fontsize for x label
font2 = 16				# fontsize for Y label
font3 = 16				# fontsize for text on figures
weight = 1.5



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
colour = "k"


# read the RW Tri data 
cc,dd = np.loadtxt("rwtri/new_eclipse.dat", unpack=True, comments="#", usecols=(0,1))
cc_no, dd_no = np.loadtxt("rwtri/rwtri_opt_noeclipse.dat", unpack=True, comments="#", usecols=(0,1))






# adjust RW Tri from MJy to F_lambda in CGS units
nus = (C) / (cc*ANGSTROM)
dd = dd * nus / cc

nus_no = (C) / (cc_no*ANGSTROM)
dd_no = dd_no * nus_no / cc_no







##############
# plot RW Tri
##############

subplot(211)
plot( cc, smooth(dd, window_len=5)*1e-23*1e11,  c=colour, linewidth=weight)
plot( cc_no, smooth(dd_no, window_len=5)*1e-23*1e11,  c=colour, linewidth=weight)
xlim(3700,6900)

# text and labels
ylabel("Flux ($10^{-11}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)", fontsize = font2)
xlabel("Wavelength (\AA)", fontsize = font1)
text(5800,0.9,"RW Tri, in eclipse", fontsize = font3)
text(5800,3,"RW Tri, out of eclipse", fontsize = font3)
semilogy()
xlim(3400,6800)
ylim(0.1,40)

# plot model
scale = 2.718 / 0.036
subplot(212)
s = rd.read_spectrum("cv_alpha4_r4r12_mdot1e9_rv1e11_opt")
s2 = rd.read_spectrum("../../latest_outputs/cv_alpha4_r4r12_mdot1e9_rv1e11_opt")
plot( s["Lambda"], smooth(s["A80P0.50"], window_len=5)*1e11*scale,  c=colour, linewidth=weight)
plot( s["Lambda"], smooth(s["A80P0.00"], window_len=5)*1e11*scale,  c=colour, linewidth=weight)
plot( s2["Lambda"], smooth(s2["A80P0.50"], window_len=5)*1e11*scale,  c='r', linewidth=weight)
plot( s2["Lambda"], smooth(s2["A80P0.00"], window_len=5)*1e11*scale,  c='r', linewidth=weight)
xlim(3700,6900)


# text and labels
ylabel("Scaled Flux ($10^{-11}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)", fontsize = font2)
xlabel("Wavelength (\AA)", fontsize = font1)
#text(6000,0.9,"RW Tri, in eclipse", fontsize = font3)
#text(6000,3,"RW Tri, out of eclipse", fontsize = font3)


linefiles = ["data/atomic_macro/he_top_lines.py"]
#"data/atomic_macro/h20_lines.py"]

#for i in range(linefiles):
lines, ions = get_linelist(linefiles, ionreturn=True)


he1_lines = [5879,6680, 3889]
#hlines = [6563,	4861,	4341,	4102,	3970,	3889,	3835]
he2_lines = [4686]

lines = [5879,6680,4472,4714,
         4686, 5410, 4541,
         6563, 4861,	4341, 4102, 3889, 3934, 3969]

heii = [4686, 5410, 4541, 3934, 3969]
other = [5879,6680,4472,4714,
         6563, 4861,4341,4102, 3889]


labels = [r"He~\textsc{i}",r"He~\textsc{i}",r"He~\textsc{i}",r"He~\textsc{i}",
          r"He~\textsc{ii}",r"He~\textsc{ii}",r"He~\textsc{ii}",
          r"H$\alpha$",r"H$\beta$", r"H$\gamma$", r"H$\delta$", r"He~\textsc{i}","",r"Ca~\textsc{ii}"]

offset = [0,0,0,0,-19.85,-19.85,-19.85,0,0,0,0, 0,-19.85, -19.85]
vlines(other,13,23, linewidth=2)
vlines(heii,0.15,0.25, linewidth=2)

i = 0
for l in lines:
	text(l+20, 20 + offset[i], labels[i])
	i+=1

#arrow(4102, 14, -416, 0, head_width=5, head_length=40, fc='k', ec='k')
vlines([3646],0.1,40, linestyle="--")
ylim(0.1,40)
xlim(3400,6800)
semilogy()






tight_layout(pad=0.1)
# finally, save
savefig("../../figures/fig13.eps", bbox_inches = "tight")
savefig("fig13.png")


#show()

















