# compute the integrals over neutrino fluxes needed for computation of neutrino recoil spectra
# saved in "Neutrino_background/Integrated_fluxes"

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import scipy.integrate as integrate


c_light = 3E+08
u = 931.5E+06*1.6E-19/c_light**2 #atomic mass unit in kg
##########################################################################################
# mass in kg of considered recoiling nucleus
M=1.008*u

# same recoil energies as considered for the tracklength spectra (from the table generated by SRModule), convert to J
ER = np.loadtxt('SRIM-table-file',usecols=(0),unpack=True)*1.6E-16
# and corresponding tracklengths in m
tracklengths = np.loadtxt('tracklengths.txt')

ldata=len(ER)
##############################################################################################################

# txt-files containing neutrino fluxes (solar,atmospheric,supernova) in 1/(cm^2 s MeV) with the respective neutrino energy in MeV
# fluxes and their respective energy ranges (i.e. the maximum energy of each contribution) taken from https://arxiv.org/pdf/1604.03858.pdf
# and saved in "Neutrino_background/Neutrino_flux"
# (monoenergetic contributions to the flux will be accounted for in the integration)
E_1,flux_11,flux_12,flux_13,flux_14 = np.loadtxt('nu-flux_1.txt',unpack=True)
E_2,flux_21,flux_22,flux_23,flux_24 = np.loadtxt('nu-flux_2.txt',unpack=True)

# convert them to J and 1/(m^2 s J) rsepectively
E_1 = E_1*1.6E-13
E_2 = E_2*1.6E-13
flux_11 = flux_11/1.6E-17
flux_12 = flux_12/1.6E-17
flux_13 = flux_13/1.6E-17
flux_14 = flux_14/1.6E-17
flux_21 = flux_21/1.6E-17
flux_22 = flux_22/1.6E-17
flux_23 = flux_23/1.6E-17
flux_24 = flux_24/1.6E-17

#############################################################################################################
# interpolate fluxes and flux/E^2 within their respective energy ranges

def flux_11ip(E):
    ip = interp1d(E_1,flux_11,kind='cubic')
    if(E<0.42341*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_11ip_d_Enu2(E):
	return flux_11ip(E)/E**2

def flux_12ip(E):
    ip = interp1d(E_1,flux_12,kind='cubic')
    if(E<=18.726*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_12ip_d_Enu2(E):
	return flux_12ip(E)/E**2

def flux_13ip(E):
    ip = interp1d(E_1,flux_13,kind='cubic')
    if(E<=16.360*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_13ip_d_Enu2(E):
	return flux_13ip(E)/E**2

def flux_14ip(E):
    ip = interp1d(E_1,flux_14,kind='cubic')
    if(E<=1.199*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_14ip_d_Enu2(E):
	return flux_14ip(E)/E**2

def flux_21ip(E):
    ip = interp1d(E_2,flux_21,kind='cubic')
    if(E<=1.732*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_21ip_d_Enu2(E):
	return flux_21ip(E)/E**2

def flux_22ip(E):
    ip = interp1d(E_2,flux_22,kind='cubic')
    if(E<=1.740*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_22ip_d_Enu2(E):
	return flux_22ip(E)/E**2

def flux_23ip(E):
    ip = interp1d(E_2,flux_23,kind='cubic')
    if(E<=91.201*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_23ip_d_Enu2(E):
	return flux_23ip(E)/E**2

def flux_24ip(E):
    ip = interp1d(E_2,flux_24,kind='cubic')
    if(E>=13.379*1.6E-13 and E<=981.748*1.6E-13):
        return ip(E)
    else:
        return 0
def flux_24ip_d_Enu2(E):
	return flux_24ip(E)/E**2

############################################################################################

# arrays in which the integrated quantities can be written for each recoil energy
Phi = np.zeros(ldata)
Phi_d_Enu2 = np.zeros(ldata)

# perform computations only for recoil energies which produce tracklengths long enough to be of interest in order to save time
start_integration = 0
while (tracklengths[start_integration] < 0.9E-9):
	start_integration +=1

for j in range(start_integration,ldata):
    print(ldata-j)
    # lower integration limit
    Enu_min = np.sqrt(M*c_light**2*ER[j]/2)

    # perform integrations, summing over each contribution
    Phi[j] = integrate.quad(flux_11ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_12ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_13ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_14ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_21ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_22ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_23ip,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_24ip,Enu_min,1000*1.6E-13,limit=100)[0]
    Phi_d_Enu2[j] = integrate.quad(flux_11ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_12ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_13ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_14ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_21ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_22ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_23ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]+integrate.quad(flux_24ip_d_Enu2,Enu_min,1000*1.6E-13,limit=100)[0]

    # account for the monoenergetic contributions
    if(Enu_min<=384.3E3*1.6E-19):
        Phi[j] += 4.8E+08/1.6E-17*384.3E3*1.6E-19
        Phi_d_Enu2[j] += 4.8E+08/1.6E-17/(384.3E3*1.6E-19)
    if(Enu_min<=861.3E3*1.6E-19):
        Phi[j] += 4.3E+09/1.6E-17*861.3E3*1.6E-19
        Phi_d_Enu2[j] += 4.3E+09/1.6E-17/(861.3E3*1.6E-19)
    if(Enu_min<=1.446E+06*1.6E-19):
        Phi[j] += 1.5E+08/1.6E-17*1.446E+06*1.6E-19
        Phi_d_Enu2[j] += 1.5E+08/1.6E-17/(1.446E+06*1.6E-19)

# save this to be able to compute neutrino recoil spectra with "Neutrino_background.py"
np.savetxt('nu-flux.txt',Phi)
np.savetxt('nudEnu2.txt',Phi_d_Enu2)
