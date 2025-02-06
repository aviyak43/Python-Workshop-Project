import numpy as np


def compute_mean_power(cond_processed_trials):
    '''
    The function concatenates all processed trials of a condition and computes the mean power.
    Input: np array of trial objects
    Output: 2D np array, shape (num_electrodes, num_frequency_bands)
    '''
    # concatenate all processed trials
    concatenated_trials = np.concatenate(cond_processed_trials, axis=1)
    # compute mean
    mean_power = np.mean(concatenated_trials, axis=1)
    return mean_power
# Tested!
