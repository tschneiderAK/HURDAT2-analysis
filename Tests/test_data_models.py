from datetime import datetime
import unittest
from typing import List


from repositories import StormTextRepository as st

class TestStormTextRepository(unittest.TestCase):
    
    data = None
    source = r"./hurdat_sample.txt"
    name = "myTestSource"

    @classmethod
    def setUpClass(cls):

        cls.ts = st(source_path=cls.source, source_name=cls.name)
        cls.data = cls.ts.extract_data()

    def test_init(self):
        source = self.ts

        self.assertEqual(source.source_path, self.source)
        self.assertEqual(source.source_name, self.name)

    def test_extract_data(self):
        data = self.data

        self.assertIsInstance(data, ent.DataSet)
        self.assertIsInstance(data.tracks, list)

    def test_parse_tracks(self):
        data = self.data

        self.assertEqual(len(data.tracks), 5)
        self.assertIsInstance(data.tracks[0], ent.Track)

    def test_parse_track_entry(self):
        data = self.data
        te = data.tracks[0].track_entries[0]
        
        self.assertEqual(len(data.tracks[0].track_entries), 14)
        self.assertIsInstance(te, ent.TrackEntry)
        self.assertEqual(te.latitude, -28.0)
        self.assertEqual(te.longitude, -94.8)
        self.assertEqual(te.datetime, datetime.fromisoformat('18510625T0000Z'))
        self.assertEqual(te.system_status, 'HU')
        self.assertEqual(te.max_windspeed, 80)


if __name__ == '__main__':
    unittest.main()

