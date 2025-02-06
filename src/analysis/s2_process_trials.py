import numpy as np


def trim_edges(trial, fs, start_time, end_time):
    '''
    The function gets a trial object and fs, and trims sample points from its edges, based on start and end times it gets
    Input: trial object (3D np array)
    output: trial object (3D np array)
    '''
    start_index = int(start_time * fs)
    end_index = -int(end_time * fs)
    trimmed_trial = trial[:, start_index:end_index, :]
    return trimmed_trial
# Tested!


def process_trials_of_condition(condition_trials, fs, start_time, end_time):
    '''
    The function gets condition trials, trim edges of each trial and returns processed trials.
    Input: np array of trial objects
    Output: np array of trial objects
    '''
    if not (start_time > 0 or end_time > 0):
        raise ValueError("start_time and end_time should be greater than 0")

    # Exclusion of rest condition (which is a single trial)
    if condition_trials.ndim == 3:
        trial = condition_trials
        processed_trials = np.empty(1, dtype=object)
        curr_trial = trim_edges(trial, fs, start_time, end_time)
        processed_trials[0] = curr_trial
    else:
        processed_trials = np.empty(condition_trials.shape, dtype=object)

        # Trim edges of each trial
        for i, trial in enumerate(condition_trials):
            curr_trial = trim_edges(trial, fs, start_time, end_time)
            processed_trials[i] = curr_trial
    return processed_trials
# Tested!
