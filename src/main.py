from analysis.run_for_all_patients import run_analysis_for_all_patients
from df_for_visualization import convert_mat_results_to_df
from config import ITERATIONS, RES_DIR, SAVE_DIR


def main(res_dir=RES_DIR, save_dir=SAVE_DIR, iterations=ITERATIONS):
    run_analysis_for_all_patients(res_dir, iterations)
    convert_mat_results_to_df(res_dir, save_dir)

if __name__ == "__main__":
    main()
