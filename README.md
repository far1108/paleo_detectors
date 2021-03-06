# Paleo detectors
[Python scripts](python-Scripts) and the resulting [data](Data) used in my bachelor thesis on WIMP-induced nuclear recoil tracks.

- [Tracklength_spectrum.py](python-Scripts/Tracklength_spectrum.py): calculating tracklengths and differential recoil spectra for one element in a solid based on stopping powers obtained with SRIM.
- [Neutrino_flux_integration.py](python-Scripts/Neutrino_flux_integration.py) and [Neutrino_background.py](python-Scripts/Neutrino_background.py): computing differential recoil spectra induced by neutrino background.
- [Sensitivity_projection.py](python-Scripts/Sensitivity_projection.py): finding projected sensitivities based on a simple cut-and-count-analysis.
- [TRIM_tracklengths.py](python-Scripts/TRIM_tracklengths.py): calculating mean tracklengths and straggling based on TRIM simulation using TRIM-output file 'EXYZ.txt'


Curiously enough I obtained wrong results with this code using versions of Python below 3.7., so you might have to upgrade. The libraries I used are listed [here](requirements.txt).
