from unittest import TestCase
from nose.tools import assert_equals, assert_true, assert_false
from rent_reckoner.data_access.data_provider import DataProvider
from rent_reckoner.reckoner.rent_reckoner import RentReckoner
import mock
import numpy as np

TEST_BILLS_FILE = "D:/github/rent-calculator-service/tests/data/test_bills.json"
TEST_RESIDENTS_FILE = 'D:/github/rent-calculator-service/tests/data/test_residents.json'
BILL_START = 1483228800
BILL_END = 1485907200
RESIDENT_START = 1472688000
RESIDENT_END = 1504224000
DAY = 86400
BILL_AMOUNT = 80000
TEST_RESIDENTS = [{"name": "Peti",
                   "end": RESIDENT_END,
                   "start": RESIDENT_START,
                   "paid": 80000}]
TEST_BILLS = [{"amount": BILL_AMOUNT,
               "type": "rent",
               "start": BILL_START,
               "end": BILL_END}]


class TestDataProvider(TestCase):

    @classmethod
    def setup_class(cls):
        cls.data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)

    def test_get_bills(self):
        assert_equals(self.data_provider.get_bills(), TEST_BILLS)

    def test_get_residents(self):
        assert_equals(self.data_provider.get_residents(), TEST_RESIDENTS)


class TestRentReckoner(TestCase):

    @classmethod
    def setup_class(cls):
        data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
        cls.rent_reckoner = RentReckoner(data_provider)

    @mock.patch.object(RentReckoner, 'is_dwell')
    @mock.patch.object(DataProvider, 'get_residents')
    def test_get_dweller_count(self, mock_get_residents, mock_is_dwell):
        mock_get_residents.return_value = TEST_RESIDENTS
        mock_is_dwell.return_value = True
        date = RESIDENT_START + 1
        assert_equals(self.rent_reckoner.get_dweller_count(date), 1)
        mock_is_dwell.assert_called_with(TEST_RESIDENTS[0], date)

        mock_is_dwell.return_value = False
        date = RESIDENT_START - 1
        assert_equals(self.rent_reckoner.get_dweller_count(date), 0)
        for resident in TEST_RESIDENTS:
            mock_is_dwell.assert_called_with(resident, date)

    def test_is_dwell(self):
        resident = {
            "name": "Peti",
            "end": RESIDENT_END,
            "start": RESIDENT_START,
            "paid": 252308
        }
        date = RESIDENT_START + 1
        assert_true(self.rent_reckoner.is_dwell(resident, date))
        date = RESIDENT_START - 1
        assert_false(self.rent_reckoner.is_dwell(resident, date))

    def test_get_time_coverage_percent(self):
        bill = {
            "amount": BILL_AMOUNT,
            "type": "rent",
            "start": BILL_START,
            "end": BILL_END
        }
        start = BILL_START
        end = BILL_END
        assert_equals(self.rent_reckoner.get_time_coverage_percent(
            bill, start, end), 1)
        start = BILL_START
        end = BILL_START + (BILL_END - BILL_START) / 2
        assert_equals(self.rent_reckoner.get_time_coverage_percent(
            bill, start, end), 0.5)

    @mock.patch.object(DataProvider, 'get_bills')
    @mock.patch.object(RentReckoner, 'get_time_coverage_percent')
    @mock.patch.object(RentReckoner, 'get_dweller_count')
    def test_get_cost_per_skull(self, mock_get_dweller_count,
                                mock_get_time_coverage_percent, mock_get_bills):
        mock_get_bills.return_value = TEST_BILLS
        mock_get_dweller_count.return_value = 1
        mock_get_time_coverage_percent.return_value = 1 / 31
        date = BILL_START
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), BILL_AMOUNT / 31)
        for bill in TEST_BILLS:
            mock_get_time_coverage_percent.assert_called_with(
                bill, date, date + 86400)
        mock_get_bills.assert_called()
        mock_get_dweller_count.assert_called_with(date)

        mock_get_dweller_count.return_value = 2
        mock_get_time_coverage_percent.return_value = 1 / 31
        date = BILL_END - DAY
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), BILL_AMOUNT / 31 / 2)
        for bill in TEST_BILLS:
            mock_get_time_coverage_percent.assert_called_with(
                bill, date, date + 86400)
        mock_get_bills.assert_called()
        mock_get_dweller_count.assert_called_with(date)

        mock_get_dweller_count.return_value = 2
        mock_get_time_coverage_percent.return_value = 1 / 60
        date = BILL_START - (DAY / 2)
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), BILL_AMOUNT / 60 / 2)
        for bill in TEST_BILLS:
            mock_get_time_coverage_percent.assert_called_with(
                bill, date, date + 86400)
        mock_get_bills.assert_called()
        mock_get_dweller_count.assert_called_with(date)

        mock_get_dweller_count.return_value = 3
        mock_get_time_coverage_percent.return_value = 1 / 30
        date = BILL_END - (DAY / 2)
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), BILL_AMOUNT / 30 / 3)
        for bill in TEST_BILLS:
            mock_get_time_coverage_percent.assert_called_with(
                bill, date, date + 86400)
        mock_get_bills.assert_called()
        mock_get_dweller_count.assert_called_with(date)

    @mock.patch.object(RentReckoner, 'get_cost_per_skull')
    def test_sum_cost_per_skull(self, mock_get_cost_per_skull):
        mock_get_cost_per_skull.return_value = 1000
        start = 0
        end = 30 * DAY
        assert_equals(self.rent_reckoner.sum_cost_per_skull(
            start, end), 30 * 1000)
        start = 30 * DAY
        end = 40 * DAY
        assert_equals(self.rent_reckoner.sum_cost_per_skull(
            start, end), 10 * 1000)
        start = 10 * DAY
        end = 0
        assert_equals(self.rent_reckoner.sum_cost_per_skull(start, end), 0)
        for date in np.arange(start, end, 86400):
            mock_get_cost_per_skull.assert_called_with(date)

    @mock.patch.object(RentReckoner, 'sum_cost_per_skull')
    def test_get_debt(self, mock_sum_cost_per_skull):
        mock_sum_cost_per_skull.return_value = 80000
        assert_equals(self.rent_reckoner.get_debt(TEST_RESIDENTS[0]), 0)
        mock_sum_cost_per_skull.assert_called_with(
            TEST_RESIDENTS[0]["start"], TEST_RESIDENTS[0]["end"])

    @mock.patch.object(DataProvider, 'get_bills')
    @mock.patch.object(RentReckoner, 'get_time_coverage_percent')
    def test_sum_cost(self, mock_get_time_coverage_percent, mock_get_bills):
        mock_get_bills.return_value = TEST_BILLS
        mock_get_time_coverage_percent.return_value = 10 / 31
        start = BILL_START
        end = BILL_END
        assert_equals(self.rent_reckoner.sum_cost(
            start, end), BILL_AMOUNT * (10 / 31))
        for bill in TEST_BILLS:
            mock_get_time_coverage_percent.assert_called_with(
                bill, start, end)
        mock_get_bills.assert_called()
