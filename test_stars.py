import os, sys, glob
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter

sns.set_theme(style="darkgrid")

G_star = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/TestStars/HD109358_melchiors347600.dat"
B_star = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/TestStars/HD120315_Melchiors327246.dat"
F_star = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/TestStars/HD194093_Melchiors474733.dat"



data_G = np.loadtxt(G_star)
wavelength_G = data_G[:, 0]
flux_G = data_G[:, 1]

data_B = np.loadtxt(B_star)
wavelength_B = data_B[:, 0]
flux_B = data_B[:, 1]

data_F = np.loadtxt(F_star)
wavelength_F = data_F[:, 0]
flux_F = data_F[:, 1]

def normalize_spectrum_smooth(wavelength, flux, window_length=101, polyorder=3):
    smoothed_flux = savgol_filter(flux, window_length, polyorder)

    norm_flux = flux / smoothed_flux

    return norm_flux

# Example: Normalizing the G_star spectrum with a smoothing method
norm_flux_G_smooth = normalize_spectrum_smooth(wavelength_G, flux_G)
norm_flux_F_smooth = normalize_spectrum_smooth(wavelength_F, flux_F)
norm_flux_B_smooth = normalize_spectrum_smooth(wavelength_B, flux_B, polyorder=1)

# Important absorption lines for classification
absorption_lines = {
    r'H_{\alpha}': 6563,
    r'H_{\beta}': 4861,
    r'H_{\gamma}': 4341,
    r'H_{\delta}': 4102,
    'He I 4471': 4471,
    'He I 4026': 4026,
    'Ca II K': 3933,
    'Ca II H': 3968,
    'Fe I 4383': 4383,
    'Fe I 5270': 5270,
    'Na I D1': 5890,
    'Na I D2': 5896
}
# Group absorption lines by element for consistent coloring
element_colors = {
    'H': 'r',
    'He': 'g',
    'Ca': 'b',
    'Mg': 'm',
    'Fe': 'y',
    'Na': 'c'
}

# Plotting the normalized and unnormalized spectra for G star
plt.figure()
plt.plot(wavelength_G, flux_G, label='Unnormalized Flux', linestyle='-', alpha=0.5)
plt.plot(wavelength_G, norm_flux_G_smooth, label='Normalized Flux', linestyle='-')
for line_name, line_wavelength in absorption_lines.items():
    element = line_name.split()[0] if ' ' in line_name else line_name.split('_')[0]
    color = element_colors.get(element, 'k')
    plt.axvline(x=line_wavelength, color=color, linestyle=':', label=f'${line_name}$')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.title('HD109358 (G Star) - Normalized and Unnormalized Spectrum')
plt.legend()
plt.show()

# Plotting the normalized and unnormalized spectra for F star
plt.figure()
plt.plot(wavelength_F, flux_F, label='Unnormalized Flux', linestyle='-', alpha=0.5)
plt.plot(wavelength_F, norm_flux_F_smooth, label='Normalized Flux', linestyle='-')
for line_name, line_wavelength in absorption_lines.items():
    element = line_name.split()[0] if ' ' in line_name else line_name.split('_')[0]
    color = element_colors.get(element, 'k')
    plt.axvline(x=line_wavelength, color=color, linestyle=':', label=f'${line_name}$')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.title('HD194093 (F Star) - Normalized and Unnormalized Spectrum')
plt.legend()
plt.show()

# Plotting the normalized and unnormalized spectra for B star
plt.figure()
plt.plot(wavelength_B, flux_B, label='Unnormalized Flux', linestyle='-', alpha=0.5)
plt.plot(wavelength_B, norm_flux_B_smooth, label='Normalized Flux', linestyle='-')
for line_name, line_wavelength in absorption_lines.items():
    element = line_name.split()[0] if ' ' in line_name else line_name.split('_')[0]
    color = element_colors.get(element, 'k')
    plt.axvline(x=line_wavelength, color=color, linestyle=':', label=f'${line_name}$')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.title('HD120315 (B Star) - Normalized and Unnormalized Spectrum')
plt.legend()
plt.show()
