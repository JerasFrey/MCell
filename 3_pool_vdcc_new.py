import os

#Give the paths to the input directories
#give original path (data path) seperate from avgdir
modeldir = "output/RyR/"
modelname = "RSDr000/"
resultsdir = "results/RyR/"+modelname[:-1]+"_avg/"+"all_rels/"
dataPath = modeldir + modelname
path = modeldir + modelname

seedfolders = os.listdir(path)
seedfolders =[d for d in seedfolders if os.path.isdir(path+d)]

#refer to the output directory created with smoothing_seeds.py
avgdir = resultsdir
#Check if the average output directory exists, if not: create it
if not os.path.exists(avgdir):
    os.makedirs(avgdir)

os.system("cat " + dataPath + "/*/dat/vdcc.spont.dat > " + avgdir + "/rel_spont.dat")
os.system("cat " + dataPath + "/*/dat/vdcc.async_*.dat > " + avgdir + "/rel_async.dat")
os.system("cat " + dataPath + "/*/dat/vdcc.sync_*.dat > " + avgdir + "/rel_sync.dat")

#Sum all releases together
for i in range(len(seedfolders)):
	os.system("cat " + dataPath + seedfolders[i] + "/dat/vdcc.*.dat > " + dataPath + seedfolders[i] + "/dat/rel_all.dat")

os.system("cat " + dataPath + "/*/dat/vdcc.*.dat > " + avgdir + "/rel_all.dat")
