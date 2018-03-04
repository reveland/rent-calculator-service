import json
import flask
from flask import request
from rent_reckoner.reckoner import RentReckoner
from rent_reckoner.provider.google_sheet_provider import GoogleDataProvider
from rent_reckoner.provider.provider_trello import TrelloDataProvider

app = flask.Flask(__name__)

GOOGLE_DATA_PROVIDER = GoogleDataProvider()
TRELLO_DATA_PROVIDER = TrelloDataProvider()
RENT_RECKONER = RentReckoner(GOOGLE_DATA_PROVIDER)

DATA_PROVIDERS = [GOOGLE_DATA_PROVIDER, TRELLO_DATA_PROVIDER]

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
    bills = GOOGLE_DATA_PROVIDER.get_bills(habitant_id)
    bills = json.dumps(bills)
    return create_response(bills)

@app.route("/habitations/<int:habitant_id>/residents")
def get_residents(habitant_id):
    residents = GOOGLE_DATA_PROVIDER.get_residents(habitant_id)
    residents = json.dumps(residents)
    return create_response(residents)

@app.route("/habitations/<int:habitant_id>/update_depts")
def update_depts(habitant_id):
    RENT_RECKONER.update_debts(habitant_id)
    return "updated"

@app.route("/habitations/<int:habitant_id>/residents", methods=['POST'])
def add_resident(habitant_id):
    resident = request.get_json()

    GOOGLE_DATA_PROVIDER.add_resident(habitant_id, resident['start'], resident['end'], resident['name'])
    return create_response(resident)

@app.route("/habitations/<int:habitant_id>/bills", methods=['POST'])
def add_bill(habitant_id):
    bill = request.get_json()

    GOOGLE_DATA_PROVIDER.add_bill(habitant_id, bill['start'], bill['end'], bill['type'], bill['amount'], bill['paid_by'])
    return create_response(bill)

@app.route("/habitations/<int:habitant_id>/merge/<int:source_id>/<int:target_id>", methods=['GET'])
def merge(habitant_id, source_id, target_id):
    DATA_PROVIDERS[source_id].merge(habitant_id, DATA_PROVIDERS[target_id])
    return 'merged'

if __name__ == "__main__":
    app.run(debug=True)
