import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

# File paths for the selected stars
main_sequence_stars = {
    'O4V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD46223_O4V_Melchiors517392.dat",
    'O8V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD48279_O8V_Melchiors506884.dat",
    'B0.2V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD149438_B0V_Melchiors885093.dat",
    'B3V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD32630_B3V_Melchiors343338.dat",
    'A0V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD103287_A0V_Melchiors475111.dat",
    'A4V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD216956_A4V_Melchiors584202.dat",
    'F2V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD113139_F2V_Melchiors347601.dat",
    'F5V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD134083_F5V_Melchiors340879.dat",
    'G0V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD141004_G0V_Melchiors327763.dat",
    'G5V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD50806_G5V_Melchiors956756.dat",
    'K0V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD185144_K0V_Melchiors361734.dat",
    'M0V': "/Users/madsmikkelsen/ULL/1. Semester/Atmosferas_Estelares/ExampleStars/HD79211_M0V_Melchiors389347.dat"
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
    6284: 'DIB', # Snow, York & Welty 1977, Herbig 1995
    6347: 'TENT.',
    6380: 'TENT.',
    6561: 'Hα', # Gray
    6614: 'DIB', # Herbig 1995
    6684: 'TENT.'
}

# Constants for separating spectra on the plot
flux_offset = 2.0

# Plotting the spectra with offsets
plt.figure(figsize=(12, 10))
for i, (star_type, file_path) in enumerate(main_sequence_stars.items()):
    data = np.loadtxt(file_path)
    wavelength = data[:, 0]
    flux = data[:, 1]
    
    # Offset the flux for better visibility
    plt.plot(wavelength, flux + i * flux_offset, label=f'{star_type}')

    plt.text(wavelength[-1] + 50, flux[-1] + i * flux_offset, star_type, color=plt.gca().lines[-1].get_color(), fontsize=10, verticalalignment='center')

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

plt.xlabel('Wavelength (Å)')
plt.ylabel('Normalized Flux + Constant')
plt.show()
