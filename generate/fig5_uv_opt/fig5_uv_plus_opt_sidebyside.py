import numpy as numpy
from pylab import *
import os, sys
from cobra_sub import smooth
import py_read_output as rd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import py_plot_util as util 

util.parse_rcparams()

fname = "specs/cv_alpha15_r4r12_mdot1e9_rv7e10_uv"
fname2 = "specs/cv_alpha15_r4r12_mdot1e9_rv7e10_opt"

rd.setpars()

nx = 2

ratio = 8.27 / 11.02
figure(figsize=(8.27,12))
incs = ("10", "17.5", "45", "62.5", "80")

s = rd.read_spectrum(fname)

subplot(111)
#xlabel("Wavelength [\AA]", fontsize=20)
nspec = 5

grids = [1,3,5,7,9]

dticks = [10,10,10,5,5]

for i in range(nspec):

	subplot(nspec,2,grids[i])
	xlim(1000,2000)

	plot(s["Lambda"], 1e12*smooth(s[s.colnames[9+i]] ), c="k")

	if i == 2: ylabel("Flux at 100pc ($10^{-12}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)", fontsize=20)

	#text(6100, 0.7*1e12*(np.max(s.spec[i])), "$i=%s^{\circ}$" % incs[i])
	ax = gca()
	

	print grids[i]
	#if grids[i] < 8: ax.set_xticklabels([])
	if i<4:ax.set_xticklabels([])


	start, end = ax.get_ylim()

	if i == 4:
		start, end = 0,35
	ax.yaxis.set_ticks(np.arange(start, end, dticks[i]))
	ylim(start,end)




#ylim(0,49)
labels = [r"Ly-$\alpha$", r"C\textsc{iv}", r"He~\textsc{ii}~$\lambda1640$"]
lines = [1215,1550, 1640]
vlines(lines, 27,30)

offs = [-90,0,0]
for i in range(len(labels)):
	text(lines[i]+offs[i],31,labels[i], fontsize=10)


#ax is name of original plot so change this to whatever your plot is called, 
#loc is where in graph you want box containing zoomed plot, mess with numbers
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
ax = gca()
axins = zoomed_inset_axes(ax, 2, loc=5) 
axins.plot(s["Lambda"], 1e12*smooth(s[s.colnames[8+nspec]] ), c="k")
axins.axis([1590,1690,1,12]) #x and y range of zoomed portion
setp(axins.get_xticklabels(), visible=False) #tick labels are annoying
setp(axins.get_yticklabels(), visible=False)
# # #loc1 and loc2 are where you want to draw the lines to connect your 
# # #zoomed area with original plot, experiment with these, 
# # #1,2,3,4 represent one corner of the box. 
# # #fc and ec are...|'m not sure, colours I think.
mark_inset(ax, axins, loc1=2, loc2=4,fc="none", ec="0.5") 



s = rd.read_spectrum(fname2)

dticks = [0.5,0.5,0.5,0.2,0.1]

for i in range(nspec):

	subplot(nspec,2,grids[i]+1)
	xlim(3100,6900)

	plot(s["Lambda"], 1e12*smooth(s[s.colnames[9+i]] ), c="k")

	#if i == 2: ylabel("Flux ($10^{-12}$~erg s$^{-1}$ cm$^{-3}$ \AA$^{-1}$)")

	ax = gca()
	if grids[i]+1 < 9: ax.set_xticklabels([])
	#ax.set_yticklabels([])

	if i < nspec - 1:
		start, end = ax.get_ylim()

	else:
		start, end = 0,0.69
	ax.yaxis.set_ticks(np.arange(start, end, dticks[i]))
	ylim(start,end)

	text( 7000,start + 0.6 * (end - start), r"$i=%s^\circ$" % incs[i], rotation="vertical")


text(1800,-0.25, "Wavelength (\AA)", fontsize=20)
labels = [r"He~\textsc{ii}~$\lambda3202$", r"He~\textsc{ii}~$\lambda4686$", r"H$\alpha$"]
lines = [3202,4686,6563]
vlines(lines, 0.55,0.60)

for i in range(len(labels)):
	text(lines[i]+0,0.62,labels[i], fontsize=10)


#ax is name of original plot so change this to whatever your plot is called, 
#loc is where in graph you want box containing zoomed plot, mess with numbers
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
ax = gca()
axins = zoomed_inset_axes(ax, 3, loc=5) 
axins.plot(s["Lambda"], 1e12*smooth(s[s.colnames[8+nspec]] ), c="k")
axins.axis([6463,6663,0.03,0.13]) #x and y range of zoomed portion
setp(axins.get_xticklabels(), visible=False) #tick labels are annoying
setp(axins.get_yticklabels(), visible=False)
# # #loc1 and loc2 are where you want to draw the lines to connect your 
# # #zoomed area with original plot, experiment with these, 
# # #1,2,3,4 represent one corner of the box. 
# # #fc and ec are...|'m not sure, colours I think.
mark_inset(ax, axins, loc1=3, loc2=4,fc="none", ec="0.5") 



#subplot(111)
#xlabel("Wavelength [\AA]", fontsize=20)
subplots_adjust(hspace=0, wspace=0.13)
#subplots_adjust(hspace=0, wspace=0)
savefig("fig5_uv_opt.png",facecolor='w',edgecolor='w',bbox_inches='tight')
savefig("../../figures/fig5_uv_opt.eps",facecolor='w',edgecolor='w',bbox_inches='tight')
#show()