from abc import ABC, abstractmethod

from shapely import Geometry

from entities import *

class IArea(ABC):
    """
    Abstract class to serve as an interface for area sources.

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

    """

    @abstractmethod
    def extract_data() -> List[Track]:
        pass

class AreaService:
    """
    Service for a distinct geographical area.

    Attributes:
    -----------
        repository: IArea
            Instance of the IArea repository base class, used for ingesting area data.
        shape:      shapely.Geometry
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
    repo:   IStorm
        Instance of the IStorm interface base class. Used to ingest storm data.
    area:   IArea
        Instance of the IArea interface base class. Used to hold data and methods for the area being analyzed.
    tracks: List[Track]
        A list of Track instances for the storm data ingested.

    Static Methods:
    ---------------
    get_landfall_dates(track, area)
        Returns all dates and times when the storm makes landfall over an area, with the max windspeed at that time.

    Public Methods:
    ---------------
    record_landfall_dates(self)
        Returns a list of dict object containing the track name and a list of all landfall times and wind speeds.

    
    get_max_windspeed()
    """

    def __init__(self, repo: IStorm, source_path: str, area: IArea):
        self.repo = repo(source_path)
        self.area = area
        self.tracks = self.repo.extract_data()

    @staticmethod
    def get_landfall_dates(track: Track, area: Geometry) -> List[TrackEntry]:
        """
        
        Returns all dates and times when the storm makes landfall over an area, with the max windspeed at that time.

        Parameters:
        -----------
        track: Track
            Track object of the storm being analyzed.
        area: Area
            The area where we want to identify landfall events.

        Returns:
        --------
            List of TrackEntry instances.
        
        """
        in_area = False
        entries = []
        for track_entry in track.track_entries:
            # Check if this point is in the area specified, and has a hurricane designation.
            if not (track_entry.system_status == 'HU' and area.contains(track_entry.location.to_point())):
                in_area = False
                continue
            # If the in_area flag is True, then this is not a new landfall event: the storm has not yet moved out of the target area.
            if in_area:
                continue

            # Append the new landfall event to entries.
            else:                
                in_area = True
                entries.append(track_entry)

        return entries

    def record_landfall_events(self) -> List[dict]:
        """
        Returns a list of dict object containing the track name and a list of all landfall times and wind speeds.
        """
        records = []

        for track in self.tracks:
            landfalls = StormDataService.get_landfall_dates(track, self.area.geometry)
            if not landfalls:
                continue
            record = {
                'name': track.name,
                'landfall_events': [ {'datetime': landfall.datetime.isoformat(), 'max_windspeed_kts': landfall.max_windspeed} for landfall in landfalls]
            }
            records.append(record)
        
        return records

    


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

    Public Methods:
    --------
    generate(fields):


    """

    def __init__(self, repo: IReport) -> None:
        self.report = {}
        self.report_date = datetime.today()
        self.repository = repo()

    def generate(self, storms) -> None:
        """
        Adds a report date to the storms parameter and saves them to the instance for saving.

        Paramters:
        ----------
        storms: List[dict]
            A list of dicts containing information about storms to be added to the report.

        """
        self.report = {
            'Report Date': str(self.report_date),
            'Storms making landfall:': storms,
        }

    def save(self, target: str) -> int:
        """"
        
        Saves the report attribute using the provided IReport repository.
        Returns a success (200) or error (400) code.

        Parameters:
        -----------
        target: str
            String of the relative target directory path.

        """
        return_code = self.repository.save(target, self.report)
        return return_code