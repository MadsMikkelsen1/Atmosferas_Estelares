import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import seaborn as sns
sns.set_theme(style="darkgrid")

unknown_stars = {
    'unknown_star_1': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar1.dat",
    'unknown_star_2': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar2.dat"
}

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

# Constants for separating spectra on the plot
flux_offset = 2.0

# Function to normalize spectrum
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

# Function to plot spectra with annotated absorption lines
def plot_spectrum_with_lines(wavelength, flux, norm_flux, title):
    plt.figure(figsize=(15, 10))
    plt.plot(wavelength, flux, label='Unnormalized Flux', linestyle='-', alpha=0.5)
    plt.plot(wavelength, norm_flux, label='Normalized Flux', linestyle='-')
    
    # Adding vertical lines for absorption lines with labels
    label_y_positions = []
    for line_wavelength, line_label in absorption_lines.items():
        y_position = min(norm_flux) - 0.05 * (max(norm_flux) - min(norm_flux)) 
        plt.axvline(x=line_wavelength, color='k', linestyle='--', ymin=0.05, ymax=0.95, alpha=0.5)
        plt.text(line_wavelength + 10, y_position, line_label, color='k', fontsize=8, rotation=90, verticalalignment='bottom')

    
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(title)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

# Example usage for problem stars
unknown_star_1 = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar1.dat"
unknown_star_2 = "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ProblemStar2.dat"

# Process the unknown spectra
wavelength_1, flux_1 = np.loadtxt(unknown_star_1, unpack=True)
norm_flux_1 = normalize_spectrum_smooth(wavelength_1, flux_1)
plot_spectrum_with_lines(wavelength_1, flux_1, norm_flux_1, 'Unknown Star 1 - Normalized and Unnormalized Spectrum')

wavelength_2, flux_2 = np.loadtxt(unknown_star_2, unpack=True)
norm_flux_2 = normalize_spectrum_smooth(wavelength_2, flux_2)
plot_spectrum_with_lines(wavelength_2, flux_2, norm_flux_2, 'Unknown Star 2 - Normalized and Unnormalized Spectrum')

plt.show()
