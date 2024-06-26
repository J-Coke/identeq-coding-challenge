import pandas as pd

def validate_addresses(input_df, abp_df):
    valid_addresses = process_abp_data(abp_df)
    addresses_for_validation = input_df.fillna('')
    addresses_for_validation['Street_In_Postcode'] = addresses_for_validation.apply(
        lambda row: is_valid_address(row['Address_Line_1'], row['Address_Line_2'], row['Address_Line_3'], row['Postcode'], valid_addresses), axis=1
    )

    return addresses_for_validation

def process_abp_data(abp_table):
    valid_addresses_by_postcode = {}
    for index, row in abp_table.iterrows():
        if row['POSTCODE'] not in valid_addresses_by_postcode:
            valid_addresses_by_postcode[row['POSTCODE']] = [row['STREET_NAME']]
        else:
            valid_addresses_by_postcode[row['POSTCODE']].append(row['STREET_NAME'])
    return valid_addresses_by_postcode

def process_input_row(column_1, column_2, column_3):
    joined_address_lines = " ".join([str(column_1), str(column_2), str(column_3)])
    upper_cased_address_lines = joined_address_lines.upper()
    unabbreviated_address_lines = upper_cased_address_lines.replace(" RD", " ROAD")
    return unabbreviated_address_lines.strip()

def is_valid_address(column_1, column_2, column_3, postcode, valid_addresses):
    for street in valid_addresses[postcode]:
        if street in process_input_row(column_1, column_2, column_3):
            return 'Yes'
    return 'No'

