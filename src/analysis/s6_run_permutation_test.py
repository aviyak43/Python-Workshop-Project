import numpy as np
from matplotlib import pyplot as plt
from src.analysis.s4_concat_all_trials import concat_all_trials
from src.analysis.s5_create_surrogate_data import create_surrogate_data
from src.logger import logger


def permutation_test(processed_cond_1, processed_cond_2, observed_ratio, tasks_order, n_elec, n_freq_bands, n_permutations):
    '''
    This function gets trials of 2 conditions and performs permutation test using the rotation method.
    On each iteration:
    1. create surrogate data (meaning "new trials")
    2. compute permuted mean power ratio value
    Input: trials of first condition, trials of second condition (np arrays of trial objects)
    Output: the null distribution (n_elec X n_freq_bands X n_permutations) and the p_values (n_elec X n_freq_bands)
    '''
    # Concatenate data in the tasks order and get sizes of each trial
    concatenated_trials, trials_sizes = concat_all_trials(processed_cond_1, processed_cond_2, tasks_order)

    # Initialize an array to store p-values
    p_values = np.zeros(observed_ratio.shape)

    # Initialize an array to store permutation statistics
    mean_power_ratio_distribution = np.zeros((n_elec, n_freq_bands, n_permutations))

    logger.info("Starting permutation test...")
    for elec in range(n_elec):
        for freq in range(n_freq_bands):
            # Perform permutations
            for i in range(n_permutations):
                # Create "new" trials of 2 conditions (hard, easy)
                perm_cond_1, perm_cond_2 = create_surrogate_data(
                    concatenated_trials[elec, :, freq], trials_sizes, tasks_order)

                # Calculate the permutation statistic: compute mean power ratio for hard vs. easy condition
                perm_cond_1_mean_power = np.mean(perm_cond_1)
                perm_cond_2_mean_power = np.mean(perm_cond_2)

                # Avoid zero division
                if perm_cond_2_mean_power == 0:
                    perm_ratio = np.nan
                else:
                    perm_ratio = perm_cond_1_mean_power / perm_cond_2_mean_power
                mean_power_ratio_distribution[elec, freq, i] = perm_ratio

            # Calculate p-value
            p_value = np.mean(mean_power_ratio_distribution[elec, freq] > observed_ratio[elec, freq])
            if observed_ratio[elec, freq] > 0 and observed_ratio[elec, freq] < 1:
                p_value = 1 - p_value
            p_values[elec, freq] = p_value

    return mean_power_ratio_distribution, p_values
# Tested!


def check_significancy(observed_power_ratio, p_value, alpha=0.05):
    logger.info(f"Observed Power Ratio: {observed_power_ratio}")
    logger.info(f"P-value: {p_value}")
    if p_value < alpha/2:
        logger.info("Significant!\n")


def plot_null_dist(null_dist, observed, patient, elec):
    null_dist = np.nan_to_num(null_dist, nan=0.0)
    mean = np.mean(null_dist)
    std = np.std(null_dist)

    plt.figure(figsize=(8, 6))
    plt.hist(null_dist, color='pink', bins=100, density=True, label=f'μ={mean:.2f}, σ={std:.2f}')
    plt.axvline(x=observed, color='blue', linestyle='solid', linewidth=2, label=f'observed power ratio={observed:.2f}')

    # Calculate and plot the 2.5th and 97.5th percentiles
    percentiles = np.percentile(null_dist, [2.5, 97.5])
    plt.axvline(x=percentiles[0], color='red', linestyle='dotted', linewidth=2, label='2.5th percentile')
    plt.axvline(x=percentiles[1], color='red', linestyle='dotted', linewidth=2, label='97.5th percentile')

    # Add labels and title
    plt.xlabel('Power Ratio Values')
    plt.ylabel('Density')
    plt.title(f'Distribution of Power Ratio - {patient}, channel no.{elec}')
    plt.legend()
    plt.savefig(f'results/{patient}/Null distribution - {patient}, channel no.{elec}.pdf')