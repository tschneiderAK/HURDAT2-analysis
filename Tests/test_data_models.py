import sys, os

sys.path.append('../hurdat2')

from datetime import datetime
import unittest
from typing import List

from repositories import StormTextRepository as repo
import entities as ent

class TestStormTextRepository(unittest.TestCase):
    
    data = None
    source = os.path.join(os.path.dirname(__file__), './data/hurdat_sample.txt')
    name = "myTestSource"

    @classmethod
    def setUpClass(cls):

        cls.repo = repo(source_path=cls.source, source_name=cls.name)
        cls.data = cls.repo.extract_data()

    def test_init(self):
        source = self.repo

        self.assertEqual(source.source_path, self.source)
        self.assertEqual(source.source_name, self.name)

    def test_extract_data(self):
        data = self.data

        self.assertIsInstance(data, List)
        self.assertEqual(len(data), 5)


    def test_parse_tracks(self):
        data = self.data
        track = data[0]

        self.assertIsInstance(track, ent.Track)
        self.assertEquals(len(track.track_entries), 14)


    def test_parse_track_entry(self):
        data = self.data
        track_entry = data[0].track_entries[0]
        
        self.assertIsInstance(track_entry, ent.TrackEntry)
        self.assertEqual(track_entry.location.latitude, 28.0)
        self.assertEqual(track_entry.location.longitude, -94.8)
        self.assertEqual(track_entry.datetime, datetime.fromisoformat('18510625T0000Z'))
        self.assertEqual(track_entry.system_status, 'HU')
        self.assertEqual(track_entry.max_windspeed, 80)


if __name__ == '__main__':
    unittest.main()

