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
#   1. Change the filename in the load_data(filename) call to the name of your data file.
#   2. Change the conversion_factor to convert from the measurement unit of your compressor to the kPa.
# 
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def load_data(filename):
    with open(filename) as f:
        content = json.load(f)

        return content['data'][:-1]

def maximal_number_of_sessions(reg):
    # Calculate the slope and intercept of the regression line
    slope = reg.coef_[0]
    intercept = reg.intercept_
    
    # Define the y value at which you want to find the corresponding x value
    y_value = 200
    
    # Calculate the x value at which the regression line crosses the given y value
    return (y_value - intercept) / slope

# Change the filename to the name of your data file.
data = load_data("L24R2.json")

# The compressor that was used in the test at Inventors' Way provides the tank
# pressure in psi, while the script assumes the pressure is in kPa. 
#
# This conversion must be changes to convert from the unit of the DUT to kPa.
conversion_factor = 6.89475729 #psi to kPa

# Collect the air tank pressures from the loaded data
pressure = []
sessions = []


for index, session in enumerate(data, 1):
    survey = session['SURVEY']
    
    # Check if the data set for the SURVEY test contains the air tank pressure
    # (PRESSURE) key is present in the collection.
    #
    # If for some reason the test was not run, either because of an operator 
    # error or if it is the last session in the test where the supply pressure
    # failed then this key will not be present in the data set.
    if 'PRESSURE' in survey:
        value = survey['PRESSURE'] * conversion_factor
        pressure.append(value)
        sessions.append(index)

pressure = np.array(pressure)
sessions = np.array(sessions)

# Perform linear regression on the data in order to acount for measurement errors
# in each individual session.
x = sessions.reshape((-1, 1))
reg = LinearRegression().fit(x, pressure)

# Make predictions using the model
pressure_pred = reg.predict(x)

numberOfSessions = maximal_number_of_sessions(reg)

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
plt.title('24L Compressor')

# Create the plot
plt.scatter(sessions, pressure, color='blue')
plt.plot(sessions, pressure_pred, color='black')
plt.xlim([0, 18])
#plt.xticks([0, 5, 10, 15, 20], ['0', '5', '10', '15', '20'])
plt.ylim([0, 800])

# Show the plot
plt.savefig('L24R2.png')
plt.show()

# Determining and printing our the maximal number of sessions that can be 
# performed consequetively with the DUT.
print("Maximal number of sessions with the device under test: {maxSessions:.0f} sessions".format(maxSessions = numberOfSessions))
print("Average air pressure drop for each session: {slope:.0f} kPa".format(slope = -reg.coef_[0]))