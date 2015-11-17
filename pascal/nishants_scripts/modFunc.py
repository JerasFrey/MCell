#!/usr/bin/python

from numpy import *#
from pylab import *#
import os, sys

class analysis:
	
	#	Set dataPath and resultPath
	def __init__(self, dp, rp):
		self.dataPath = dp
		self.resultPath = rp
		
	#	Get list of directories in the path starting with 's_'
	def getDirs(self, path, sstr='s_'):
		dirs = [d for d in os.listdir(path) if os.path.isdir(path + '/' + d) and sstr in d]
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
		
		avg = genfromtxt(self.dataPath+'/'+dirs[0]+inFile)
		for i in range(1,self.seeds):
			avg += genfromtxt(self.dataPath+'/'+dirs[i]+inFile)
		avg = avg/self.seeds
		

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
		savetxt(of, avg, fmt='%.6f')

	#	Ca Concentration Calculation
	def conc_calc(self, step, inFile="/ca.dat", outFile="/CaConc"):
		data = genfromtxt(self.resultPath + inFile)

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
	def relppf(self, ts, vdcc, dist, tc=0.02):
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
		nRel.append(int(dist)) # nRel[16] = Distance
		
		#	Print Results
		r = open(self.resultPath + '/result', 'w')
		print nRel
		for a in nRel:
			if not isinstance(a,int):
				r.write(format(a,'.2')+"\t")
			else:
				r.write(str(a)+"\t")
		r.write("\n")
		print "done"

	#	Get Vesicle Release Statistics for PTP
	def relptp(self, conf, tc=0.02):
		n = conf[0]
		isi = conf[1]
		ptd = conf[2]
		
		self.ts = [i*isi for i in range(n)]
		self.ts.append((n-1)*isi+ptd)
		self.ts = [(i+2.5)/1000.0 for i in self.ts]
		
		nRel = [0]*len(self.ts) # [Rel1, Rel2,... Reln] 
		dirs = self.getDirs(self.dataPath)	
		for d in [(self.dataPath + '/' + dir + '/dat/') for dir in dirs]:
			os.system("cd " + d + "; cat vdcc.* > rel.dat")
			
			fpath = (d + "/rel.dat")
			f = open(fpath,'r')

			#	Get no. of vesicles released after AP specified by self.ts
			for line in f: 
				time = float(line.strip("\n").split(" ")[0])
				for i in range(len(self.ts)):
					if (time>self.ts[i] and time<self.ts[i]+tc):
						nRel[i] += 1

		#	print nRel
		os.system("cat " + self.dataPath + "/*/dat/rel.dat > " + self.resultPath + "/vesRel")
		os.system("cat " + self.dataPath + "/*/dat/vdcc.async_*.dat > " + self.resultPath + "/asyncRel")
		os.system("cat " + self.dataPath + "/*/dat/vdcc.sync_*.dat > " + self.resultPath + "/syncRel")
		
		#	Print Results
		r = open(self.resultPath + '/result', 'w') 
		savetxt(r,[nRel],fmt="%d",delimiter="\t")

		print nRel
	
	#	Plot all 
	def plotAll(self, dataDirName, colorScheme = 'black'):
		# These are the "Tableau 20" colors as RGB.  
		tableau10 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189), 
			(140, 86, 75), (227, 119, 194), (127, 127, 127), (188, 189, 34), (23, 190, 207)]  
		  
		# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
		for i in range(len(tableau10)):  
			r, g, b = tableau10[i]  
			tableau10[i] = (r / 255., g / 255., b / 255.) 

		# Global Settings
		rcParams['figure.figsize'] = 5,4
		lw = 0.3 # linewidth
		params = {'xtick.major.size': 2, 'xtick.major.width': 0.5,
				  'axes.linewidth':lw, 'axes.labelsize':4, 'xtick.labelsize':4, 'ytick.labelsize':4}
		rcParams.update(params)
		nSubPlots = 3
		f, ax = subplots(nSubPlots, sharex='col')

		subplots_adjust(left=0.08, bottom=0.08, right=0.93, top=0.98, wspace=0.4, hspace=None)
		if colorScheme == 'black':
			f.patch.set_facecolor('black')
			#f.patch.set_alpha(1)
		
			# Settings for Texts and Axes
			txtcolor = 'white'
			axiscolor = '#777777'
			titlecolor = 'orange'
		
			# Color set for plots
			
			avgcolor = '#0077ff'
			onecolor = 'g'
			allcolor = '#292929'
			cumulcolor = '#cc2299'
			y2color = 'r'
		
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
			y2color = 'g'
		
		for i in range(nSubPlots):
			ax[i].get_xaxis().tick_bottom()  
			ax[i].get_yaxis().tick_left()
			
			ax[i].patch.set_facecolor('black')
			ax[i].patch.set_alpha(0.0)
			
			ax[i].spines['bottom'].set_color(axiscolor)
			ax[i].spines['left'].set_color(axiscolor)
			
			ax[i].tick_params(axis='x', colors=axiscolor)
			ax[i].tick_params(axis='y', colors=axiscolor)

			ax[i].yaxis.label.set_color(txtcolor)
			ax[i].xaxis.label.set_color(txtcolor)
			
			ax[i].title.set_color(titlecolor)
		
		ax[-1].set_xlabel('Time (sec)')
		
		
		dirs = self.getDirs(self.dataPath)
		
		gCaData = genfromtxt(self.resultPath + '/ca.dat')
		nBin = int(gCaData[-1,0]/0.020)
		
		# Vesicle Release Histogram
		row = 0
		ax[row].spines['right'].set_color(y2color)
		ptpData = genfromtxt(self.resultPath + '/result')
		ptpData /= float(ptpData[0])
		ax[row].plot(self.ts,ptpData, lw=lw, color=avgcolor)
		ax[row].set_ylabel('Facilitation ($n^{th}/1^{st}$)')
		
		axt = ax[row].twinx()
		axt.tick_params(axis='y', colors=y2color)
		axt.get_yaxis().tick_right()
		vesRelData = genfromtxt(self.resultPath + '/vesRel')
		n, bins, patches = axt.hist(vesRelData[:,0], nBin, lw =lw, color=y2color, histtype='step')
		axt.set_ylabel('Vesicles (num)', color=y2color)
		ax[row].set_zorder(axt.get_zorder()+1)
		
		# Avg. cytosol [Ca]	and ER [Ca]
		row += 1
		#ax[row].spines['right'].set_color(y2color)
		lCaData = genfromtxt(self.resultPath + '/CaConc')
		ax[row].plot(lCaData[:,0], lCaData[:,1], lw=lw, color=avgcolor) # Local [Ca]
		#ax[row].plot(gCaData[:,0], [i/602.3 for i in gCaData[:,2]], lw=lw, color='r') # Global [Ca]
		ax[row].set_ylabel('[Ca$^{2+}$]$_{cyt}$ ($\mu$M)')
		'''
		axt = ax[row].twinx()
		axt.tick_params(axis='y', colors=y2color)
		axt.get_yaxis().tick_right()
		axt.plot(gCaData[:,0], [i/24.5 for i in gCaData[:,3]], lw=lw, color=y2color)
		axt.set_ylabel('[Ca$^{2+}$]$_{ER}$ ($\mu$M)', color=y2color)
		'''	
		# RRP (num)
		row += 1
		rrpData = genfromtxt(self.resultPath + '/rrp.dat')
		#ax[row].fill_between(data[:,0], data[:,1] - data[:,2], data[:,1] + data[:,2], color="#3F5D7D")
		ax[row].plot(rrpData[:,0], rrpData[:,1], lw=lw, color=avgcolor)
		ax[row].set_ylabel('RRP (num)')
		'''
		# Open RyR and Ca flux from RyR
		row += 1
		ax[row].spines['right'].set_color(y2color)
		
		openRyrData = genfromtxt(self.resultPath + '/ryrMol.dat')
		ax[row].plot(openRyrData[:,0], [i[6]+i[7]+(i[8]+i[13]+i[14]) for i in openRyrData], lw=lw, color=avgcolor)
		ax[row].set_ylabel('Open RyR (num)')

		ryrCaFluxRateData = genfromtxt(self.resultPath + '/ryrCaFluxRate.dat')
		ryrCaFluxData = genfromtxt(self.resultPath + '/ryrCaFlux.dat')
		
		axt = ax[row].twinx()
		axt.tick_params(axis='y', colors=y2color)
		axt.get_yaxis().tick_right()
		#axt.plot(ryrCaFluxData[:,0],ryrCaFluxData[:,1], lw=lw, color=cumulcolor)
		#axt.plot(ryrCaFluxData[:,0],ryrCaFluxData[:,2], lw=lw, color=cumulcolor)
		axt.plot(ryrCaFluxData[:,0],ryrCaFluxData[:,1]-ryrCaFluxData[:,2], lw=lw, color=y2color)
		axt.set_ylabel('RyR Ca Cum. Flux (num)', color=y2color)
		
		# Extra Ca Bound to Serca
		row += 1
		sercaData = genfromtxt(self.resultPath + '/sercaMol.dat')
		boundCa = [i[2]+i[5]+(i[3]+i[4])*2-2170 for i in sercaData]
		ax[row].plot(sercaData[:,0], boundCa, lw=lw, color=avgcolor)
		ax[row].set_ylabel('SERCA-Bound Ca$^{2+}$')
		
		# SERCA States
		row += 1
		sercaData = genfromtxt(self.resultPath + '/sercaMol.dat')
		for i in range(1,7):
			ax[row].plot(sercaData[:,0], sercaData[:,i], lw=lw, color=tableau10[2*i])
		ax[row].set_ylabel('SERCA States (num)')

		ax[-1].set_xlim(0,gCaData[-1,0])
		'''
		'''
		# Glu (num) 
		if chkSim.find("I") != -1:
			row += 1
			gluData = genfromtxt(self.dataPath + '/' + dirs[0] + '/dat/glu.dat')
			ax[row].plot(gluData[:,0], gluData[:,1], lw=lw, color=onecolor)
			ax[row].set_ylabel('[Glu] (num)',fontsize=labelfont)
		
		
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
				ax[row].vlines(trial, ith, ith + 1, color='g',lw=lw)
				ax[row].set_ylim(0.0, len(events))
			ax[row].set_ylabel('Trial no.',fontsize=labelfont)
			
		
		# [IP3]
		if chkSim.find("I") != -1:
			row += 1
			for i in range(20,0,-1):
				ip3Data = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/ip3.dat')
				if i==1:
					ax[row].plot(ip3Data[:,0], [i/602.3 for i in ip3Data[:,1]], lw=lw, color=onecolor)
				else:
					ax[row].plot(ip3Data[:,0], [i/602.3 for i in ip3Data[:,1]], lw=lw, color=allcolor)
		
			ip3Data = genfromtxt(self.resultPath + '/ip3.dat')
			ax[row].plot(ip3Data[:,0], [i/602.3 for i in ip3Data[:,1]], lw=lw, color=avgcolor)
			ax[row].set_ylabel('[IP3] ($\mu$M)',fontsize=labelfont)
		
		row = 0
		col = 1
		# Open IP3R
		if chkSim.find("I") != -1:
			row += 1
			for i in range(20,0,-1):
				openIp3rData = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/ip3r_open.dat')
				if i==1:
					ax[row].plot(openIp3rData[:,0], openIp3rData[:,1], lw=lw, color=onecolor)
				else:
					ax[row].plot(openIp3rData[:,0], openIp3rData[:,1], lw=lw, color=allcolor)
		
			openIp3rData = genfromtxt(self.resultPath + '/ip3rOpen.dat')
			ax[row].plot(openIp3rData[:,0], openIp3rData[:,1], lw=lw, color=avgcolor)
			ax[row].set_ylabel('Open IP3R (num)',fontsize=labelfont)
		
		# Ca flux from IP3R
		if chkSim.find("I") != -1:
			row += 1
			ip3rCaFluxData = genfromtxt(self.resultPath + '/ip3rCaFlux.dat')
			ax[row].plot(ip3rCaFluxData[:,0], ip3rCaFluxData[:,1], lw=lw, color=avgcolor)
			ax[row].set_ylabel('IP3R Ca Flux (num)',fontsize=labelfont)
			
		# Ca flux from VDCC
		if chkSim.find("I") == -1:
			row += 1
			vdccCaFluxData = genfromtxt(self.resultPath + '/vdccCaFluxRate.dat')
			ax[row].plot(vdccCaFluxData[:,0],[i/1000 for i in vdccCaFluxData[:,1]], lw=lw, color=avgcolor)
			ax[row].set_ylabel('vdcc Ca Flux (num/ms)',fontsize=labelfont)
		
			
		# Cumulative Ca flux from VDCC
		if chkSim.find("I") == -1:
			row += 1
			vdccCaFluxData = genfromtxt(self.resultPath + '/vdccCaFlux.dat')
			ax[row].plot(vdccCaFluxData[:,0], vdccCaFluxData[:,1], lw=lw, color=avgcolor)
			ax[row].set_ylabel('vdcc Ca Flux (num/ms)',fontsize=labelfont)
		
		# No. of IP3 Produced via mGluR Pathway
		if chkSim.find("I") != -1:
			row += 1
			for i in range(20,0,-1):
				ip3cData = genfromtxt(self.dataPath + '/' + dirs[i] + '/dat/ip3_create.dat')
				if i==1:
					ax[row].plot(ip3cData[:,0], ip3cData[:,1], lw=lw, color=onecolor)
				else:
					ax[row].plot(ip3cData[:,0], ip3cData[:,1], lw=lw, color=allcolor)
		
			ip3cData = genfromtxt(self.resultPath + '/ip3Create.dat')
			ax[row].plot(ip3cData[:,0], ip3cData[:,1], lw=lw, color=avgcolor)
			ax[row].set_ylabel('IP3 Produced (num)',fontsize=labelfont)
			
		# Cumulative Ca Leak from PMCA
		
		if chkSim.find("S") != -1:
			row += 1
			pmcaData = genfromtxt(self.resultPath + '/pmca_leak.dat')
			ax[row].plot(pmcaData[:,0], [(i[1]-i[2]) for i in pmcaData], lw=lw, color=avgcolor)
			ax[row].set_ylabel('PMCA Leak (num)',fontsize=labelfont)
		
		'''
		# Save Figure
		savefig(self.resultPath + '/figwhite.png', format='png', dpi=300, facecolor=f.get_facecolor(), transparent=True)
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
	
