'''
time intervals of the arriving APs:
fist one: 2.5 - 22.5
second one: 22.5 - 42.5
'''
#import warnings
#warnings.simplefilter("ignore", Warning)

import numpy as np
import os

modeldir = "output/RyR/"
infilename = "rel_all.dat"
outfilename = infilename[:-4] + "_assorted.dat"

ts = [2.5, 22.5]
ts = [i/1000 for i in ts]
P = [0]*len(ts)
tc = 0.02 #for how long are you counting afer spike


modelfolds = os.listdir(modeldir)
modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]

for k in range(len(modelfolds)):
	print modelfolds[k]
	nRel = [0]*len(ts)
	resultdir = "results/RyR/"+modelfolds[k]+"_avg/"+"all_rels/"
	seedfolders = os.listdir(modeldir+modelfolds[k]+"/")
	seedfolders = [d for d in seedfolders if os.path.isdir(modeldir+modelfolds[k]+"/"+d)]
	for j in range(len(seedfolders)):	
		fpath = (modeldir+modelfolds[k]+"/"+seedfolders[j]+"/dat/"+infilename)
		f = open(fpath,'r')
		P = [0]*len(ts)#reset P (container for if a release has happened (1), no mattr how many releases actually happened)
		for line in f: 
			time = float(line.strip("\n").split(" ")[0])
			for i in range(len(ts)):
				if (time>ts[i] and time<ts[i]+tc):
					P[i] = 1
			for j in range(len(ts)):
				nRel[j] += P[j]
	print nRel
	s = ' '.join([str(x) for x in ts])
	np.savetxt(resultdir+outfilename, [nRel], header=s, fmt='%d')
