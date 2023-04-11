from domain_models import *

class AreaService:
    """
    Provides an application service related to a defined area.

    Methods:
    --------
    contains(LatLongPoint):
        Returns whether a LatLongPoint is within or on the boundary polygon.
    """

    def area_contains_point(self, area: GeoArea, point: LatLongPoint) -> bool:
        pass

    def area_contains_any(self, area: GeoArea, points: List[LatLongPoint]) -> bool:
        for point in points:
            if self.area_contains_point(area, point):
                return True
        return False

class StormReportService:
    """
    Service for analyzing a storm or set of storms.

    Attributes:
    -----------
    track: Track
        A Track instance.

    Methods:
    --------
    makes_landfall(self, area)
        Returns whether the storm track contains any points which are within area.

    get_landfall_dates(self, area)
        Returns a list of TrackEntry instances where the storm has made landfall.
        A storm is considered to make landfall multiple times when at least 1 TrackEntry outside area falls between

    
    get_max_windspeed()
    """

    def __init__(self, track: Track):
        self.track = track
        landfall_entries = []

    def get_landfall_dates(self, area: GeoArea) -> List[TrackEntry]:
        """
        
        Returns all dates and times when the storm makes landfall over an area.

        Parameters:
        -----------
        area: GeoArea
            The land where we want to identify landfall events.

        Returns:
        --------
            List of strings, formatted in ISO 8601 format ({YYYY}{MM}{DD}T{HH}{MM}).
        
        """
        in_area = False
        entries = []
        for track_entry in self.track.track_entries:
            # Check if this point is in the area specified.
            if not area.contains(track_entry.location):
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
