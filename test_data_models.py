import unittest

import data_models as dm

class TestTextSource(unittest.TestCase):

    @classmethod
    def setUpCLass(cls):
        source = r"./hurdat_sample.txt"
        name = "myTestSource"
        cls.ts = dm.TextSource(source_path = source, source_name=name)

    def test_init(self):
        self.assertEqual(self.ts.source_path, self.source)
        self.assertEqual(self.ts.source_name, self.name)

    def test_extract(self):
        self.ts.extract_data()
        self.assertEqual()
        

if __name__ == '__main__':
    TestTextSource.setUpCLass()

