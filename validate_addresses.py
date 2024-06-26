import pandas as pd


def process_abp_data(abp_table):
    valid_addresses_by_postcode = {}
    for index, row in abp_table.iterrows():
        if row['POSTCODE'] not in valid_addresses_by_postcode:
            valid_addresses_by_postcode[row['POSTCODE']] = [row['STREET_NAME']]
        else:
            valid_addresses_by_postcode[row['POSTCODE']].append(row['STREET_NAME'])
    return valid_addresses_by_postcode

def process_input_row(column_1, column_2, column_3):
    return " ".join([column_1.upper(), column_2.upper(), column_3.upper()])

def is_valid_address(column_1, column_2, column_3, postcode, valid_addresses):
    for street in valid_addresses[postcode]:
        if street in process_input_row(column_1, column_2, column_3):
            return 'Yes'
    return 'No'