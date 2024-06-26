import pytest
import pandas as pd
import numpy as np

from validate_addresses import process_abp_data, process_input_row, is_valid_address, validate_addresses


def test_process_abp_data_can_process_one_address():
    input_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA"],
        'POSTCODE': ['CB2 1AB'],
        'STREET_NAME': ['REGENT STREET']
    })
    output = process_abp_data(input_data)
    expected_output = {'CB2 1AB':['REGENT STREET']}
    assert output == expected_output

def test_process_abp_data_can_process_multiple_addresses():
    input_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA", "BBB", "CCC"],
        'POSTCODE': ['CB2 1AB', 'CB2 1AB', 'CB3 5DF'],
        'STREET_NAME': ['REGENT STREET', 'NEW STREET', 'REGENT STREET']
    })
    output = process_abp_data(input_data)
    expected_output = {'CB2 1AB':['REGENT STREET', 'NEW STREET'],
                       'CB3 5DF':['REGENT STREET']}
    assert output == expected_output

def test_process_input_row_converts_to_upper_case():
    output = process_input_row('Trough Field Supply', 'Delgate Bank', 'Weston Hills')
    expected_output = 'TROUGH FIELD SUPPLY DELGATE BANK WESTON HILLS'
    assert output == expected_output

def test_process_input_row_converts_rd_to_road():
    output = process_input_row('IN WAREHOUSE', 'ATLAS RD', '')
    expected_output = 'IN WAREHOUSE ATLAS ROAD'
    assert output == expected_output

def test_is_valid_address_returns_yes_for_valid_address():
    abp_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA"],
        'POSTCODE': ['PE12 6DW'],
        'STREET_NAME': ['DELGATE BANK']
    })
    valid_addresses = process_abp_data(abp_data)
    output = is_valid_address('Trough Field Supply', 'Delgate Bank', 'Weston Hills', 'PE12 6DW', valid_addresses)
    assert output == 'Yes'

def test_is_valid_address_returns_no_for_invalid_street_at_valid_postcode():
    abp_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA"],
        'POSTCODE': ['PE12 6DW'],
        'STREET_NAME': ['REGENT STREET']
    })
    valid_addresses = process_abp_data(abp_data)
    output = is_valid_address('Trough Field Supply', 'Delgate Bank', 'Weston Hills', 'PE12 6DW', valid_addresses)
    assert output == 'No'

def test_is_valid_address_returns_no_for_invalid_postcode():
    abp_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA"],
        'POSTCODE': ['PE12 6DW'],
        'STREET_NAME': ['REGENT STREET']
    })
    valid_addresses = process_abp_data(abp_data)
    output = is_valid_address('Trough Field Supply', 'Delgate Bank', 'Weston Hills', 'SL6 6GY', valid_addresses)
    assert output == 'No'

def test_validate_addresses_produces_correct_output():
    input_file = pd.read_csv('test_input_data.csv')
    abp_file = pd.read_csv('example_abp_data.csv')

    output_df = validate_addresses(input_file, abp_file)
    expected_output = ["Yes", "Yes", "Yes", "Yes", "Yes"]
    assert np.array_equal(output_df['Street_In_Postcode'].values, expected_output)