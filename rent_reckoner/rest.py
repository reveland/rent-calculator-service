from reckoner import RentReckoner
from provider import DataProvider
from flask import Flask
import json


APP = Flask(__name__)

BILLS_FILE = "D:/github/rent-calculator-service/rent_reckoner/data/bills.json"
RESIDENTS_FILE = 'D:/github/rent-calculator-service/rent_reckoner/data/residents.json'

DATA_PROVIDER = DataProvider(BILLS_FILE, RESIDENTS_FILE)
RENT_RECKONER = RentReckoner(DATA_PROVIDER)


@APP.route("/dept/<int:resident_id>")
def get_dept(resident_id):
    dept = "%d" % RENT_RECKONER.get_debt(
        DATA_PROVIDER.get_resident_by_id(resident_id))
    return dept


@APP.route("/bills")
def get_bills():
    bills = {
        "start": "2017-02-10T00:00:00.000Z",
        "end": "2017-05-10T00:00:00.000Z",
        "maxMaxAmountPerDay": 3666.9843005545576,
        "types": [
            {
                "id": 1,
                "maxAmountPerDay": 2580.6451612903224,
                "name": "rent",
                        "start": "2017-03-01T00:00:00.000Z",
                        "end": "2017-03-31T00:00:00.000Z",
                        "bills": [
                            {
                                "id": 1,
                                "start": "2017-03-01T00:00:00.000Z",
                                "end": "2017-03-31T00:00:00.000Z",
                                "amountPerDay": 2580.6451612903224,
                                "amount": 80000
                            }
                        ]
            },
            {
                "id": 2,
                "maxAmountPerDay": 425.80645161290323,
                "name": "common",
                        "start": "2017-03-01T00:00:00.000Z",
                        "end": "2017-03-31T00:00:00.000Z",
                        "bills": [
                            {
                                "id": 2,
                                "start": "2017-03-01T00:00:00.000Z",
                                "end": "2017-03-31T00:00:00.000Z",
                                "amountPerDay": 425.80645161290323,
                                "amount": 13200
                            }
                        ]
            },
            {
                "id": 3,
                "maxAmountPerDay": 285.7142857142857,
                "name": "elec",
                        "start": "2017-02-10T00:00:00.000Z",
                        "end": "2017-03-20T00:00:00.000Z",
                        "bills": [
                            {
                                "id": 3,
                                "start": "2017-02-10T00:00:00.000Z",
                                "end": "2017-03-20T00:00:00.000Z",
                                "amountPerDay": 285.7142857142857,
                                "amount": 8000
                            }
                        ]
            },
            {
                "id": 4,
                "maxAmountPerDay": 203.38983050847457,
                "name": "water",
                        "start": "2017-02-10T00:00:00.000Z",
                        "end": "2017-04-20T00:00:00.000Z",
                        "bills": [
                            {
                                "id": 4,
                                "start": "2017-02-10T00:00:00.000Z",
                                "end": "2017-04-20T00:00:00.000Z",
                                "amountPerDay": 203.38983050847457,
                                "amount": 12000
                            }
                        ]
            },
            {
                "id": 5,
                "maxAmountPerDay": 171.42857142857142,
                "name": "misc",
                        "start": "2017-03-10T00:00:00.000Z",
                        "end": "2017-05-10T00:00:00.000Z",
                        "bills": [
                            {
                                "id": 5,
                                "start": "2017-03-10T00:00:00.000Z",
                                "end": "2017-04-05T00:00:00.000Z",
                                "amountPerDay": 153.84615384615384,
                                "amount": 4000
                            },
                            {
                                "id": 6,
                                "start": "2017-04-05T00:00:00.000Z",
                                "end": "2017-05-10T00:00:00.000Z",
                                "amountPerDay": 171.42857142857142,
                                "amount": 6000
                            }
                        ]
            }
        ]
    }
    return json.dumps(bills, default=lambda o: o.__dict__)


if __name__ == "__main__":
    APP.run()
