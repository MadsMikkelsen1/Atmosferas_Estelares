import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.integrate import simps
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
    4102: 'Hδ', # Gray
    4340: 'Hγ', # Gray
    4383: 'Fe I', # Gray
    4471: 'He I', # NIST
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
    6560: 'Hα', # Gray
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

def calculate_equivalent_width(wavelength, flux, line_center, width=5):
    """
    Calculate the equivalent width of an absorption line.

    Parameters:
    wavelength: array-like
        Array of wavelength values.
    flux: array-like
        Array of flux values.
    line_center: float
        Central wavelength of the absorption line.
    width: float
        Range around the line center to consider for integration, in Angstroms.

    Returns:
    equivalent_width: float
        The equivalent width of the absorption line.
    """
    # Define the integration range around the line center
    min_range = line_center - width
    max_range = line_center + width

    # Select the wavelength and flux in the range of interest
    mask = (wavelength >= min_range) & (wavelength <= max_range)
    selected_wavelength = wavelength[mask]
    selected_flux = flux[mask]

    continuum_flux = np.mean(selected_flux[:5])

    # Calculate the equivalent width using Simpson's rule for integration
    ew = simps(1 - (selected_flux / continuum_flux), selected_wavelength)
    
    return ew

# Calculate equivalent width for selected absorption lines
for line_wavelength, line_label in absorption_lines.items():
    if line_wavelength in [4102, 4340, 4471, 4540, 4684, 4860, 6560]:  
        ew = calculate_equivalent_width(wavelength_1, norm_flux_1, line_wavelength)
        print(f"Equivalent Width of {line_label} at {line_wavelength} Å: {ew:.2f} Å")

plt.show()
