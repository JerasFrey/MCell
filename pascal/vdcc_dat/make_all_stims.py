from pylab import *

# Note: stimuli are 5 ms wide.

n = 30			# n = number of pules in tetanic pulse
isi = 50e-3		# isi = Inter-Spike Interval
ptd = 2000e-3	# ptd = Post-Tetanic Delay 


for n in [4, 6, 10, 15, 20, 30]:
	for ptd in [100e-3, 250e-3, 500e-3, 1000e-3, 2000e-3]:
		d = 0e-3	# d = delay in first pulse
		rti = 0e-3	# rti = Reading Time Interval

		infile=[0]*9
		outfile=[0]*9

		infile[0]="VDCC_PQ_C01.dat"
		infile[1]="VDCC_PQ_C10.dat" 
		infile[2]="VDCC_PQ_C12.dat"
		infile[3]="VDCC_PQ_C21.dat"
		infile[4]="VDCC_PQ_C23.dat"
		infile[5]="VDCC_PQ_C32.dat"
		infile[6]="VDCC_PQ_C34.dat"
		infile[7]="VDCC_PQ_C43.dat"
		infile[8]="VDCC_PQ_Ca.dat"

		# Generate outfile
		for (i,f) in enumerate(infile):
			f = f.split(".")[0]+"_"
			ptdS = int(ptd*1000)
			unit = "ms"
			if ptd >= 1:
				if ptd % 1 == 0: ptdS = int(ptd)
				else: ptdS = ptd
				unit = "s"
			outfile[i] = "ptp/"+f+str(n)+"_"+str(int(1/isi))+"hz_"+str(ptdS)+unit+"_ptp.dat"

		# Generate Stim for PTP
		for i in range(len(infile)):

			# Read The Stim
			idata = genfromtxt(infile[i])

			# Make The Stim
			ofile = open(outfile[i], 'w')
			duration = idata[-1][0]
	
			# Post-Tetanic Pulse with number of spikes n and interspike interval isi
			for i in range(n):
				tdelay = d + rti + i*isi
				for j in range(len(idata)):
					ofile.write(str(idata[j][0]+tdelay)+"\t"+str(idata[j][1])+"\n")
	
			# Last Pulse with dalay post-tetanic delay ptd
			tdelay += ptd
			for j in range(len(idata)):
				ofile.write(str(idata[j][0]+tdelay)+"\t"+str(idata[j][1])+"\n")


