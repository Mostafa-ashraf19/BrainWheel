import math
import pandas as pd
import numpy as np

from scipy import signal
from .freq_function import *


class helper:

	@staticmethod
	def CAR(Data, train = True):
		"""
			input: dataframe of one trial
			return: dataframe
			description: remove common noise affects all channels
		"""
		if not train:
			mean = Data.mean(axis=1)
			for i in Data.columns[:]:
				Data[i] = Data[i] - mean
		else:
			mean = Data.mean(axis=1)
			for i in Data.columns[:-1]:
				Data[i] = Data[i] - mean
		return Data


	@staticmethod
	def butter_band_filter(df, lowcut, highcut, FS=128, Order=5, train=True):
		"""
			input: dataframe of one trial
			output: dataframe
			description: filter the needed range of frequency from signal
		"""
		if not train:
			for ch in df.columns[:].tolist():
				# df[ch] = butter_bandpass_filter(df[ch].values, lowcut, highcut, fs=FS, order=Order)
				df[ch] = butter_lowpass_filter(df[ch].values, highcut, fs=FS, order=Order)
				df[ch] = butter_highpass_filter(df[ch].values, lowcut, fs=FS, order=Order)
		else:
			for ch in df.columns[:-1].tolist():
				# df[ch] = butter_bandpass_filter(df[ch].values, lowcut, highcut, fs=FS, order=Order)
				df[ch] = butter_lowpass_filter(df[ch].values, highcut, fs=FS, order=Order)
				df[ch] = butter_highpass_filter(df[ch].values, lowcut, fs=FS, order=Order)
		return df


	@staticmethod
	def welch(df, train=True , visualize =False):
		"""
            input: dataframe of one trial
            output: list of lists, each has power of each channel
        """
		power = []
		freq = []
		if train:
			lable = df['Label'].iloc[0]
			df = df.drop(columns='Label')

		for ch in df.columns.tolist():
			f, Pxx_den = signal.welch(df[ch].values, fs=128, nfft=5 * 128)
			freq.append(f)
			power.append(Pxx_den)

		if visualize:
			return (freq, power,lable)
		elif train:
			return (power, lable)
		else:
			return power

	def welch_file(df, flickering_time):
		"""
            input: df:dataframe of whole file
                   flickering_time: time of flickering of boxes

            output: list of tuple for each trail

            description: calculate welch for each trial in the file

        """
		return_data = list()
		file_len = df.shape[0]
		samples = flickering_time * 128
		number_of_trials = int(file_len / samples)
		# print (f'number fo trials{number_of_trials}')
		for i in range(number_of_trials):
			df_temp = df.iloc[i * samples:(i + 1) * samples, :]
			return_data.append(helper.welch(df_temp))

		return return_data

	def featureExtraction_welch_real(welch_output, harmonic_num, channel):
		"""
			input: list of tuple, tuple(power,lable)#one for each trial
				   harmonic: int (2nd-3rd) hramonic of main frequencies
				   channel: list of channle

			return: list of list for each trial and list for lables
			description: from welch, power range of interested frequencies are extracted
		"""
		features_trial = list()
		frequency_resolution = 0.2
		if harmonic_num == 2:
			adaptave_freq = [6.6, 7.6, 8.6, 10.0, 12.0, 13.2, 15.2, 17.2, 20, 24]
		else:
			adaptave_freq = [6.6, 7.6, 8.6, 10.0, 12.0, 13.2, 15.2, 17.2, 20, 24, 19.8, 22.8, 25.8, 30, 36]

		channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

		for ch in channel:  # loop over channels
			index_pos = channels_def.index(ch)
			features_ch = list()
			for f in adaptave_freq:
				idx = math.ceil(f / frequency_resolution)
				features_ch += welch_output[index_pos][idx - 2:idx + 3].tolist()
			# print(features_ch)
			features_trial += features_ch

		return [features_trial]


	def featureExtraction_welch(welch_output, harmonic_num, channel):
		"""
            input: list of tuple, tuple(power,lable)#one for each trial
                   harmonic: int (2nd-3rd) hramonic of main frequencies
                   channel: list of channle

            return: list of list for each trial and list for lables
            description: from welch, power range of interested frequencies are extracted
        """
		X = list()
		lable = list()

		frequency_resolution = 0.2
		if harmonic_num == 2:
			adaptave_freq = [6.6, 7.6, 8.6, 10.0, 12.0, 13.2, 15.2, 17.2, 20, 24]
		else:
			adaptave_freq = [6.6, 7.6, 8.6, 10.0, 12.0, 13.2, 15.2, 17.2, 20, 24, 19.8, 22.8, 25.8, 30, 36]

		channels_def = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

		for i in range(len(welch_output)):  # loop over trials
			features_trial = list()
			Pxx_den = welch_output[i][0]
			lable.append(welch_output[i][1])

			for ch in channel:  # loop over channels
				index_pos = channels_def.index(ch)
				features_ch = list()
				for f in adaptave_freq:
					idx = math.ceil(f / frequency_resolution)
					features_ch += Pxx_den[index_pos][idx - 2:idx + 3].tolist()
				features_trial += features_ch
			X.append(features_trial)
		return X, lable


	@staticmethod
	def PCA (pca_ptr, Data, Train=False):
		# TODO
		if Train:
			pca_ptr.fit(Data)
			return pca_ptr.transform(Data)
		else:
			return pca_ptr.transform(Data)


		pass


# if __name__ == '__main__':

	# print(helper.CAR.__doc__)