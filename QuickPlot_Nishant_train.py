import matplotlib.pyplot as plt
import numpy as np

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

plt.figure(1)
fileread = np.genfromtxt("/home/pascal/Documents/IISER_Internship/MCell/Presynapse_MCell_Model/results/c_IP3_T10Hz/IP3_T10Hz.dat")
#plt.scatter(fileread[16], fileread[11])
time = np.linspace(0.1, 0.5, num=5)
j=-1
for i in fileread:
	j = j+1
	#if j%3!=0: continue
	y_pos = i[-2]/i[0]-0.05
	plt.text(0.51, y_pos, str(i[-1]), color=tableau20[j%20])
	plt.plot(time, i[:-1]/i[0], lw=2, color=tableau20[j%20])
plt.xlim([0.1,0.53])
plt.title('IP3 100ms Train')
plt.xlabel('t in ms')
plt.ylabel('Pn / P1 -> PTP')
plt.savefig("/home/pascal/Documents/IISER_Internship/MCell/Presynapse_MCell_Model/results/c_IP3_T10Hz/IP3_T10Hz_PTP.eps", dpi=300, format='eps')
plt.show()
