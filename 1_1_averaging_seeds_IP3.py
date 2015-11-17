from time import time
import numpy as np
import os

tstart = time()

#Give the paths to the output directories
modeldir = "output/IP3_100/"
resultsdir = "results/IP3_100/"

#Get all different seeds by getting the names of all folders (= s_0000x) each containing a different seed

#Put in here all file names that should be averaged in the end
filelist = ['ca.dat','ip3.dat','ip3r_open.dat','ip3r_ca_flux.dat','rrp.dat']
#Check if the average output directory exists, if not: create it
#if not os.path.exists(avgdir):
#    os.makedirs(avgdir)

#2 for-loops:
#	f is iterating through the vector called filelist to apply the i loop on every file in filelist by loading the file into the rxn_data vector
#		i is iterating through all existing seed folders in the output directory
#		with += it adds up all values in each row and column of the documents with the same name in all existing seed folders
#	after iterating through i, with /= all the data in all columns and rows is divided by the number of existing seed folders in the output directory and saved before getting to the next entry in the filelist

modelfolds = os.listdir(modeldir)
modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]

#print(os.listdir(modeldir+modelfolds[0]+"/"+seedfolders[0]+"/dat/"))

for k in range(len(modelfolds)):
	print modelfolds[k]
	tend1 = time()
	print "Time Taken: ", tend1-tstart, " sec"
	if not os.path.exists(resultsdir+modelfolds[k]+"_avg/"):
		os.makedirs(resultsdir+modelfolds[k]+"_avg/")
	for f in filelist:
		path1 = modeldir+modelfolds[k]+"/"
		seedfolders = os.listdir(path1)
		seedfolders =[d for d in seedfolders if os.path.isdir(path1+d)]
		outfilename = f[:-4] + "_avg.dat"
		rxn_data = np.genfromtxt(modeldir+modelfolds[k]+"/"+seedfolders[0]+"/dat/"+f, dtype=float)

		for i in range(1,len(seedfolders)):
			rxn_data += np.genfromtxt(modeldir+modelfolds[k]+"/"+seedfolders[i]+"/dat/"+f, dtype=float)

		rxn_data /= len(seedfolders)
		np.savetxt(resultsdir+modelfolds[k]+"_avg/"+outfilename, rxn_data)
tend = time()
print("Time Taken Final: "+tend-tstart+" sec")
