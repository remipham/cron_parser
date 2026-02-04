# cron_parser

A simple Python CLI tool and library to parse cron strings and print their expanded fields.

## Features
- Parse standard 5-field cron expressions (minute, hour, day of month, month, day of week)
- Print expanded values for each field
- Warnings for invalid or unusual cron combinations

## Requirements
- Python 3.7+

## Installation
Clone the repository:
```sh
git clone <your-repo-url>
cd cron_parser
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

## Running Tests
To run all tests with coverage:

```sh
pytest
```

This will show a coverage report for the `cron_parser` package.
