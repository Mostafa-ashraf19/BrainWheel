import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from BCInterface.Helpers import helper

channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

class graphs:

	@staticmethod
	def time_vis(df):
		"""
			input: dataframe for one trial
			output: figure
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
            input: output from welch function
                   list of channel to visualize
            used to visualize power spectrum for each given channel
        """

		xcoords = [7.50, 8.57, 10, 12]
		# colors for the lines
		colors = ['g', 'r', 'g', 'r']

		ig, axis = plt.subplots(int(len(channel) / 2), 2, figsize=(20, 20))
		ig.suptitle('frequency:{}'.format(lable))

		i = 0
		print(f'len of f {len(freq)}')
		for f, Pxx_den in zip(freq, power):
			# to print till freq approx equals 50 hz
			f = f[:-80]
			Pxx_den = Pxx_den[:-80]
			for xc, c in zip(xcoords, colors):
				axis[i % 7, int(i >= 7)].axvline(x=xc, label='line at x = {}'.format(xc), c=c)
			axis[i % 7, int(i >= 7)].plot(f, Pxx_den)
			axis[i % 7, int(i >= 7)].set_title(channel[i])
			axis[i % 7, int(i >= 7)].grid(True)
			i += 1


		plt.title
		plt.show()

