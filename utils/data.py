import pandas as pd
import numpy as np



def standardize_df_data(df_original, norm_conditions, norm_vars):

    if type(norm_vars) is not list: 
        norm_vars = [norm_vars]

    df = df_original.copy()
    for var in norm_vars:
        group_mean = df.groupby(norm_conditions)[var].transform('mean')
        group_std = df.groupby(norm_conditions)[var].transform('std')
        df[var] = (df[var] - group_mean) / group_std

    return df


def extract_2x2_data(df, choices, var='count'):

    subjects = df['subject'].unique()
    condition_data = np.zeros((len(subjects), 4)) 

    for i, subject in enumerate(subjects):
        for j, structured in enumerate([True, False]):
            for k, first_choice in enumerate(choices):
                
                data_subject = df[(df['subject'] == subject) & (df['structured'] == structured) & (df['first_choice'] == first_choice)][var]
                if len(data_subject) == 0:
                    value_subject = 0
                elif len(data_subject) == 1:
                    value_subject = data_subject.item()
                else:
                    value_subject = np.nanmean(data_subject)

                condition_data[i, j*2 + k] = value_subject
    return condition_data


def extract_2x3_data(df, var='count'):

    subjects = df['subject'].unique()
    condition_data = np.zeros((len(subjects), 6)) 

    for i, subject in enumerate(subjects):
        for j, structured in enumerate([True, False]):
            for k, first_choice in enumerate(['H', 'S', 'C']):
                
                data_subject = df[(df['subject'] == subject) & (df['structured'] == structured) & (df['first_choice'] == first_choice)][var]
                if len(data_subject) == 0:
                    value_subject = 0
                elif len(data_subject) == 1:
                    value_subject = data_subject.item()
                else:
                    value_subject = np.nanmean(data_subject)

                condition_data[i, j*3 + k] = value_subject
    return condition_data




def fix_count_df(df_counts):

    subjects = df_counts['subject'].unique()
    first_choice_type = df_counts['first_choice'].unique()
    environments = [True, False]

    for subject in subjects:
        for choice in first_choice_type:
            for env_structured in environments:
                # Check if the combination exists, if not, add it with count 0
                if not ((df_counts['subject'] == subject) & (df_counts['structured'] == env_structured) & (df_counts['first_choice'] == choice)).any():
                    df_counts = pd.concat((df_counts, pd.DataFrame({'subject': subject, 'structured': env_structured, 'first_choice': choice, 'count': 0}, index=[len(df_counts)])))

    return df_counts