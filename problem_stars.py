import os, sys, glob
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import normPlot
from scipy.signal import find_peaks, savgol_filter
sns.set_theme(style="darkgrid")

def normalize_spectrum_smooth(wavelength, flux, window_length=101, polyorder=3):
    """
    Normalize the flux of the spectrum by smoothing over local peaks.

    Parameters:
    wavelength: array-like
        Array of wavelength values.
    flux: array-like
        Array of flux values.
    window_length: int
        The length of the filter window (number of points). Must be odd.
    polyorder: int
        The order of the polynomial used to fit the samples.

    Returns:
    norm_flux: array-like
        The normalized flux.
    """
    # Smooth the flux to estimate the continuum
    smoothed_flux = savgol_filter(flux, window_length, polyorder)

    # Normalize the flux
    norm_flux = flux / smoothed_flux

    return norm_flux

# Function to load and normalize unknown spectra
def process_unknown_spectrum(file_path):
    data = np.loadtxt(file_path)
    wavelength = data[:, 0]
    flux = data[:, 1]
    norm_flux = normalize_spectrum_smooth(wavelength, flux)
    return wavelength, flux, norm_flux

# Important absorption lines for classification
absorption_lines = {
    r'H_{\alpha}': 6563,
    r'H_{\beta}': 4861,
    r'H_{\gamma}': 4341,
    r'H_{\delta}': 4102,
    r'He I 4471': 4471,
    r'He I 4026': 4026,
    r'Ca II K': 3933,
    r'Ca II H': 3968,
    r'Fe I 4383': 4383,
    r'Na I D1': 5890,
    r'Na I D2': 5896
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

# Function to plot spectra
def plot_spectrum(wavelength, flux, norm_flux, title):
    plt.figure()
    plt.plot(wavelength, flux, label='Unnormalized Flux', linestyle='-', alpha=0.5)
    plt.plot(wavelength, norm_flux, label='Normalized Flux', linestyle='-')
    for line_name, line_wavelength in absorption_lines.items():
        element = line_name.split()[0] if ' ' in line_name else line_name.split('_')[0]
        color = element_colors.get(element, 'k')
        plt.axvline(x=line_wavelength, color=color, linestyle=':', label=f'${line_name}$')
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(title)
    plt.legend()
    plt.show()

# Example usage for unknown spectra
problem_star_1 = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar1.dat"
problem_star_2 = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar2.dat"

wavelength_1, flux_1, norm_flux_1 = process_unknown_spectrum(problem_star_1)
plot_spectrum(wavelength_1, flux_1, norm_flux_1, 'Unknown Star 1 - Normalized and Unnormalized Spectrum')

wavelength_2, flux_2, norm_flux_2 = process_unknown_spectrum(problem_star_2)
plot_spectrum(wavelength_2, flux_2, norm_flux_2, 'Unknown Star 2 - Normalized and Unnormalized Spectrum')

# Adding main sequence test stars
main_sequence_stars = {
    'O4V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD46223_O4V_Melchiors517392.dat",
    'O8V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD48279_O8V_Melchiors506884.dat",
    'B0.2V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD149438_B0V_Melchiors885093.dat",
    'B3V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD32630_B3V_Melchiors343338.dat",
    'B5V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD45321_B5V_Melchiors868970.dat"
}

# Plotting all main sequence stars in a single figure for comparison
plt.figure(figsize=(15, 10))
for star_type, file_path in main_sequence_stars.items():
    data = np.loadtxt(file_path)
    wavelength = data[:, 0]
    flux = data[:, 1]
    plt.plot(wavelength, flux, label=f'{star_type}', linestyle='-')
    for line_name, line_wavelength in absorption_lines.items():
        element = line_name.split()[0] if ' ' in line_name else line_name.split('_')[0]
        color = element_colors.get(element, 'k')
        plt.axvline(x=line_wavelength, color=color, linestyle=':', alpha=0.3)

plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.title('Comparison of Main Sequence Stars - Normalized Spectra')
plt.legend()
plt.show()