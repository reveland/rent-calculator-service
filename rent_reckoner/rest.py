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
    dept = "# %d #" % RENT_RECKONER.get_debt(
        DATA_PROVIDER.get_resident_by_id(resident_id))
    return dept


@APP.route("/bills")
def get_bills():
    return json.dumps(RENT_RECKONER.get_bills_to_ui(), default=lambda o: o.__dict__)


if __name__ == "__main__":
    APP.run()
