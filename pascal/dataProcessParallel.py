#!/usr/bin/python
	
import multiprocessing as mp, os, sys
from time import time
from modFunc import *

#	define function to be parallelised	
def runAnalysis(dataDirName):
	
	ts = time()
	dataPath = "/media/nishant/4tb/output/c1000/2r/" + dataDirName
	#dataPath = "/media/nishant/4tb/output/c250/c250/" + dataDirName
	#dataPath = "/home/nishant/output/c250/" + dataDirName

	resultPath = "/home/nishant/Dropbox/labDocuments/results/c1000/2r/" + dataDirName
	
	if not os.path.exists(resultPath):
		os.makedirs(resultPath)
	
	print "\n\ndataPath : ", dataPath
	print "resultPath : ", resultPath

	ns = analysis(dataPath, resultPath)
	'''
	ns.avg_dat(inFile="/dat/ca.dat", outFile="/ca.dat")
	ns.conc_calc(5, inFile="/ca.dat", outFile="/CaConc")
	ns.avg_dat(inFile="/dat/rrp.dat", outFile="/rrp.dat")
	
	ns.avg_dat(inFile="/dat/vdcc_pq_ca_flux.dat", outFile="/vdccCaFlux.dat")
	ns.fluxCurrent(inFile="/vdccCaFlux.dat", outFile="/vdccCaFluxRate.dat")
	ns.avg_dat(inFile="/dat/pmca&leak_ca_flux.dat", outFile="/pmca_leak.dat")
	ns.avg_dat(inFile="/dat/calbindin_mol.dat", outFile="/calB.dat")

	ns.avg_dat(inFile="/dat/serca_ca_flux.dat", outFile="/sercaCaFlux.dat")
	ns.avg_dat(inFile="/dat/serca_mol.dat", outFile="/sercaMol.dat")
	
	ns.avg_dat(inFile="/dat/ryr_ca_flux.dat", outFile="/ryrCaFlux.dat")
	ns.avg_dat(inFile="/dat/ryr_mol.dat", outFile="/ryrMol.dat")
	ns.fluxCurrent(inFile="/ryrCaFlux.dat", outFile="/ryrCaFluxRate.dat", line=2)
	
	ns.avg_dat(inFile="/dat/ip3.dat", outFile="/ip3.dat")
	ns.avg_dat(inFile="/dat/ip3_create.dat", outFile="/ip3Create.dat")
	ns.avg_dat(inFile="/dat/ip3r_open.dat", outFile="/ip3rOpen.dat")
	ns.avg_dat(inFile="/dat/ip3r_ca_flux.dat", outFile="/ip3rCaFlux.dat")
	ns.fluxCurrent(inFile="/ip3rCaFlux.dat", outFile="/ip3rCaFluxRate.dat")
	ns.avg_dat(inFile="/dat/mglur.dat", outFile="/mglur.dat")
	ns.avg_dat(inFile="/dat/plc.dat", outFile="/plc.dat")
	ns.avg_dat(inFile="/dat/glu.dat", outFile="/glu.dat")
	'''

	# For PPF
	
	pls1 = 2.5
	isi = float(dataDirName.split("SI")[1].split("V")[0])
	vdcc = dataDirName.split("V")[1]
	ns.relppf([pls1, pls1+isi], vdcc)
	'''
	# For PTP
	s = dataDirName.split("_")
	n = int(s[1])
	isi = 1000/float(s[2].split("hz")[0])
	if "ms" in s[3]:
		ptd = float(s[3].split("ms")[0])
	else:
		ptd = float(s[3].split("s")[0])*1000
	ns.relptp([n, isi, ptd])
	ns.plotAll(dataDirName,colorScheme = 'white')
	'''
	
	te = time()
	print "Time Taken: ", te-ts, " sec"

if __name__ == "__main__":
	
	var = os.listdir("/media/nishant/4tb/output/c1000/2r/")
	var = [d for d in var if "RSI" in d]
	#var = ['RSI200V80', 'RSI150V80', 'RSI125V80']
	print var, len(var)
	
	# Define an output queue
	output = mp.Queue()
	# Setup a list of processes that we want to run
	processes = [mp.Process(target=runAnalysis, args=(v,)) for v in var]
	# Run processes
	for p in processes:
		p.start()
	# Exit the completed processes
	for p in processes:
		p.join()
		
	'''
	r = "/home/nishant/Dropbox/labDocuments/results/c1000/"
	dfilename = 'RSdata.dat'
	dfile = open(r + dfilename, 'w')
	dfile.write("#N00\tNs10\tN01\tN11\tN1\tN2\tNtot\tP00\tP10\tP01\tP11\tP1\tP2\tPPF\tISI(ms)\tVDCC\n#")
	for i in range(16): dfile.write(str(i)+"\t")
	dfile.write("\n\n")
	dfile.close()
	
	for d in var:
		os.system("cd " + r + "; cat " + d + "/result >> " + dfilename)
	'''
