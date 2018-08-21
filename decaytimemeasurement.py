#Author: Rikako Hatoya
#E-mail: 15hatoyar@gmail.com
#Purpose: Curve fitting decay time strains for Excitations in KAGRA Type-B SR3 Oplev
#         and measuring movement (Yaw-motion) of Test Mass.

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import hilbert, chirp
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


# Model exponential function for fitting
def func(x, w_1, w_2, t_1, t_2, a, b, c):
    return a * (e**(-x / t_1)) * np.sin(w_1 * x) + b * (e**(
        -x / t_2)) * np.sin(w_2 * x) + c


while True:
    filename = prompt_for_input("name of file")
    fp = "Data/" + filename
    time[filename], magnitude[filename] = np.transpose(np.genfromtxt(fp))
    x = time[filename]
    y = magnitude[filename]

    plt.plot(x, y, label='Original Data')
    plt.title("K1:VIS-SR3_TM_DAMP_Y_IN1_" + filename)
    plt.xlabel("Time [s]")
    plt.ylabel("Magnitude [μm]")

    #Envelope function
    y = np.abs(hilbert(y))
    plt.plot(x, y)

    # Moving average of the Envelope Function
    N = 100000
    y = (np.convolve(np.ones((N, )) / N, y, mode='same'))
    plt.plot(x, y, label='Moving Average')

    #Curve Fit of the Envelop Function
    popt, pcov = curve_fit(func, x, y)
    print("w_1=", popt[0] / (2 * pi), "w_2=", popt[1] / (2 * pi), "t_1=",
          popt[2], "t_2=", popt[3], "a=", popt[4], "b=", popt[5], "c=",
          popt[6])

    print("Decay Time= ", y[0] / e)
    plt.plot(x, func(x, *popt), label="Linear Regression")

    plt.subplots_adjust(left=0.06, right=0.99)
    plt.figure(figsize=(20, 10))
    plt.show()
