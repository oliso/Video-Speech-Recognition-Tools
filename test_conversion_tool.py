# -*- coding: utf-8 -*-
"""
Test script for conversion_tool.

@author: Oliver
"""


import pytest
import conversion_tool as ct


# Test valid cases:
def test_valid_conversion_tool():
    """Test valid cases."""
    assert ct.convert_file(file_path="C:/Users/Oliver/PycharmProjects/Afringa_Video_Analysis",
                           file_list=['A_CV']
                           ) == 'Success!'
    assert ct.convert_file(file_path="C:/Users/Oliver/PycharmProjects/Afringa_Video_Analysis",
                           file_list=['A_test', 'B_test']
                           ) == 'Success!'
    


# Test invalid cases:
def test_invalid_conversion_tool():
    """Test invalid cases."""
    with pytest.raises(Exception):
        assert ct.convert_file(file_path="C:/Users/Oliver/PycharmProjects/Afringa_Video_Analys",
                               file_list=['A_test', 'B_test']
                               )
        assert ct.convert_file(file_path="C:/Users/Oliver/PycharmProjects/Afringa_Video_Analysis",
                               file_list=['test', 'B_test']
                               )
        assert ct.convert_file(file_path="C:/Users/Oliver/PycharmProjects/Afringa_Video_Analysis",
                               file_list=['A_tt']
                               )
        assert ct.convert_file(file_path="C:/Users/Oliver/PycharmProjects/Afringa_Video_Analysis",
                               file_list="A_test"
                               )
        assert ct.convert_file(file_list=['A_test', 'B_test']) # these are not in my cwd
