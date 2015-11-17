import numpy as np
import os
import matplotlib.pyplot as plt

#Name the results-path, get all folders in the resultspath into a list
modelname = "RP20V100"
filename = "ryr_ca_flux_avg.dat" # = file to be plotted
resultsdir = "results/"+modelname+"/"

modelfolders = os.listdir(resultsdir)
modelfolders =[e for e in modelfolders if os.path.isdir(resultsdir+e)]
if 'Plots' in modelfolders:
	modelfolders.remove('Plots')

if not os.path.exists(resultsdir+"Plots"):
		os.makedirs(resultsdir+"Plots")

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

'''
#get filenames for first figure
ca_avg_file = "ca_avg.dat"
ca_avg_uncumu_file = "ca_avg_uncumu.dat"

plt.figure(1)
#subplotnr = str(len(modelfolders))+"1"
#create a list, in which all columns (unpack = 1) of the respective ca_avg.dat files all over the different folders are appended to a sublist: [0][0] for 0st model, 0st column, [1][0] for first model, 0st column, ...
ca_avg = []
for i in range(len(modelfolders)):
	ca_avg.append(np.genfromtxt(resultsdir+modelfolders[i]+"/"+ca_avg_file, dtype=float, unpack=1))

#for the length of the appended list plot for each model (j) the 0st (time) vs the 1st (cummulated [C]) column: give the modelfoldername as a label to associate the line with the model
plt.subplot(311)
plt.title('ca_avg col1 (cummulative)')
for j in range(len(ca_avg)):
	plt.plot(ca_avg[j][0], ca_avg[j][1], label=modelfolders[j])
plt.xlabel('time in s')
plt.ylabel('[C]')
#plot the legend for the graph
plt.legend()

plt.subplot(312)
plt.title('ca_avg col2 (concentration)')
for k in range(len(ca_avg)):
	plt.plot(ca_avg[k][0], ca_avg[k][2], label=modelfolders[k])
plt.xlabel('time in s')
plt.ylabel('[C]')
#plot the legend for the graph
plt.legend()

plt.subplot(313)
ca_avg_uncumu = []
for l in range(len(modelfolders)):
	ca_avg_uncumu.append(np.genfromtxt(resultsdir+modelfolders[l]+"/"+ca_avg_uncumu_file, dtype=float, unpack=1))

plt.title('ca_avg col1 (uncummulative)')
for m in range(len(ca_avg_uncumu)):
	plt.plot(ca_avg_uncumu[m][0], ca_avg_uncumu[m][1], label=modelfolders[m])
plt.xlabel('time in s')
plt.ylabel('[C]')
#plot the legend for the graph
plt.legend()
'''

plot_list = []

for n in range(len(modelfolders)):
	plot_list.append(np.genfromtxt(resultsdir+modelfolders[n]+'/'+filename, skip_header=1, unpack=1))
	y_pos =  str(modelfolders[n])
	
#difference between [1] and [2]
plt.figure(2)
for o in range(len(plot_list)):
	#plot_list
	y_pos = plot_list[o][2][-1]
	plt.text(0.05, y_pos, modelfolders[o], color=tableau20[o])
	plt.plot(plot_list[o][0], plot_list[o][2], color=tableau20[o])
plt.title('RyR Ca Flux in '+modelname)
plt.xlabel('Distance from VDCC; VDCC @ 350, AZ @ 0')
plt.ylabel('N10+N11/# of simulations')
#plt.ylim([0,1])
plt.legend()
plt.savefig(resultsdir+'Plots/'+'P1_'+modelname+'.eps', dpi=300, format='eps')

#plot all graphs
plt.show()
