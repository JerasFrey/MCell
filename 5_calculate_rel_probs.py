'''
time intervals of the arriving APs:
fist one: 2.5 - 22.5
second one: 22.5 - 42.5
'''
#import warnings
#warnings.simplefilter("ignore", Warning)

import numpy as np
import os
from time import time

tstart = time()

modeldir = "output/RyR/"
infilename = "rel_all.dat"
outfilename = infilename[:-4] + "_assorted.dat"

ts = [2.5, 22.5]
isi = ts[1] - ts[0]
ts = [i/1000 for i in ts]
P = [0]*len(ts)
tc = 0.02 #for how long are you counting afer spike


modelfolds = os.listdir(modeldir)
modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]

#for for loop: len(modelfolds)
for k in range(len(modelfolds)):
	print modelfolds[k]
#	tend1 = time()
#	print "Time Taken: ", tend1-tstart, " sec"
	nRel = [0]*15
	dst = modelfolds[k][-3:]
	nRel[0] = int(dst)
	resultdir = "results/RyR/"+modelfolds[k]+"_avg/"+"all_rels/"
	seedfolders = os.listdir(modeldir+modelfolds[k]+"/")
	seedfolders = [d for d in seedfolders if os.path.isdir(modeldir+modelfolds[k]+"/"+d)]
	for j in range(len(seedfolders)):	
		fpath = (modeldir+modelfolds[k]+"/"+seedfolders[j]+"/dat/"+infilename)
		f = open(fpath,'r')
		P = [0]*len(ts)#reset P (container for if a release has happened (1), no mattr how many releases actually happened)
		Q = [0]*len(ts)
		for line in f: 
			time = float(line.strip("\n").split(" ")[0])
			for i in range(len(ts)):
				if (time>ts[i] and time<ts[i]+tc):
					Q[i] += 1
					P[i] = 1
		if (P==[0,0]):
			nRel[1] += 1
		if (P==[1,0]):
			nRel[2] += 1
		if (P==[0,1]):
			nRel[3] += 1
		if (P==[1,1]):
			nRel[4] += 1
		for j in range(len(ts)):
			nRel[j+5] += Q[j]
			
		
	nRel[7] = (float(nRel[1]) / (nRel[1] + nRel[3])) #P00 = N00 / N00 + N01
	nRel[8] = (float(nRel[2]) / (nRel[2] + nRel[4])) #P10 = N10 / N10 + N11
	nRel[9] = (float(nRel[3]) / (nRel[3] + nRel[1])) #P01 = N01 / N01 + N00?
	nRel[10] = (float(nRel[4]) / (nRel[4] + nRel[2])) #P11 = N11 / N11 + N10
	
	nRel[11] = ((float(nRel[2])+nRel[4]) / len(seedfolders))#P1 = N10 + N11 / no. seedfolders
	nRel[12] = ((float(nRel[3])+nRel[4]) / len(seedfolders))#P2 = N01 + N11 / no. seedfolders
	
	nRel[13] = ((float(nRel[12]) / nRel[11]))#PPF = P2/P1
	print(nRel[1]+nRel[2]+nRel[3]+nRel[4])
	
	nRel[14] = isi
	s = "Distance N00 N10 N01 N11 N1 N2 P00 P10 P01 P11 P1 P2 PPF ISI"
	np.savetxt(resultdir+outfilename, [nRel], header=s, fmt=('%d', '%d', '%d', '%d', '%d', '%d', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%d'))
	
tend = time()
print "Time Taken Final: ", tend-tstart, " sec"
