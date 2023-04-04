from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from re import match
from typing import List, Optional


@dataclass
class TrackEntry:

    """
    Class representing one tracking point entry in a cyclone's Track.

    Attributes:
    -----------
    latitude: float
        The latitude of the entry.
    longitude: float
        The longitude of the entry.
    datetime: datetime
        The date and time, in UTC (Zulu) of the entry.
    record_identifier: [Optional]str
        Single-letter identifier:
            C Closest approach to a coast, not followed by a landfall
            G Genesis
            I An intensity peak in terms of both pressure and wind
            L Landfall (center of system crossing a coastline)
            P Minimum in central pressure
            R Provides additional detail on the intensity of the cyclone when rapid changes are underway
            S Change of status of the system
            T Provides additional detail on the track (position) of the cyclone
            W Maximum sustained wind speed
    system_status: str
        Two-letter status code for the storm at the time of entry.
            TD Tropical cyclone of tropical depression intensity (< 34 knots)
            TS Tropical cyclone of tropical storm intensity (34-63 knots)
            HU Tropical cyclone of hurricane intensity (> 64 knots)
            EX Extratropical cyclone (of any intensity)
            SD Subtropical cyclone of subtropical depression intensity (< 34 knots)
            SS Subtropical cyclone of subtropical storm intensity (> 34 knots)
            LO A low that is neither a tropical cyclone, a subtropical cyclone, nor an extratropical cyclone (of any intensity)
            WV Tropical Wave (of any intensity)
            DB Disturbance (of any intensity)
    max_windspeed: int
        Maximum sustained windspeed for this entry, in knots.


    Methods:
    --------

    """
    latitude:           float
    longitude:          float
    datetime:           datetime
    record_identifier:  Optional[str]
    system_status:      str
    max_windspeed:      int


@dataclass
class Track:
    basin:              str
    year:               int
    cyclone_no:         int
    no_track_entries:   int
    track_entries:      List[TrackEntry]

@dataclass
class DataSet:
    tracks:      List[Track]
    source_type: str = 'Unnamed source'
    name:        str = 'Unnamed data set'


class DataSource(ABC):
    """
    Abstract class to serve as an interface for data sources.

    Methods:
    --------
    extract_data()
        Will extract the data from the given source and parse it into a DataSet object.
    export_events()
        Returns the DataSet object.

    """

    @abstractmethod
    def extract_data():
        pass


@dataclass    
class TextSource(DataSource):
    """
    
    DataSource subclass which ingests data from a .txt file.
    
    Attributes:
    -----------
    source_path: Path
        a Path object for the .txt source file
    source_name: str, optional
        name of the TextSource instance, defaults to the string form of source_path
    header_regex: str
        Regex pattern which indicates a header line in the source file.
        Defaults to '^AL\d{6}'

    Methods:
    --------
    extract_data()
        Will extract the data from the given source and parse it into a DataSet object.
    export_events()
        Returns the DataSet object.
    
    """

    source_path:    str
    source_name:    Optional[str] = None
    header_regex:   Optional[str] = r"^AL(\d{6})"


    def __post_init__(self):
        """
        
        Sets the source_name to source_path if not provided.

        """
        if not self.source_name:
            self.source_name = self.source_path

    def extract_data(self) -> DataSet:
        """

        Extracts data and returns a DataSet object.

        """

        with open(self.source_path, 'r') as source_data:
            lines = source_data.readlines()
            tracks = self._parse_tracks(lines)
        
        return DataSet(tracks=tracks, source_type='text', name= 'self.source_name')


    def _parse_tracks(self, lines) -> List[Track]:
            line_ct = len(lines)
            i = 0
            tracks = []
            while i < line_ct:
                if self._is_header(lines[i]):
                    header = lines[i].split(',')
                    header = [part.strip() for part in header]
                    basin =  header[0][:2]
                    cyclone_no = int(header[0][2:4])
                    year = int(header[0][4:8])
                    name = header[1]
                    no_track_entries = int(header[2])
                    track_entries = []
                    
                    i += 1
                    while i < line_ct and not self._is_header(lines[i]):
                        print(i)
                        if not lines[i]:
                             i += 1
                             continue
                        track_entries.append(self._parse_data_line(lines[i]))
                        i += 1

                    track = Track(basin=basin,
                                  year=year,
                                  cyclone_no=cyclone_no,
                                  no_track_entries=no_track_entries,
                                  track_entries=track_entries)
                    tracks.append(track)
            return tracks


    def _is_header(self, line):
            if match(self.header_regex, line):
                return True
                  

    def _parse_data_line(self, line):
        # Break the data line on commas.
                    # Split line on commas and remove leading and trailing whitespace
                    data_line = line.split(',')
                    data_line = [part.strip() for part in data_line]

                    # Parse to get track entry data as a datetime object
                    entry_date_time = data_line[0] + 'T' + data_line[1] + 'Z'
                    track_datetime = datetime.fromisoformat(entry_date_time)

                    # Parse meteorological data
                    record_identifier = data_line[2]
                    system_status = data_line[3]
                    max_windspeed = data_line[6]

                    # Parse lat/lon and convert S/W coords to negative values.
                    latitude = float(data_line[4][:-1]) * (-1 ** (data_line[4][-1] == 'S'))
                    longitude = float(data_line[5][:-1]) * (-1 ** (data_line[5][-1] == 'W'))
                  
                    # Create a TrackEntry object for this line of data and return
                    track_entry = TrackEntry(latitude= latitude, 
                                             longitude=longitude, 
                                             datetime=track_datetime,
                                             record_identifier=record_identifier,
                                             system_status=system_status,
                                             max_windspeed= max_windspeed)
                    
                    return track_entry           






