import json
from reckoner import RentReckoner
from provider_trello import DataProvider
import flask
from flask import request

APP = flask.Flask(__name__)

DATA_PATH = "./rent_reckoner/data/"

DATA_PROVIDER = DataProvider(DATA_PATH)
RENT_RECKONER = RentReckoner(DATA_PROVIDER)

def create_response(data):
    resp = flask.Response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@APP.route("/habitations/<int:habitant_id>/bills_to_ui")
def get_bills_to_ui(habitant_id):
    bills_to_ui = RENT_RECKONER.get_bills_to_ui(habitant_id)
    bills_to_ui = json.dumps(bills_to_ui, default=lambda o: o.__dict__)
    return create_response(bills_to_ui)


@APP.route("/habitations/<int:habitant_id>/residents_to_ui")
def get_residents_to_ui(habitant_id):
    residents_to_ui = RENT_RECKONER.get_residents_to_ui(habitant_id)
    residents_to_ui = json.dumps(residents_to_ui, default=lambda o: o.__dict__)
    return create_response(residents_to_ui)


@APP.route("/habitations/<int:habitant_id>/bills")
def get_bills(habitant_id):
    bills = DATA_PROVIDER.get_bills(habitant_id)
    bills = json.dumps(bills)
    return create_response(bills)


@APP.route("/habitations/<int:habitant_id>/residents")
def get_residents(habitant_id):
    residents = DATA_PROVIDER.get_residents(habitant_id)
    residents = json.dumps(residents)
    return create_response(residents)


@APP.route("/habitations/<int:habitant_id>/update_depts")
def update_depts(habitant_id):
    RENT_RECKONER.update_debts(habitant_id)
    return "updated"


@APP.route("/habitations/<int:habitant_id>/residents", methods=['POST'])
def add_resident(habitant_id):
    start = request.args.get('start')
    end = request.args.get('end')
    name = request.args.get('name')

    added_resident = DATA_PROVIDER.add_resident(habitant_id, start, end, name)
    resp = flask.Response(added_resident)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@APP.route("/habitations/<int:habitant_id>/bills", methods=['POST'])
def add_bill(habitant_id):
    start = request.args.get('start')
    end = request.args.get('end')
    type = request.args.get('type')
    amount = request.args.get('amount')

    added_bill = DATA_PROVIDER.add_bill(habitant_id, start, end, type, amount)
    resp = flask.Response(added_bill)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    APP.run()
