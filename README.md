# HURDAT2 Data Analysis Tool

## Background

This application will analyze a data set in the format of the HURDAT2 as defined and provided by the NOAA National Hurricance Center. Data sets and explanations of their format can be found at the [NHC Data Archive.](https://www.nhc.noaa.gov/data/.)

## Installation

### Python

Requires Python 3.11 to run. [Download Python 3.11](https://www.python.org/downloads/release/python-3110/) and run the installer. When prompted, add the python installation to system PATH.

### Packages and Dependencies

Required dependencies are documented in requirements.txt. Install in your virtual or local environment:

```
user@host: $ python -m pip install requirements.txt
```

## Use

### Configuration

Configuration details can be altered in constants.py. To analyze all hurricanes which made landfall in Florida from 1851-2022, no changes are needed.

### Run

Call main.py as follows:

```
user@host: $ python main.py
```

## Output

Output report will be exported to the /reports/ directory. Currently, only .JSON formatted exports are supported.