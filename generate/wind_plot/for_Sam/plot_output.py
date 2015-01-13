import read_sub as sub
from pylab import * 
import numpy as np 
import sys

'''
usage
 e.g. python plot_output.py sv 
'''
 

fname = sys.argv[1]



##### MAKING A WIND PLOT
# run py_wind- only need to runt his to create the files
sub.run_py_wind("77a_dev", fname)

# read electron density from the file - could also try e.g. te or ionC4
x, z, value = sub.read_pywind_smart(fname + ".ne.dat")

# make a contour plot- note that z and x are in a weird order here
# take the log with np.log10
contourf(z,x,np.log10(value) )


# make the y and x axes log!
semilogy()
semilogx()

# add a colorbar
colorbar()

# add a title and axes labels
#title("Title")
#xlabel("X")
#ylabel("Y")
#edit xlims and ylims with xlim(30,40)

show()		# show the figure

#save with 
#savefig("filename.png")

#clear figure
clf() 



##### MAKING A SPECTRUM PLOT

# read spec file
s = sub.read_spec_file(fname)

# plot the 0th element of the array which is the first viewing angle
# use the function smooth to smooth the data
plot(s.wavelength, sub.smooth(s.spec[0]) )
show()

