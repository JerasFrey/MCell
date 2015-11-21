import numpy as np
import os
import matplotlib.pyplot as plt

#Name the results-path, get all folders in the resultspath into a list
modelname = "RP20V80"
resultsdir = "results/"+modelname+"/"
modelfolders = os.listdir(resultsdir)
modelfolders =[e for e in modelfolders if os.path.isdir(resultsdir+e)]

if not os.path.exists(resultsdir+"Plots"):
		os.makedirs(resultsdir+"Plots")
if 'Plots' in modelfolders:
	modelfolders.remove('Plots')
#outputdir = "output/IP3/"
#outmodels = os.listdir(outputdir)


#release probabilities
'''
all_rels_assorted = []

for k in range(len(modelfolders)):
	print(k, " " ,resultsdir+modelfolders[k]+"/all_rels/rel_all_assorted.dat")
	all_rels_assorted.append(np.genfromtxt(resultsdir+modelfolders[k]+"/all_rels/rel_all_assorted.dat", skip_header=1, unpack=1))
'''
'''
#N00, N10, N01, N11

plt.figure(2)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][1])
plt.title('N00 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('# of no releases after first and second spike')
plt.legend()

plt.figure(3)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][2])
plt.title('N10 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('# of releases after first spike, no releases after 2nd spike')
plt.legend()

plt.figure(4)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][3])
plt.title('N01')
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('# of no releases after first spike, releases after 2nd spike')
plt.legend()

plt.figure(5)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][4])
plt.title('N11 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('# of releases after first spike, releases after 2nd spike')
plt.legend()
'''

#N1 and N2
'''
plt.figure(6)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][5])
plt.title('N1 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('Total releases after 1st spike in all simulations / # of simulations')
plt.legend()

plt.figure(7)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][6])
plt.title('N2 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('Total releases after 2nd spike in all simulations / # of simulations')
plt.legend()


#conditional probability

plt.figure(8)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][7])
plt.title('P00 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('N00/N00+N01')
plt.legend()

plt.figure(9)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][8])
plt.title('P10 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('N10/N10+N11')
plt.legend()

plt.figure(10)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][9])
plt.title('P01 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('N01/N01+N00')
plt.legend()

plt.figure(11)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][10])
plt.title('P11 '+modelname)
plt.xlabel('Distance from VDCC; AZ @ 0')
plt.ylabel('N11/N11+N10')
plt.legend()

'''
'''
#P1 and P2 and PPF

plt.figure(12)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][11])
plt.title('P1 '+modelname)
plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
plt.ylabel('N10+N11/# of simulations')
#plt.ylim([0,1])
plt.legend()
plt.savefig(resultsdir+'Plots/'+'P1_'+modelname+'.eps', dpi=300, format='eps')

plt.figure(13)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][11])
plt.title('P1 '+modelname+'static axes')
plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
plt.ylabel('N10+N11/# of simulations')
plt.ylim([0,1])
plt.legend()
plt.savefig(resultsdir+'Plots/'+'P1_'+modelname+'_static_axes'+'.eps', dpi=300, format='eps')

plt.figure(14)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][12])
plt.title('P2 '+modelname)
plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
plt.ylabel('N01+N11/# of simulations')
#plt.ylim([0,1])
plt.legend()
plt.savefig(resultsdir+'Plots/'+'P2_'+modelname+'.eps', dpi=300, format='eps')

plt.figure(15)
for l in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[l][0], all_rels_assorted[l][12])
plt.title('P2 '+modelname+'static axes')
plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
plt.ylabel('N01+N11/# of simulations')
plt.ylim([0,1])
plt.legend()
plt.savefig(resultsdir+'Plots/'+'P2_'+modelname+'_static_axes'+'.eps', dpi=300, format='eps')

plt.figure(16)
for m in range(len(all_rels_assorted)):
	plt.scatter(all_rels_assorted[m][0], all_rels_assorted[m][13])
plt.title('PPF '+modelname)
plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
plt.ylabel('P2/P1')
plt.legend()
plt.savefig(resultsdir+'Plots/'+'PPF_'+modelname+'.eps', dpi=300, format='eps')
'''

'''
all_rels = []

for n in range(len(modelfolders)):
	all_rels.append(np.genfromtxt(resultsdir+modelfolders[n]+"/all_rels/rel_all.dat", skip_header=1, usecols=0))
for i in range(len(all_rels)):
	plt.figure(str(i))
	n, bins, patches = plt.hist(all_rels[i], 8)
	plt.ylim([0,200])
	plt.title('# of releases over time '+modelfolders[i]+'static axes')
	plt.xlabel('Distance relative to AZ: AZ = 0, VDCC = 350 nm')
	plt.ylabel('# of releases')
	plt.legend()
	plt.savefig(resultsdir+'Plots/'+'Histogram '+modelfolders[i]+'_static_axes'+'.eps', dpi=300, format='eps')
'''

'''`
for o in range(len(all_rels[0:1])):
	plt.figure(o)
	n, bins, patches = plt.hist(all_rels[o], 8)
	print all_rels[o]
	plt.title('P2 '+modelname+'static axes')
	plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
	plt.ylabel('N01+N11/# of simulations')
	plt.ylim([0,1])
	plt.legend()
	plt.savefig(resultsdir+'Plots/'+'P2_'+modelname+'_static_axes'+'.eps', dpi=300, format='eps')
'''

for n in range(len(modelfolders)):
	if modelfolders[n][-5] == '0':# or modelfolders[o][-1] == '5': #-5 for my data, -1 for cluster data
		sync_rel = np.genfromtxt(resultsdir+modelfolders[n]+"/all_rels/rel_sync.dat", usecols=0)
		assync_rel = np.genfromtxt(resultsdir+modelfolders[n]+"/all_rels/rel_async.dat", usecols=0)
		container = modelfolders[n] 
		#print sync_rel
		plt.figure(2)
		n, bins, patches = plt.hist([sync_rel,assync_rel], 50, color=['r','g'], stacked=True, edgecolor = "none")
		plt.ylim([0,85])
		plt.title('# of releases over time '+container)
		plt.xlabel('time in ms')
		plt.ylabel('# of releases (red = sync rel; green = async rel)')
		plt.legend()
		#plt.savefig(resultsdir+'Plots/'+'Histogram '+container+'.png', dpi=300, format='png')
		plt.close()
		#plt.show()
#hist([syncRelData[:,0],asyncRelData[:,0]], 50, color=['r','g'], stacked=True)


#plot all graphs
#plt.show()
