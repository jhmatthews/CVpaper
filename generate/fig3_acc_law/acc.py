'''
acc.py 

Created the plot of the velocity law 
for CV paper 2014
'''

import py_plot_util as util 
util.parse_rcparams()


from pylab import *

figure()

import read_output as rd 
rd.setpars()
import matplotlib.pyplot as plt 
plt.rcParams["lines.linewidth"] = 2 

plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True


def vel_law (l, R_v, alpha):

	v0 = 6
	v_inf=10000

	v = (v_inf - v0) * (l / R_v)**alpha 

	v /= 1.0 + (l / R_v)**alpha 

	v += v0

	return v


alphas = [0.2,0.5,1, 1.5, 3,5,10]

R_v = 7e10

l = np.logspace(7,12,num=100000)

colors = ["b", "g", "r", "k", "y", "c", "m"]

i=0

for alpha in alphas:

	print alpha, np.log10(alpha)

	plot(l/R_v, vel_law(l, R_v, alpha)/10000, label="$\\alpha=%.1f$" % alpha, c=colors[i])

	i+=1



xlim(0,2.0)
legend(loc=4)

xlabel("$l/R_v$", fontsize=16)
ylabel("$v/v_{\infty}$", fontsize=16)

savefig("acc_law.png")
savefig("acc_law.eps", facecolor='w',edgecolor='w',bbox_inches='tight')


