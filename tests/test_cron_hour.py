from cron_parser.cron import Cron, Hour
import pytest

def test_valid_split_star_hour():
    valid_cron = "0 * 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    hour = Hour(cron.raw_hour)
    assert hour.parse() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

def test_valid_split_range_hour():
    valid_cron = "0 0-15 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    hour = Hour(cron.raw_hour)
    assert hour.parse() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def test_valid_split_value_separator_hour():
    valid_cron = "0 0,12 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    hour = Hour(cron.raw_hour)
    assert hour.parse() == [0, 12]
    
def test_valid_split_step_star_base_hour():
    valid_cron = "0 */3 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    hour = Hour(cron.raw_hour)
    assert hour.parse() == [0, 3, 6, 9, 12, 15, 18, 21]

def test_valid_split_step_range_base_hour():
    valid_cron = "0 5-21/4 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    hour = Hour(cron.raw_hour)
    assert hour.parse() == [5, 9, 13, 17, 21]

def test_outside_of_range_hour():
    invalid_cron = "0 24 1 0 0"
    with pytest.raises(
        ValueError,
        match="Invalid value in hour. Received 24 as hour, expected value between 0 and 23.",
    ):
        cron = Cron(invalid_cron)

def test_outside_of_range_hour_range_split():
    invalid_cron = "0 1-26/4 1 1 0"
    with pytest.raises(
        ValueError,
        match="Invalid range in base value. Received 1-26 as base for hour, expected base value between 0-23.",
    ):
        cron = Cron(invalid_cron)
