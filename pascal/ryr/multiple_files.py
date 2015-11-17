import multiprocessing as mp, os, sys

'''
mdlFile = sys.argv[1]
mdlFile1 = sys.argv[2]
mdlFile2 = sys.argv[3]
'''
output = mp.Queue()

def runmdl(mdlFile):
	os.system("mcell %s -logfreq 1000 seed 10" % (mdlFile))

path = "./"
mdlFile = os.listdir(path)
mdlFile =[d for d in mdlFile if "RSDr" in d]

processes = [mp.Process(target=runmdl, args=(f,)) for f in mdlFile[0:2]]

for p in processes:
	p.start()

for p in processes:
	p.join()

results = [output.get() for p in processes]

print(results)
sys.exit()

