# ANALYSIS OF COMPRESSOR DATA
#
# This script will load the data from the ctscpmauto@labbench.io and will plot
# the remaining pressure at the end of each session as a function of the number
# of sessions run.
#
# The script assumes that the data export from LabBench contains only sessions
# that are run in chronological order, from when the air tank was fully 
# pressurised until the air tank was depleted and that the last session failed
# because the LabBench CPAR+ reported to low supply pressure.
#
# For that reason the last session in the data set is discarded from the data 
# analysis.
#
# To use the script to analyse data for your compressor (Device Under Test (DUT):
#
#   1. Change the filename in line 38 to the name of your data file.
#   2. Change the conversion factor in line 44 to convert from the measurement 
#      unit of your compressor to the kPa.
# 
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def load_data(filename):
    with open(filename) as f:
        content = json.load(f)

        return content['data'][:-1]

def maximal_number_of_sessions(pressure):
    for index, value in enumerate(pressure, 1):
        if (value < 200):
            return index - 1
    
    return len(pressure) + 1

# Change the filename to the name of your data file.
data = load_data("L24compressor.json")

# The compressor that was used in the test at Inventors' Way provides the tank
# pressure in psi, while the script assumes the pressure is in kPa. 
#
# This conversion must be changes to convert from the unit of the DUT to kPa.
conversion_factor = 6.89475729 #psi to kPa

pressure = np.array([session['SURVEY']['PRESSURE'] * conversion_factor for session in data])
pressure[11] = 54 * conversion_factor # Data entry error during the test (these things happens unfortunately)
sessions = np.array(range(1, len(pressure) + 1))

# Perform linear regression on the data in order to acount for measurement errors
# in each individual session.
x = sessions.reshape((-1, 1))
reg = LinearRegression().fit(x, pressure)

# Make predictions using the model
pressure_pred = reg.predict(x)

# Plotting the data in a figure that displayes the remaining air tank pressure
# at the end of each session as a function of the number of sessions that has 
# been executed.
fig, ax = plt.subplots()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set the x-axis label
plt.xlabel('Sessions []')

# Set the y-axis label
plt.ylabel('Pressure [kPa]')

# Set the title
plt.title('Pressure at the end of a session')

# Create the plot
plt.scatter(sessions, pressure, color='blue')
plt.plot(sessions, pressure_pred, color='black')
plt.xlim([0, 20])
plt.xticks([0, 5, 10, 15, 20], ['0', '5', '10', '15', '20'])

# Show the plot
plt.savefig('L24.png')
plt.show()

# Determining and printing our the maximal number of sessions that can be 
# performed consequetively with the DUT.
print("Maximal number of sessions with the device under test: {maxSessions} sessions".format(maxSessions = maximal_number_of_sessions(pressure_pred)))
print("Average air pressure drop for each session: {slope:.1f} kPa".format(slope = -reg.coef_[0]))

## copy-paste area
