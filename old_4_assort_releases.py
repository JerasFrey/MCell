'''
time intervals of the arriving APs:
fist one: 2.5 - 22.5
second one: 22.5 - 42.5
'''

import numpy as np
import os

#Defining the right input directory
modeldir = "results/RyR/"
modelname = "RSDr000_avg/"
path = modeldir + modelname

infilename = "rel_all.dat"

#Create the output filename by appending _uncumu.dat
outfilename = infilename[:-4] + "_assorted.dat"


ts = [2.5, 22.5]
#convert microns given by defining the vectro into nanometers
ts = [i/1000 for i in ts]

nRel = [0]*len(ts)
P = [0]*len(ts)

#read in the file where all releases were collected
rxn_rel = np.genfromtxt(path+infilename, dtype=None)

### for one file, do:
	for i in range(len(rxn_rel)):
		for f in range(len(ts)):
			if rxn_rel[i][0] >= ts[f] and rxn_rel[i][0] <= ts[f]+0.02:
				P[f] = 1
	for j in len(ts):
		nRel[j] += P[j]


#read in the file where all releases were collected
rxn_rel = np.genfromtxt(path+infilename, dtype=None)

#go through all releases
#for each spike that is between pairwise called values given in the ts list, add +1 to the nRel vector at the corresponding position, correlating to the ts list
for i in range(len(rxn_rel)):
	for f in range(len(ts)):
		if rxn_rel[i][0] >= ts[f] and rxn_rel[i][0] <= ts[f]+0.02:
			nRel[f] += 1

#make the header for the outputfile as a string with the corresponding time value of ts
#nRel = str([ts]) + [nRel]
s = ' '.join([str(x) for x in ts])
#save the nRel vector in decimal numbers
np.savetxt(path+outfilename, [nRel], header=s, fmt='%d')

#dtype=[float,float,float,float,None]
