from analysis.run_for_all_patients import run_analysis_for_all_patients
from df_for_visualization import convert_mat_results_to_df


# CONSTANTS
ITERATIONS = 10000  # according to Yaara - this is enough to replicate the results
RES_DIR = '/home/eng/keisara/Python-Workshop/results'
SAVE_DIR = '/home/eng/keisara/Python-Workshop/bands_results_df'

def main(res_dir=RES_DIR, save_dir=SAVE_DIR, iterations=ITERATIONS):
    run_analysis_for_all_patients(res_dir, iterations)
    convert_mat_results_to_df(res_dir, save_dir)

if __name__ == "__main__":
    main()
