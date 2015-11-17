from time import time
import numpy as np
import multiprocessing as mp
import os

tstart = time()

modeldir = "output/IP3/"

modelfolds = os.listdir(modeldir)
modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]


def pool(currfold):
	print(currfold)
	tend1 = time()
	print "Time Taken: ", tend1-tstart, " sec"
	seedfolders = os.listdir(modeldir+currfold+"/")
	seedfolders =[d for d in seedfolders if os.path.isdir(modeldir+modelfolds[j]+"/"+d)]
	
	resultsdir = "results/IP3/"+modelfolds[j]+"_avg/"+"all_rels/"
	if not os.path.exists(resultsdir):
		os.makedirs(resultsdir)
	dataPath = modeldir+modelfolds[j]+"/"
	
	os.system("cat " + dataPath + "/*/dat/vdcc.spont.dat > " + resultsdir + "/rel_spont.dat")
	os.system("cat " + dataPath + "/*/dat/vdcc.async_*.dat > " + resultsdir + "/rel_async.dat")
	os.system("cat " + dataPath + "/*/dat/vdcc.sync_*.dat > " + resultsdir + "/rel_sync.dat")
	
	dataPath = modeldir+modelfolds[j]+"/"
	for i in range(len(seedfolders)):
		os.system("cat " + dataPath + seedfolders[i] + "/dat/vdcc.*.dat > " + dataPath + seedfolders[i] + "/dat/rel_all.dat")


print "Time Taken Final: ", tend-tstart, " sec"
