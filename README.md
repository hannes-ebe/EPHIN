# EPHIN
A simple loader for Level 3 PHA data from SOHO-EPHIN.

The EPHIN sensor (Electron Proton Helium INstrument) onboard the SOHO spacecraft (SOlar and Heliospheric Observatory) is a detector to measure energy spectra. It can measure electrons with energies from 250 keV up to > 8.7 MeV and hydrogen and helium isotopes from 4 MeV/nuc up to > 53 MeV/nuc using a combination of solid state detectors.

The file ephin.py contains the class EPHIN which can be used to load level 3 PHA data for SOHO-EPHIN. The total energy deposited in the instrument is calculated as well. There are also some functions implemented to work with the data. 

An example of its use is shown in Ephin.ipynb. 
