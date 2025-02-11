import pandas as pd
from scipy.io import loadmat
import os
from src.logger import logger


def get_patients_list(directory):
    '''
    The function gets all patients names into a list and returns it
    '''
    patients = os.listdir(directory)
    patients_list = [pat for pat in patients if not pat.endswith('.mat')]
    return sorted(patients_list)


def mat_to_df(mat_file_path, patient_df):
    '''
    The function extracts a patient PSC and p-values results from the mat file.
    It returns a list of 6 dataframes with the results of each frequency band.
    '''
    data = loadmat(mat_file_path)
    if not data:
        raise ValueError("No variables found in the .mat file to export.")
    mean_power_ratio = data['mean_power_ratio_alt_countF']
    PSC = (mean_power_ratio - 1) * 100
    p_values = data['p_values']
    n_bands = mean_power_ratio.shape[1]
    dataframes = []
    for band in range(n_bands):
        res_df = pd.DataFrame({
            'PSC': PSC[:, band],
            'p-value': p_values[:, band]
        })
        df = pd.concat([patient_df, res_df], axis=1)
        df = df.dropna(subset=['Network'])
        df = df[~df['Electrode name'].str.contains('EL4')]
        dataframes.append(df)
    return dataframes


def create_dataframes(res_directory, save_directory):
    '''
    The function creates 6 dataframes, one for each frequency band.
    Each df contains all patients results of analysis. 
    Excluded are 3 patients that were excluded as well from the original analysis
    ['2017_08', '2018_03', '2019_01']
    '''
    all_electrodes_info = pd.read_csv(f'{save_directory}/all_elec_info.csv')
    patients = get_patients_list(res_directory)
    # Exclude 3 patients from the analysis
    patients.remove('2017_08')
    patients.remove('2018_03')
    patients.remove('2019_01')

    # Create a list of dataframes (will contain the results for each frequency band)
    combined_dataframes = [None] * 6
    # Extract each patient results into a DataFrame and concatenate them into one united DataFrame.
    for patient in patients:
        # Filter electrodes of the given patient
        pat_elec_info = all_electrodes_info[all_electrodes_info.Patient == patient]
        pat_elec_info = pat_elec_info.reset_index(drop=True)
        existing_df = [None] * 6
        mat_file_path = f'{res_directory}/{patient}/results.mat'
        patient_df = mat_to_df(mat_file_path, pat_elec_info)

        for i in range(len(existing_df)):
            if existing_df[i] is None:
                existing_df[i] = patient_df[i]
            else:
                existing_df[i] = pd.merge(existing_df[i], patient_df[i])

        for i in range(len(combined_dataframes)):
            if combined_dataframes[i] is None:
                combined_dataframes[i] = existing_df[i]
            else:
                combined_dataframes[i] = pd.concat([combined_dataframes[i], existing_df[i]], ignore_index=True)
    return combined_dataframes


def save_df_to_csv(dataframes, save_directory):
    '''
    Save dataframes as CSV files, for later usage
    '''
    bands_names = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma', 'HG']
    # Ensure the directory exists, if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    for i, df in enumerate(dataframes):
        file_path = os.path.join(save_directory, f'Band{i}-{bands_names[i]} Results.csv')
        df.to_csv(file_path, index=False)
        logger.info(f"Saved DataFrame for Band {i}-{bands_names[i]} Results to {file_path}")


def convert_mat_results_to_df(res_dir, save_dir):
    '''The function converts results from mat files into 6 dataframes (one for each frequency band) and saves them to csv files'''
    logger.info(f"Starting conversion of MAT results in {res_dir} and saving to {save_dir}")
    bands_dataframes = create_dataframes(res_dir, save_dir)
    save_df_to_csv(bands_dataframes, save_dir)
    logger.info("MAT file results conversion and saving completed.")
