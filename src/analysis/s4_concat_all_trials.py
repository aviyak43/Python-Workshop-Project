import numpy as np


def concat_all_trials(processed_cond1_trials, processed_cond2_trials, tasks_order):
    '''
    The function concatenates trials of two conditions according to the order it was performed during the operation.
    Input: trials of first condition, trials of second condition (np arrays of trial objects)
    Output: 3D np array of the concatenated trials
    '''
    n_trials_cond1 = processed_cond1_trials.shape[0]
    n_trials_cond2 = processed_cond2_trials.shape[0]

    # Create an empty array with a total length of n_trials_cond_1 + n_trials_cond_2
    total_trials = n_trials_cond1 + n_trials_cond2
    concatenated_trials = np.empty(total_trials, dtype=object)
    
    # Create an empty array to save the trial sizes
    trials_sizes = np.zeros(total_trials, dtype=int)
    
    # Concatenate trials according to tasks order
    cond1_trial_ind = 0
    cond2_trial_ind = 0
    trial_ind = 0
    for cond in tasks_order:
        if cond == 'alt':
            concatenated_trials[trial_ind] = processed_cond1_trials[cond1_trial_ind]
            trials_sizes[trial_ind] = concatenated_trials[trial_ind].shape[1]
            cond1_trial_ind += 1
            trial_ind += 1
        elif cond == 'countF':
            concatenated_trials[trial_ind] = processed_cond2_trials[cond2_trial_ind]
            trials_sizes[trial_ind] = concatenated_trials[trial_ind].shape[1]
            cond2_trial_ind += 1
            trial_ind += 1
    concatenated_trials = np.concatenate(concatenated_trials, axis=1)

    return concatenated_trials, trials_sizes
