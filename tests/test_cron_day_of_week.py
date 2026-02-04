
from cron_parser.cron import Cron, DayOfWeek
import pytest


def test_valid_split_star_day_of_week():
    valid_cron = "* 0 1 * *"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_week = DayOfWeek(cron.raw_day_of_week)
    assert day_of_week.value == [0, 1, 2, 3, 4, 5, 6]

def test_valid_split_range_day_of_week():
    valid_cron = "* * * * 1-6"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_week = DayOfWeek(cron.raw_day_of_week)
    assert day_of_week.value == [1, 2, 3, 4, 5, 6]

def test_valid_split_value_separator_day_of_week():
    valid_cron = "1 1 1 1 0,1,6"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_week = DayOfWeek(cron.raw_day_of_week)
    assert day_of_week.value == [0, 1, 6]

def test_valid_split_step_star_base_day_of_week():
    valid_cron = "1 0 1 1 */2"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_week = DayOfWeek(cron.raw_day_of_week)
    assert day_of_week.value == [0, 2, 4, 6]
    
def test_valid_split_step_range_base_day_of_week():
    valid_cron = "1 0 1 1 1-6/3"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    day_of_week = DayOfWeek(cron.raw_day_of_week)
    assert day_of_week.parse() == [1, 4]

def test_outside_of_range_day_of_week():
    invalid_cron = "0 0 1 1 13"
    with pytest.raises(
        ValueError,
        match="Invalid value in day_of_week. Received 13 as day_of_week, expected value between 0 and 7.",
    ):
        cron = Cron(invalid_cron)

def test_outside_of_range_day_of_week_range_split():
    invalid_cron = "0 0 1 1 1-14/3"
    with pytest.raises(
        ValueError,
        match="Invalid range in base value. Received 1-14 as base for day_of_week, expected base value between 0-7.",
    ):
        cron = Cron(invalid_cron)
