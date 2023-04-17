# TODO: Replace this with a .env file.

# Header row column numbers for parsing
HEADER_REGEX = r"^([A-Z]{2})(\d{2})(\d{4})"
HEADER_ID_COL = 0
HEADER_NAME_COL = 1
HEADER_COUNT_COL = 2

# Data row column numbers for parsing
DATA_DATE_COL = 0
DATA_TIME_COL = 1
DATA_RECORD_ID_COL = 2
DATA_SYSTEM_STATUS_COL = 3
DATA_LAT_COL = 4
DATA_LON_COL = 5
DATA_MAX_WIND_COL = 6


# File directories
FLORIDA_GEOJSON = './data/florida.json'
HURDAT_DATA = './data/hurdat2-1851-2021-100522.txt'
REPORT = './reports/'
