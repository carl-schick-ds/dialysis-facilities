# Import needed libraries.  Unless noted above, all libraries are available in the baseline conda environment.
import pandas as pd

def raw_analysis(raw_facilities_df):
    raw_facilities_df.info()
    print(raw_facilities_df['Measure'].nunique())
    print(raw_facilities_df['Measure ID'].nunique())
    print(raw_facilities_df['CCN'].nunique())
    print(raw_facilities_df['NPI'].nunique())
    print(raw_facilities_df['Provider Name'].nunique())
    print(raw_facilities_df['Chain Name'].value_counts())
    npi_list = raw_facilities_df['NPI'].value_counts()
    npi_blank_CCNs = raw_facilities_df[raw_facilities_df['NPI'] == "."]['CCN'].value_counts()
    raw_facilities_df[raw_facilities_df['CCN'] == 332770]

def get_facilities(raw_facilities_df):
    facility_cols = ['State', 'CCN', 'Provider Name', 'City', 'Ownership Type', 'ESRD Network', 'NPI', 'Chain Name', 'Modality', 'Alternate CCN(s)']
    facilities_df = raw_facilities_df.drop_duplicates(subset=facility_cols)[facility_cols].set_index('CCN')

    print('Raw Facilities:', raw_facilities_df['CCN'].nunique())
    print('Extracted Facilities:', facilities_df.shape[0])

    return facilities_df

def get_measures(raw_facilities_df):
    measure_cols = ['Measure', 'Measure ID']
    measures_df = raw_facilities_df.drop_duplicates(subset=measure_cols)[measure_cols].set_index('Measure ID')

    corr_text_1 = 'F: Adult Incident Patients (2728) - Average age, '
    corr_text_2 = 'F: SHR (ED) - % Patients with at Least One ED Visit, '
    agmy_corr_dict = {'agemy1_f': corr_text_1 + '2016', 'agemy2_f': corr_text_1 + '2017', 'agemy3_f': corr_text_1 + '2018', 'agemy4_f': corr_text_1 + '2019'}
    edpt_corr_dict = {'edpty1_f': corr_text_2 + '2016', 'edpty2_f': corr_text_2 + '2017', 'edpty3_f': corr_text_2 + '2018', 'edpty4_f': corr_text_2 + '2019'}

    for key in agmy_corr_dict:
        measures_df.loc[key]['Measure'] = agmy_corr_dict[key]
    for key in edpt_corr_dict:
        measures_df.loc[key]['Measure'] = edpt_corr_dict[key]

    print('Raw Measures:', raw_facilities_df['Measure ID'].nunique())
    print('Extracted Measures:', measures_df.shape[0])

    return measures_df

def get_scores(raw_facilities_df):
    # display(raw_facilities_df['Year(s) covered by the measure'].value_counts())
    raw_facilities_df.rename(columns={'Year(s) covered by the measure' : 'Year'}, inplace=True)
    fac_scores_df = raw_facilities_df[['CCN', 'Measure ID', 'Year', 'Measure Score']]

    print('Raw Scores:', raw_facilities_df.shape[0])
    print('Extracted Scores:', fac_scores_df.shape[0])

    return fac_scores_df