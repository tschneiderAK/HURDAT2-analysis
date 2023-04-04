from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from re import match
from typing import List, Optional

# Create a time zone object representing a 0-hour offset from UTC, aka Zulu time.
zulu = timezone(timedelta(), name = 'Zulu Time (UTC)')


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


    Methods:
    --------

    """
    latitude:           float
    longitude:          float
    datetime:           datetime
    record_identifier:  Optional[str]
    system_status:      str


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
        if not self.source_name:
            self.source_name = self.source_path

    def extract_data(self) -> bool:
        data = DataSet
        with open(self.source_path, 'r') as source_data:
            for line in source_data:
                # check if the line is a header line, as defined by header_regex:
                if match(self.header_regex, line):
                    header = ''.split(line)
                    basin =  header[0][:2]
                    cyclone_no = header[0][2:4]
                    year = header[0][4:8]
                    track = Track(basin, cyclone_no, year)
                    self.data.tracks.append(track)
                # If not a header line, parse non-empty line as a data line.
                elif line:
                    # Break the data line on commas.
                    data_line = ','.split(line)
                    # Remove leading and trailing whitespace
                    for i, entry in enumerate(data_line):
                        data_line[i] = entry.strip()
                    # Parse to get track entry data.
                    entry_year = data_line[0][:4]
                    entry_month = data_line[0][4:6]
                    entry_day = data_line[0][6:8]
                    entry_hour = data_line[1][:2]
                    entry_minute = data_line[1][2:4]
                    record_identifier = data_line[2]
                    system_status = data_line[3]
                    latitude = float(data_line[4][:-1]) * (-1 * data_line[4][-1] == 'S')
                    longitude = float(data_line)[5][:-1] * (-1 * data_line[5][-1] == 'W')
                    max_windspeed = data_line[6]
                    
                    # Create a datetime object for the entry
                    track_datetime = datetime(entry_year, 
                                              entry_month, 
                                              entry_day, 
                                              entry_hour, 
                                              entry_minute,
                                              tzinfo=zulu)
                    
                    # Create a TrackEntry object for this line of data and append to the Track object
                    track_entry = TrackEntry(latitude= latitude, 
                                             longitude=longitude, 
                                             datetime=track_datetime,
                                             record_identifier=record_identifier,
                                             system_status=system_status)
                    
                    track.track_entries.append(track_entry)
        
        return data
                    






