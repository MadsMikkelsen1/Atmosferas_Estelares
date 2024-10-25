import os, sys, glob
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import normPlot

"""
TO DO:
- Perform normalisation on the test spectra
- Find more spectral lines from the example stars
- Characterise the test stars from the example stars
- Normalise the problem stars and characterise them
"""

### Seaborn customisation ###
sns.set_theme(style="darkgrid")

### Paths to example, test and problem stars ###
example_data = glob.glob("ExampleStars/*.dat")
test_data = glob.glob("TestStars/*.dat")

### Choose which stellar spectrum to plot ###
file_index_example = int(input(f"\nEnter the index of the file you want to plot [EXAMPLE STAR] (0-{len(example_data)-1}): "))
file_index_test = int(input(f"\nEnter the index of the file you want to plot [TEST STAR] (0-{len(test_data)-1}): "))

plt.figure(num=1001)

selected_example = example_data[file_index_example]
example_star = pd.read_csv(selected_example, sep='\t', header=None, names=["Wavelength", "Flux"])

sns.lineplot(x="Wavelength", y="Flux", data=example_star)
plt.title(f"Spectrum from {os.path.basename(selected_example)}")
plt.xlabel("Wavelength [A]")
plt.ylabel(r"Normalised Flux [erg/cm$^2$/A/s]")

plt.figure(num=2001)

### Normalisation of test spectrum ###
normPlot.normplot(example_star)

selected_test = test_data[file_index_test]
test_star = pd.read_csv(selected_test, sep='\t', header=None, names=["Wavelength", "Flux"])

sns.lineplot(x="Wavelength", y="Flux", data=test_star)
plt.title(f"Spectrum from {os.path.basename(selected_test)}")
plt.xlabel("Wavelength [A]")
plt.ylabel(r"Normalised Flux [erg/cm$^2$/A/s]")

### Plotting vertical lines at spectral lines of interest ###
    ### Balmer series ###
wavel = [6562.79, 4861.35, 4340.472, 4101.734, 3970.075]
for wl in wavel:
    plt.axvline(x=wl, color="red", linestyle="dotted", alpha=0.5)

#plt.close(1001)
plt.show()