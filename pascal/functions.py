#!/usr/bin/python

from pylab import *
import os, sys

class analysis:
	
	#	Set dataPath and resultPath
	def __init__(self, dp, rp):
		self.dataPath = dp
		self.resultPath = rp
		self.RP = 0
		
	#	Get list of directories in the path starting with 's_'
	def getDirs(self, path, sstr='s_'):
		dirs = [ d for d in os.listdir(path) if os.path.isdir(path + '/' + d) and sstr in d ]
		dirs.sort()
		return(dirs)

	#	Get data from dataFile in array
	def getData(self, dataFile):
		data = []
		f = open(dataFile, "r")

		for l in f:
			if not l.startswith('#'): data.append([float(x) for x in l.strip('\n').strip(" ").split(" ")])
		return (data)

	#	Average Over all Seeds
	def avg_dat(self, inFile="/dat/ca.dat", outFile="/ca.dat", err=False):
		print "\nCalculating Average..."
		# Get list of directories in data path
		dirs = self.getDirs(self.dataPath)
		self.seeds = len(dirs)
		
		avg = []	
		for d in dirs:
			dataFile = self.dataPath + "/" + d + inFile
			data = self.getData(dataFile)

			if len(avg) == 0:
				avg = data
			else:
				for j in range(len(data)):
					for k in range(1,len(data[0])):
						avg[j][k] += data[j][k]
						
		for j in range(len(avg)):
			for k in range(1,len(data[0])):
				avg[j][k] = float(avg[j][k])/float(self.seeds)
		
		'''
		# Calc Error
		if err:
			s = [0]*2
			avgErr = []
			for d in dirs:
				dataFile = self.dataPath + "/" + d + inFile
				data = self.getData(dataFile)
				
				if len(avgErr) == 0:
					avgErr = [[0]*len(data[0])]*len(data)
				else:
					for j in range(len(data)):
						for k in range(1,len(data[0])):
							avgErr[j][k] += (avg[j][k] - data[j][k])**2
							if (j==199 or j==200 and k==1): 
								s[j-199] += (avg[j][k] - data[j][k])**2
								print avgErr[j][k], data[j][k], (avg[j][k] - data[j][k])**2, s
			
			
			for j in range(len(avgErr)):
				for k in range(1,len(avgErr[0])):
					avgErr[j][k] = sqrt(float(avgErr[j][k])/float(self.seeds))
			
		'''
		of = self.resultPath + outFile
		print "\nWriting average to: " + of
		outfile = open(of,'w')
		for j in range(len(avg)):
			avgline = ""
			for k in range(1,len(data[0])):
				avgline += str(avg[j][k]) + " "# + str(avgErr[j][k]) + " "
			outfile.write('%g %s\n' % (avg[j][0],avgline))
		outfile.close()
		
	#	Ca Concentration Calculation
	def conc_calc(self, step, inFile="/ca.dat", outFile="/CaConc"):
		data = self.getData(self.resultPath + inFile)

		print "Calculating Calcium Concentration..."
		c_tc = []
		c_out = []
		for i in range(len(data)):
			c_tc.append(data[i][0]*data[i][1])
		dt=step*(data[1][0]-data[0][0])
		for i in range(0,len(data)-step-1,step):
			c_out.append((data[i][0], (c_tc[i+step]-c_tc[i])/dt))
		  
		print "Writing Ca Conc. to file:" + outFile
		outfile = open(self.resultPath + outFile, 'w')
		for j in range(len(c_out)):
			outfile.write('%g %g\n' % (c_out[j][0],c_out[j][1]))
		outfile.close()
	
	#	Get Vesicle Release Statistics for PPF
	def relppf(self, ts, vdcc, tc=0.02):
		isi = (ts[1]-ts[0])
		ts = [i/1000.0 for i in ts]
		
		nRel = [0]*(len(ts)+4) # [P00, P01, P10, P11, Rel1, Rel2,... Reln] 
		dirs = self.getDirs(self.dataPath)	
		for d in [(self.dataPath + '/' + dir + '/dat/') for dir in dirs]:
			os.system("cd " + d + "; cat vdcc.* > rel.dat")
			
			fpath = (d + "/rel.dat")
			f = open(fpath,'r')
			
			#	Get no. of vesicles released after AP specified by ts
			p = [0, 0]	
			for line in f: 
				time = float(line.strip("\n").split(" ")[0])

				for i in range(len(ts)):
					if (time>ts[i] and time<ts[i]+tc):
						p[i] = 1
						nRel[4+i] += 1

			#	Calculate Conditional Release Probabilities			
			if(p[0]==0 and p[1] ==0): nRel[0] += 1
			if(p[0]==1 and p[1] ==0): nRel[1] += 1
			if(p[0]==0 and p[1] ==1): nRel[2] += 1
			if(p[0]==1 and p[1] ==1): nRel[3] += 1
		
		os.system("cat " + self.dataPath + "/*/dat/rel.dat > " + self.resultPath + "/vesRel")
		os.system("cat " + self.dataPath + "/*/dat/vdcc.async_*.dat > " + self.resultPath + "/asyncRel")
		os.system("cat " + self.dataPath + "/*/dat/vdcc.sync_*.dat > " + self.resultPath + "/syncRel")
		
		nRel.append(nRel[0]+nRel[1]+nRel[2]+nRel[3]) # nRel[6] = N_tot
		nRel.append(float(nRel[0])/(float(nRel[0])+float(nRel[2]))) # nRel[7] = P00
		nRel.append(float(nRel[1])/(float(nRel[1])+float(nRel[3]))) # nRel[8] = P10
		nRel.append(float(nRel[2])/(float(nRel[0])+float(nRel[2]))) # nRel[9] = P01
		nRel.append(float(nRel[3])/(float(nRel[1])+float(nRel[3]))) # nRel[10] = P11
		nRel.append((float(nRel[1])+float(nRel[3]))/float(nRel[6])) # nRel[11] = P1
		nRel.append((float(nRel[2])+float(nRel[3]))/float(nRel[6])) # nRel[12] = P2
		nRel.append(float(nRel[12])/float(nRel[11])) # nRel[13] = PPF
		nRel.append(int(isi)) # nRel[14] = isi
		nRel.append(int(vdcc)) # nRel[15] = vdcc
		
		#	Print Results
		r = open(self.resultPath + '/result', 'w')
		print nRel
		for a in nRel:
			if not isinstance(a,int):
				r.write(format(a,'.2')+"\t")
			else:
				r.write(str(a)+"\t")
		r.write("\n")

	#	Get Vesicle Release Statistics for PTP
	def relptp(self, ts, tc=0.02):
		
		ts = [i/1000.0 for i in ts]
		nRel = [0]*(len(ts)) # [Rel1, Rel2,... Reln] 
		dirs = self.getDirs(self.dataPath)	
		for d in [(self.dataPath + '/' + dir + '/dat/') for dir in dirs]:
			os.system("cd " + d + "; cat vdcc.* > rel.dat")
			
			fpath = (d + "/rel.dat")
			f = open(fpath,'r')

			#	Get no. of vesicles released after AP specified by ts
			for line in f: 
				time = float(line.strip("\n").split(" ")[0])
				for i in range(len(ts)):
					if (time>ts[i] and time<ts[i]+tc):
						nRel[i] += 1
		
		os.system("cat " + self.dataPath + "/*/dat/rel.dat > " + self.resultPath + "/vesRel")
		os.system("cat " + self.dataPath + "/*/dat/vdcc.async_*.dat > " + self.resultPath + "/asyncRel")
		os.system("cat " + self.dataPath + "/*/dat/vdcc.sync_*.dat > " + self.resultPath + "/syncRel")
		
		#	Print Results
		r = open(self.resultPath + '/result', 'w')
		self.PTP = float(nRel[1])/float(nRel[0])
		r.write("P1\tP2\tPTP\n")
		r.write(str(nRel[0])+"\t"+str(nRel[1])+"\t"+format(self.PTP, '.2f'))

		print "\nP1\tP2\tPPF\t\n", nRel, format(self.PTP, '.2f')
	
	#	Plot all 
	def plotAll(self, dataDirName, colorScheme = 'black'):
		# These are the "Tableau 20" colors as RGB.  
		tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
				     (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
				     (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
				     (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
				     (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
		  
		# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
		for i in range(len(tableau20)):  
			r, g, b = tableau20[i]  
			tableau20[i] = (r / 255., g / 255., b / 255.) 
		# Check which Components were there in the Simulation
		chkSim = ""
		if dataDirName.find("NS") != -1:
			chkSim = "N"
		else:
			if dataDirName.find("I") != -1: chkSim += "I"
			if dataDirName.find("S") != -1: chkSim += "S"
			if dataDirName.find("R") != -1: chkSim += "R"

		# Global Settings
		rcParams['figure.figsize'] = 11, 13
		colorScheme = 'black'
		nSubPlots = [7,2]
		f, ax = subplots(*nSubPlots, sharex='col')

		subplots_adjust(left=None, bottom=0.05, right=0.95, top=0.98, wspace=0.4, hspace=None)
		if colorScheme == 'black':
			f.patch.set_facecolor('black')
			#f.patch.set_alpha(1)
		
			# Settings for Texts and Axes
			txtcolor = 'white'
			axiscolor = '#777777'
			titlecolor = 'orange'
		
			# Color set for plots
			avgcolor = 'r'
			onecolor = '#0077ff'
			allcolor = '#292929'
			cumulcolor = '#cc2299'
		
		elif colorScheme == 'white':
			f.patch.set_facecolor('white')
			# Settings for Texts and Axes
			txtcolor = 'black'
			axiscolor = '#777777'
			titlecolor = 'orange'
		
			# Color set for plots
			avgcolor = 'r'
			onecolor = 'g'
			allcolor = '#cccccc'
		
		for i in range(nSubPlots[0]):
			for j in range(nSubPlots[1]):
				ax[i,j].locator_params(nbins=3)
		
				ax[i,j].spines["top"].set_visible(False)
				ax[i,j].spines["right"].set_visible(False)
				
				ax[i,j].get_xaxis().tick_bottom()  
				ax[i,j].get_yaxis().tick_left()
				
				ax[i,j].patch.set_facecolor('black')
				ax[i,j].patch.set_alpha(0.0)
				
				ax[i,j].spines['bottom'].set_color(axiscolor)
				ax[i,j].spines['left'].set_color(axiscolor)
				
				ax[i,j].tick_params(axis='x', colors=axiscolor)
				ax[i,j].tick_params(axis='y', colors=axiscolor)

				ax[i,j].yaxis.label.set_color(txtcolor)
				ax[i,j].xaxis.label.set_color(txtcolor)
				
				ax[i,j].title.set_color(titlecolor)
		
		ax[-1,0].set_xlabel('Time (sec)')
		ax[-1,1].set_xlabel('Time (sec)')
		
		labelfont = 10
		matplotlib.rcParams.update({'font.size': 8})
		lw = 1.0 # linewidth
		
		
		dirs = self.getDirs(self.dataPath)
		row = 0
		col = 0
		
		# Avg. cytosol [Ca]		
		lCaData = genfromtxt(self.resultPath + '/CaConc')
		gCaData = genfromtxt(self.resultPath + '/ca.dat')
		ax[row,col].plot(lCaData[:,0], lCaData[:,1], lw=lw, color=avgcolor) # Local [Ca]
		#ax[row,col].plot(gCaData[:,0], [i/602.3 for i in gCaData[:,2]], lw=lw, color='r') # Global [Ca]
		ax[row,col].set_ylabel('[Ca$^{2+}$]$_{cyt}$ ($\mu$M)',fontsize=labelfont)
			
		# Glu (num) 
		if chkSim.find("I") != -1:
			row += 1
			gluData = genfromtxt(self.dataPath + '/' + dirs[0] + '/dat/glu.dat')
			ax[row,col].plot(gluData[:,0], gluData[:,1], lw=lw, color=onecolor)
			ax[row,col].set_ylabel('[Glu] (num)',fontsize=labelfont)
		
		
		# Raster Plot of Vesicle Release
		if chkSim.find("I") == -1:
			row += 1
			events = []
			for d in [(self.dataPath + '/' + dir + '/dat/') for dir in dirs]:
				fname = open(d + "/rel.dat",'r')
				eventTime = []
				for line in fname: 
					t = float(line.strip("\n").split(" ")[0])
					eventTime.append(t)
				events.append(eventTime)

			for ith, trial in enumerate(events):
				ax[row,col].vlines(trial, ith, ith + 1, color='g',lw=lw)
				ax[row,col].set_ylim(0.0, len(events))
			ax[row,col].set_ylabel('Trial no.',fontsize=labelfont)
		
		# Vesicle Release Histogram
		row += 1
		vesRelData = genfromtxt(self.resultPath + '/vesRel')
		syncRelData = genfromtxt(self.resultPath + '/syncRel')
		asyncRelData = genfromtxt(self.resultPath + '/asyncRel')
		n, bins, patches = ax[row,col].hist([syncRelData[:,0],asyncRelData[:,0]], 50, color=['r','g'], stacked=True)
		ax[row,col].set_ylabel('Vesicles (num)',fontsize=labelfont)
		
		
		# RRP (num)
		row += 1
		for i in range(20,0,-1):
			rrpData = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/rrp.dat')
			if i==1:
				ax[row,col].plot(rrpData[:,0], rrpData[:,1], lw=lw, color=onecolor)
			else:
				ax[row,col].plot(rrpData[:,0], rrpData[:,1], lw=lw, color=allcolor)
		
		rrpData = genfromtxt(self.resultPath + '/rrp.dat')
		#ax[row,col].fill_between(data[:,0], data[:,1] - data[:,2], data[:,1] + data[:,2], color="#3F5D7D")
		ax[row,col].plot(rrpData[:,0], rrpData[:,1], lw=lw, color=avgcolor)
		ax[row,col].set_ylabel('RRP (num)',fontsize=labelfont)
		
		
		# Extra Ca Bound to Serca
		if chkSim.find("S") != -1:
			row += 1
			sercaData = genfromtxt(self.resultPath + '/sercaMol.dat')
			boundCa = [i[2]+i[5]+(i[3]+i[4])*2-2170 for i in sercaData]
			ax[row,col].plot(sercaData[:,0], boundCa, lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('SERCA-Bound Ca$^{2+}$ (num)',fontsize=labelfont)
			
		# Open RyR
		if chkSim.find("R") != -1:
			row += 1
			for j in range(20,0,-1):
				ryrMolData = genfromtxt(self.dataPath + '/' + dirs[j] + '/dat/ryr_mol.dat')
				if j==1:
					ax[row,col].plot(ryrMolData[:,0], [i[6]+i[7]+(i[8]+i[13]+i[14]) for i in ryrMolData], lw=lw, color=onecolor)
				else:
					ax[row,col].plot(ryrMolData[:,0], [i[6]+i[7]+(i[8]+i[13]+i[14]) for i in ryrMolData], lw=lw, color=allcolor)
		
			openIp3rData = genfromtxt(self.resultPath + '/ryrMol.dat')
			ax[row,col].plot(ryrMolData[:,0], [i[6]+i[7]+(i[8]+i[13]+i[14]) for i in ryrMolData], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('Open RyR (num)',fontsize=labelfont)
		
		# [IP3]
		if chkSim.find("I") != -1:
			row += 1
			for i in range(20,0,-1):
				ip3Data = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/ip3.dat')
				if i==1:
					ax[row,col].plot(ip3Data[:,0], [i/602.3 for i in ip3Data[:,1]], lw=lw, color=onecolor)
				else:
					ax[row,col].plot(ip3Data[:,0], [i/602.3 for i in ip3Data[:,1]], lw=lw, color=allcolor)
		
			ip3Data = genfromtxt(self.resultPath + '/ip3.dat')
			ax[row,col].plot(ip3Data[:,0], [i/602.3 for i in ip3Data[:,1]], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('[IP3] ($\mu$M)',fontsize=labelfont)
		
		row = 0
		col += 1
		# Avg. ER [Ca]
		if chkSim.find("N") == -1:
			ax[row,col].plot(gCaData[:,0], [i/24.5 for i in gCaData[:,3]], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('[Ca$^{2+}$]$_{ER}$ ($\mu$M)',fontsize=labelfont)
		
		# Open IP3R
		if chkSim.find("I") != -1:
			row += 1
			for i in range(20,0,-1):
				openIp3rData = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/ip3r_open.dat')
				if i==1:
					ax[row,col].plot(openIp3rData[:,0], openIp3rData[:,1], lw=lw, color=onecolor)
				else:
					ax[row,col].plot(openIp3rData[:,0], openIp3rData[:,1], lw=lw, color=allcolor)
		
			openIp3rData = genfromtxt(self.resultPath + '/ip3rOpen.dat')
			ax[row,col].plot(openIp3rData[:,0], openIp3rData[:,1], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('Open IP3R (num)',fontsize=labelfont)
		
		# Ca flux from IP3R
		if chkSim.find("I") != -1:
			row += 1
			ip3rCaFluxData = genfromtxt(self.resultPath + '/ip3rCaFlux.dat')
			ax[row,col].plot(ip3rCaFluxData[:,0], ip3rCaFluxData[:,1], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('IP3R Ca Flux (num)',fontsize=labelfont)
			
		# Ca flux from RyR
		if chkSim.find("R") != -1:
			row += 1
			ryrCaFluxRateData = genfromtxt(self.resultPath + '/ryrCaFluxRate.dat')
			ryrCaFluxData = genfromtxt(self.resultPath + '/ryrCaFlux.dat')
			
			ax[row,col].plot(ryrCaFluxData[:,0],ryrCaFluxData[:,1], lw=lw, color=cumulcolor)
			ax[row,col].plot(ryrCaFluxData[:,0],ryrCaFluxData[:,2], lw=lw, color=cumulcolor)
			ax[row,col].plot(ryrCaFluxData[:,0],ryrCaFluxData[:,1]-ryrCaFluxData[:,2], lw=lw, color='g')
			ax[row,col].set_ylabel('RyR Ca Flux (num)', fontsize=labelfont)
			
			'''
			axtwin = ax[row,col].twinx()
			axtwin.spines["right"].set_visible(True)
			axtwin.spines['right'].set_color(axiscolor)
			axtwin.get_yaxis().tick_right()
			axtwin.tick_params(axis='y', colors=axiscolor)
			axtwin.yaxis.label.set_color(txtcolor)
			axtwin.plot(ryrCaFluxRateData[:,0],[i/1000 for i in ryrCaFluxRateData[:,1]], lw=lw, color=onecolor)
			axtwin.plot(ryrCaFluxRateData[:,0],[i/1000 for i in ryrCaFluxRateData[:,2]], lw=lw, color=avgcolor)
			axtwin.set_ylabel('RyR Ca Flux (num/ms)', fontsize=labelfont, color=cumulcolor)
			'''
		
		# Ca flux from VDCC
		if chkSim.find("I") == -1:
			row += 1
			vdccCaFluxData = genfromtxt(self.resultPath + '/vdccCaFluxRate.dat')
			ax[row,col].plot(vdccCaFluxData[:,0],[i/1000 for i in vdccCaFluxData[:,1]], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('vdcc Ca Flux (num/ms)',fontsize=labelfont)
		
			
		# Cumulative Ca flux from VDCC
		if chkSim.find("I") == -1:
			row += 1
			vdccCaFluxData = genfromtxt(self.resultPath + '/vdccCaFlux.dat')
			ax[row,col].plot(vdccCaFluxData[:,0], vdccCaFluxData[:,1], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('vdcc Ca Flux (num/ms)',fontsize=labelfont)
		
		# No. of IP3 Produced via mGluR Pathway
		if chkSim.find("I") != -1:
			row += 1
			for i in range(20,0,-1):
				ip3cData = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/ip3_create.dat')
				if i==1:
					ax[row,col].plot(ip3cData[:,0], ip3cData[:,1], lw=lw, color=onecolor)
				else:
					ax[row,col].plot(ip3cData[:,0], ip3cData[:,1], lw=lw, color=allcolor)
		
			ip3cData = genfromtxt(self.resultPath + '/ip3Create.dat')
			ax[row,col].plot(ip3cData[:,0], ip3cData[:,1], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('IP3 Produced (num)',fontsize=labelfont)
		
		# SERCA States
		if chkSim.find("S") != -1:
			row += 1
			sercaData = genfromtxt(self.resultPath + '/sercaMol.dat')
			for i in range(1,7):
				ax[row,col].plot(sercaData[:,0], sercaData[:,i], lw=lw, color=tableau20[2*i])
			ax[row,col].set_ylabel('SERCA States (num)',fontsize=labelfont)
			
		# Cumulative Ca Leak from PMCA
		
		if chkSim.find("S") != -1:
			row += 1
			pmcaData = genfromtxt(self.resultPath + '/pmca_leak.dat')
			ax[row,col].plot(pmcaData[:,0], [(i[1]-i[2]) for i in pmcaData], lw=lw, color=avgcolor)
			ax[row,col].set_ylabel('PMCA Leak (num)',fontsize=labelfont)
		
	
		# Save Figure
		savefig(self.resultPath + '/fig.eps', format='eps', dpi=300, facecolor=f.get_facecolor(), transparent=True)
		#show()
	
	#	Calculate Current (pA)
	def fluxCurrent(self, inFile, outFile, step=10, ncharge=1, line=1):
		dataFile = self.resultPath + inFile
		data = self.getData(dataFile)

		charge = 1#1.602e-7 #pico Coulomb
		c_out = []
		dt=step*(data[1][0]-data[0][0])
		for i in range(0,len(data)-step-1,step):
			temp = [data[i+step][0]-dt/2]
			for l in range(1,line+1):
				temp.append(ncharge*charge*(data[i+step][l]-data[i][l])/dt)
			#c_out.append([data[i+step][0]-dt/2, ncharge*charge*(data[i+step][line]-data[i][line])/dt])
			c_out.append(temp)

		of = self.resultPath + outFile
		print "\nWriting average to file: " + of
		outfile = open(of,'w')
		for l in c_out:
			s = ""
			for d in l: s += str(d) + " "
			outfile.write(s + '\n')
		outfile.close()
		
	#	Get Cumulative Count
	def cumulativeCount(self, inFile, outFile):
		data = getData(inFile)
	
