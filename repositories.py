import json, logging
from dataclasses import dataclass
from re import findall, match
from pathlib import Path
from typing import List, Optional

from shapely.geometry import shape

from constants import *
from entities import *
from services import IArea, IReport, IStorm


class AreaJSONRepository(IArea):
    """
    
    Repository for creating a Geometry object from a geoJSON file.

    Public Methods:
    ---------------
    extract_geometry(self, file_source)


    """

    def extract_geometry(self, file_source):
        """
        
        Returns a shapely Geomtry object representing the area defined by the geoJSON in file_source.

        Paramters:
        ----------
        source_file: str
            String relative path to the geoJSON file to be ingested.

        Returns:
        --------
        area:   Geometry
            Geometry object created from the geoJSON.

        """
        with open(file_source, 'r') as f:
            data = json.load(f)
        area = shape(data['geometry'])
        return area


@dataclass
class StormTextRepository(IStorm):
    """
    
    Implementation of the IStorm interface using a .txt file data source.
    
    Attributes:
    -----------
    source_path: Path
        a Path object for the .txt source file
    source_name: str, optional
        name of the TextRepository instance, defaults to the string form of source_path
    header_regex: str
        Regex pattern which indicates a header line in the source file.
        Defaults to '^AL\d{6}'

    Public Methods:
    --------
    extract_data()
        Extracts the data from the given text file and returns a list of Track objects.
    
    
    """

    # Attributes
    source_path:    str
    source_name:    Optional[str] = None
    header_regex:   Optional[str] = HEADER_REGEX

    # Methods
    def __post_init__(self):
        """
        
        Sets the source_name to source_path if not provided.

        """
        if not self.source_name:
            self.source_name = self.source_path

    def extract_data(self) -> List[Track]:
        """

        Extracts data and returns a list of Track objects.

        Parameters:
        -----------
        None

        Returns:
        --------
        tracks: List[Track]
            List of Tracks from this data source.

        """

        with open(self.source_path, 'r') as source_data:
            lines = source_data.readlines()
            tracks = self._parse_tracks(lines)
        
        
        return tracks


    def _parse_tracks(self, lines) -> List[Track]:
        """
        Parses the data set and returns a list of Track objects representing the track of one storm.

        Parameters:
        -----------
        lines: list
            List of lines from the text file.
        
        Returns:
        --------
            List of Track objects found in the lines.

        """
        tracks = []

        for line in lines:
            if self._is_header(line):
                # _parse_header returns a Track
                track = self._parse_header(line)
                tracks.append(track)
            elif line:
                track.track_entries.append(self._parse_track_entry(line))

        # Call the validate_entries method for each track before returning to ensure all track entries were parsed.
        return [track for track in tracks if track.validate_entries()]


    def _is_header(self, line) -> bool:
        """
        Returns if the line is a header, based on the regex.
        
        Parameters:
        -----------
        line: str
            A string representing a header line from the input file.
        
        Returns:
        --------
        Boolean of whether the line meets the header line format.

        """
        
        if match(self.header_regex, line):
            return True
        
    def _parse_header(self, line) -> Track:
        """
        
        Returns a Track object created from the data in a header line.

        Parameters:
        -----------
        line: str
            A string representing a header line from the input file.
        
        Returns:
        --------
        track: Track
            A Track object instantiated with the header line's data.

        """
        # Split the header and strip whitespace
        header = [part.strip() for part in line.split(',')]

        # Parse the columns in the header
        basin, str_cyclone_no, str_year = findall(self.header_regex, header[HEADER_ID_COL])[0]
        cyclone_no, year = int(str_cyclone_no), int(str_year)
        name = header[HEADER_NAME_COL]
        no_track_entries = int(header[HEADER_COUNT_COL])

        # Create a Track instance to store track entries
        track = Track(
            basin=basin,
            year=year,
            cyclone_no=cyclone_no,
            name=name,
            no_track_entries=no_track_entries)
        logging.info('Storm parsed from data: Name: %s Year: %i Cyclone Number: %i' % (name, year, cyclone_no))
        return track

    def _parse_track_entry(self, line) -> TrackEntry:
        """
        Parses a data entry line and returns a TrackEntry object with the data.

        Parameters:
        -----------
        line: str
            A string representing a single line from the data file.

        Returns:
        --------
        track_entry: TrackEntry
            A TrackEntry object which contains the data from line.
        """

        # Split line on commas and remove leading and trailing whitespace
        data_line = line.split(',')
        data_line = [part.strip() for part in data_line]

        # Parse to get track entry data as a datetime object, using UTC/Zulu time.
        track_datetime = datetime.fromisoformat(data_line[DATA_DATE_COL] + 'T' + data_line[DATA_TIME_COL] + 'Z')

        # Parse lat/lon and convert S/W coords to negative values (S and W are multiplied by -1).
        latitude = float(data_line[DATA_LAT_COL][:-1]) * (-1 if data_line[DATA_LAT_COL][-1] == 'S' else 1)
        longitude = float(data_line[DATA_LON_COL][:-1]) * (-1 if data_line[DATA_LON_COL][-1] == 'W' else 1)
        location = LatLongPoint(latitude, longitude)

        # Create a TrackEntry object for this line of data and return
        track_entry = TrackEntry(
                                location=location,
                                datetime=track_datetime,
                                record_identifier = data_line[DATA_RECORD_ID_COL],
                                system_status = data_line[DATA_SYSTEM_STATUS_COL],
                                max_windspeed = int(data_line[DATA_MAX_WIND_COL])
                                )
        
        return track_entry
    
    
class JSONReportRepository(IReport):
    """
    
    Implementation of the IReport interface, using json as the file format.

    Public Methods:
    ---------------
    save(self, target, data)
        Saves the data to a JSON file in the target directory.
    
    """
    
    def save(self, target: str, data: List[dict]) -> bool:
        """
        
        Saves the data to a JSON file in the target directory.

        Parameters:
        -----------
        target: str
            String relative directory path for the report to be saved in.
        data:   List[dict]
            Data to be saved in the report.

        Returns:
        --------
        200 (success) or 400 (failure)


        """
        directory = Path(target)
        # Check if the target is a valid directory.
        if not directory.exists() or not directory.is_dir():
            return 400
        
        # Specify the report file path.
        # TODO: Add logic to avoid overwriting existing files.
        report_path = Path(target + "/HURDAT2_REPORT.json")
        
        # Write the data to file.
        with report_path.open(mode='w') as file:
            json.dump(data, file)

        return 200