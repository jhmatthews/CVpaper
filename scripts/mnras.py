

import sys
import numpy as np
filename = sys.argv[1]
outfilename = sys.argv[2]


texfile =  open(filename, "r")
outfile = open(outfilename, "w")


outfile.write("\documentclass[useAMS,usenatbib]{mn2ejm}\n")

for line in texfile:
	if "begin{abstract}" in line:
		outfile.write("\maketitle\n")
		outfile.write(line)

	elif "documentclass" not in line and "maketitle" not in line:
		outfile.write(line)

outfile.close()
