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

absorption_lines = {
    3932: 'Ca II', # Gray
    3967: 'Ca II', # Gray
    4030: 'blend', # Gray
    4101: 'Hδ', # Gray
    4338: 'Hγ', # Gray
    4383: 'Fe I', # Gray
    4540: 'He II', # Walborn & Fitzpatrick 1990
    4684: 'He II', # Walborn & Fitzpatrick 1990
    4860: 'Hβ', # Gray
    4921: 'Fe I', # Gray
    5014: 'TENT.',
    5411: 'TENT.',
    5875: 'TENT.',
    5890: 'Na I D1', # Gray, Morton 2003
    5896: 'Na I D2', # Gray, Morton 2003
    6270: 'TENT.',
    6284: 'DIB', # Snow, York & Welty 1977, Herbig 1995
    6347: 'TENT.',
    6380: 'TENT.',
    6561: 'Hα', # Gray
    6614: 'DIB', # Herbig 1995
    6684: 'TENT.'
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
# Function to plot spectra with annotated absorption lines
def plot_spectrum(wavelength, flux, norm_flux, title):
    plt.figure(figsize=(15, 10))
    plt.plot(wavelength, flux, label='Unnormalized Flux', linestyle='-', alpha=0.5)
    plt.plot(wavelength, norm_flux, label='Normalized Flux', linestyle='-')
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(title)
    plt.legend()
    plt.show()

# Example usage for unknown spectra
unknown_star_1 = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar1.dat"
unknown_star_2 = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar2.dat"

wavelength_1, flux_1, norm_flux_1 = process_unknown_spectrum(unknown_star_1)
plot_spectrum(wavelength_1, flux_1, norm_flux_1, 'Unknown Star 1 - Normalized and Unnormalized Spectrum')

wavelength_2, flux_2, norm_flux_2 = process_unknown_spectrum(unknown_star_2)
plot_spectrum(wavelength_2, flux_2, norm_flux_2, 'Unknown Star 2 - Normalized and Unnormalized Spectrum')

label_y_positions = []
for line_wavelength, line_label in absorption_lines.items():
    if line_wavelength == 5875:  # Plotting He I at 5875 differently
        y_position = max(label_y_positions) + 0.5 if label_y_positions else 0
        plt.axvline(x=line_wavelength, color='k', linestyle='--', ymin=0.05, ymax=0.95, alpha = 0.5)
        plt.text(line_wavelength - 25, y_position, 'He I', color='k', fontsize=8, rotation=90, verticalalignment='bottom')
        label_y_positions.append(y_position)
    elif line_wavelength not in [5890, 5896]:  # Skip Na I D1 and D2 for later plotting
        y_position = max(label_y_positions) + 0.5 if label_y_positions else 0
        plt.axvline(x=line_wavelength, color='k', linestyle='--', ymin=0.05, ymax=0.95, alpha = 0.5)
        plt.text(line_wavelength + 12, y_position, line_label, color='k', fontsize=8, rotation=90, verticalalignment='bottom')
        label_y_positions.append(y_position)

# Adding Na I D1 and D2 lines separately for better readability
plt.axvline(x=5890, color='k', linestyle='--', ymin=0.05, ymax=0.95, alpha = 0.5)
y_position = max(label_y_positions) + 0.5 if label_y_positions else 0
plt.text(5890 - 5, y_position, 'Na I D1', color='k', fontsize=8, rotation=90, verticalalignment='bottom')
label_y_positions.append(y_position)

plt.axvline(x=5896, color='k', linestyle='--', ymin=0.05, ymax=0.95, alpha = 0.5)
y_position = max(label_y_positions) - 2.5
plt.text(5896 + 5, y_position, 'Na I D2', color='k', fontsize=8, rotation=90, verticalalignment='bottom')
label_y_positions.append(y_position)

# Adding main sequence test stars (already normalized)
main_sequence_stars = {
    'O4V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD46223_O4V_Melchiors517392.dat",
    'O8V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD48279_O8V_Melchiors506884.dat",
    'B0.2V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD149438_B0V_Melchiors885093.dat",
    'B3V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD32630_B3V_Melchiors343338.dat",
    'B5V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD45321_B5V_Melchiors868970.dat"
}

# Linestyles for the main sequence stars
linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]

# Plotting all main sequence stars in a single figure for comparison
plt.figure(figsize=(15, 10))
for (star_type, file_path), linestyle in zip(main_sequence_stars.items(), linestyles):
    data = np.loadtxt(file_path)
    wavelength = data[:, 0]
    flux = data[:, 1]
    plt.plot(wavelength, flux, label=f'{star_type}', linestyle=linestyle)
    
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.title('Comparison of Main Sequence Stars - Normalized Spectra')
plt.ylim(-0.15, 1.1)
plt.legend()
plt.show()