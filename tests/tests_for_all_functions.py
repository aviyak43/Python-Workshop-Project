from src.logger import logger
import src.analysis.s2_process_trials as s1
import src.analysis.s3_compute_mean_power as s2
import src.analysis.s4_concat_all_trials as s3
import src.analysis.s5_create_surrogate_data as s4
import src.analysis.s6_run_permutation_test as s5
import numpy as np


def create_toy_input():
    # 3D arrays shape = (2, 4, 3) meaning 2 electrodes, 4 data points, 3 freq. bands
    # Define arrays for List 1
    array1_cond1 = np.array([
        [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
        [[13, 14, 15], [16, 17, 18], [19, 20, 21], [22, 23, 24]]
    ])

    array2_cond1 = np.array([
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9], [1.0, 1.1, 1.2]],
        [[1.3, 1.4, 1.5], [1.6, 1.7, 1.8], [1.9, 2.0, 2.1], [2.2, 2.3, 2.4]]
    ])

    # Define arrays for List 2
    array1_cond2 = np.array([
        [[0.5, 0.6, 0.7], [0.8, 0.9, 1.0], [1.1, 1.2, 1.3], [1.4, 1.5, 1.6]],
        [[1.7, 1.8, 1.9], [2.0, 2.1, 2.2], [2.3, 2.4, 2.5], [2.6, 2.7, 2.8]]
    ])

    array2_cond2 = np.array([
        [[10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21]],
        [[22, 23, 24], [25, 26, 27], [28, 29, 30], [31, 32, 33]]
    ])

    array3_cond2 = np.array([
        [[-1, -2, -3], [-4, -5, -6], [-7, -8, -9], [-10, -11, -12]],
        [[-13, -14, -15], [-16, -17, -18], [-19, -20, -21], [-22, -23, -24]]
    ])
    example_object_1 = np.empty(2, object)
    example_object_2 = np.empty(3, object)
    example_object_1[:] = [array1_cond1, array2_cond1]  # demonstrate 2 hard trials
    example_object_2[:] = [array1_cond2, array2_cond2, array3_cond2]  # demonstrate 3 easy trials
    return example_object_1, example_object_2


'''Stage 1: Process trials of one condition'''


def test_trim_edges(example_list_1):
    logger.info("Testing trim_edges")
    logger.debug(f'Trial shape before trimming: {example_list_1[0].shape}')
    res = s1.trim_edges(example_list_1[0], 1, 1, 1)
    logger.debug(f'Trial shape after trimming  1 sample from both edges: {res.shape}')


def test_process_trials_of_condition(example_list_1):
    logger.info("Testing process_trials_of_condition")
    res = s1.process_trials_of_condition(example_list_1, 1, 1, 1)
    logger.debug(f'Trial1 shape after processing: {res[0].shape}')


'''Stage 2: Compute mean power ratio'''


def test_compute_mean_power(example_list_1):
    logger.info("Testing compute_mean_power")
    res = s2.compute_mean_power(example_list_1)
    logger.debug(f'Shape of mean power of cond1: {res.shape}')


'''Stage 3: concatenate all trials in the right order'''


def test_concat_all_trials(example_list_1, example_list_2):
    logger.info("Testing concat_all_trials")
    concatenated, trials_sizes = s3.concat_all_trials(example_list_1, example_list_2,
                                                      tasks_order=['alt', 'countF', 'alt', 'countF', 'countF'])
    logger.debug(f'Total trials: {len(trials_sizes)}')
    logger.debug(f'Shape of concatenated trials: {concatenated.shape}')
    return concatenated, trials_sizes


''' Stage 4: Create surrogate data for the permutation test'''


def test_rotate_data_randomly(concatenated):
    logger.info("Testing rotate_data_randomly")
    rotated_data = s4.rotate_data_randomly(concatenated)
    logger.debug(f'Shape of rotated_data: {rotated_data.shape}')
    logger.debug(f'Rotated_data: {rotated_data[0]}')
    return rotated_data


def test_split_back_to_original_conditions(rotated_data, trials_sizes):
    logger.info("Testing split_back_to_original_conditions")
    l1, l2 = s4.split_back_to_original_conditions(rotated_data, trials_sizes,
                                                  tasks_order=['alt', 'countF', 'alt', 'countF', 'countF'])
    logger.debug(f'New cond1 shape: {l1.shape}')
    logger.debug(f'New cond2 shape: {l2.shape}')


def test_create_surrogate_data(concatenated, trials_sizes):
    logger.info("Testing create_surrogate_data")
    l1, l2 = s4.create_surrogate_data(concatenated, trials_sizes,
                                      tasks_order=['alt', 'countF', 'alt', 'countF', 'countF'])
    logger.debug(f'New cond1 shape: {l1.shape}')
    logger.debug(f'New cond2 shape: {l2.shape}')


'''Stage 5: Run permutation test'''


def test_permutation_test(example_list_1, example_list_2):
    logger.info("Testing permutation_test")
    mean_power_cond1 = s2.compute_mean_power(example_list_1)
    mean_power_cond2 = s2.compute_mean_power(example_list_2)
    mean_power_ratio = mean_power_cond2 / mean_power_cond1
    mean_power_ratio_distribution, p_values = s5.permutation_test(example_list_1, example_list_2, mean_power_ratio,
                                                                  tasks_order=['alt', 'countF',
                                                                               'alt', 'countF', 'countF'],
                                                                  n_elec=2, n_freq_bands=3, n_permutations=1000)
    logger.debug(f'Mean power ratio results:\n {mean_power_ratio}')
    logger.debug(f'P-values results:\n {p_values}')
    logger.debug(f'Null distribution shape: {mean_power_ratio_distribution.shape}')


if __name__ == "__main__":
    example_object_1, example_object_2 = create_toy_input()
    logger.info(f'Trials in cond1: {example_object_1.shape}')
    logger.info(f'Shape of each trial: {example_object_1[0].shape} (elec X samples X bands)')
    logger.info(f'Trials in cond2: {example_object_2.shape}')
    logger.info(f'Shape of each trial: {example_object_2[0].shape} (elec X samples X bands)')

    test_trim_edges(example_object_1)
    test_process_trials_of_condition(example_object_1)
    test_compute_mean_power(example_object_1)
    concatenated, trials_sizes = test_concat_all_trials(example_object_1, example_object_2)
    rotated_data = test_rotate_data_randomly(concatenated[0, :, 1])
    test_split_back_to_original_conditions(rotated_data, trials_sizes)
    test_create_surrogate_data(concatenated, trials_sizes)
    test_permutation_test(example_object_1, example_object_2)
