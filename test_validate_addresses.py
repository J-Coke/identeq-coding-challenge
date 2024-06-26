import pytest
import pandas as pd

from validate_addresses import process_abp_data


def test_process_abp_data_can_process_one_address():
    input_data = pd.DataFrame({
        'SINGLE_LINE_ADDRESS': ["AAA"],
        'POSTCODE': ['CB2 1AB'],
        'STREET_NAME': ['REGENT STREET']
    })
    print(type(input_data))
    output = process_abp_data(input_data)
    expected_output = {'CB2 1AB':['REGENT STREET']}
    assert output == expected_output