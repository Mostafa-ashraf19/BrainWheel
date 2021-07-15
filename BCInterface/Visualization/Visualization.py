import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from BCInterface.Helpers import helper

channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

class graphs:

	@staticmethod
	def time_vis(df):
		"""
			parameter: dataframe for one trial
			output: graph of time domain.
		"""
		df = df.drop(columns='Label')

		plt.figure(figsize=(10,7))
		plt.plot(df+ 80 * np.arange(13,-1,-1))
		plt.yticks([])
		plt.axis('tight')
		plt.legend(channels_def)
		plt.show()

	@staticmethod
	def welch_vis(freq, power, lable, channel):
		"""
			used to visualize power spectrum for each given channel
			Parameters:
				freq,power: output from welch function "freq-power"
				channel: list of channel to visualize
				lable: list of frequecnies
        """

		num_channels = len(channel)
		xcoords = [7.50, 8.57, 10, 12]
		# colors for the lines
		colors = ['g', 'r', 'g', 'r']

		if num_channels >7:
			half = math.ceil(num_channels / 2)
			ig, axis = plt.subplots(half, 2, figsize=(20, 20))
			for i, current_c in enumerate(channel):
				# to print till freq approx equals 50 hz
				f = freq[current_c][:-80]
				Pxx_den = power[current_c][:-80]
				for xc, c in zip(xcoords, colors):
					axis[i % half, int(i >= half)].axvline(x=xc, label='line at x = {}'.format(xc), c=c)
				axis[i % half, int(i >= half)].plot(f, Pxx_den)
				axis[i % half, int(i >= half)].set_title(channels_def[current_c])
				axis[i % half, int(i >= half)].grid(True)
		else:
			ig, axis = plt.subplots(num_channels, figsize=(20, 20))
			for i, current_c in enumerate(channel):
				# to print till freq approx equals 50 hz
				f = freq[current_c][:-80]
				Pxx_den = power[current_c][:-80]
				for xc, c in zip(xcoords, colors):
					axis[i].axvline(x=xc, label='line at x = {}'.format(xc), c=c)
				axis[i].plot(f, Pxx_den)
				axis[i].set_title(channels_def[current_c])
				axis[i].grid(True)

		ig.suptitle('frequency:{}'.format(lable))

		plt.title
		plt.show()

