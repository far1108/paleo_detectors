# reading TRIM output and calculating resulting mean tracklength and straggling
# results for Halite (sigma_x=30nm, epsilon=1kgMyr) saved in "Data/TRIM_Deviation"

import numpy as np

# TRIM output file "EXYZ.txt" with an increment of 1eV
# containing ion number and 3d-position
ion_numb,x,y,z = np.loadtxt("SRIM-2013\\SRIM Outputs\\EXYZ.txt",unpack=True,skiprows=15,usecols=(0,2,3,4))

# insert 0 at beginning in order to simplify if-statement below
# convert coordinates to units nm
ion_numb = np.insert(ion_numb,0,0)
x = np.insert(x,0,0)/10
y = np.insert(y,0,0)/10
z = np.insert(z,0,0)/10

total_number_of_ions = ion_numb[len(ion_numb)-1]
tracklengths = np.zeros(int(total_number_of_ions))

# calculate tracklengths by summing up distances between consecutive positions
# here: starting position (100,0,0) (settable with TRIM.dat)
for j in range(1,len(ion_numb)):
    if(ion_numb[j]!=ion_numb[j-1]):
        tracklengths[int(ion_numb[j])-1] += np.sqrt((x[j]-100)**2+(y[j])**2+(z[j])**2)
    else:
        tracklengths[int(ion_numb[j])-1] += np.sqrt((x[j]-x[j-1])**2+(y[j]-y[j-1])**2+(z[j]-z[j-1])**2)

# calculate everything you need from that
mean = np.mean(tracklengths)
std = np.std(tracklengths)

# standard deviation from pre-calculated mean via SRIM
# def stdev(x,mean):
#     if(len(x)<1):
#         return 0
#     else:
#         return np.sqrt(1/len(x)*np.sum((x-mean)**2))
#
# calc_mean =...
# std_SRIM = stdev(tracklengths,calc_mean)
