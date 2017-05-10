import json
from reckoner import RentReckoner
from provider import DataProvider
import flask


APP = flask.Flask(__name__)

DATA_PATH = "./rent_reckoner/data/"

DATA_PROVIDER = DataProvider(DATA_PATH)
RENT_RECKONER = RentReckoner(DATA_PROVIDER)


@APP.route("/habitations/<int:habitant_id>/residents/<int:resident_id>/dept")
def get_dept(habitant_id, resident_id):
    dept = "# %d #" % RENT_RECKONER.get_debt(
        habitant_id, DATA_PROVIDER.get_resident_by_id(habitant_id, resident_id))
    resp = flask.Response(dept)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@APP.route("/habitations/<int:habitant_id>/bills")
def get_bills(habitant_id):
    bills = json.dumps(RENT_RECKONER.get_bills_to_ui(
        habitant_id), default=lambda o: o.__dict__)
    resp = flask.Response(bills)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == "__main__":
    APP.run()
