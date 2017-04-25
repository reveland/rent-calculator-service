from nose.tools import assert_equals, assert_true, assert_false
from rent_reckoner.data_access.data_provider import DataProvider
from rent_reckoner.reckoner.rent_reckoner import RentReckoner

TEST_BILLS_FILE = "D:/github/rent-calculator-service/tests/data/test_bills.json"
TEST_RESIDENTS_FILE = 'D:/github/rent-calculator-service/tests/data/test_residents.json'
BILL_START = 1483228800
BILL_END = 1485907199
RESIDENT_START = 1472688000
RESIDENT_END = 1504224000
DAY = 86400
BILL_AMOUNT = 80000


class TestDataProvider:

    @classmethod
    def setup_class(cls):
        cls.data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)

    def test_get_bills(self):
        expected = [
            {
                "amount": BILL_AMOUNT,
                "type": "rent",
                "start": BILL_START,
                "end": BILL_END
            }
        ]
        assert_equals(self.data_provider.get_bills(), expected)

    def test_get_residents(self):
        expected = [
            {
                "name": "Peti",
                "end": RESIDENT_END,
                "start": RESIDENT_START,
                "paid": 252308
            }
        ]
        assert_equals(self.data_provider.get_residents(), expected)


class TestRentReckoner:

    @classmethod
    def setup_class(cls):
        data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
        cls.rent_reckoner = RentReckoner(data_provider)

    def test_get_dweller_count(self):
        date = RESIDENT_START + 1
        assert_equals(self.rent_reckoner.get_dweller_count(date), 1)
        date = RESIDENT_START - 1
        assert_equals(self.rent_reckoner.get_dweller_count(date), 0)

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

    def test_get_cost_per_skull(self):
        date = BILL_START
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), 2580.6461247932066)  # TODO BILL_AMOUNT / 31
        date = BILL_END - DAY
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), 2580.6461247932066)  # TODO BILL_AMOUNT / 31
        date = BILL_END - (DAY / 2)
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), 1290.3230623966033)  # TODO BILL_AMOUNT / 31 / 2
        date = BILL_START - (DAY / 2)
        assert_equals(self.rent_reckoner.get_cost_per_skull(
            date), 1290.3230623966033)  # TODO BILL_AMOUNT / 31 / 2
        date = BILL_START - DAY
        assert_equals(self.rent_reckoner.get_cost_per_skull(date), 0)
        date = BILL_END
        assert_equals(self.rent_reckoner.get_cost_per_skull(date), 0)

    def test_sum_cost_per_skull(self):
        start = BILL_START
        end = BILL_END
        assert_equals(self.rent_reckoner.sum_cost_per_skull(
            start, end), BILL_AMOUNT)
        start = BILL_START
        end = BILL_END - (BILL_END - BILL_START) / 2
        assert_equals(self.rent_reckoner.sum_cost_per_skull(
            start, end), 41290.337996691305)  # TODO BILL_AMOUNT / 2
        start = BILL_START + (BILL_END - BILL_START) / 2
        end = BILL_END
        assert_equals(self.rent_reckoner.sum_cost_per_skull(
            start, end), 39999.999999999993)  # TODO BILL_AMOUNT / 2
        start = BILL_START + (BILL_END - BILL_START) / 2
        end = BILL_END + (BILL_END - BILL_START) / 2
        assert_equals(self.rent_reckoner.sum_cost_per_skull(
            start, end), 39999.999999999993)  # TODO BILL_AMOUNT / 2
        start = BILL_START + (BILL_END - BILL_START)
        end = BILL_END + (BILL_END - BILL_START)
        assert_equals(self.rent_reckoner.sum_cost_per_skull(start, end), 0)

    def test_get_debt(self):
        resident = {
            "name": "Peti",
            "end": RESIDENT_END,
            "start": RESIDENT_START,
            "paid": BILL_AMOUNT
        }
        assert_equals(self.rent_reckoner.get_debt(resident), 0)

    def test_sum_cost(self):
        start = BILL_START
        end = BILL_END
        assert_equals(self.rent_reckoner.sum_cost(start, end), BILL_AMOUNT)
        start = BILL_START
        end = BILL_END - (BILL_END - BILL_START) / 2
        assert_equals(self.rent_reckoner.sum_cost(
            start, end), BILL_AMOUNT / 2)
        start = BILL_START + (BILL_END - BILL_START) / 2
        end = BILL_END
        assert_equals(self.rent_reckoner.sum_cost(
            start, end), BILL_AMOUNT / 2)
        start = BILL_START + (BILL_END - BILL_START) / 2
        end = BILL_END + (BILL_END - BILL_START) / 2
        assert_equals(self.rent_reckoner.sum_cost(
            start, end), BILL_AMOUNT / 2)
        start = BILL_START + (BILL_END - BILL_START)
        end = BILL_END + (BILL_END - BILL_START)
        assert_equals(self.rent_reckoner.sum_cost(start, end), 0)
