
from cron_parser.cron import Cron, Minute
import pytest


def test_valid_split_star_minute():
    valid_cron = "* 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

def test_valid_split_range_minute():
    valid_cron = "0-15 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def test_valid_split_value_separator_minute():
    valid_cron = "0,15,30,45 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 15, 30, 45]

def test_valid_split_step_star_base_minute():
    valid_cron = "*/15 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 15, 30, 45]

def test_valid_split_step_range_base_minute():
    valid_cron = "5-59/15 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [5, 20, 35, 50]

def test_outside_of_range_minute():
    invalid_cron = "60 0 1 1 0"
    with pytest.raises(
        ValueError,
        match="Invalid value in minute. Received 60 as minute, expected value between 0 and 59.",
    ):
        cron = Cron(invalid_cron)

def test_outside_of_range_day_of_month_range_split():
    invalid_cron = "0-79/2 0 1 1 0"
    with pytest.raises(
        ValueError,
        match="Invalid range in base value. Received 0-79 as base for minute, expected base value between 0-59.",
    ):
        cron = Cron(invalid_cron)
