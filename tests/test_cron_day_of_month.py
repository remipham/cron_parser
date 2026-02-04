
from cron_parser.cron import Cron, DayOfMonth
import pytest


def test_valid_split_star_day_of_month():
    valid_cron = "* 0 * 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_month = DayOfMonth(cron.raw_day_of_month)
    assert day_of_month.parse() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

def test_valid_split_range_day_of_month():
    valid_cron = "* * 1-15 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_month = DayOfMonth(cron.raw_day_of_month)
    assert day_of_month.parse() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def test_valid_split_value_separator_day_of_month():
    valid_cron = "1 1 1,2,3 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_month = DayOfMonth(cron.raw_day_of_month)
    assert day_of_month.parse() == [1, 2, 3]

def test_valid_split_step_star_base_day_of_month():
    valid_cron = "1 0 */5 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_month = DayOfMonth(cron.raw_day_of_month)
    assert day_of_month.parse() == [1, 6, 11, 16, 21, 26, 31]
    
def test_valid_split_step_range_base_day_of_month():
    valid_cron = "1 0 1-15/3 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_month = DayOfMonth(cron.raw_day_of_month)
    assert day_of_month.parse() == [1, 4, 7, 10, 13]

def test_outside_of_range_day_of_month():
    invalid_cron = "0 0 0 1 0"
    with pytest.raises(
        ValueError,
        match="Invalid value in day_of_month. Received 0 as day_of_month, expected value between 1 and 31.",
    ):
        cron = Cron(invalid_cron)

    invalid_cron = "0 0 32 1 0"
    with pytest.raises(
        ValueError,
        match="Invalid value in day_of_month. Received 32 as day_of_month, expected value between 1 and 31.",
    ):
        cron = Cron(invalid_cron)

def test_outside_of_range_day_of_month_range_split():
    invalid_cron = "0 0 3-32/4 1 0"
    with pytest.raises(
        ValueError,
        match="Invalid range in base value. Received 3-32 as base for day_of_month, expected base value between 1-31.",
    ):
        cron = Cron(invalid_cron)
