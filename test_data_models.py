import unittest

import data_models as dm

class TestDataModels(unittest.TestCase):

    def test_text_source__init(self):
        source = r"./hurdat_sample.txt"
        name = "myTestSource"
        ts = dm.TextSource(source_path = source, source_name=name)
        self.assertEqual(ts.source_path, source)
        self.assertEqual(ts.source_name, name)

if __name__ == '__main__':
    unittest.main()