import matplotlib.pyplot as plt 
from pylab import * 
import numpy as np 
import csv, sys, os, array, warnings, subprocess
import pywind_sub as ps
import matplotlib as mpl
from matplotlib.mlab import bivariate_normal
from matplotlib.colors import LogNorm
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
import time
import read_output as rd


def run_py_wind (vers, fname, cmds=None, ilv=None):
	'''
	run version vers of py_wind on file fname.wind_save
	'''

	if cmds == None:
		cmds = np.array(["1", "n","t", "r","v","1","2","3","-1", "I", "i","0", "1","1","1","2","2","2","2","1","2","3","6", \
			          "3","6","4","6","5","0","q"])

	x = cmds
	np.savetxt("_tempcmd.txt", x, fmt = "%s")


	isys = os.system('py_wind'+vers+' '+fname+' < _tempcmd.txt > tempfile &')
	time.sleep(3)

	# remove temporary file
	#os.system("rm -f _tempcmd.txt")
	return isys




def run_pydc (vers, fname, nplasma = 1):
	'''
	run version vers of py_wind on file fname.wind_save
	'''

	x = np.array(["1","M","4",str(nplasma),"1","-1","r","n","t","w", "q"])
	np.savetxt("_tempcmd.txt", x, fmt = "%s")


	isys = os.system('py_wind'+vers+' '+fname+' < _tempcmd.txt')
	time.sleep(3)

	# remove temporary file
	#os.system("rm -f _tempcmd.txt")
	return isys

#ix,iz,x,z,lx,lz,xmax,zmax=ps.get_wind_geom(fname+'.ioncH1.dat')



#nplasmas = ps.pywind_read(fname+'.pnum.dat',ix,iz)

def read_pywind_smart(filename, return_inwind=False):
	'''
	read a py_wind file using np array reshaping and manipulation
	'''

	# first, simply load the filename 
	d = np.loadtxt(filename, comments="#", dtype = "float", unpack = True)

	# our indicies are already stored in the file- we will reshape them in a sec
	zindices = d[-1]
	xindices = d[-2]

	# we get the grid size by finding the maximum in the indicies list 99 => 100 size grid
	zshape = int(np.max(zindices) + 1)
	xshape = int(np.max(zindices) + 1)


	# reshape our indices arrays
	xindices = xindices.reshape(xshape, zshape)
	zindices = zindices.reshape(xshape, zshape)

	# now reshape our x,z and value arrays
	x = d[0].reshape(xshape, zshape)
	z = d[1].reshape(xshape, zshape)

	values = d[2].reshape(xshape, zshape)

	# these are the values of inwind PYTHON spits out
	inwind = d[3].reshape(xshape, zshape)

	# create an inwind boolean to use to create mask
	inwind_bool = (inwind >= 0)
	mask = (inwind < 0)

	# finally we have our mask, so create the masked array
	masked_values = np.ma.masked_where ( mask, values )

	#print xshape, zshape, masked_values.shape

	#return the transpose for contour plots.
	if return_inwind:
		return x, z, masked_values.T, inwind_bool.T
	else:
		return x, z, masked_values.T

def read_pywind_logspace(filename):

	'''
	convert to logspace coordinates
	'''

	x,z,s = read_pywind_smart(filename)

	x = np.log10(x)
	z = np.log10(z)

	return x,z,s


def get_nplasmas(vers, fname):

	cmds = ["1","B","q"]
	run_py_wind (vers, fname, cmds)

	x,z,masked_plasma = read_pywind_smart(fname+".pnum.dat")

	return masked_plasma


def masked_to_lin(masked_array, nplasmas, NPLASMA):

	x = np.zeros(NPLASMA)

	for n in range(NPLASMA):

		where = (nplasmas == n)

		print masked_array[where].nonzero()[0]

		x[n] = masked_array[where].nonzero()[0]

	return x




fname = sys.argv[1]


#run_py_wind("77a_dev", fname)
rd.setpars()




x, z,H1=read_pywind_smart(fname+'.ioncH1.dat')
x, z,H2=read_pywind_smart(fname+'.ioncH2.dat')

x, z,He1=read_pywind_smart(fname+'.ionHe1.dat')
x, z,He2=read_pywind_smart(fname+'.ionHe2.dat')
x, z,He3=read_pywind_smart(fname+'.ionHe3.dat')

mean_He = ( He1 + (He2*2.0) + (He3*3.0) )
print np.mean(mean_He)

x, z,IP=read_pywind_smart(fname+'.IP.dat')
x, z,te=read_pywind_smart(fname+'.te.dat')
x, z,ne=read_pywind_smart(fname+'.ne.dat')
#tr=ps.pywind_log_read(fname+'.tr.dat',ix,iz)
x, z,vy=read_pywind_smart(fname+'.vy.dat')
x, z,vx=read_pywind_smart(fname+'.vx.dat')
x, z,vz=read_pywind_smart(fname+'.vz.dat')


ix = len(x)
iz = len(z)
vxz=np.empty([ix,iz])
for i in range(ix):
	for j in range(iz):
		vxz[i][j]=(np.sqrt(vx[i][j]*vx[i][j]+vz[i][j]*vz[i][j]))


lwind_scale=[8,12,8,12]
wind_scale=[1e13,1e18,1e13,1e18]
wscale = [0,7e11,0,7e11]
#wscale = [8.8,11.7,9.2,11.7]

#x = np.log10(x)
#z = np.log10(z)



fig=plt.figure(figsize=[14,14])
fig.subplots_adjust(hspace=0.15,wspace=0.1)

ax=fig.add_subplot(3,2,1)
plt.axis(wscale)
plt.contourf(z,x,np.log10(ne),[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],extend='both')
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{log (electron~density/cm^{-3}}$)')
plt.grid()
ax.set_ylabel(r"log(z/cm)")
ax.set_xlabel(r"log(x/cm)")

ax=fig.add_subplot(322)
plt.axis(wscale)
plt.contourf(z,x,np.log10(te),np.arange(2.6,5,0.2),extend='both')
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{log (electron~temperature/K)}$')
plt.grid()
ax.set_xlabel(r"log(x/cm)")



ax=fig.add_subplot(323)
plt.axis(wscale)
vxz=vxz/100000.0
plt.contourf(z,x,vxz,levels=[5,10,20,30,40,50,60,70,80,90,
100,200,300,400,500,600,700,800,900,
1000,2000,3000,4000,5000,6000,7000,8000,9000,
10000,20000,30000,40000,50000],norm=LogNorm())
ax.set_ylabel(r"log(z/cm)")
ax.set_xlabel(r"log(x/cm)")
cbar=plt.colorbar(format='%2.0e',ticks=[10,100,1000,10000],orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{Poloidal~velocity/km~s^{-1}}$')
#plt.contour(x,z,vxz,levels=[10,100,1000,10000],norm=LogNorm(),colors='k')
plt.grid()



ax=fig.add_subplot(324)
plt.axis(wscale)
vy=vy/100000.0
plt.contourf(z,x,vy,levels=[10,20,30,40,50,60,70,80,90,
100,200,300,400,500,600,700,800,900,
1000,2000,3000,4000,5000,6000,7000,8000,9000,
10000,20000,30000,40000,50000],norm=LogNorm())
ax.set_xlabel(r"log(x/cm)")
cbar=plt.colorbar(format='%2.0e',ticks=[10,100,1000,10000],orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{Rotational~velocity/km~s^{-1}}$')
#plt.contour(lx,lz,vy,levels=[10,100,1000,10000],norm=LogNorm(),colors='k')
plt.grid()



ax=fig.add_subplot(325)
plt.axis(wscale)
plt.contourf(z,x,mean_He,np.arange(1,3.1,0.1),extend='both')
ax.set_xlabel(r"log(x/cm)")
ax.set_ylabel(r"log(z/cm)")
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel('Mean Charge of He')
#plt.contour(lx,lz,vy,levels=[10,100,1000,10000],norm=LogNorm(),colors='k')
plt.grid()



ax=fig.add_subplot(326)
plt.axis(wscale)
plt.contourf(z,x,np.log10(IP),np.arange(-8,6,1))
ax.set_xlabel(r"log(x/cm)")
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r'$\log (U)$')
#plt.contour(lx,lz,vy,levels=[10,100,1000,10000],norm=LogNorm(),colors='k')
plt.grid()



#show()
#savefig('fig5.png',facecolor='w',edgecolor='w',bbox_inches='tight')
#savefig('fig5.eps',facecolor='w',edgecolor='w',bbox_inches='tight')

savefig('fig5_lin.png',facecolor='w',edgecolor='w',bbox_inches='tight')
savefig('fig5_lin.eps',facecolor='w',edgecolor='w',bbox_inches='tight')





