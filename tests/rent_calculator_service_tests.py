from nose.tools import assert_equals, assert_true, assert_false
from rent_reckoner.data_access.data_provider import DataProvider
from rent_reckoner.reckoner.rent_reckoner import RentReckoner

TEST_BILLS_FILE = "D:/github/rent-calculator-service/tests/data/test_bills.json"
TEST_RESIDENTS_FILE = 'D:/github/rent-calculator-service/tests/data/test_residents.json'


def test_get_bills():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    expected = [
        {
            "amount": 80000,
            "type": "rent",
            "start": 1483228800,
            "end": 1485907199
        }
    ]
    assert_equals(data_provider.get_bills(), expected)


def test_get_residents():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    expected = [
        {
            "name": "Peti",
            "end": 1504224000,
            "start": 1472688000,
            "paid": 252308
        }
    ]
    assert_equals(data_provider.get_residents(), expected)


def test_get_dweller_count():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)

    date = 1472688001
    assert_equals(rent_reckoner.get_dweller_count(date), 1)
    date = 1472687999
    assert_equals(rent_reckoner.get_dweller_count(date), 0)


def test_is_dwell():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)
    resident = {
        "name": "Peti",
        "end": 1504224000,
        "start": 1472688000,
        "paid": 252308
    }
    date = 1472688001
    assert_true(rent_reckoner.is_dwell(resident, date))
    date = 1472687999
    assert_false(rent_reckoner.is_dwell(resident, date))


def test_get_time_coverage_percent():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)
    bill = {
        "amount": 80000,
        "type": "rent",
        "start": 1483228800,
        "end": 1485820800
    }
    start = 1483228800
    end = 1485820800
    assert_equals(rent_reckoner.get_time_coverage_percent(bill, start, end), 1)
    start = 1483228800
    end = 1484524800
    assert_equals(rent_reckoner.get_time_coverage_percent(
        bill, start, end), 0.5)


def test_get_cost_per_skull():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)
    date = 1483228800
    assert_equals(rent_reckoner.get_cost_per_skull(date), 2580.6461247932066)
    date = 1485907200 - 86400
    assert_equals(rent_reckoner.get_cost_per_skull(date), 2580.6162562037994)
    date = 1485907200 - 43200
    assert_equals(rent_reckoner.get_cost_per_skull(date), 1290.293193807196)
    date = 1483228800 - 43200
    assert_equals(rent_reckoner.get_cost_per_skull(date), 1290.3230623966033)
    date = 1483228800 - 86400
    assert_equals(rent_reckoner.get_cost_per_skull(date), 0)
    date = 1485907200
    assert_equals(rent_reckoner.get_cost_per_skull(date), 0)


def test_sum_cost_per_skull():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)
    start = 1483228800
    end = 1485907200
    assert_equals(rent_reckoner.sum_cost_per_skull(start, end), 80000)
    start = 1483228800
    end = 1485907200 - (1485907200 - 1483228800) / 2
    assert_equals(rent_reckoner.sum_cost_per_skull(
        start, end), 41290.337996691305)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200
    assert_equals(rent_reckoner.sum_cost_per_skull(
        start, end), 39999.985065705288)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200 + (1485907200 - 1483228800) / 2
    assert_equals(rent_reckoner.sum_cost_per_skull(
        start, end), 39999.985065705288)
    start = 1483228800 + (1485907200 - 1483228800)
    end = 1485907200 + (1485907200 - 1483228800)
    assert_equals(rent_reckoner.sum_cost_per_skull(start, end), 0)


def test_get_debt():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)
    resident = {
        "name": "Peti",
        "end": 1504224000,
        "start": 1472688000,
        "paid": 80000
    }
    assert_equals(rent_reckoner.get_debt(resident), 0)


def test_sum_cost():
    data_provider = DataProvider(TEST_BILLS_FILE, TEST_RESIDENTS_FILE)
    rent_reckoner = RentReckoner(data_provider)
    start = 1483228800
    end = 1485907200
    assert_equals(rent_reckoner.sum_cost(start, end), 80000)
    start = 1483228800
    end = 1485907200 - (1485907200 - 1483228800) / 2
    assert_equals(rent_reckoner.sum_cost(start, end), 40000.014934294704)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200
    assert_equals(rent_reckoner.sum_cost(start, end), 39999.985065705296)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200 + (1485907200 - 1483228800) / 2
    assert_equals(rent_reckoner.sum_cost(start, end), 39999.985065705296)
    start = 1483228800 + (1485907200 - 1483228800)
    end = 1485907200 + (1485907200 - 1483228800)
    assert_equals(rent_reckoner.sum_cost(start, end), 0)
