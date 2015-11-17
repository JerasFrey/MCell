import numpy as np
import os

#Give the delta t (number of rows to be skipped from the original folder) here
skipped_lines = 5

#Defining the right input directory
modeldir = "results/RyR/"
modelname = "RSDr000_avg/"
path = modeldir + modelname

#give the name of the input file to be processed here:
infilename = "ca_avg.dat"

#Create the output filename by appending _uncumu.dat
outfilename = infilename[:-4] + "_uncumu.dat"

#Read the ca.dat file as a 2dimensional array
rxn_conc = np.genfromtxt(path+infilename, dtype=float)

#Define a blank array for the processed data
rxn_conc_new = []

#Start i with the number of lines to be skipped (,) as long as the input vector is (,) in steps of the number of lines to be skipped
#The loop will stop when it is not possible to divide the number by <skipped lines> anymore
for i in range(skipped_lines,len(rxn_conc),skipped_lines):
	#Append the column containing the time (in milliseconds) to the new vector to be able to plot the new document with Gnuplot later
	rxn_conc_new.append([rxn_conc[i][0], 
	
	#implement the following formular to reverse the MCell formular <ESTIMATE_CONC> by calculating:
	#	time(t)i * concentration(c)i - t(i-steps) * c(i-steps) / ti - ti-steps
	(((rxn_conc[i][0] * rxn_conc[i][1]) - (rxn_conc[(i-skipped_lines)][0] * rxn_conc[(i-skipped_lines)][1])) /
	 (rxn_conc[i][0] - rxn_conc[(i-skipped_lines)][0]))])

#save the content of the vector containing the processed data to the same path as the input file but with the <outfilename>
#Use a different format for both columns: Time (1st column) being at the scale of microseconds, is not exceeding 6 digits after 0 and the precision of the concentration (2nd column) is sufficientt when giving it with 3 digits.
np.savetxt(path+outfilename, rxn_conc_new, fmt=['%.6f','%.3f'])
