import unittest
import mock
from mock import Mock

from rent_reckoner.reckoner import RentReckoner
from rent_reckoner.provider.provider import DataProvider

b1 = {
    "start": 1470960000,
    "end": 1473638400,
    "type": "Electronics",
    "amount": 5859,
    "paid_by": ""
}

b2 = {
    "start": 1472688000,
    "end": 1475193600,
    "type": "Rent",
    "amount": 80000,
    "paid_by": ""
}

b22 = {
    "start": 1472688000,
    "end": 1475193600,
    "type": "Rent",
    "amount": 80000,
    "paid_by": ""
}

b3 = {
    "start": 1468886400,
    "end": 1474070400,
    "type": "Heat/gas",
    "amount": 580,
    "paid_by": ""
}

class TestRentReckoner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DataProvider.__abstractmethods__ = set()
        cls.undertest = DataProvider()

    @mock.patch.object(DataProvider, 'get_bills', autospec=True)
    def test_merge(self, mock_get_bills):
        attrs = {'get_bills.return_value': [b1, b22], 'add_bill.return_value': 0}
        target = Mock(**attrs)
        mock_get_bills.return_value = [b2, b3]

        actual = self.undertest.merge(1, target)
        
        target.add_bill.assert_called_with(1, '2016-07-19', '2016-09-17', 'Heat/gas', 580, '')
        self.assertEqual(actual, [b3])

if __name__ == '__main__':
    unittest.main()