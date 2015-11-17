	#	Get Vesicle Release Statistics for PPF
	#	def relppf(self, ts, vdcc, tc=0.02):
import os, sys
		ts = [2.5, 22.5]
		modeldir = "output/RyR/"
		modelfolds = os.listdir(modeldir)
		modelfolds =[e for e in modelfolds if os.path.isdir(modeldir+e)]
		dataPath = modeldir + str(modelfolds)

print dataPath
'''
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
'''
