#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python -i

import csv, sys, os, array, warnings, subprocess
import matplotlib.pyplot as plt
import numpy as np
import pywind_sub as ps
import matplotlib as mpl
from matplotlib.mlab import bivariate_normal
from matplotlib.colors import LogNorm
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl

mpl.rcParams['text.usetex']='true'


fname=sys.argv[1]

#cmdline='py_wind78a '+fname+' < paper_pywindcmds'
#subprocess.check_call(cmdline,shell=True)	

x=[]
z=[]
x1=[]
z1=[]
lx=[]
lz=[]
lx1=[]
lz1=[]

data=[]
IPtemp=[]
tetemp=[]
nhtemp=[]
xtemp=[]
ztemp=[]

tetemp=[]
trtemp=[]

convtemp=[]

vx=[]
vz=[]

H1=[]
H2=[]
C4temp=[]
Si4temp=[]
N5temp=[]
O6temp=[]



ix,iz,x,z,lx,lz,xmax,zmax=ps.get_wind_geom(fname+'.ioncH1.dat')



H1=ps.pywind_read(fname+'.ioncH1.dat',ix,iz)
H2=ps.pywind_read(fname+'.ioncH2.dat',ix,iz)

H=np.empty([ix,iz])
for i in range(ix):
	for j in range(iz):
		H[i][j]=np.log10(H1[i][j]+H2[i][j])



IP=ps.pywind_read(fname+'.IP.dat',ix,iz)
te=ps.pywind_log_read(fname+'.te.dat',ix,iz)
#tr=ps.pywind_log_read(fname+'.tr.dat',ix,iz)
vx=ps.pywind_read(fname+'.vz.dat',ix,iz)
vy=ps.pywind_read(fname+'.vy.dat',ix,iz)
vz=ps.pywind_read(fname+'.vz.dat',ix,iz)
#nagn=ps.pywind_log_read(fname+'.nphot.dat',ix,iz)





vxz=np.empty([ix,iz])
for i in range(ix):
	for j in range(iz):
		vxz[i][j]=(np.sqrt(vx[i][j]*vx[i][j]+vz[i][j]*vz[i][j]))


#These are the lines for reading in all the extra ions fractions

#C3=ps.pywind_log_read(fname+'.ionC3.dat',ix,iz)
C4=ps.pywind_log_read(fname+'.ionC4.dat',ix,iz)
#C5=ps.pywind_log_read(fname+'.ionC5.dat',ix,iz)
#C6=ps.pywind_log_read(fname+'.ionC6.dat',ix,iz)
#C7=ps.pywind_log_read(fname+'.ionC7.dat',ix,iz)
#Si4=ps.pywind_log_read(fname+'.ionSi4.dat',ix,iz)
#N5=ps.pywind_log_read(fname+'.ionN5.dat',ix,iz)
#O6=ps.pywind_log_read(fname+'.ionO6.dat',ix,iz)

#cmdline='py_wind74b4 '+fname+' < ~/Python_scripts/pywindcmds2'
#subprocess.check_call(cmdline,shell=True)
#ndisk=ps.pywind_log_read(fname+'.nphot.dat',ix,iz)
#tauc4=ps.pywind_read(fname+'.ionC4.dat',ix,iz)
ne=ps.pywind_log_read(fname+'.ne.dat',ix,iz)

lwind_scale=[16.5,19,15.01,19]
wind_scale=[1e13,1e18,1e13,1e18]

fig=plt.figure(figsize=[14,14])
fig.subplots_adjust(hspace=0.15,wspace=0.1)
plt.rcParams['font.size']=12



'''ax=fig.add_subplot(321)
plt.axis(lwind_scale)
plt.grid()
ax.set_xlabel(r"log(x/cm)")
ax.set_ylabel(r"log(z/cm)")
plt.contourf(lx,lz,H,[0,1,2,3,4,5,6,7,8,9,10,11,12])
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r"$\rm{log (hydrogen~density/cm^{-3}}$)")
'''

ax=fig.add_subplot(323)
plt.axis(lwind_scale)
vxz=vxz/100000.0
plt.contourf(lx,lz,vxz,levels=[10,20,30,40,50,60,70,80,90,
100,200,300,400,500,600,700,800,900,
1000,2000,3000,4000,5000,6000,7000,8000,9000,
10000,20000,30000,40000,50000],norm=LogNorm())
ax.set_ylabel(r"log(z/cm)")
ax.set_xlabel(r"log(x/cm)")
cbar=plt.colorbar(format='%2.0e',ticks=[10,100,1000,10000],orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{Poloidal~velocity/km~s^{-1}}$')
plt.contour(lx,lz,vxz,levels=[10,100,1000,10000],norm=LogNorm(),colors='k')
plt.grid()

ax=fig.add_subplot(324)
plt.axis(lwind_scale)
vy=vy/100000.0
plt.contourf(lx,lz,vy,levels=[10,20,30,40,50,60,70,80,90,
100,200,300,400,500,600,700,800,900,
1000,2000,3000,4000,5000,6000,7000,8000,9000,
10000,20000,30000,40000,50000],norm=LogNorm())
ax.set_xlabel(r"log(x/cm)")
cbar=plt.colorbar(format='%2.0e',ticks=[10,100,1000,10000],orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{Rotational~velocity/km~s^{-1}}$')
plt.contour(lx,lz,vy,levels=[10,100,1000,10000],norm=LogNorm(),colors='k')
plt.grid()



ax=fig.add_subplot(322)
plt.axis(lwind_scale)
plt.contourf(lx,lz,te,[3,3.2,3.4,3.6,3.8,4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6],extend='both')
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{log (electron~temperature/K)}$')
plt.grid()

ax.set_xlabel(r"log(x/cm)")

ax=fig.add_subplot(325)
plt.axis(lwind_scale)
plt.contourf(lx,lz,IP,[-6,-5,-4,-3,-2,-1,0,1,2,3,4],extend='both')
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{log (U)}$')
plt.grid()
plt.plot(np.log10(1e17),np.log10(1e16),'s',color='k',markersize=10,mfc='none')
plt.plot(np.log10(1e18),np.log10(1.94e17),'s',color='k',markersize=10,mfc='none')
plt.plot(np.log10(3.66e18),np.log10(1.09e18),'s',color='k',markersize=10,mfc='none')
ap=dict(arrowstyle='->')

plt.annotate('Cell A',xy=(np.log10(1e17),np.log10(1e16)),xytext=(16.6,17), arrowprops=ap)
plt.annotate('Cell B',xy=(np.log10(1e18),np.log10(1.94e17)),xytext=(18.2,16), arrowprops=ap)
plt.annotate('Cell C',xy=(np.log10(3.66e18),np.log10(1.09e18)),xytext=(18.1,18.5), arrowprops=ap)


ax.set_xlabel(r"log(x/cm)")
ax.set_ylabel(r"log(z/cm)")

ax=fig.add_subplot(3,2,1)
plt.axis(lwind_scale)
plt.contourf(lx,lz,ne,[0,1,2,3,4,5,6,7,8,9,10,11,12])
cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r'$\rm{log (electron~density/cm^{-3}}$)')
plt.grid()
ax.set_ylabel(r"log(z/cm)")
ax.set_xlabel(r"log(x/cm)")


ax=fig.add_subplot(326)
plt.axis(lwind_scale)
CS6=plt.contourf(lx,lz,C4,[-6,-5,-4,-3,-2,-1,0],extend='both')


angles=[40,75,80,85]
for angle in angles:
	zcoord=[]
	for xcoord in lx:
		zcoord.append(np.log10(((10**xcoord))*np.tan(np.radians(90.-angle))))
	plt.plot(lx,zcoord,color='k',linewidth=1.0)
	plt.text(16.55,(np.log10(((10**16.6))*np.tan(np.radians(90.-angle)))),angle,fontsize=8)

'''angles=[20,40,60,89]
for angle in angles:
	zcoord=[]
	for xcoord in lx:
		zcoord.append(np.log10(((10**xcoord))*np.tan(np.radians(90.-angle))))
	plt.plot(lx,zcoord,color='k',linewidth=0.25)
	plt.text(16.55,(np.log10(((10**16.6))*np.tan(np.radians(90.-angle)))),angle,fontsize=8)'''


cbar=plt.colorbar(orientation='horizontal')
cbar.ax.set_xlabel(r"$\rm{log (C~\textsc{iv}~proportion)}$")
plt.grid()
ax.set_xlabel(r"log(x/cm)")

plt.savefig('fig5.eps',facecolor='w',edgecolor='w',bbox_inches='tight')
plt.savefig('fig5.png',facecolor='w',edgecolor='w',bbox_inches='tight')

