import unittest
import mock

from rent_reckoner.reckoner import RentReckoner
from rent_reckoner.provider import DataProvider

class TestRentReckoner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mock_data_provider = mock.create_autospec(DataProvider)
        cls.undertest = RentReckoner(mock_data_provider)

    @mock.patch.object(RentReckoner, 'is_dwell', autospec=True)
    def test_get_dweller_count_when_dwelled(self, mock_is_dwell):
        mock_is_dwell.return_value = True

        actual = self.undertest.get_dweller_count('habitant_id', 'date', [{}])
        
        self.assertEqual(actual, 1)
        mock_is_dwell.assert_called_with(self.undertest, {}, 'date')

    @mock.patch.object(RentReckoner, 'is_dwell', autospec=True)
    def test_get_dweller_count_when_not_dwelled(self, mock_is_dwell):
        mock_is_dwell.return_value = False
        
        actual = self.undertest.get_dweller_count('habitant_id', 'date', [{}])
        
        self.assertEqual(actual, 0)
        mock_is_dwell.assert_called_with(self.undertest, {}, 'date')

    def test_is_dwell(self):
        self.assertTrue(self.undertest.is_dwell({"start": 1, "end": 3}, 2))
        self.assertTrue(self.undertest.is_dwell({"start": 1, "end": 3}, 1))
        self.assertTrue(self.undertest.is_dwell({"start": 1, "end": 3}, 3))
        self.assertFalse(self.undertest.is_dwell({"start": 1, "end": 3}, 4))
        self.assertFalse(self.undertest.is_dwell({"start": 1, "end": 3}, 0))

if __name__ == '__main__':
    unittest.main()