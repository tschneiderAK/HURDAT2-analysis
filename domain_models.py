from dataclasses import dataclass, field
from datetime import datetime
import logging
from typing import List, Optional, Tuple

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

    basin:              str
    year:               int
    cyclone_no:         int
    no_track_entries:   int
    track_entries:      List[TrackEntry] = field(default_factory=list)
    max_windspeed:      int = 0
    name:               str = 'UNNAMED'

    def validate_entries(self) -> bool:
        """
        Validates that the number of TrackEntry instances matches no_track_entries expected.
        """
        if not len(self.track_entries) == self.no_track_entries:
            logging.warning('Number of track entries parsed does not match expected: %s' % self)
            return False
        else:
            return True


class GeoArea:
    """
    
    Represents a geographical area defined by a polygon of LatLongPoints.

    Attributes:
    -----------
    boundary: List[LatLongPoint]
        Defines the boundary of the area.

    Methods:
    --------
    contains(LatLongPoint):
        Returns whether a LatLongPoint is within or on the boundary polygon.
    
    """
    def __init__(self, name, boundary_points: List[Tuple[float, float]]):
        # Check if 3 or more distinct points are provided, raise exception if not.
        if len(set(boundary_points)) < 3:
            raise ValueError('Fewer than 3 points passed to initialize GeoArea. At least 3 distinct points are required to create a GeoArea.')
        self.boundary = boundary_points

    def contains(self, point: LatLongPoint) -> bool:
        pass

@dataclass
class StormReport:
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
