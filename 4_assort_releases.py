'''
time intervals of the arriving APs:
fist one: 2.5 - 22.5
second one: 22.5 - 42.5
'''
import warnings
warnings.simplefilter("ignore", Warning)

import numpy as np
import os

#Defining the right input directory
modeldir = "output/RyR/"
modelname = "RSDr000/"
path = modeldir + modelname

resultdir = "results/RyR/"+modelname[:-1]+"_avg/"+"all_rels/"

infilename = "rel_all.dat"

#Create the output filename by appending _uncumu.dat
outfilename = infilename[:-4] + "_assorted.dat"

seedfolders = os.listdir(path)
seedfolders =[d for d in seedfolders if os.path.isdir(path+d)]

ts = [2.5, 22.5]
#convert microns given by defining the vectro into nanometers
ts = [i/1000 for i in ts]

nRel = [0]*len(ts)
P = [0]*len(ts)
tc = 0.02 #for how long are you counting afer spike

for j in range(len(seedfolders)):	
	fpath = (path+seedfolders[j]+"/dat/"+infilename)
	f = open(fpath,'r')
	P = [0]*len(ts)#reset P (container for if a release has happened (1), no mattr how many releases actually happened)
	print fpath
	for line in f: 
		time = float(line.strip("\n").split(" ")[0])
		for i in range(len(ts)):
			if (time>ts[i] and time<ts[i]+tc):
				P[i] = 1
		for j in range(len(ts)):
			nRel[j] += P[j]

#make the header for the outputfile as a string with the corresponding time value of ts
#nRel = str([ts]) + [nRel]
print nRel

s = ' '.join([str(x) for x in ts])
#save the nRel vector in decimal numbers
np.savetxt(resultdir+outfilename, [nRel], header=s, fmt='%d')

#dtype=[float,float,float,float,None]

