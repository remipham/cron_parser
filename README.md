# cron_parser

A simple Python CLI tool and library to parse cron strings and print their expanded fields.

## Features
- Parse standard 5-field cron expressions (minute, hour, day of month, month, day of week)
- Print expanded values for each field
- Warnings for invalid or unusual cron combinations

## Requirements
- Python 3.10 minimum

## Installation
Clone the repository:
```sh
git clone https://github.com/remipham/cron_parser.git
cd cron_parser
```

The package uses Poetry for package dependencies management. Check https://python-poetry.org/docs/#installation and run

```sh
poetry install
```

## Usage
You can run the CLI with the following command in the root folder

```sh
python -m cron_parser '*/15 0 1,15 * 1-5'
```

This will output the expanded cron fields, e.g.:
```
minute       0 15 30 45
hour         0
day_of_month 1 15
month        1 2 3 4 5 6 7 8 9 10 11 12
day_of_week  1 2 3 4 5
```

Some basic warnings have been implemented to alert when some dates in the cron expression won't be possible (for now, more days than in the month)

## Running Tests
To run all tests:

```sh
pytest
```
