import pytest
import pandas as pd

from validate_addresses import process_abp_data, process_input_row, is_valid_address


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
    input_data = pd.DataFrame({

        'Address_Line_1': ['Trough Field Supply'],
        'Address_Line_2': ['Delgate Bank'],
        'Address_Line_3': ['Weston Hills'],
        'Address_Line_4': ['SPALDING'],
        'Address_Line_5': [''],
        'Postcode': ['PE12 6DW']
    })
    output = process_input_row('Trough Field Supply', 'Delgate Bank', 'Weston Hills')
    expected_output = 'TROUGH FIELD SUPPLY DELGATE BANK WESTON HILLS'
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

def test_is_valid_address_returns_no_for_invalid_address():
    abp_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA"],
        'POSTCODE': ['PE12 6DW'],
        'STREET_NAME': ['REGENT STREET']
    })
    valid_addresses = process_abp_data(abp_data)
    output = is_valid_address('Trough Field Supply', 'Delgate Bank', 'Weston Hills', 'PE12 6DW', valid_addresses)
    assert output == 'No'