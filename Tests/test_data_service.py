import sys
from datetime import datetime

sys.path.append('../hurdat2')

import os
import json
import unittest

from shapely import geometry

from services import StormDataService
from repositories import StormTextRepository


class TestDataServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        florida_path = os.path.join( os.path.dirname(__file__), '../data/florida.json' )
        with open(florida_path) as f:
            data = json.load(f)

        cls.multi_area_florida = geometry.shape(data['geometry'])
        # Orlando is roughly 28.5 N, 81.4 W. Point() initializes with x, y
        cls.point_orlando = geometry.Point(-81.4, 28.5)

        data_path = os.path.join(os.path.dirname(__file__), './data/services_test_storms.txt')
        data_repo = StormTextRepository(source_path=data_path)

        cls.irma_track = data_repo.extract_data()[0]
        cls.katia_track = data_repo.extract_data()[1]
        cls.wilma_track = data_repo.extract_data()[2]

    def test_contains(self):
        self.assertTrue(TestDataServices.multi_area_florida.contains(TestDataServices.point_orlando))

    def test_get_landfall_dates(self):
        # Arrange
        wilma_expected_date = datetime.fromisoformat('20051024T1030Z')
        irma_expected_dates = [datetime.fromisoformat('20170910T1300Z'), datetime.fromisoformat('20170910T1930Z')]
        
        # Act
        wilma_dates = StormDataService.get_landfall_dates(TestDataServices.wilma_track, TestDataServices.multi_area_florida)
        irma_dates = StormDataService.get_landfall_dates(TestDataServices.irma_track, TestDataServices.multi_area_florida)
        katia_dates = StormDataService.get_landfall_dates(TestDataServices.katia_track, TestDataServices.multi_area_florida)

        # Assert

        # Hurricane Wilma made landfall in Florida only once on Oct 24, 2005 at 105kts despite landfall in other areas.
        self.assertEqual(len(wilma_dates), 1)
        self.assertEqual(wilma_dates[0].max_windspeed, 105)
        self.assertEqual(wilma_expected_date, wilma_dates[0].datetime)

        # Hurricane Irma made landfall in the Florida Keys, and again on mainland. Two entries expected.
        self.assertEqual(len(irma_dates), 2)
        self.assertEqual(irma_dates[0].datetime, irma_expected_dates[0])
        self.assertEqual(irma_dates[1].datetime, irma_expected_dates[1])
        
        # Hurricane Katia made landfall once, but not in Florida. No entries expected.
        self.assertEqual(len(katia_dates), 0)
        

if __name__ == '__main__':
    unittest.main()
