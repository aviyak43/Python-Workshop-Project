import numpy as np
from src.analysis.s1_get_main_variables import get_main_variables
from src.analysis.s2_process_trials import process_trials_of_condition
from src.analysis.s3_compute_mean_power import compute_mean_power
from src.analysis.s6_run_permutation_test import permutation_test, check_significancy, plot_null_dist


def main_analysis(patient, ITERATIONS):
    # Get the main variables to work with
    patient_dict = get_main_variables(patient)

    # From the dictionary, extract data and variables that required for the analysis
    hard_trials = patient_dict['all_alt_bands_power_cell']
    easy_trials = patient_dict['all_countF_bands_power_cell']
    rest = patient_dict['all_rest_bands_power']
    tasks_order = patient_dict['tasks_order']
    fs = patient_dict['fs']
    n_elec = patient_dict['n_elec']
    n_freq_bands = patient_dict['n_freq_bands']

    # Process trials of 3 conditions
    processed_hard_trials = process_trials_of_condition(hard_trials, fs, start_time=4, end_time=1)
    processed_easy_trials = process_trials_of_condition(easy_trials, fs, start_time=1, end_time=1)
    processed_rest_cond = process_trials_of_condition(rest, fs, start_time=2, end_time=2)

    # Compute mean power for each condition
    forward_mean_power = compute_mean_power(processed_easy_trials)
    alt_mean_power = compute_mean_power(processed_hard_trials)
    rest_mean_power = compute_mean_power(processed_rest_cond)

    # Compute mean power ratio for hard vs. easy condition
    mean_power_ratio = np.divide(alt_mean_power, forward_mean_power,
                                 out=np.zeros_like(alt_mean_power), where=forward_mean_power != 0)

    # Permutation test for the mean power ratio
    mean_power_ratio_distribution, p_values = permutation_test(processed_hard_trials, processed_easy_trials,
                                                               mean_power_ratio, tasks_order, n_elec, n_freq_bands, ITERATIONS)

    # Print and save plot results for a random electrode, just for HG band
    HG = 5
    # Choose random elecrode
    elec = np.random.randint(0, n_elec)
    while np.isnan(mean_power_ratio[elec, HG]):
        # If we randomly chose a reference electrode (nan values), re-select a new one
        elec = np.random.randint(0, n_elec)

    check_significancy(mean_power_ratio[elec, HG], p_values[elec, HG])
    plot_null_dist(mean_power_ratio_distribution[elec, HG, :], mean_power_ratio[elec, HG], patient, elec)

    results_dict = {
        'alt_mean_power': alt_mean_power,
        'countF_mean_power': forward_mean_power,
        'rest_mean_power': rest_mean_power,
        'mean_power_ratio_alt_countF': mean_power_ratio,
        'permutation_test_mean_power_ratio_distribution': mean_power_ratio_distribution,
        'p_values': p_values
    }
    return results_dict

# Access a specific signal you can plot: curr_trial = cond_bands_power[0, 0][0, trial][elec, :, frequency_band]
# Access a trial (=3D np array): cond_bands_power_cell[trial]
