import analysis.Stage_1_Process_trials as s1
import analysis.Stage_2_Compute_mean_power as s2
import analysis.Stage_3_Concat_all_trials as s3
import analysis.Stage_4_Create_surrogate_data as s4
import analysis.Stage_5_Run_permutation_test as s5
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
    print("test_trim_edges:")
    print(f'trial shape before trimming: \n{example_list_1[0].shape}')
    res = s1.trim_edges(example_list_1[0], 1, 1, 1)
    print(f'\ntrial shape after trimming 1 sample from both edges:\n{res.shape}\n')


def test_process_trials_of_condition(example_list_1):
    print("test_process_trials_of_condition:")
    res = s1.process_trials_of_condition(example_list_1, 1, 1, 1)
    print(f'trial1 shape after processsing: \n{res[0].shape}\n')


'''Stage 2: Compute mean power ratio'''


def test_compute_mean_power(example_list_1):
    print("test_compute_mean_power:")
    res = s2.compute_mean_power(example_list_1)
    print(f'shape of mean power of cond1:\n{res.shape}\n')


'''Stage 3: concatenate all trials in the right order'''


def test_concat_all_trials(example_list_1, example_list_2):
    print("test_concat_all_trials:")
    concatenated, trials_sizes = s3.concat_all_trials(example_list_1, example_list_2,
                                                      tasks_order=['alt', 'countF', 'alt', 'countF', 'countF'])
    print(f'total trials: {len(trials_sizes)}')
    print(f'shape of concatenated trials: {concatenated.shape}\n')
    return concatenated, trials_sizes


''' Stage 4: Create surrogate data for the permutation test'''


def test_rotate_data_randomly(concatenated):
    print("test_rotate_data_randomly:")
    rotated_data = s4.rotate_data_randomly(concatenated)
    print(f'shape of rotated_data: {rotated_data.shape}')
    print(f'rotated data:\n {rotated_data[0]}\n')
    return rotated_data


def test_split_back_to_original_conditions(rotated_data, trials_sizes):
    print("test_split_back_to_original_conditions:")
    l1, l2 = s4.split_back_to_original_conditions(rotated_data, trials_sizes,
                                                  tasks_order=['alt', 'countF', 'alt', 'countF', 'countF'])
    print(f'new cond1 shape:{l1.shape}')
    print(f'new cond2 shape: {l2.shape}')


def test_create_surrogate_data(concatenated, trials_sizes):
    print("test_create_surrogate_data:")
    l1, l2 = s4.create_surrogate_data(concatenated, trials_sizes,
                                      tasks_order=['alt', 'countF', 'alt', 'countF', 'countF'])
    print(f'new cond1 shape:{l1.shape}')
    print(f'new cond2 shape: {l2.shape}\n')


'''Stage 5: Run permutation test'''


def test_permutation_test(example_list_1, example_list_2):
    print("test_permutation_test:")
    mean_power_cond1 = s2.compute_mean_power(example_list_1)
    mean_power_cond2 = s2.compute_mean_power(example_list_2)
    mean_power_ratio = mean_power_cond2 / mean_power_cond1
    mean_power_ratio_distribution, p_values = s5.permutation_test(example_list_1, example_list_2, mean_power_ratio,
                                                                  tasks_order=['alt', 'countF',
                                                                               'alt', 'countF', 'countF'],
                                                                  n_elec=2, n_freq_bands=3, n_permutations=1000)
    print(f'mean_power_ratio results:\n {mean_power_ratio}')
    print(f'p_values results:\n {p_values}')
    print(f'null distribution shape: {mean_power_ratio_distribution.shape}')


if __name__ == "__main__":
    example_object_1, example_object_2 = create_toy_input()
    print(f'trials in cond1:{example_object_1.shape}')
    print(f'shape of each trial: {example_object_1[0].shape} (elec X samples X bands)')
    print(f'trials in cond2:{example_object_2.shape}')
    print(f'shape of each trial: {example_object_2[0].shape} (elec X samples X bands)')

    test_trim_edges(example_object_1)
    test_process_trials_of_condition(example_object_1)
    test_compute_mean_power(example_object_1)
    concatenated, trials_sizes = test_concat_all_trials(example_object_1, example_object_2)
    rotated_data = test_rotate_data_randomly(concatenated[0, :, 1])
    test_split_back_to_original_conditions(rotated_data, trials_sizes)
    test_create_surrogate_data(concatenated, trials_sizes)
    test_permutation_test(example_object_1, example_object_2)
