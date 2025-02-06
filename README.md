## Overview
This project aims to reproduce findings and reaffirm conclusions from the paper *"High gamma activity distinguishes frontal cognitive control regions from adjacent cortical networks" (Cortex, 2023)*.\
\
In this paper the researchers aim to differentiate frontal cognitive control regions from adjacent cortical networks within the lateral frontal cortex by analyzing high gamma activity (70–250 Hz) during verbal tasks requiring attentional switching.\
The study employs ECOG recordings to observe these neural oscillations.

## Citation
**Link to original study:** https://doi.org/10.1016/j.cortex.2022.12.007

## Project Data
Intraoperative ECOG data collected from **13 patients** with a total of **59 electrodes**.\
Unfortunately, due to medical confidentiality, original raw ECOG data can not be provided.

## Project Documentation

### Project Structure
```bash
Python-Workshop-Project
│   .gitignore
│   Python Workshop - Final Project Report.pdf
│   README.md
│
├───src
│   │   main.py
│   │   __init__.py
│   │
│   ├───analysis
│   │      run_for_all_patients.py
│   │      s1_get_main_variables.py
│   │      s2_process_trials.py
│   │      s3_compute_mean_power.py
│   │      s4_concat_all_trials.py
│   │      s5_create_surrogate_data.py
│   │      s6_run_permutation_test.py
│   │      s7_main_analysis.py
│   │      __init__.py
│   │ 
│   │
│   ├───df_for_visualization
│   │       convert_mat_results_to_df.py
│   │
│   ├───visualization
│           power_modulations_hg_lg_beta_alpha_theta_delta.ipynb
│           power_modulations_within_and_outside_fpn.ipynb
│   
└───tests
        tests_for_all_functions.py
```

### Workflow / Pipeline
#### 1. Data Preprocessing (Previously Done)
- Signal preprocessing includes: re-referencing, down-sampling, and noise filtering.
- Bandpass filtering into 6 frequency bands:\
(delta: 1-4Hz theta: 4-8Hz, alpha: 8-12Hz, beta: 12-30Hz, low gamma: 30-70 Hz, high gamma (HG): 70-250Hz),
- Instantaneous power computed for each frequency band.

#### 2. Data Cleaning
- **For all trials:** Removing 1sec from the beginning and end of each task trials (since onset and offset markers were manually recorded).
- **For the hard trials:** Additional 3-second trimming from the beginning (to focus on the most demanding part of the tasks).  

#### 3. Computation of Task-Related Neural Changes
- Percentage of Signal Change (PSC) calculated for hard vs. easy conditions (easy vs. rest not analyzed).
- PSC used to identify electrodes that showed power modulations in response to increased cognitive demand.

#### 4. Statistical Analysis
<ins>Permutation testing:</ins>
- Power time series from all trials in each condition are concatenated into a loop, and trial markers are randomly shifted to generate surrogate datasets.
- 10,000 iterations (vs. 100,000 in the original study) to produce a null distribution to assess statistical significance.
- Performed separately for each electrode and frequency band.
- Computation time: 3.32 hours.

#### 5. Results Visualization
From the paper we have reproduced the following figures:
<img src="https://ars.els-cdn.com/content/image/1-s2.0-S0010945222003380-gr2_lrg.jpg" width="600">
<img src="https://ars.els-cdn.com/content/image/1-s2.0-S0010945222003380-gr3_lrg.jpg" width="600">

## To run the project follow this commands
All command should run under project root/working-directory
```bash 
#install Virtualenv is - a tool to set up your Python environments
pip install virtualenv
#create virtual environment (serve only this project):
python -m venv venv
#activate virtual environment
.\venv\Scripts\activate
+ (venv) should appear as prefix to all command (run next command just after activating venv)
#update venv's python package-installer (pip) to its latest version
python.exe -m pip install --upgrade pip
#install projects packages (Everything needed to run the project)
pip install -e .
#install dev packages (Additional packages for linting, testing and other developer tools)
pip install -e .[dev]
``` 
