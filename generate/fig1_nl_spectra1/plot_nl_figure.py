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
import py_plot_util as util 

util.parse_rcparams("../params.rc")
rd.setpars()

# some fontsizes for figure
font1 = 16				# fontsize for x label
font2 = 16				# fontsize for Y label
font3 = 16				# fontsize for text on figures
weight = 2			# lineweight

from matplotlib.ticker import MultipleLocator, FormatStrFormatter


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
subplot(411)
plot(x1,y1, c=colour ,linewidth=weight)
semilogy()

#ylabel("Flux\n($10^{-13}$~erg s$^{-1}$ cm$^{-2}$ \AA$^{-1}$)", fontsize = 12)
text( 6000, 3.5,"RW Sex", fontsize = font3)




gca().set_xticklabels([])

# vlines(lines,4.5,5, linewidth=2)
# i = 0
# for l in lines:
# 	text(l+20, 5, labels[i])
# 	i+=1

ylim(0.9,6.3)
vlines([3646], 0.9,6.3, linestyle="--")
xlim(3500,6900)

majorFormatter = FormatStrFormatter('%d')
majorLocator   = MultipleLocator(1)
minorFormatter = FormatStrFormatter('%d')

# ax.yaxis.set_major_locator(majorLocator)
ax = gca()
ax.yaxis.set_major_formatter(majorFormatter)
ax.yaxis.set_major_locator(majorLocator)

##############
# plot IX Vel
##############
# subplot(412)
# plot(x[(y > 0.92745)][20:-10],smooth(y[(y > 0.92745)][20:-10] , window_len=20), c=colour,linewidth=weight)

# plot( a[45:], b[45:], c=colour, linewidth=weight)

# gca().set_xticklabels([])
# xlim(3500,6900)
# ylim(0.7, 4.2)
# vlines([3646], 0.7, 4.2, linestyle="--")
# semilogy()

# majorFormatter = FormatStrFormatter('%d')
# majorLocator   = MultipleLocator(1)
# minorFormatter = FormatStrFormatter('%d')

# # ax.yaxis.set_major_locator(majorLocator)
# ax = gca()
# ax.yaxis.set_major_formatter(majorFormatter)
# ax.yaxis.set_major_locator(majorLocator)

# # text and labels
# ylabel("Relative Flux", fontsize = 12)
# text( 6000, 1.4, "IX Vel", fontsize =font3)

# 
import pyfits as py
def get_lambda(fname, length):
  
  delta = py.getval(fname, "CDELT1")
  start = py.getval(fname, "CRVAL1")

  w = np.arange(start, start + ((length) * delta), delta)

  if len(w) != length:
    print "error, lambda array is length %i not %i" % (len(w), length)

  unit = py.getval(fname, "CUNIT1")

  if unit == "nm":
    w = w * 10.0 # convert to Angstroms

  return w

slits = ["/Users/jmatthews/XShooter_data/IXVel/1.3_slit", "/Users/jmatthews/XShooter_data/IXVel/5_slit"]

cols=["k","r"]

subplot(412)
for i in range(1):

  vis_fname = "%s/No_telluric/VIS/IX-Vel_SCI_SLIT_FLUX_MERGE1D_VIS_tac.asc" % slits[i]
  uv_fname = "%s/UVB/IX-Vel_SCI_SLIT_FLUX_MERGE1D_UVB.fits" % slits[i]

  w,f = np.loadtxt(vis_fname, unpack=True, usecols=(2,3), comments="#")

  w = w * 1e4
  select1 = (w < 6364) * (w > 5596)
  select2 = (w < 6850) * (w > 6381)
  select = select1 + select2
  #select = (w > 3000)
  plot(w[select],smooth(f[select], window_len=5)*1e12*3.4,c=colour, linewidth=weight*0.7)
  #plot(w[select2],smooth(f[select2]),c = cc[i], label=labels[i])
  f = py.getdata(uv_fname)
  w = get_lambda(uv_fname, len(f))
  select = (w < 5500) *  (w > 3688)
  plot(w[select],smooth(f[select], window_len=5)*1e12*3.4, c=colour, linewidth=weight*0.7)
  ylim(0.9,6.3)
  xlim(3500,6900)
  semilogy()

ax = gca()

majorLocator   = MultipleLocator(1)
majorFormatter = FormatStrFormatter('%d')
minorLocator   = MultipleLocator(0.1)
minorFormatter = FormatStrFormatter('%d')

ax.yaxis.set_major_locator(majorLocator)
ax.yaxis.set_major_formatter(majorFormatter)
text( 6000, 3.5,"IX Vel", fontsize = font3)
#ylabel("Flux\n($10^{-13}$~erg s$^{-1}$ cm$^{-2}$ \AA$^{-1}$)", fontsize = 12)
gca().set_xticklabels([])


lines = [5879,6680,
         4686, 5410,
         6563, 4861, 4341,  4102]
labels = [r"He~\textsc{i}",r"He~\textsc{i}",
          r"He~\textsc{ii}",r"He~\textsc{ii}",
          r"H$\alpha$",r"H$\beta$", r"H$\gamma$", r"H$\delta$"]
lines1 = [5879,
         4686, 5410,
         4861, 4341,  4102]
lines2 = [6563, 6680]
vlines(lines1,1,1.3, linewidth=2)
vlines(lines2,3,4, linewidth=2)
i = 0
for l in lines:
  if l == 6680 or l == 6563:
    text(l+20, 4, labels[i])
  else:
    text(l+20, 1, labels[i])
  i+=1

labels = [r"He~\textsc{i}",r"He~\textsc{i}",r"He~\textsc{i}",r"He~\textsc{i}",
          r"He~\textsc{ii}",r"He~\textsc{ii}",r"He~\textsc{ii}",
          r"H$\alpha$",r"H$\beta$", r"H$\gamma$", r"H$\delta$"]

##############
# plot RW Tri
##############

subplot(212)
plot( cc_no, smooth(dd_no, window_len=5)*1e-23*1e11,  c=colour, linewidth=weight)
semilogy()
xlim(3500,6900)
ylim(0.2,6.98)


# text and labels
#ylabel("Flux ($10^{-11}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)", fontsize = font2)


text(5800,4,"RW Tri, out of eclipse", fontsize = font3)
subplots_adjust(wspace=0.0)

ax = gca()

#majorLocator   = MultipleLocator(10)
majorFormatter = FormatStrFormatter('%.1f')
# minorLocator   = MultipleLocator(1)
minorFormatter = FormatStrFormatter('%.1f')

# ax.yaxis.set_major_locator(majorLocator)
#ax.yaxis.set_major_formatter(majorFormatter)
# ax.yaxis.set_minor_locator(minorLocator)
#ax.yaxis.set_minor_formatter(minorFormatter)

#ylim(1.2,6.99)
#ax.set_yticklabels(np.arange(2.0,7, 1.0), minor=False)

#subplot(414)
plot( cc, smooth(dd, window_len=5)*1e-23*1e11,  c=colour, linewidth=weight)
xlabel("Wavelength (\AA)", fontsize = font1)
#ylabel("Flux ($10^{-11}$~erg s$^{-1}$ cm$^{-2}$ \AA$^{-1}$)", fontsize = 12, rotation="vertical")
text(5800,0.7,"RW Tri, in eclipse", fontsize = font3)

xlim(3500,6900)
vlines([3646], 0.2, 6.98, linestyle="--")

semilogy()

ax = gca()

majorLocator   = MultipleLocator(1)
majorFormatter = FormatStrFormatter('%d')
minorLocator   = MultipleLocator(0.1)
minorFormatter = FormatStrFormatter('%d')

ax.yaxis.set_major_locator(majorLocator)
ax.yaxis.set_major_formatter(majorFormatter)
#ax.yaxis.set_minor_locator(LogLocator(10.0, subs=[1.0]))
#ax.yaxis.set_minor_formatter(minorFormatter)

#ax.set_yticklabels(np.arange(0.3,1.1,0.1), minor=False)
#ax.set_yticklabels(["","","","0.5","","","","",'1.0',""], minor=False)
#ax.yaxis.set_minor_ticks(np.arange(0.1,1.1, 0.1))


text (3320,15,r"Flux (F$_\lambda$, Arb. units)",rotation="vertical",fontsize=16)


subplots_adjust(hspace=0.0)
#show()
#tight_layout(pad=0.2)

# finally, save
savefig("../../figures/fig1.eps", bbox_inches = "tight")
savefig("fig1.png")




















