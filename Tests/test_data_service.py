import sys

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

        wilma_path = os.path.join(os.path.dirname(__file__), './data/wilma.txt')
        wilma_repo = StormTextRepository(source_path=wilma_path)
        cls.wilma_track = wilma_repo.extract_data()[0]

    def test_contains(self):
        self.assertTrue(TestDataServices.multi_area_florida.contains(TestDataServices.point_orlando))

    def test_get_landfall_dates(self):
        landfall_dates = StormDataService.get_landfall_dates(TestDataServices.wilma_track, TestDataServices.multi_area_florida)
        self.assertGreater(len(landfall_dates), 0)

if __name__ == '__main__':
    unittest.main()
