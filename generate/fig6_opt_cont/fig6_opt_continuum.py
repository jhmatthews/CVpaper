import numpy as numpy
from pylab import *
import os, sys
from cobra_sub import smooth
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from plot_norm import *
import py_read_output as rd
import py_plot_util as util 

util.parse_rcparams()

fname = "specs/cv_alpha15_r4r12_mdot1e9_rv7e10_opt"
fname2 = "specs/cv_alpha4_r4r12_mdot1e9_rv1e11_opt"

rd.setpars()

mode = sys.argv[1]

atomic_filenames = [ "data/atomic_macro/h10_lines.py", "data/atomic73/lines_linked_ver_2.py", 
	                     "data/atomic_macro/he_top_lines.py" ]
lines = get_linelist(atomic_filenames)

nx = 2

figure(figsize=(8.3,11.6))
incs = ("10", "17.5", "45", "62.5", "80")

s = rd.read_spectrum(fname)
s2 = rd.read_spectrum(fname2)

subplot(111)
xlabel("Wavelength (\AA)", fontsize=20)
nspec = 5



for i in range(nspec):

	subplot(nspec,1,i+1)
	xlim(3040,6900)

	a = get_continuum(s["Lambda"], s[s.colnames[9+i]], lines)

	if mode == 'a':
		plot(s["Lambda"], smooth(s[s.colnames[9+i]] /make_f(a, s["Lambda"]), window_len=5  ), c="k")

	elif mode == "b":
		plot(s["Lambda"], smooth(s[s.colnames[9+i]] /make_f(a, s["Lambda"]), window_len=5 ), c="#d3d3d3", label="A")
		a = get_continuum(s2["Lambda"], s2[s2.colnames[9+i]], lines)
		plot(s2["Lambda"], smooth(s2[s2.colnames[9+i]] /make_f(a, s2["Lambda"]), window_len=5), c="k", label="B")
	

	if i == 2: ylabel("Flux/Continuum", fontsize=20)

	if i == 0 and mode == "b":
		legend()

	#text(6100, 0.7*1e12*(np.max(s[s.colnames[9+i]])), "$i=%s^{\circ}$" % incs[i])
	ax = gca()
	ylim(0.4,1.95)

	print i
	#if grids[i] < 8: ax.set_xticklabels([])
	if i<4:ax.set_xticklabels([])

	vlines([3646],0.4,1.95, linestyle="--")

	if mode == "b":
		vlines([5696],0.4,1.95, linestyle="--")

	if i == 3:
		text(3656, 1.6, "Balmer edge")
		if mode == "b":
			text(5706,0.6, r"He~\textsc{ii}, $n=5$ edge")




#ax is name of original plot so change this to whatever your plot is called, 
#loc is where in graph you want box containing zoomed plot, mess with numbers
# from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
# from mpl_toolkits.axes_grid1.inset_locator import mark_inset
# ax = gca()
# axins = zoomed_inset_axes(ax, 2, loc=3) 
# axins.plot(s["Lambda"], smooth(s[s.colnames[9+i]] /make_f(a, s["Lambda"]) ), c="k")
# axins.axis([6100,6300,1,3]) #x and y range of zoomed portion
# setp(axins.get_xticklabels(), visible=False) #tick labels are annoying
# setp(axins.get_yticklabels(), visible=False)
# # #loc1 and loc2 are where you want to draw the lines to connect your 
# # #zoomed area with original plot, experiment with these, 
# # #1,2,3,4 represent one corner of the box. 
# # #fc and ec are...|'m not sure, colours I think.
# mark_inset(ax, axins, loc1=1, loc2=2, fc="none", ec="0.5") 



lines = [3202,4686,6563]
subplot(515)
vlines(lines,0.5,0.65, linewidth=2)
#labels = [r"He~\textsc{ii}~$\lambda3202$", r"He~\textsc{ii}~$\lambda4686$", r"H$\alpha$"]
labels = [r"He~\textsc{ii}", r"He~\textsc{ii}", r"H$\alpha$"]
i = 0
for l in lines:
	text(l+20, 0.5, labels[i])
	i+=1

#vlines([3646],0.4,1.95, linestyle="--")
#text(3656, 1.6, "Balmer edge")

#subplot(111)
xlabel("Wavelength (\AA)", fontsize=20)
subplots_adjust(hspace=0, wspace=0.13)
#subplots_adjust(hspace=0, wspace=0)

if mode!="b":
	savefig("modela_opt_cont.png",facecolor='w',edgecolor='w',bbox_inches='tight')
	savefig("../../figures/modela_opt_cont.eps",facecolor='w',edgecolor='w',bbox_inches='tight')
else:
	savefig("modelb_opt_cont.png",facecolor='w',edgecolor='w',bbox_inches='tight')
	savefig("../../figures/modelb_opt_cont.eps",facecolor='w',edgecolor='w',bbox_inches='tight')
#show()



