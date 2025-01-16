import numpy as np


def rotate_data_randomly(concatenated_trials):
    '''The function rotates the data points of the trials with a random shift'''
    # Get the data length, which will be used as the upper bound for the random shift values
    concat_trials_len = concatenated_trials.shape[0]

    # Initialize array for rotated data
    rotated_data = np.zeros(concatenated_trials.shape)
    rand_shift = np.random.randint(1, concat_trials_len)
    # Apply the random shift. The negative sign ensures the rotation direction aligns with MATLAB's code behavior
    rotated_data = np.roll(concatenated_trials, -rand_shift)

    return rotated_data
# Tested!


def split_back_to_original_conditions(rotated_data, trials_sizes, tasks_order):
    '''
    This function splits the rotated data back into the original conditions, based on the provided tasks order.
    It returns two lists of trial objects: one for the 'alt' condition and one for the 'countF' condition.
    '''
    # Calculate cumulative indices
    cumulative_indices = np.cumsum(trials_sizes)[:-1]
    # Split rotated_data based on trial sizes
    new_trials_l = np.split(rotated_data, cumulative_indices, axis=0)

    # Assign back to 2 conditions according to tasks order
    cond1_trials = []
    cond2_trials = []
    trial_ind = 0
    for cond in tasks_order:
        if cond == 'alt':
            cond1_trials.append(new_trials_l[trial_ind])
            trial_ind += 1
        elif cond == 'countF':
            cond2_trials.append(new_trials_l[trial_ind])
            trial_ind += 1

    # np.concatenate can handle lists of numpy arrays
    concat_cond1_trials = np.concatenate(cond1_trials, axis=0)
    concat_cond2_trials = np.concatenate(cond2_trials, axis=0)

    return concat_cond1_trials, concat_cond2_trials
# Tested!


def create_surrogate_data(concatenated_trials, trials_sizes, tasks_order):
    '''
    The function gets the concatenated trials (from 2 conditions), rotates them randomly
    and splits them back to the original conditions.
    Input: 1D np array of the concatenated trials
    Output: "new" concatenated trials of first condition, "new" concatenated trials of second condition (1D np arrays)  
    '''
    # Shuffle
    rotated_data = rotate_data_randomly(concatenated_trials)
    # split back to 2 conditions (hard, easy)
    perm_cond_1, perm_cond_2 = split_back_to_original_conditions(rotated_data, trials_sizes, tasks_order)
    return perm_cond_1, perm_cond_2
# Tested!
