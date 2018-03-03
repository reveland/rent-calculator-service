import json
import flask
from flask import request
from rent_reckoner.reckoner import RentReckoner
from rent_reckoner.provider_trello import DataProvider

app = flask.Flask(__name__)

DATA_PATH = "./rent_reckoner/data/"

DATA_PROVIDER = DataProvider(DATA_PATH)
RENT_RECKONER = RentReckoner(DATA_PROVIDER)

def create_response(data):
    resp = flask.Response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/habitations/<int:habitant_id>/bills_to_ui")
def get_bills_to_ui(habitant_id):
    bills_to_ui = RENT_RECKONER.get_bills_to_ui(habitant_id)
    bills_to_ui = json.dumps(bills_to_ui, default=lambda o: o.__dict__)
    return create_response(bills_to_ui)


@app.route("/habitations/<int:habitant_id>/residents_to_ui")
def get_residents_to_ui(habitant_id):
    residents_to_ui = RENT_RECKONER.get_residents_to_ui(habitant_id)
    residents_to_ui = json.dumps(residents_to_ui, default=lambda o: o.__dict__)
    return create_response(residents_to_ui)


@app.route("/habitations/<int:habitant_id>/bills")
def get_bills(habitant_id):
    bills = DATA_PROVIDER.get_bills(habitant_id)
    bills = json.dumps(bills)
    return create_response(bills)


@app.route("/habitations/<int:habitant_id>/residents")
def get_residents(habitant_id):
    residents = DATA_PROVIDER.get_residents(habitant_id)
    residents = json.dumps(residents)
    return create_response(residents)


@app.route("/habitations/<int:habitant_id>/update_depts")
def update_depts(habitant_id):
    RENT_RECKONER.update_debts(habitant_id)
    return "updated"


@app.route("/habitations/<int:habitant_id>/residents", methods=['POST'])
def add_resident(habitant_id):
    r = request.get_json()

    added_resident = DATA_PROVIDER.add_resident(habitant_id, r['start'], r['end'], r['name'])
    return create_response(r)


@app.route("/habitations/<int:habitant_id>/bills", methods=['POST'])
def add_bill(habitant_id):
    b = request.get_json()

    added_bill = DATA_PROVIDER.add_bill(habitant_id, b['start'], b['end'], b['type'], b['amount'], b['paid_by'])
    return create_response(b)

if __name__ == "__main__":
    app.run(debug=True)
