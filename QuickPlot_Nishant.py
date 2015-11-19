import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
fileread = np.genfromtxt("/home/pascal/Documents/IISER_Internship/MCell/Presynapse_MCell_Model/results/c_IP3_100/IP3_100.dat", skip_header=1, unpack=1)
plt.scatter(fileread[16], fileread[13])
plt.title('IP3 100ms PPF - PPF')
plt.savefig("/home/pascal/Documents/IISER_Internship/MCell/Presynapse_MCell_Model/results/c_IP3_100/c_IP3_100_PPF.eps", dpi=300, format='eps')
