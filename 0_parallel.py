from time import time
import numpy as np
import multiprocessing as mp
import os

#Give the paths to the output directories
setting = "IP3_100"
filelist = ['ca.dat','ip3.dat','ip3r_open.dat','ip3r_ca_flux.dat','rrp.dat']
skipped_lines = 5

modeldir = "output/"+setting+"/"
resultsdir = "results/"+setting+"/"

modelfolds = os.listdir(modeldir)
modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]

def avg(currfold):
	# Averaging
	print currfold
	tstart = time()
	if not os.path.exists(resultsdir+currfold+"_avg/"):
		os.makedirs(resultsdir+currfold+"_avg/")
	for f in filelist:
		path1 = modeldir+currfold+"/"
		seedfolders = os.listdir(path1)
		seedfolders =[d for d in seedfolders if os.path.isdir(path1+d)]
		outfilename = f[:-4] + "_avg.dat"
		rxn_data = np.genfromtxt(modeldir+currfold+"/"+seedfolders[0]+"/dat/"+f, dtype=float)

		for i in range(1,len(seedfolders)):
			rxn_data += np.genfromtxt(modeldir+currfold+"/"+seedfolders[i]+"/dat/"+f, dtype=float)

		rxn_data /= len(seedfolders)
		np.savetxt(resultsdir+currfold+"_avg/"+outfilename, rxn_data)
		
	# Uncumulating
	infilename = "ca_avg.dat"
	outfilename = infilename[:-4] + "_uncumu.dat"
	rxn_conc = np.genfromtxt(resultsdir+currfold+"_avg/"+infilename, dtype=float)
	rxn_conc_new = []
	
	for i in range(skipped_lines,len(rxn_conc),skipped_lines):
		rxn_conc_new.append([rxn_conc[i][0], 
	
	#implement the following formular to reverse the MCell formular <ESTIMATE_CONC> by calculating:
	#	time(t)i * concentration(c)i - t(i-steps) * c(i-steps) / ti - ti-steps
		(((rxn_conc[i][0] * rxn_conc[i][1]) - (rxn_conc[(i-skipped_lines)][0] * rxn_conc[(i-skipped_lines)][1])) /
		 (rxn_conc[i][0] - rxn_conc[(i-skipped_lines)][0]))])

	np.savetxt(resultsdir+currfold+"_avg/"+outfilename, rxn_conc_new, fmt=['%.6f','%.3f'])
		
	tend = time()
	print "Time taken for " + currfold + ": " + str(tend-tstart) + " sec"


# Define an output queue
output = mp.Queue()
# Setup a list of processes that we want to run
processes = [mp.Process(target=avg, args=(currfold,)) for currfold in modelfolds]
# Run processes
for p in processes:
	p.start()
# Exit the completed processes
for p in processes:
	p.join()
