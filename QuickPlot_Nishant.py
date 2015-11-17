import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
fileread = np.genfromtxt("/home/pascal/Documents/IISER_Internship/MCell/Nishants_model/results/c_RI20V80/RI20V80.dat", skip_header=1, unpack=1)
plt.scatter(fileread[16], fileread[11])
plt.savefig("/home/pascal/Documents/IISER_Internship/MCell/Nishants_model/results/c_RI20V80/c_RI20V80_P1.eps", dpi=300, format='eps')
