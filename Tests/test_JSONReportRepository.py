import unittest
import pathlib

import repositories

class TestJSONReportRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_directory = "./"
        cls.invalid_directory = "./thisdoesnotexist/"
        cls.data = {
            'Int Key': 777,
            'Text Key': 'Seven Seven Seven',
            'List Key': [7, 7, 7]
            }
        cls.repo = repositories.JSONReportRepository()

    def test_valid_directory(self):
        # Act    
        valid_return = self.repo.save(self.valid_directory, self.data)
        
        # Assert
        self.assertEqual(valid_return, 200)

    def test_invalid_directory(self):
        # Act
        invalid_return =self.repo.save(self.invalid_directory, self.data)
        
        # Assert
        self.assertEqual(invalid_return, 400)
