import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple

from shapely import Point

from constants import *


@dataclass
class LatLongPoint:
    """
    
    Contains validated latitude and longitude points.

    Properties:
    -----------
    latitude: float
        The latitude of the entry in degrees. Negative values denote degrees south.
    longitude: float
        The longitude of the entry in degrees. Negative values denote degrees west.

    """
    # init
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    # Attributes
    _latitude:  float
    _longitude: float

    # Properties
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, latitude: float) -> bool:
        if abs(latitude) > 90:
            return False
        self._latitude = latitude
        return True

    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, longitude: float) -> bool:
        if abs(longitude) >= 180:
            return False
        self._longitude = longitude
        return True
    
    # Methods

    # Convert to shapely point, which uses x,y (long, lat)
    def to_point(self):
        return Point(self.longitude, self.latitude)


@dataclass
class TrackEntry:

    """
    Class representing one entry in a cyclone's Track.

    Attributes:
    -----------
    location: LatLongPoint
        Location of the entry.
    datetime: datetime
        The date and time, in UTC (Zulu) of the entry.
    record_identifier: str
        Single char which contains data on the storm at this point.
        Not found in every entry.
    system_status:  str
        Two-char string which contains data on the storm at this point.
    max_windspeed: int
        Maximum wind speed at this point, in knots.

    """
    location:           LatLongPoint
    datetime:           datetime
    record_identifier:  Optional[str]
    system_status:      str
    max_windspeed:      int
    

@dataclass
class Track:
    """
    
    Represents a storm's track.

    Attributes:
    -----------
    basin: str
        The oceanic basin in which the storm originated. AL = Atlantic
    year: int
        Hurricane season year.
    cyclone_no: int
        Sequential number of the storm that year.
    no_track_entries:
        Number of expected data points in this track.
    max_windspeed:
        Max wind speed for any point in the track.
    name: str
        Name of the storm, if named. 'UNNAMED' if not.
    """

    basin:              str
    year:               int
    cyclone_no:         int
    no_track_entries:   int
    track_entries:      List[TrackEntry] = field(default_factory=list)
    max_windspeed:      int = 0
    name:               str = 'UNNAMED'

    def __post_init__(self):
        self.id = self.basin + str(self.year) + str(self.cyclone_no)

    def set_max_windspeed(self, entry: TrackEntry):
        self.max_windspeed = max(self.max_windspeed, entry.max_windspeed)

    def validate_entries(self) -> bool:
        """
        Validates that the number of TrackEntry instances matches no_track_entries expected.
        """
        if not len(self.track_entries) == self.no_track_entries:
            logging.warning('Number of track entries parsed does not match expected: %s' % self)
            return False
        else:
            return True


@dataclass
class Report:
    """
    
    Represents a report on a storm/track.

    Attributes:
    -----------
    name: str
        The name of the storm, or 'UNNAMED' if not named.
    max_windspeed: int
        Maximum windspeed, in knots, of the storm at any point in its life.
    landfall_dates: str
        String representation of the date and time, in UTC/Zulu time, of all landfall events for the storm.
    """

    name:           str
    max_windspeed:  int
    landfall_dates: List[str]
