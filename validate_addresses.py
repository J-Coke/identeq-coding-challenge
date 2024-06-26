import pandas as pd


def process_abp_data(abp_input_table):
    abp_data_by_postcode = {}
    for index, row in abp_input_table.iterrows():
        abp_data_by_postcode[row['POSTCODE']] = [row['STREET_NAME']]
    return abp_data_by_postcode
