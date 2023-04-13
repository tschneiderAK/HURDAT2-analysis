from abc import ABC, abstractmethod

from matplotlib.path import Path as mpltPath
from shapely import Geometry

import constants
from entities import *

class IArea(ABC):
    """
    Abstract class to serve as an interface for area sources.

    Methods:
    --------
    extract_geometry()
        Extracts a list of points which form the boundary of an area.
    """

    @abstractmethod
    def extract_geometry():
        pass

class IReport(ABC):
    """
    Abstract base class to serve as an interface for saving reports.

    """

    @abstractmethod
    def save():
        pass

class IStorm(ABC):
    """
    Abstract class to serve as an interface for track data sources.

    Methods:
    --------
    extract_data()
        Extracts the data from the given source and returns a list of Track objects.

    """

    @abstractmethod
    def extract_data() -> List[Track]:
        pass

class AreaService:
    """
    Service for a distinct geographical area.

    Attributes:
    -----------
        name:       str
            Name of the area
        shape:      shaprely.Geometry
            Geometry instance object.

    Methods:
    --------
    contains_point(LatLongPoint):
        Returns whether a LatLongPoint is within or on the boundary of the polygon.

    """

    def __init__(self, repository: IArea, file_source=None) -> None:
        self.repository = repository()
        self.geometry = self.repository.extract_geometry(file_source=file_source)

class StormDataService:
    """
    Creates one or more storm Track instances and provides analysis on them.

    Attributes:
    -----------
    tracks: List[Track]
        A list of Track instances.

    Methods:
    --------
    makes_landfall(self, area)
        Returns whether the storm track contains any points which are within area.

    get_landfall_dates(self, area)
        Returns a list of TrackEntry instances where the storm has made landfall.
        A storm is considered to make landfall multiple times when at least 1 TrackEntry outside area falls between

    
    get_max_windspeed()
    """

    def __init__(self, repo: IStorm, source_path: str, area: IArea):
        self.repo = repo(source_path)
        self.area = area
        self.tracks = self.repo.extract_data()

    def record_landfall_events(self):
        records = []

        for track in self.tracks:
            landfalls = StormDataService.get_landfall_dates(track, self.area.geometry)
            if not landfalls:
                continue
            record = {
                'name': track.name,
                'lf_events': [(str(landfall.datetime), landfall.max_windspeed) for landfall in landfalls]
            }
            records.append(record)
        
        return records

    @staticmethod
    def get_landfall_dates(track: Track, area: Geometry) -> List[TrackEntry]:
        """
        
        Returns all dates and times when the storm makes landfall over an area, 
        with the max windspeed at that time.

        Parameters:
        -----------
        area: Area
            The land where we want to identify landfall events.

        Returns:
        --------
            List of TrackEntry instances.
        
        """
        in_area = False
        entries = []
        for track_entry in track.track_entries:
            # Check if this point is in the area specified.
            if not area.contains(track_entry.location.to_point()):
                in_area = False
                continue
            # If the in_area flag is True, then this is not a new landfall event.
            if in_area:
                continue

            # Append the new landfall event to entries.
            else:                
                in_area = True
                entries.append(track_entry)

        return entries


class ReportService():
    """
    Creates one or more Report instances and calls implementation of the IReport
     interface to save.

    Attributes:
    -----------
    records: List[Dict]
        List of dicts which will be reported.
    report_date: str
        The date the report was made, in the format {YYYY}{MM}{DD}

    Methods:
    --------
    create_report(fields:)
    """

    def __init__(self, repo) -> None:
        self.report = {}
        self.report_date = datetime.today()
        self.repository = repo()

    def generate(self, storms):
        self.report = {
            'Report Date': str(self.report_date),
            'Storms making landfall:': storms,
        }

    def save(self, target: str):
        self.repository.save(target, self.report)