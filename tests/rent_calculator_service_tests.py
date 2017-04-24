from nose.tools import *
from datetime import datetime
from rent_calculator_service.data_access.data_provider import DataProvider
from rent_calculator_service.calculator.rent_calculator import RentCalculator

test_bills_file = 'D:/github/rent-calculator-service/tests/data/test_bills.json'
test_residents_file = 'D:/github/rent-calculator-service/tests/data/test_residents.json'

def test_data_provider():
    dataProvider = DataProvider(test_bills_file, test_residents_file)

def test_get_bill_is_not_empty():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    expected = [
      {
        "amount": 80000,
        "type": "rent",
        "start": 1483228800,
        "end": 1485907199
      }
    ]
    assert_equals(dataProvider.getBills(), expected)

def test_get_residents_is_not_empty():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    expected = [
      {
        "name": "Peti",
        "end": 1504224000,
        "start": 1472688000,
        "paid": 252308
      }
    ]
    assert_equals(dataProvider.getResidents(), expected)

def test_rent_calculator():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)

def test_rent_calculator_get_dweller_count():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)

    date = 1472688001
    assert_equals(rentCalculator.getDwellerCount(date), 1)
    date = 1472687999
    assert_equals(rentCalculator.getDwellerCount(date), 0)

def test_rent_calculator_is_dwell():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)
    resident = {
        "name": "Peti",
        "end": 1504224000,
        "start": 1472688000,
        "paid": 252308
    }
    date = 1472688001
    assert_true(rentCalculator.isDwell(resident, date))
    date = 1472687999
    assert_false(rentCalculator.isDwell(resident, date))

def test_rent_calculator_get_time_coverage_percent():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)
    bill = {
      "amount": 80000,
      "type": "rent",
      "start": 1483228800,
      "end": 1485820800
    }
    start = 1483228800
    end = 1485820800
    assert_equals(rentCalculator.getTimeCoveragePercent(bill, start, end), 1)
    start = 1483228800
    end = 1484524800
    assert_equals(rentCalculator.getTimeCoveragePercent(bill, start, end), 0.5)

def test_rent_calculator_get_cost_per_skull():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)
    date = 1483228800
    assert_equals(rentCalculator.getCostPerSkull(date), 2580.6451612903224)
    date = 1485907200 - 86400
    assert_equals(rentCalculator.getCostPerSkull(date), 2580.6451612903224)
    date = 1485907200 - 43200
    assert_equals(rentCalculator.getCostPerSkull(date), 1290.3225806451612)
    date = 1483228800 - 43200
    assert_equals(rentCalculator.getCostPerSkull(date), 1290.3225806451612)
    date = 1483228800 - 86400
    assert_equals(rentCalculator.getCostPerSkull(date), 0)
    date = 1485907200
    assert_equals(rentCalculator.getCostPerSkull(date), 0)

def test_rent_calculator_get_cost_per_skull():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)
    start = 1483228800
    end = 1485907200
    assert_equals(rentCalculator.sumCostPerSkull(start, end), 80000)
    start = 1483228800
    end = 1485907200 - (1485907200 - 1483228800) / 2
    assert_equals(rentCalculator.sumCostPerSkull(start, end), 41290.337996691305)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200
    assert_equals(rentCalculator.sumCostPerSkull(start, end), 39999.985065705288)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200 + (1485907200 - 1483228800) / 2
    assert_equals(rentCalculator.sumCostPerSkull(start, end), 39999.985065705288)
    start = 1483228800 + (1485907200 - 1483228800)
    end = 1485907200 + (1485907200 - 1483228800)
    assert_equals(rentCalculator.sumCostPerSkull(start, end), 0)

def test_rent_calculator_get_debt():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)
    resident = {
        "name": "Peti",
        "end": 1504224000,
        "start": 1472688000,
        "paid": 80000
    }
    assert_equals(rentCalculator.getDebt(resident), 0)

def test_rent_calculator_sum_cost():
    dataProvider = DataProvider(test_bills_file, test_residents_file)
    rentCalculator = RentCalculator(dataProvider)
    start = 1483228800
    end = 1485907200
    assert_equals(rentCalculator.sumCost(start, end), 80000)
    start = 1483228800
    end = 1485907200 - (1485907200 - 1483228800) / 2
    assert_equals(rentCalculator.sumCost(start, end), 40000.014934294704)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200
    assert_equals(rentCalculator.sumCost(start, end), 39999.985065705296)
    start = 1483228800 + (1485907200 - 1483228800) / 2
    end = 1485907200 + (1485907200 - 1483228800) / 2
    assert_equals(rentCalculator.sumCost(start, end), 39999.985065705296)
    start = 1483228800 + (1485907200 - 1483228800)
    end = 1485907200 + (1485907200 - 1483228800)
    assert_equals(rentCalculator.sumCost(start, end), 0)
