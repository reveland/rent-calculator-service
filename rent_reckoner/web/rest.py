from flask import Flask
from rent_reckoner.data_access.data_provider import DataProvider
from rent_reckoner.reckoner.rent_reckoner import RentReckoner
APP = Flask(__name__)

BILLS_FILE = "D:/github/rent-calculator-service/rent_reckoner/data_access/data/bills.json"
RESIDENTS_FILE = 'D:/github/rent-calculator-service/rent_reckoner/data_access/data/residents.json'

data_provider = DataProvider(BILLS_FILE, RESIDENTS_FILE)
rent_reckoner = RentReckoner(data_provider)


@APP.route("/dept/<int:resident_id>")
def get_dept(resident_id):
    return rent_reckoner.get_debt(data_provider.get_residents()[resident_id])


if __name__ == "__main__":
    APP.run()
