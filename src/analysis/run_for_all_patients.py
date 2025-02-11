from scipy.io import savemat
import os
import time
from src.logger import logger
from src.analysis.s7_main_analysis import main_analysis


def run_analysis_for_all_patients(directory, iterations):
    start_time = time.time()

    # Get all patients' IDs into a list (for a loop)
    base_data_dir = '/mnt/jane_data/Intraop-Cam/elecphys_data/'
    patients = os.listdir(base_data_dir)
    patients = [pat for pat in patients if not pat.endswith('.mat')]
    logger.info("Starting analysis for all patients...")

    '''
    This loop performs the main analysis for all patients and saves the results in the dedicated folder
    '''
    # Go through all patients' data
    for patient in patients:
        logger.info(f'Starting analysis for patient: {patient}')

        # Ensure the directory for saving the results exists, if not, create it
        save_directory = f'{directory}/{patient}'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Perform the analysis
        results_d = main_analysis(patient, iterations)

        # Get results
        alt_mean_power = results_d['alt_mean_power']
        countF_mean_power = results_d['countF_mean_power']
        rest_mean_power = results_d['rest_mean_power']
        mean_power_ratio_alt_countF = results_d['mean_power_ratio_alt_countF']
        p_values = results_d['p_values']
        permutation_test_mean_power_ratio_distribution = results_d[
            'permutation_test_mean_power_ratio_distribution']
        logger.info(f"Results for patient {patient} - p-values: {p_values}")

        # Save results in dedicated folder
        savemat(f'{save_directory}/results.mat',
                {'permutation_test_mean_power_ratio_distribution': permutation_test_mean_power_ratio_distribution,
                    'mean_power_ratio_alt_countF': mean_power_ratio_alt_countF,
                    'p_values': p_values,
                    'alt_mean_power': alt_mean_power,
                    'countF_mean_power': countF_mean_power,
                    'rest_mean_power': rest_mean_power},
                format='5')

    logger.info(f"Process finished --- {time.time() - start_time} seconds")