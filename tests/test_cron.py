from io import StringIO
import sys
import pytest
from cron_parser.cron import Cron, Minute, Hour, DayOfMonth, Month, DayOfWeek

def test_sample_cron():
    sample_cron = "*/15 0 1,15 * 1-5"
    cron = Cron(sample_cron)
    assert cron.input_string == sample_cron
    assert cron.minute.value == [0, 15, 30, 45]
    assert cron.hour.value == [0]
    assert cron.day_of_month.value == [1, 15]
    assert cron.month.value == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    assert cron.day_of_week.value == [1, 2, 3, 4, 5]

def test_valid_cron():
    valid_cron = "* * * * *"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron


def test_invalid_cron_too_few_parts():
    invalid_cron = "* * * *"
    with pytest.raises(
        ValueError,
        match="Invalid format. The string should contain exactly 5 parts separated by spaces, got 4 parts.",
    ):
        cron = Cron(invalid_cron)


def test_invalid_cron_too_many_parts():
    invalid_cron = "* * * * * *"
    with pytest.raises(
        ValueError,
        match="Invalid format. The string should contain exactly 5 parts separated by spaces, got 6 parts.",
    ):
        cron = Cron(invalid_cron)


def test_valid_cron_with_numbers():
    valid_cron = "0 12 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    assert cron.minute.value == [0]
    assert cron.hour.value == [12]
    assert cron.day_of_month.value == [1]
    assert cron.month.value == [1]
    assert cron.day_of_week.value == [0]


def test_invalid_cron_with_invalid_characters():
    invalid_cron = "0 12 1 1 A"
    with pytest.raises(
        ValueError, match="Invalid format. The string contains invalid characters."
    ):
        cron = Cron(invalid_cron)


def test_valid_split_star_minute():
    valid_cron = "* 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
    assert cron.day_of_week.value == [0]

def test_valid_split_range_minute():
    valid_cron = "0-15 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert cron.day_of_week.value == [0]

def test_valid_split_value_separator_minute():
    valid_cron = "0,15,30,45 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 15, 30, 45]
    assert cron.day_of_week.value == [0]

def test_valid_split_step_star_base_minute():
    valid_cron = "*/15 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [0, 15, 30, 45]
    assert cron.day_of_week.value == [0]

def test_valid_split_step_range_base_minute():
    valid_cron = "5-59/15 0 1 1 0"
    cron = Cron(valid_cron)
    assert cron.input_string == valid_cron
    minute = Minute(cron.raw_minute)
    assert minute.parse() == [5, 20, 35, 50]
    assert cron.day_of_week.value == [0]

def test_print_output_basic(monkeypatch):
    # Arrange
    cron_str = "*/15 0 1,15 * 1-5"
    cron = Cron(cron_str)
    captured = StringIO()
    monkeypatch.setattr(sys, "stdout", captured)

    # Act
    cron.print_output()

    # Reset stdout
    sys.stdout = sys.__stdout__
    output = captured.getvalue().strip().split("\n")

    # Assert
    assert output[0].startswith("minute")
    assert output[1].startswith("hour")
    assert output[2].startswith("day_of_month")
    assert output[3].startswith("month")
    assert output[4].startswith("day_of_week")
    # Check some expected values
    assert "0 15 30 45" in output[0]
    assert output[1].replace(" ","").startswith("hour0")
    assert output[2].replace(" ","").startswith("day_of_month115")
    assert output[3].replace(" ","").startswith("month123456789101112")
    assert output[4].replace(" ","").startswith("day_of_week12345")

def test_print_output_single_values(monkeypatch):
    cron_str = "5 6 7 8 2"
    cron = Cron(cron_str)
    captured = StringIO()
    monkeypatch.setattr(sys, "stdout", captured)
    cron.print_output()
    sys.stdout = sys.__stdout__
    output = captured.getvalue().strip().split("\n")
    assert output[0].replace(" ","").startswith("minute5")
    assert output[1].replace(" ","").startswith("hour6")
    assert output[2].replace(" ","").startswith("day_of_month7")
    assert output[3].replace(" ","").startswith("month8")
    assert output[4].replace(" ","").startswith("day_of_week2")
