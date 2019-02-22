# calculate projected sensitivities (90%CL) via a cut-and-count-analysis
# results saved in "Data/Sensitivities"

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
import scipy.integrate as integrate
from scipy.interpolate import interp1d
from scipy.stats import norm

# spatial resolution of read-out method in nm
sigma_x = 30

# range of tracklengths from sigma_x/2 up to approx. 1000 nm with bin widths sigma_x
n = int((1000-sigma_x/2)/sigma_x)
xrange = np.linspace(sigma_x/2,sigma_x/2+n*sigma_x,n+1)

###########################################################################################
# txt-files containing tracklengths for each of the atoms the target contains as generated by "Tracklength_spectrum.py"
# convert to nm
tracklengths_atom1 = np.loadtxt('atom1_tracklengths.txt')*1E9
tracklengths_atom2 = np.loadtxt('atom2_tracklengths.txt')*1E9
# tracklengths_atom3 = ....

###########################################################################################
# background:

# assumed relative systematic error of the background
Sigma_B = 1

# txt-files containing neutrino induced recoil spectra as generated by "Neutrino_background.py"
# convert to 1/(kg nm Myr)
dRdx_atom1_nu = np.loadtxt('atom1_nu-spectrum.txt')*3.1536E+4
dRdx_atom2_nu = np.loadtxt('atom2_nu-spectrum.txt')*3.1536E+4

# need to interpolate due to different tracklengths of different atoms for same recoil energy
dRdx_atom1_nu_ip = interp1d(tracklengths_atom1,dRdx_atom1_nu,kind='cubic')
dRdx_atom2_nu_ip = interp1d(tracklengths_atom2,dRdx_atom2_nu,kind='cubic')

# sum weighted by respective mass fraction in the target
def dRdx_nu(x):
    return 0.5*dRdx_atom1_nu_ip(x)+0.5*dRdx_atom2_nu_ip(x)

# calculate number of expected background events in each considered tracklength interval (in this case: for an exposure of 1 kg Myr)
B_events = np.zeros(len(xrange))
for i in range(1,len(xrange)):
    B_events[i] = integrate.romberg(dRdx_nu,xrange[i-1],xrange[i],divmax=50)

# assume the track lengths of each event in a bin will be measured corresponding to a Gaussian with std=sigma_x
# and smear the distribution accordingly
B_events_smeared = np.zeros(len(xrange))
for i in range(len(xrange)):
    def smeared(x):
        return B_events[i]*norm.pdf(x,loc=xrange[i]-sigma_x/2,scale=sigma_x)
    for j in range(1,len(xrange)):
        B_events_smeared[j] += integrate.quad(smeared,xrange[j-1],xrange[j],limit=5000)[0]

# compute the sums of background events for every possible tracklength interval within xrange
B_sums = np.ones((len(xrange),len(xrange)+1))
for i in range(1,len(xrange)):
    for j in range(1,len(xrange)+1):
        B_sums[i][j] = np.sum(B_events_smeared[i:j])

#################################################################################
# signal:

# list of considered WIMP masses in GeV
mchis = [1,2,5,10,20,50,100,200,500,1000]

foundsigmasandcutoffs=np.ones((8,5))

for mchi in mchis:
    # txt-files containing recoil rates from WIMP scattering, convert to units 1/(kg*Myr*nm)
    # as generated by "Tracklength_spectrum.py"
    # for which the WIMP-nucleon-cross section was assumed to be 10^-45 cm^2
    dRdx_atom1 = np.loadtxt('atom1_spectrum_'+str(mchi)+'.txt')*3.1536E+4
    dRdx_atom2 = np.loadtxt('atom2_spectrum_'+str(mchi)+'.txt')*3.1536E+4

    # do the same as for background events...

    dRdx_atom1_ip = interp1d(tracklengths_atom1,dRdx_atom1,kind='cubic')
    dRdx_atom2_ip = interp1d(tracklengths_atom2,dRdx_atom2,kind='cubic')

    def dRdx(x):
        return 0.5*dRdx_atom1_ip(x)+0.5*dRdx_atom2_ip(x)#+5E-6*dRdx_H_ip(x)+1.5E-5*dRdx_C_ip(x)#+0.6496*dRdx_O_ip(x)


    S_events = np.zeros(len(xrange))
    for i in range(1,len(xrange)):
        S_events[i] = integrate.romberg(dRdx,xrange[i-1],xrange[i],divmax=50)


    S_events_smeared = np.zeros(len(xrange))

    for i in range(len(xrange)):
        def smeared(x):
            return S_events[i]*norm.pdf(x,loc=xrange[i]-sigma_x/2,scale=sigma_x)*norm.cdf(x,loc=5*sigma_x,scale=sigma_x)
        for j in range(1,len(xrange)):
            S_events_smeared[j] += integrate.quad(smeared,xrange[j-1],xrange[j],limit=5000)[0]

    S_sums = np.ones((len(xrange),len(xrange)+1))
    for i in range(1,len(xrange)):
        for j in range(1,len(xrange)+1):
            S_sums[i][j] = np.sum(S_events_smeared[i:j])

    ########################################################################################################
    # sensitivity projection:

    # compute signal-to-noise-ratio for every tracklength interval within xrange for which x_max >= x_min+2sigma_x holds
    # considering only those with at least 5 signal events
    # with the signal-to-noise-ratio being defined as   Signal_events / sqrt(Background_events + Absolute_systematic_error_of_background_events^2)
    SNRs = np.zeros((len(xrange),len(xrange)+1))
    for i in range(len(xrange)):
        for j in range(len(xrange)+1):
            if(j>=i+2 and B_sums[i][j]!=0 and S_sums[i][j]>=5):
                SNRs[i][j] = S_sums[i][j]/np.sqrt(B_sums[i][j]+Sigma_B**2*B_sums[i][j]**2)

    # the experiment is considered to be sensitive to the signal if SNR >= 3
    # -> find interval with maximal SNR and compute WIMP-nucleon-cross section needed to achieve a SNR this high,
    # which will in turn be the optimized interval regarding sensitivity

    # save this information, rounding the number of expected contributing events
    foundsigmasandcutoffs[mchi_no][0] = 3/(np.max(SNRs)/1E-45)
    cutoffindices = np.unravel_index(np.argmax(SNRs),SNRs.shape)
    foundsigmasandcutoffs[mchi_no][1] = xrange[cutoffindices[0]-1]
    foundsigmasandcutoffs[mchi_no][2] = xrange[cutoffindices[1]-1]
    foundsigmasandcutoffs[mchi_no][3] = np.around(S_sums[cutoffindices[0]][cutoffindices[1]]*3/(np.max(SNRs)))
    foundsigmasandcutoffs[mchi_no][4] = np.around(B_sums[cutoffindices[0]][cutoffindices[1]])

    np.savetxt('Sensitivities'+str(sigma_x)+'.txt',foundsigmasandcutoffs)
