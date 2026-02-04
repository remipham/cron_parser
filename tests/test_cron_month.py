
from cron_parser.cron import Cron, Month
import pytest


def test_valid_split_star_month():
    valid_cron = "* 0 1 * 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    month = Month(cron.raw_month)
    assert month.parse() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def test_valid_split_range_month():
    valid_cron = "* * * 1-6 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    month = Month(cron.raw_month)
    assert month.parse() == [1, 2, 3, 4, 5, 6]

def test_valid_split_value_separator_month():
    valid_cron = "1 1 1 1,2,6 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    month = Month(cron.raw_month)
    assert month.parse() == [1, 2, 6]

def test_valid_split_step_star_base_month():
    valid_cron = "1 0 1 */3 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    month = Month(cron.raw_month)
    assert month.parse() == [1, 4, 7, 10]
    
def test_valid_split_step_range_base_month():
    valid_cron = "1 0 1 1-11/3 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    month = Month(cron.raw_month)
    assert month.parse() == [1, 4, 7, 10]

def test_outside_of_range_month():
    invalid_cron = "0 0 1 0 0"
    with pytest.raises(
        ValueError,
        match="Invalid value in month. Received 0 as month, expected value between 1 and 12.",
    ):
        cron = Cron(invalid_cron)

    invalid_cron = "0 0 1 13 0"
    with pytest.raises(
        ValueError,
        match="Invalid value in month. Received 13 as month, expected value between 1 and 12.",
    ):
        cron = Cron(invalid_cron)

def test_outside_of_range_month_range_split():
    invalid_cron = "0 0 1 1-14/3 0"
    with pytest.raises(
        ValueError,
        match="Invalid range in base value. Received 1-14 as base for month, expected base value between 1-12.",
    ):
        cron = Cron(invalid_cron)
