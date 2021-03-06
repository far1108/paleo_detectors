# calculate tracklengths and recoil spectra induced by WIMP scattering for one sort of nuclei in a mineral
# results saved in "Data/Tracklengths_recoilrates"

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sp
import scipy.integrate as integrate
from scipy.interpolate import interp1d

c_light = 3E+08
m_n = 939E+06*1.6E-19/c_light**2 #nucleon mass in kg
u = 931.5E+06*1.6E-19/c_light**2 #atomic mass unit in kg
#######################################################################################

# Enter number of nucleons and mass (in kg) of considered nucleus
A=1
M=1.008*u

############################################################################################################################
# txt-file which consists of three columns (as generated by SRModule (chopping off the header)):
# recoil energy (keV), stopping power due to energy loss to target electrons (eV/Angstrom), stopping power due to energy loss to target nuclei (eV/Angstrom)
# the lowest included recoil energy should be "very small" and the spacing between them tight enough as to guarentee reasonable interpolations
ER,dEdx_el,dEdx_nucl = np.loadtxt('SRIM-table-file',unpack=True)

ER = ER*1.6E-16 #recoil energy in J
dEdx = (dEdx_nucl+dEdx_el)*1.6E-9 #total stopping power in J/m
l = len(ER)

##############################################################################################################################

# calculate expected track length for every considered recoil energy
# from the SRIM data find the dependency dx/dE(E)
dEdx_ip = interp1d(ER,dEdx,kind='cubic')
def dxdE(E):
	return 1/(dEdx_ip(E))

# integrating (dx/dE(E))dE from 0 to ER yields the expected track length for the recoil energy ER
def x(E):
	return integrate.quad(dxdE,ER[0],E)[0]

# calculate for every considered recoil energy
x_T = np.zeros(l)
for i in range(l):
	x_T[i] = x(ER[i])

#save for further use
np.savetxt('tracklengths.txt',x_T)
########################################################################################################################

# Helm form factor
# needed parameters (in fm)
s = 0.9
a = 0.52
c = (1.23*A**(1/3)-0.6)
R_1 = np.sqrt(c**2+7/3*np.pi**2*a**2-5*s**2)

# spherical Bessel function
def j_1(x):
	return np.sin(x)/x**2-np.cos(x)/x

# calculate momentum transfer in 1/fm depending on recoil energy in J
def q(E):
	return np.sqrt(2*(M/1.6E-10*c_light**2)*(E/1.6E-16)*10**(-6))/0.197

# calculate Helm form factor |F^2(q)| depending on momentum transfer in 1/fm
def F2(q):
	return (3*j_1(q*R_1)/(q*R_1))**2*np.exp(-q**2*s**2)

########################################################################################

# WIMP velocity distribution assumed as in Standard Halo Model (relative to galactic rest frame, neglecting motion of earth relative to sun)
# needed parameters (in m/s)
v_esc = 550000 # galactic escape velocity
v_obs = 230000 # velocity of solar system
sigma_v = 166000 # assumed WIMP velocity dispersion
N_esc = (sp.erf(v_esc/(np.sqrt(2)*sigma_v))-np.sqrt(2/np.pi)*v_esc/sigma_v*np.exp(-v_esc**2/(2*sigma_v**2))) #normalization factor

######################################################################################
# Enter assumed WIMP-nucleon-cross section (in m^2), assumed local WIMP mass density (in GeV/cm^3) and list of considered WIMP-masses (in GeV)
sigma_n = 1E-49
rho_chi = 0.4
for m_chi_GeV in [1,2,5,10,20,50,100,200,500,1000]:

	rho_d_m = (rho_chi/m_chi_GeV)*10**6 # expected WIMP-number density per m^3
	m_chi = m_chi_GeV*1E9*1.6E-19/c_light**2 # WIMP-mass in kg
	mu = M*m_chi/(m_chi+M) # WIMP-nucleus reduced mass
	mu_n = m_n*m_chi/(m_chi+m_n) # WIMP-nucleon reduced mass

	#######################################################################################

	# recoil rate per unit target mass depending on recoil energy (convolution of differential cross section and velocity distribution)
	def dRdE_func(E):
		v_min = np.sqrt(2*M*E)/(2*mu)
		v_plus = min(v_min+v_obs,v_esc)
		v_minus = min(v_min-v_obs,v_esc)
		prefactor = 2*rho_d_m*A**2*sigma_n/(4*mu_n**2)*F2(q(E))
		return prefactor/N_esc*(1/(2*v_obs)*(sp.erf(v_plus/(np.sqrt(2)*sigma_v))-sp.erf(v_minus/(np.sqrt(2)*sigma_v)))-(v_plus - v_minus)/(np.sqrt(2*np.pi)*v_obs*sigma_v)*np.exp(-v_esc**2/(2*sigma_v**2)))

	# calculate for every considered recoil energy
	dRdE = np.zeros(l)
	for i in range(l):
		dRdE[i] = dRdE_func(ER[i])

	#########################################################################################

	# finally the recoil rate depending on the track length in 1/(kg*s*m) is obtained by multiplying dRdE*dEdx
	dRdx = np.zeros(l)
	for i in range(l):
		dRdx[i] = dRdE[i]*dEdx[i]

	# where the rate dRdx[i] corresponds to the track length x_T[i]

	#########################################################################################

	# save it
	np.savetxt('spectrum_'+str(m_chi_GeV)+'.txt',dRdx)

	# or just plot it (x_T in nm and dRdx in 1/(kg*Myr*nm))
	# plt.plot(x_T*10**9,dRdx*3.1536E+4)
	# plt.ylim(1E-4,1E6)
	# plt.xscale('log')
	# plt.yscale('log')
	# plt.show()
