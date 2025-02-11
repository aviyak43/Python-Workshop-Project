from scipy.io import loadmat


def load_mat_file(file_name):
    '''
    The function loads a mat file containing struct variables into a dictionary.
    Input: str 'filename'
    Output: dictionary (keys = struct names, values = content of the structs)
    '''
    data_from_mat = loadmat(file_name, struct_as_record=False, squeeze_me=True)
    return data_from_mat


def get_main_variables(patient):
    '''
    The function loads the mat file of one patients and returns a dictionary with the main 3 variables needed for the analysis,
    plus some const parameters.
    Input: str 'patient'
    Output: dictionary
    '''

    mat_file_path = '/data/Intraop-Cam/elecphys_data/' + patient + \
        '/matlab_data/all_data_notch50_79_only_reref_bipolar_' + patient + '.mat'
    data = load_mat_file(mat_file_path)  # dictionary
    # Choose the required variable
    data_all_struct = data['data_all']  # matlab struct
    # Get the data for the countF (easy) condition: np array of trials objects
    all_countF_bands_power_cell = data_all_struct.all_countF_bands_power
    # Get the data for the alt (hard) condition: np array of trials objects
    all_alt_bands_power_cell = data_all_struct.all_alt_bands_power
    # Get the data for the rest condition: 3D np array
    all_rest_bands_power = data_all_struct.all_rest_bands_power
    # Get the order of trials conditions (required for the rotation stats)
    tasks_order_struct = data_all_struct.tasks_order_for_stats
    tasks_order_list = [task.event for task in tasks_order_struct]
    fs = data_all_struct.sr
    n_elec = data_all_struct.subj_data.nchs
    n_freq_bands = all_rest_bands_power.shape[2]

    main_variables_dict = {
        'all_countF_bands_power_cell': all_countF_bands_power_cell,
        'all_alt_bands_power_cell': all_alt_bands_power_cell,
        'all_rest_bands_power': all_rest_bands_power,
        'tasks_order': tasks_order_list,
        'fs': fs,
        'n_elec': n_elec,
        'n_freq_bands': n_freq_bands
    }
    return main_variables_dict
