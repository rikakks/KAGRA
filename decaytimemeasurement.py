#Author: Rikako Hatoya
#E-mail: 15hatoyar@gmail.com
#Purpose: Curve fitting decay time strains for Excitations in KAGRA Type-B SR3 Oplev
#         and measuring movement (Yaw-motion) of Test Mass.

from os import listdir
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import hilbert
from math import e, pi

time = {}
magnitude = {}


# User Input Prompt
def prompt_for_input(description):
    while True:
        try:
            return input(f"Enter {description}: ")
        except Exception:
            print("Please enter a valid input.")


# Showing all measurement files available and importing user-specified data file
def import_data():
    print("All files in directory: ")
    for thing in listdir("Data/"):
        print(thing)
    filename = prompt_for_input("name of file to open")
    fp = "Data/" + filename
    time[filename], magnitude[filename] = np.transpose(np.genfromtxt(fp))
    return filename, time[filename], magnitude[filename]


# Plot Settings
def plot_settings(filename):
    plt.title(filename)
    plt.xlabel("Time [s]")
    plt.ylabel("Magnitude [μrad]")
    plt.subplots_adjust(left=0.06, right=0.99)
    return


def create_graph():
    while True:
        plt.plot(x_data, y_data, label='Measurement Data', color='#1e9cce')
        plt.plot(x_data, y_env, label='Envelope Equation', color="#267777")

        #Curve Fit of the Envelop Function
        x_min = float(prompt_for_input("min x-value of curve fit"))
        x_max = float(prompt_for_input("max x-value of curve fit"))
        min_count = 0
        while x_data[min_count] < x_min:
            min_count += 1
        max_count = min_count
        while x_data[max_count] < x_max:
            max_count += 1

        # Model exponential function for fitting
        def func(x, t_1, a, b):
            return a * (e**(-(x - x_min) / t_1)) + b

        popt, pcov = curve_fit(func, x_data[min_count:max_count],
                               y_env[min_count:max_count])
        print("Decay Time: ", popt[0], ", A/e = ", popt[1] / e)
        print("(t_1=", popt[0], "a=", popt[1], "b=", popt[2], ")")

        plt.plot(
            x_data[min_count:max_count],
            func(x_data[min_count:max_count], *popt),
            label="Linear Regression",
            color="#1a487c")
        plot_settings(filename)
        plt.show()


# Initial Set-up: importing Data and plotting measurement graph
filename, x_data, y_data = import_data()
plt.plot(x_data, y_data, label='Measurement Data', color='#1e9cce')
y_env = np.abs(hilbert(y_data))
plt.plot(x_data, y_env, label='Envelope Equation', color="#267777")
plot_settings(filename)
plt.show()

# Create Graph Adjusting to the User Preference
create_graph()
