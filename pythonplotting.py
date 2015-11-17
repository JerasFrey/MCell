import numpy as np
import matplotlib.pyplot as plt

#load the path to the first condition to be compared
modeldir1 = "results/RyR/"
modelname1 = "RSDr000_avg/"
path1 = modeldir1 + modelname1

#load the path to the second condition to be compared
modeldir2 = "results/RyR/"
modelname2 = "RSDr350_avg/"
path2 = modeldir2 + modelname2

#the file that should be compared amongst the conditions
infile1 = "ca_avg.dat"
infile2 = "ca_avg_uncumu.dat"

#load the columns of the files to be compared in figure 1
plotnumbers1col1 = np.genfromtxt(path1+infile1, dtype=float, usecols=(1))
plotnumbers1_1col1 = np.genfromtxt(path1+infile2, dtype=float, usecols=(1))
plotnumbers1col2 = np.genfromtxt(path1+infile1, dtype=float, usecols=(2))
plotnumbers_t1 = np.genfromtxt(path1+infile1, dtype=float, usecols=(0))
plotnumbers_t1_1 = np.genfromtxt(path1+infile2, dtype=float, usecols=(0))

plotnumbers2col1 = np.genfromtxt(path2+infile1, dtype=float, usecols=(1))
plotnumbers2_1col1 = np.genfromtxt(path2+infile2, dtype=float, usecols=(1))
plotnumbers2col2 = np.genfromtxt(path2+infile1, dtype=float, usecols=(2))
plotnumbers_t2 = np.genfromtxt(path2+infile1, dtype=float, usecols=(0))
plotnumbers_t2_1 = np.genfromtxt(path2+infile2, dtype=float, usecols=(0))

plt.figure(1)
plt.subplot(311)
plt.title('ca_avg col1 (cummulative)')
plt.plot(plotnumbers_t1, plotnumbers1col1, label='RSDr000')
plt.plot(plotnumbers_t2, plotnumbers2col1, label='RSDr350')
plt.xlabel('time in s')
plt.ylabel('[C]')
plt.legend()

plt.subplot(312)
plt.title('ca_avg_uncumu col1 (uncummulative)')
plt.plot(plotnumbers_t1_1, plotnumbers1_1col1, label='RSDr000')
plt.plot(plotnumbers_t2_1, plotnumbers2_1col1, label='RSDr350')
plt.xlabel('time in s')
plt.ylabel('[C]')
plt.legend()

plt.subplot(313)
plt.title('ca_avg col2 (concentration)')
plt.plot(plotnumbers_t1, plotnumbers1col2, label='RSDr000')
plt.plot(plotnumbers_t2, plotnumbers2col2, label='RSDr350')
plt.xlabel('time in s')
plt.ylabel('[C]')
plt.legend()


rrp_file = "rrp_avg.dat"

rrp_1col0 = np.genfromtxt(path1+rrp_file, dtype=float, usecols=(0))
rrp_1col1 = np.genfromtxt(path1+rrp_file, dtype=float, usecols=(1))

rrp2_col0 = np.genfromtxt(path2+rrp_file, dtype=float, usecols=(0))
rrp2_col1 = np.genfromtxt(path2+rrp_file, dtype=float, usecols=(1))

plt.figure(2)
plt.title('rrp_avg')
plt.plot(rrp_1col0, rrp_1col1, label='RSDr000')
plt.plot(rrp2_col0, rrp2_col1, label='RSDr350')
plt.legend()


ryr_ca_file = "ryr_ca_flux_avg.dat"
ryr_ca_1col0 = np.genfromtxt(path1+ryr_ca_file, dtype=float, usecols=(0))
ryr_ca_1col1 = np.genfromtxt(path1+ryr_ca_file, dtype=float, usecols=(1))
ryr_ca_1col2 = np.genfromtxt(path1+ryr_ca_file, dtype=float, usecols=(2))

ryr_ca_2col0 = np.genfromtxt(path2+ryr_ca_file, dtype=float, usecols=(0))
ryr_ca_2col1 = np.genfromtxt(path2+ryr_ca_file, dtype=float, usecols=(1))
ryr_ca_2col2 = np.genfromtxt(path2+ryr_ca_file, dtype=float, usecols=(2))

plt.figure(3)
plt.subplot(211)
plt.title('ryr_ca_flux_avg')
plt.plot(ryr_ca_1col0, ryr_ca_1col1, label='RSDr000')
plt.plot(ryr_ca_2col0, ryr_ca_2col1, label='RSDr350')
plt.legend()

plt.subplot(212)
plt.plot(ryr_ca_1col0, ryr_ca_1col2, label='RSDr000')
plt.plot(ryr_ca_2col0, ryr_ca_2col2, label='RSDr350')
plt.legend()


ryr_mol_file = "ryr_mol_avg.dat"
ryr_mol1 = np.genfromtxt(path1+ryr_mol_file, dtype=float, unpack=1)
ryr_mol2 = np.genfromtxt(path2+ryr_mol_file, dtype=float, unpack=1)

ryr_mol1_t = ryr_mol1[0]
ryr_mol2_t = ryr_mol2[0]

ryr_mol1_lc = ryr_mol1[1] + ryr_mol1[2] + ryr_mol1[3] + ryr_mol1[4] + ryr_mol1[5]
ryr_mol2_lc = ryr_mol2[1] + ryr_mol2[2] + ryr_mol2[3] + ryr_mol2[4] + ryr_mol2[5]

ryr_mol1_lo = ryr_mol1[6] + ryr_mol1[7] + ryr_mol1[8]
ryr_mol2_lo = ryr_mol2[6] + ryr_mol2[7] + ryr_mol2[8]

ryr_mol1_c = ryr_mol1[9] + ryr_mol1[10] + ryr_mol1[11] + ryr_mol1[12]
ryr_mol2_c = ryr_mol2[9] + ryr_mol2[10] + ryr_mol2[11] + ryr_mol2[12]

ryr_mol1_o = ryr_mol1[13] + ryr_mol1[14]
ryr_mol2_o = ryr_mol2[13] + ryr_mol2[14]

plt.figure(4)
plt.subplot(411)
plt.title('ryr_mol sum LC')
plt.plot(ryr_mol1_t, ryr_mol1_lc, label=modelname1[:-5])
plt.plot(ryr_mol2_t, ryr_mol2_lc, label=modelname2[:-5])
plt.legend()

plt.subplot(412)
plt.title('ryr_mol sum LO')
plt.plot(ryr_mol1_t, ryr_mol1_lo, label=modelname1[:-5])
plt.plot(ryr_mol2_t, ryr_mol2_lo, label=modelname2[:-5])
plt.legend()

plt.subplot(413)
plt.title('ryr_mol sum C')
plt.plot(ryr_mol1_t, ryr_mol1_c, label=modelname1[:-5])
plt.plot(ryr_mol2_t, ryr_mol2_c, label=modelname2[:-5])
plt.legend()

plt.subplot(414)
plt.title('ryr_mol sum O')
plt.plot(ryr_mol1_t, ryr_mol1_o, label=modelname1[:-5])
plt.plot(ryr_mol2_t, ryr_mol2_o, label=modelname2[:-5])
plt.legend()


vdcc_file = "vdcc_pq_ca_flux_avg.dat"
vdcc1 = np.genfromtxt(path1+vdcc_file, dtype=float, unpack=1)
vdcc2 = np.genfromtxt(path2+vdcc_file, dtype=float, unpack=1)

plt.figure(5)
plt.title(vdcc_file[:-8])
plt.plot(vdcc1[0], vdcc1[1], label=modelname1[:-5])
plt.plot(vdcc2[0], vdcc2[1], label=modelname2[:-5])
plt.legend()

plt.show()
